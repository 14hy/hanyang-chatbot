from typing import List


class RivePresets(object):
    def __init__(self, name, sets):
        self.name: str = name
        self.sets: List[str] = sets

        assert isinstance(self.sets, List), 'Type Error'

    @staticmethod
    def from_dict(source):
        return RivePresets(**source)

    def to_dict(self):
        return self.__dict__

    def __repr__(self):
        return f'<{self.__class__.__name__}({str(self.__dict__)})>'
