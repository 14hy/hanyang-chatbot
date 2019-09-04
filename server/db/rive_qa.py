from typing import List
from db.connect import db
from utils import *


class RiveQA(object):
    def __init__(self, idx, q, a):
        self.idx: int = idx
        self.q: List[dict] = q
        self.a: List[dict] = a

    @staticmethod
    def from_dict(source):
        return RiveQA(**source)

    def to_dict(self):
        return self.__dict__

    def __repr__(self):
        return f'<{self.__class__.__name__}({str(self.__dict__)})>'

    def to_sj(self):

        _q = self.q.copy()

        for q in _q:
            for key, value in q.items():
                if 'star' in key and value is not '*':
                    logger.debug(f'star found in {key} - {value}')
                    rive_presets = db.collection('rive_presets')
                    sets = next(rive_presets.where('name', '==', value).stream()).to_dict()['sets']
                    q[key] = sets

        ret = {'q': _q, 'a': self.a, 'idx': self.idx}
        return ret
