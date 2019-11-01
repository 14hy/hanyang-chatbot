class qna(object):
    def __init__(self, question, answer):
        self.question: str = question
        self.answer: str = answer

    @staticmethod
    def from_dict(source):
        return qna(**source)

    def to_dict(self):
        return self.__dict__

    def __repr__(self):
        return f'<{self.__class__.__name__}({str(self.__dict__)})>'
