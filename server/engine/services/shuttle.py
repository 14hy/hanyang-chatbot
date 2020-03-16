import enum
from copy import deepcopy
from datetime import datetime
from pathlib import Path

import yaml

from utils import *

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper


class Season(enum.Enum):
    학기중 = 0
    계절 = 1
    방학 = 2


class Bus(enum.Enum):
    순환노선 = 0
    한대앞 = 1
    예술인 = 2


class WeekEnd(enum.Enum):
    월금 = 0
    휴일 = 1


def _load_recipe(target):
    with open(f"{Config.SHUTTLE_DIR}/{target}.yml", mode="r") as f:
        recipe = yaml.load(f, Loader)
    assert recipe is not None
    return recipe


def to_str(x):
    """
    :param x: [hour, minute, hour, minute, term]
    :return: start, end, term
    %HH:%MM
    """
    # [8, 50, 79, 50, 5]
    dt = datetime.now()
    start = datetime.strftime(datetime(dt.year, dt.month, dt.day, hour=x[0], minute=x[1]), "%H:%M")
    end = datetime.strftime(datetime(dt.year, dt.month, dt.day, hour=x[2], minute=x[3]), "%H:%M")
    return start, end, x[4]


def from_str(x):
    dt = datetime.now()
    dt = datetime(dt.year, dt.month, dt.day, hour=int(x.split(':')[0]), minute=int(x.split(':')[1]))
    return int(dt.hour), int(dt.minute)


class ShuttleBus(object):
    """
    # 정류장의 종류
    1. 창의인재원
    2. 셔틀콕
    3. 한대앞역
    4. 예술인APT
    # 노선
    ## 순환
    창의인재원 -> 셔틀콕 -> 한대앞역 -> 예술인APT -> 셔틀콕 -> 창의인재원
    ## 예술인 APT
    창의인재원 -> 셔틀콕 -> 예술인APT -> 셔틀콕 -> 창의인재원
    ## 한대앞역
    창의인재원 -> 셔틀콕 -> 한대앞역 -> 셔틀콕 -> 창의인재원
    # 소요시간
    창의인재원 <-> 셔틀콕 (5분)
    셔틀콕 <-> 한대앞역, 예술인APT (10분)
    한대앞역 <-> 예술인APT (5분)
    """

    # 학기 중, 계절학기 첫 차는 순환 운행
    # 시작시간, 끝나는 시간, 시즌, 휴일, 노선에 따라 차등 적용

    def __init__(self, template=None):
        self.recipe = _load_recipe(template or "template")

    def get_current(self):
        def _check_season(_):
            return Season.방학

        now = datetime.now(KST)
        return self.get(
            season=_check_season(now),
            weekend=WeekEnd.휴일 if now.weekday() >= 5 else WeekEnd.월금,
            hours=now.hour,
            minutes=now.minute,
            seconds=now.second,
        )

    @log_time
    def get(self, season, weekend, **kwargs):
        try:
            if isinstance(weekend, (str,)):
                weekend = WeekEnd[weekend]
            if isinstance(season, (str,)):
                season = Season[season]
        except KeyError:
            logger.error("잘못된 요일 혹은 시즌")
            raise NotImplementedError

        table = self._make_table(season.value, weekend.value)
        return self._get(table, timedelta(**kwargs))

    @staticmethod
    def set_recipe(data, season, bus, weekend, *, template="template"):
        assert isinstance(data, list)
        recipe = _load_recipe(template)
        recipe[f"{season}_{weekend}_{bus}"] = data

        with open(
                f"{Config.SHUTTLE_DIR}/{template}.yml", mode="w", encoding="utf-8"
        ) as f:
            yaml.dump(recipe, stream=f)

        recipe = _load_recipe(template)
        return recipe[f"{season}_{weekend}_{bus}"]

    @staticmethod
    def get_table(season, bus, weekend, *, template="template"):
        p = Path(Config.SHUTTLE_DIR)

        tables = []
        for target in p.glob(f"{template}.yml"):
            tables.append(_load_recipe("".join(str(target.name).split(".")[:-1])))

        table = tables[0]  # don't use template feature

        ret = []
        for k, v in table.items():
            # example k: '계절_월금_순환노선'
            k = k.split("_")
            if season not in k:
                continue
            if bus not in k:
                continue
            if weekend not in k:
                continue

            for each in v or []:
                ret.append(each)
        return ret

    def _make_table(self, season, weekend):
        """

        :return: [순환노선, 에술인, 한대앞역], 셔틀콕 기준 시간
        순환노선: 창의인재원(-5분), 셔틀콕, 한대앞역(10분), 예술인(15분), 셔틀콕2(25분), 창의인재원2(30분) # 35분코스
        예술인: 창의인재원(-5분), 셔틀콕, 예술인(10분), 셔틀콕2(20분), 창의인재원2(25분) # 30분 코스
        한대앞역: 창의인재원(-5분), 셔틀콕, 한대앞역(10분), 셔틀콕2(20분), 창의인재원2(25분) # 30분 코스
        """

        def _get_recipe_key(s, w, b):
            ret = f"{list(Season)[s].name}_{list(WeekEnd)[w].name}_{list(Bus)[b].name}"
            return ret

        recipe = self.recipe

        순환노선 = recipe.get(_get_recipe_key(season, weekend, 0), [])
        예술인 = recipe.get(_get_recipe_key(season, weekend, 1), [])
        한대앞역 = recipe.get(_get_recipe_key(season, weekend, 2), [])

        output = []
        for _ in [순환노선, 예술인, 한대앞역]:
            temp = []
            for each in _:
                s_s, s_e, e_s, e_e, t_ = each
                s = timedelta(hours=s_s, minutes=s_e)
                e = timedelta(hours=e_s, minutes=e_e)
                t = timedelta(hours=0, minutes=0 if t_ is None else t_)
                while s <= e:
                    temp.append(s)
                    s += t
                    if t_ is None:
                        break
            output.append(temp)

        return output

    def _get(self, table, current_time):
        def _get_close_time(table, current_time):
            for i in range(len(table)):
                days = (table[i] - current_time).days
                seconds = table[i].seconds - current_time.seconds
                if seconds > 0 and days != -1:
                    return seconds
            return None

        def _add_gap(table, gap):
            output = deepcopy(table)
            for i in range(len(table)):
                for j in range(len(table[i])):
                    output[i][j] = table[i][j] + gap

            return output

        def _calc_close_time(table, current_time, gap):
            table_gap = _add_gap(table, gap)
            cycle, station, artin = None, None, None
            num_lines = len(table_gap)

            if num_lines >= 1:
                cycle = _get_close_time(table_gap[0], current_time)
            elif num_lines >= 2:
                station = _get_close_time(table_gap[1], current_time)
            elif num_lines == 3:
                artin = _get_close_time(table_gap[2], current_time)
            else:
                logger.error("버스 노선 수가 잘못 되었습니다.")
                raise NotImplementedError

            return cycle, station, artin

        def _get_output(close_time):
            def _get_minutes(seconds):
                m = 0
                s = seconds
                while s >= 60:
                    s -= 60
                    m += 1
                return m

            def _get_seconds(seconds):
                m = 0
                s = seconds
                while s >= 60:
                    s -= 60
                    m += 1
                return s

            def _check_status(close_time):
                if close_time is None:
                    return False
                if close_time >= timedelta(hours=1).seconds:
                    # 순환노선과 한대앞역, 예술인역은 겹치지 않기 때문에 미리 제거
                    return False

                return True

            status = _check_status(close_time)
            if status:
                minutes = _get_minutes(close_time)
                seconds = _get_seconds(close_time)
            else:
                minutes = 0
                seconds = 0
            output = {"status": status, "minutes": minutes, "seconds": seconds}
            return output

        # 창의원
        gap = -timedelta(minutes=5)
        dorm_cycle, dorm_station, dorm_artin = _calc_close_time(
            table, current_time, gap
        )
        # None 이 들어올 시, 예외처리
        # 셔틀콕
        gap = timedelta(minutes=0)
        shuttle1_cycle, shuttle1_station, shuttle1_artin = _calc_close_time(
            table, current_time, gap
        )
        # 한대앞역
        gap = timedelta(minutes=10)
        station_cycle, station_station, station_artin = _calc_close_time(
            table, current_time, gap
        )
        # 예술인
        gap = timedelta(minutes=10)
        _, _, artin_artin = _calc_close_time(table, current_time, gap)
        gap = timedelta(minutes=15)
        artin_cycle, _, _ = _calc_close_time(table, current_time, gap)
        # 셔틀콕2
        gap = timedelta(minutes=20)
        _, shuttle2_station, shuttle2_artin = _calc_close_time(table, current_time, gap)
        gap = timedelta(minutes=25)
        shuttle2_cycle, _, _ = _calc_close_time(table, current_time, gap)

        output = {}
        output["mode"] = "shuttle_bus"
        output["dorm_cycle"] = _get_output(dorm_cycle)
        output["dorm_station"] = _get_output(dorm_station)
        output["dorm_artin"] = _get_output(dorm_artin)
        output["shuttle_cycle"] = _get_output(shuttle1_cycle)
        output["shuttle_station"] = _get_output(shuttle1_station)
        output["shuttle_artin"] = _get_output(shuttle1_artin)
        output["station_cycle"] = _get_output(station_cycle)
        output["station_station"] = _get_output(station_station)
        output["artin_artin"] = _get_output(artin_artin)
        output["artin_cycle"] = _get_output(artin_cycle)
        output["shuttle_cycle2"] = _get_output(shuttle2_cycle)
        output["shuttle_artin2"] = _get_output(shuttle2_artin)
        output["shuttle_station2"] = _get_output(shuttle2_station)
        return output
