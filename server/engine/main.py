from collections import OrderedDict
from engine.analyze.main import get_similarity
from engine.utils import Singleton
from engine.preprocessor import *
import db


class Chatbot(metaclass=Singleton):

    def __init__(self):
        pass

    def get_response(self, text):
        """전처리, 유사도분석, 카테고리 분류, 답변생성"""
        text_clean = clean.clean(text)
        similarities: OrderedDict = get_similarity(text_clean)
        answer_pk, confidence = list(similarities.items())
        answer: db.answer.Answer = db.answer.Answer.objects(pk=answer_pk).next()

        category = answer.category
        query = db.query.Query(query=text, answer=answer, confidence=confidence)
        query.save()

        return 'get_response'

    # def _handle_category(self, query: db.query.Query):
    #     answer: LazyReference = query.answer
    #     answer: db.answer.Answer = answer.fetch()
    #
    #     category = answer.category
