from db.connect import db
from db import *
from engine.preprocessor.clean import clean

collection = db.collection('qna')


def add_qna(question, answer):
    question = clean(question)
    answer = qna(question=question, answer=answer)
    ret = collection.add(answer.to_dict())

    return ret
