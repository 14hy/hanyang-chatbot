# 모든 Answer query, filter 선택으로 속도 빠르게하기. 인덱싱도 고려

# 유사도 구하기.
import db
from engine import preprocessor
from mongoengine import QuerySet
from collections import OrderedDict


def _calc_silmiarity(grams_1, grams_2):
    union = len(grams_1) + len(grams_2)
    joint = 0

    for each in grams_1:
        if each in grams_2:
            joint += 1
    return joint / (union - joint)


def get_similarity(text, n=1):
    n_gram_text = preprocessor.n_gram.bigram(text)
    answers: QuerySet = db.answer.Answer.objects()

    similarities = {}

    for each in answers:
        n_gram_answer = preprocessor.n_gram.bigram(each.answer)
        confidence = _calc_silmiarity(n_gram_answer, n_gram_text)
        similarities[each.pk] = confidence

    return OrderedDict(sorted(similarities.items(), key=lambda x: x[1], reverse=True))
