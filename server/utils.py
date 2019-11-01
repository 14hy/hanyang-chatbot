from functools import wraps
from typing import Callable
from time import time
from datetime import timezone, timedelta, datetime
import logging
from config import Basic as _CONF
from pprint import pformat

KST = timezone(offset=timedelta(hours=9))

formatter = logging.Formatter('[%(asctime)s] - %(name)s - %(levelname)s %(message)s')

handler = logging.StreamHandler()
handler.setFormatter(formatter)

logger = logging.getLogger('my-logger')
logger.setLevel(_CONF.level)
logger.addHandler(handler)

logger.info('my-logger started')


class Singleton(type):  # Type을 상속받음
    __instances = {}  # 클래스의 인스턴스를 저장할 속성

    def __call__(cls, *args, **kwargs):  # 클래스로 인스턴스를 만들 때 호출되는 메서드
        if cls not in cls.__instances:  # 클래스로 인스턴스를 생성하지 않았는지 확인
            cls.__instances[cls] = super().__call__(*args, **kwargs)  # 생성하지 않았으면 인스턴스를 생성하여 해당 클래스 사전에 저장
        return cls.__instances[cls]  # 클래스로 인스턴스를 생성했으면 인스턴스 반환


def debug_logger(fn: Callable):
    """Logger decorator"""

    @wraps(fn)
    def wrapper(*args, **kwargs):
        ret = fn(*args, **kwargs)
        logger.debug(f'in {fn.__name__}, args: {pformat(args)}, kwargs: {pformat(kwargs)}, return: {pformat(ret)}')
        return ret

    return wrapper


def basic_timer(fn: Callable):
    """Timer decorator"""

    @wraps(fn)
    def wrapper(*args, **kwargs):
        start = time()
        ret = fn(*args, **kwargs)
        end = time()
        logger.debug(f'in {fn.__name__}, Total execution time: {end - start}')
        return ret

    return wrapper
