import enum
from datetime import time, datetime, timedelta
from pytz import timezone


class Table(enum.Enum):
    # 0: 학기 중, 1: 계절학기, 2: 방학 중
    # 0: 월~금, 1: 휴일
    # 0: 순환, 1: 한대앞역, 2: 예술인

    # 2019.09.25 업데이

    학기중_월금_순환노선 = [
        [0, 0, 0],  # 0750~0750 1회
        [4, 9, 4],  # 1300~1530 30분간격
        [8, 5, 4],  # 1800~1900 30분간격
        [5, 10, 2],  # 1900~2130 10분간격
        [10, 11, 3]  # 2130~2300 15분간
    ]
    학기중_월금_예술인 = [
        [2, 12, 4],  # 0820~1220 30분간격
        [13, 14, 4]  # 1600~1730 30분간격
    ]
    학기중_월금_한대앞 = [
        [1, 2, 1],  # 0800~0820 5분간격
        [2, 7, 0],  # 0820~0850 3분간격
        [7, 15, 1],  # 0850~0920 5분간격
        [15, 16, 0],  # 0920~0950 3분간격
        [16, 17, 1],  # 0950~1030 5분간격
        [17, 18, 2],  # 1030~1100 10분간격
        [18, 19, 3],  # 1100~1200 15분간격
        [19, 12, 2],  # 1200~1220 10분간격
        [12, 20, 1],  # 1220~1230 5분간격
        [20, 21, 2],  # 1230~1250 10분간격
        [22, 23, 4],  # 1315~1445 30분간격
        [24, 25, 2],  # 1510~1520 10분간격
        [26, 27, 2],  # 1540~1600 10분간격
        [27, 28, 5],  # 1600~1754 6분간격
        [29, 30, 5],  # 1806~1824 6분간격
        [31, 32, 2],  # 1840~1850 10분간격
    ]  # 0,0,2
    학기중_휴일_순환노선 = [
        [7, 33, 4]  # 0850~2150 30분간격
    ]
    계절_월금_순환노선 = [
        [1, 1, 0],  # 0800~0800 1회
        [4, 9, 4],  # 1300~1530 30분간격
        [8, 5, 4],  # 1800~1900 30분간격
        [5, 34, 2],  # 1900~2200 10분간격
    ]  # 1,0,0
    계절_월금_예술인 = [
        [2, 12, 4],  # 0820~1220 30분간격
        [13, 14, 4]  # 1600~1730 30분간격
    ]  # 1,0,1
    계절_월금_한대앞 = [
        [35, 3, 1],  # 0810~0900 5분간격
        [3, 21, 2],  # 0900~1250 10분간격
        [36, 37, 2],  # 1310~1320 10분간격
        [38, 39, 2],  # 1340~1350 10분간격
        [40, 41, 2],  # 1410~1420 10분간격
        [24, 25, 2],  # 1510~1520 10분간격
        [26, 42, 2],  # 1540~1750 10분간격
        [43, 44, 2],  # 1810~1820 10분간격
        [31, 32, 2],  # 1840~1850 10분간격
    ]  # 1,0,2
    계절_휴일_순환노선 = [
        [7, 45, 4]  # 0850~2150 30분간격
    ]  # 1,0,0
    방학_월금_순환노선 = [
        [0, 34, 4]  # 0750~2150 30분간격
    ]
    방학_휴일_순환노선 = [
        [7, 34, 4]  # 0850~2150 30분간
    ]  # 2,1,0


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

    def __init__(self):
        self.start_time = [self.create_timedelta(50, 7),  # 0, 0750
                           self.create_timedelta(0, 8),  # 1, 0800
                           self.create_timedelta(20, 8),  # 2 0820
                           self.create_timedelta(0, 9),  # 3 0900
                           self.create_timedelta(0, 13),  # 4 1300
                           self.create_timedelta(0, 19),  # 5 1900
                           self.create_timedelta(45, 21),  # 6 2145
                           self.create_timedelta(50, 8),  # 7 0850
                           self.create_timedelta(0, 18),  # 8 1800
                           self.create_timedelta(30, 15),  # 9 1530
                           self.create_timedelta(30, 21),  # 10 2130
                           self.create_timedelta(0, 23),  # 11 2300
                           self.create_timedelta(20, 12),  # 12 1220
                           self.create_timedelta(0, 16),  # 13 1600
                           self.create_timedelta(30, 17),  # 14 1730
                           self.create_timedelta(20, 9),  # 15 0920
                           self.create_timedelta(50, 9),  # 16 0950
                           self.create_timedelta(30, 10),  # 17 1030
                           self.create_timedelta(0, 11),  # 18 1100
                           self.create_timedelta(0, 12),  # 19 1200
                           self.create_timedelta(30, 12),  # 20 1230
                           self.create_timedelta(50, 12),  # 21 1250
                           self.create_timedelta(15, 13),  # 22 1315
                           self.create_timedelta(45, 14),  # 23 1445
                           self.create_timedelta(10, 15),  # 24 1510
                           self.create_timedelta(20, 15),  # 25 1520
                           self.create_timedelta(40, 15),  # 26 1540
                           self.create_timedelta(0, 16),  # 27 1600
                           self.create_timedelta(54, 17),  # 28 1754
                           self.create_timedelta(6, 18),  # 29 1806
                           self.create_timedelta(24, 18),  # 30 1824
                           self.create_timedelta(40, 18),  # 31 1840
                           self.create_timedelta(50, 18),  # 32 1850
                           self.create_timedelta(50, 21),  # 33 2150
                           self.create_timedelta(0, 22),  # 34 2150
                           self.create_timedelta(10, 8),  # 35 0810
                           self.create_timedelta(10, 13),  # 36 1310
                           self.create_timedelta(20, 13),  # 37 1320
                           self.create_timedelta(40, 13),  # 38 1340
                           self.create_timedelta(50, 13),  # 39 1350
                           self.create_timedelta(10, 14),  # 40 1410
                           self.create_timedelta(20, 14),  # 41 1420
                           self.create_timedelta(50, 17),  # 42 1750
                           self.create_timedelta(50, 17),  # 43 1810
                           self.create_timedelta(50, 17),  # 44 1820
                           self.create_timedelta(50, 21),  # 45 2150
                           ]
        #  2019.09.25 변경
        self.end_time = self.start_time
        self.interval = [self.create_timedelta(3, 0),  # 0, 3분간격
                         self.create_timedelta(5, 0),  # 1, 5분간격
                         self.create_timedelta(10, 0),  # 2, 10분간격
                         self.create_timedelta(15, 0),  # 3, 15분간격
                         self.create_timedelta(30, 0),  # 4, 30분간격
                         self.create_timedelta(6, 0)]  # 5, 6분간격

        self.recipe = [[[Table.학기중_월금_순환노선.value, Table.학기중_월금_한대앞.value, Table.학기중_월금_예술인.value],
                        [Table.학기중_휴일_순환노선.value]],
                       [[Table.계절_월금_순환노선.value, Table.계절_월금_한대앞.value, Table.계절_월금_예술인.value],
                        [Table.계절_휴일_순환노선.value]], [[Table.방학_월금_순환노선.value], [Table.방학_휴일_순환노선.value]]]

    def make_table(self, season, weekend):
        '''

        :return: [순환노선, 에술인, 한대앞역], 셔틀콕 기준 시간
        순환노선: 창의인재원(-5분), 셔틀콕, 한대앞역(10분), 예술인(15분), 셔틀콕2(25분), 창의인재원2(30분) # 35분코스
        예술인: 창의인재원(-5분), 셔틀콕, 예술인(10분), 셔틀콕2(20분), 창의인재원2(25분) # 30분 코스
        한대앞역: 창의인재원(-5분), 셔틀콕, 한대앞역(10분), 셔틀콕2(20분), 창의인재원2(25분) # 30분 코스
        '''

        output = []
        recipe = self.recipe[season][weekend]

        for i in range(len(recipe)):
            temp = []
            for j in range(len(recipe[i])):
                temp2 = []
                s = self.start_time[recipe[i][j][0]]
                e = self.end_time[recipe[i][j][1]]
                t = self.interval[recipe[i][j][2]]
                while s <= e:
                    temp2.append(s)
                    s += t
                temp.append(temp2)
            output.append(temp)

        return output

    def response(self):
        '''
        가장 가까운 셔틀 시간을 계산하여 뿌려 줌
        :return:
        '''
        KST = timezone('Asia/Seoul')
        NOW = datetime.now().astimezone(KST)
        current_time = timedelta(hours=NOW.hour,
                                 minutes=NOW.minute,
                                 seconds=NOW.second)
        season = self.check_season(current_time)
        weekend = self.check_weekend(NOW)
        table = self.make_table(season, weekend)

        response = self.create_response(table, current_time)

        return response

    def custom_response(self, weekend, season, hours, minutes, seconds):
        '''정해진 시간으로 답변'''
        # KST = timezone('Asia/Seoul')
        NOW = datetime.now()
        NOW = datetime(year=NOW.year, month=NOW.month, day=NOW.day,
                       hour=hours, minute=minutes, second=seconds)
        current_time = timedelta(hours=NOW.hour,
                                 minutes=NOW.minute,
                                 seconds=NOW.second)
        if season == '학기중':
            season = 0
        elif season == '계절학기':
            season = 1
        elif season == '방학중':
            season = 2
        else:
            raise Exception('season must be 학기중 or 계절학기 or 방학중')

        if weekend == '평일':
            weekend = 0
        elif weekend == '주말':
            weekend = 1
        else:
            raise Exception('weekend must be 평일 or 주말')

        table = self.make_table(season, weekend)
        from pprint import pprint
        response = self.create_response(table, current_time)

        return response

    def check_season(self, current_time):
        '''
        학기중/ 계절학기/ 방학 인지
        :param time:
        :return:
        '''
        # TODO 구현
        return 0

    def check_weekend(self, now):
        '''
        월~금/ 주말, 공휴일 인지
        :return:
        '''
        if now.weekday() >= 5:
            return 1
        else:
            return 0

    @staticmethod
    def create_time(hours, minutes=0):
        return time(hour=hours, minute=minutes)

    @staticmethod
    def create_timedelta(minutes, hours=0):
        return timedelta(minutes=minutes, hours=hours)

    def create_response(self, table, current_time):
        '''
        [창의원, 셔틀콕, 한대앞역, 예술인, 셔틀콕2]
        :param table:
        :param current_time:
        :return:
        '''
        output = {}

        # 창의원
        gap = - self.create_timedelta(5)
        dorm_cycle, dorm_station, dorm_artin = self.calc_close_time(table, current_time, gap)
        # None 이 들어올 시, 예외처리
        # 셔틀콕
        gap = self.create_timedelta(0)
        shuttle1_cycle, shuttle1_station, shuttle1_artin = self.calc_close_time(table, current_time, gap)
        # 한대앞역
        gap = self.create_timedelta(10)
        station_cycle, station_station, station_artin = self.calc_close_time(table, current_time, gap)
        # 예술인
        gap = self.create_timedelta(10)
        _, _, artin_artin = self.calc_close_time(table, current_time, gap)
        gap = self.create_timedelta(15)
        artin_cycle, _, _ = self.calc_close_time(table, current_time, gap)
        # 셔틀콕2
        gap = self.create_timedelta(20)
        _, shuttle2_station, shuttle2_artin = self.calc_close_time(table, current_time, gap)
        gap = self.create_timedelta(25)
        shuttle2_cycle, _, _ = self.calc_close_time(table, current_time, gap)

        output["mode"] = "shuttle_bus"
        output["dorm_cycle"] = self.get_output(dorm_cycle)
        output["dorm_station"] = self.get_output(dorm_station)
        output["dorm_artin"] = self.get_output(dorm_artin)
        output["shuttle_cycle"] = self.get_output(shuttle1_cycle)
        output["shuttle_station"] = self.get_output(shuttle1_station)
        output["shuttle_artin"] = self.get_output(shuttle1_artin)
        output["station_cycle"] = self.get_output(station_cycle)
        output["station_station"] = self.get_output(station_station)
        output["artin_artin"] = self.get_output(artin_artin)
        output["artin_cycle"] = self.get_output(artin_cycle)
        output["shuttle_cycle2"] = self.get_output(shuttle2_cycle)
        output["shuttle_artin2"] = self.get_output(shuttle2_artin)
        output["shuttle_station2"] = self.get_output(shuttle2_station)
        return output

    def get_output(self, close_time):

        status = self.check_status(close_time)
        if status:
            minutes = self.get_minutes(close_time)
            seconds = self.get_seconds(close_time)
        else:
            minutes = 0
            seconds = 0
        output = {"status": status,
                  "minutes": minutes,
                  "seconds": seconds}

        return output

    def close_bus(self, a, b, c=None):
        if a is None:
            a = 99999
        if b is None:
            b = 99999
        if c is None:
            c = 99999

        return min(a, b, c)

    def check_status(self, close_time):
        if close_time is None:
            return False
        if close_time >= self.create_timedelta(hours=1, minutes=0).seconds:
            # 순환노선과 한대앞역, 예술인역은 겹치지 않기 때문에 미리 제거
            return False

        return True

    def get_minutes(self, seconds):

        m = 0
        s = seconds
        while s >= 60:
            s -= 60
            m += 1
        return m

    def get_seconds(self, seconds):
        m = 0
        s = seconds
        while s >= 60:
            s -= 60
            m += 1
        return s

    def calc_close_time(self, table, current_time, gap):
        table_gap = self.add_gap(table, gap)
        cycle, station, artin = None, None, None
        num_lines = len(table_gap)

        if num_lines >= 1:
            cycle = self.get_close_time(table_gap[0], current_time)
        if num_lines >= 2:
            station = self.get_close_time(table_gap[1], current_time)
        if num_lines == 3:
            artin = self.get_close_time(table_gap[2], current_time)

        return cycle, station, artin

    def add_gap(self, table, gap):
        '''

        :param table:
        :param gap:
        :return:
        '''

        output = table.copy()
        for i in range(len(table)):
            for j in range(len(table[i])):
                for k in range(len(table[i][j])):
                    output[i][j][k] = table[i][j][k] + gap

        return output

    def get_close_time(self, table, current_time):
        """

        :param table:
        :param current_time:
        :return:
        """
        for i in range(len(table)):
            for j in range(len(table[i])):
                days = (table[i][j] - current_time).days
                seconds = (table[i][j].seconds - current_time.seconds)
                if seconds > 0 and days != -1:
                    return seconds
        return None


if __name__ == "__main__":
    test = ShuttleBus()
    test.response()
