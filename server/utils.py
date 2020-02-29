import logging
import os
from datetime import timezone, timedelta
from functools import wraps
from pprint import pformat
from time import time


def is_dev():
    env = os.environ.get("env", "")
    return env.lower() == "dev" or env.lower() == "local"


if is_dev():
    from config import DevConfig as Config
else:
    from config import ProdConfig as Config

KST = timezone(offset=timedelta(hours=9))

formatter = logging.Formatter("[%(levelname)s][%(asctime)s] %(message)s")

handler = logging.StreamHandler()
handler.setFormatter(formatter)

logger = logging.getLogger(__name__)
logger.setLevel(Config.LOG_LEVEL)
logger.addHandler(handler)

logger.info(f"Logger started")


class Singleton(type):  # Type을 상속받음
    __instances = {}  # 클래스의 인스턴스를 저장할 속성

    def __call__(cls, *args, **kwargs):  # 클래스로 인스턴스를 만들 때 호출되는 메서드
        if cls not in cls.__instances:  # 클래스로 인스턴스를 생성하지 않았는지 확인
            cls.__instances[cls] = super().__call__(
                *args, **kwargs
            )  # 생성하지 않았으면 인스턴스를 생성하여 해당 클래스 사전에 저장
        return cls.__instances[cls]  # 클래스로 인스턴스를 생성했으면 인스턴스 반환


def log_fn(fn):
    """Logger decorator"""

    @wraps(fn)
    def wrapper(*args, **kwargs):
        ret = fn(*args, **kwargs)
        logger.info(
            f"in {fn.__name__}, args: {pformat(args)}, kwargs: {pformat(kwargs)}, return: {pformat(ret)}"
        )
        return ret

    return wrapper


def log_time(fn):
    """Timer decorator"""

    @wraps(fn)
    def wrapper(*args, **kwargs):
        start = time()
        ret = fn(*args, **kwargs)
        end = time()
        logger.info(f"in {fn.__name__}, Total execution time: {end - start}")
        return ret

    return wrapper
