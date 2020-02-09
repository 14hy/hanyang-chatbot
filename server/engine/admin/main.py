from db.connect import client
from db import *
from engine.preprocessor.clean import clean

collection = client.collection("qna")


def add_qa(question, answer):
    question = clean(question)
    answer = QA(question=question, answer=answer)
    ret = collection.add(answer.to_dict())

    return ret
