class UserInput(object):
    def __init__(self, text):
        self.text: str = text

    @staticmethod
    def from_dict(source):
        return UserInput(**source)

    def to_dict(self):
        return self.__dict__

    def __repr__(self):
        return f'<{self.__class__.__name__}({str(self.__dict__)})>'
