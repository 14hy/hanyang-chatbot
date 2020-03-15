class QA(object):
    def __init__(self, question, answer):
        self.question: str = question
        self.answer: str = answer

    @staticmethod
    def from_dict(source):
        return QA(**source)

    def to_dict(self):
        return self.__dict__

    def __repr__(self):
        return f"<{self.__class__.__name__}({str(self.__dict__)})>"


class UserInput(object):
    def __init__(self, text, answer=None, create_time=None):
        self.text: str = text
        self.answer: str = answer
        self.create_time: int = create_time

    @staticmethod
    def from_dict(source):
        return UserInput(**source)

    def to_dict(self):
        return self.__dict__

    def __repr__(self):
        return f"<{self.__class__.__name__}({str(self.__dict__)})>"
