from typing import List


class RiveLog(object):
    def __init__(self):
        pass

    @staticmethod
    def from_dict(source):
        return RiveLog(**source)

    def to_dict(self):
        return self.__dict__

    def __repr__(self):
        return f'<{self.__class__.__name__}({str(self.__dict__)})>'
