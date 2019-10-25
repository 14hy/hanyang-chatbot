from db.connect import db
from db.user_input import UserInput
from engine.preprocessor.n_gram import *
from collections import OrderedDict

collection_qna = db.collection('qna')


def _calc_jaacard(a, b):
    def __calc_jaccard(a_grams, b_grams):
        visited = []
        num_union = max(len(a_grams), len(b_grams))  # output 뺀 것
        num_joint = 0
        for gram_a in a_grams:
            for gram_b in b_grams:
                if (gram_a == gram_b) and (gram_a not in visited):
                    num_joint += 1
                    visited.append(gram_a)

        return num_joint / num_union

    a_grams, b_grams = bigram(a), bigram(b)
    score_bigram = __calc_jaccard(a_grams, b_grams)
    a_grams, b_grams = trigram(a), trigram(b)
    score_trigram = __calc_jaccard(a_grams, b_grams)

    return score_bigram + score_trigram


def get_response(user_input: UserInput):
    ui = user_input.to_dict()
    a = ui['text']
    stream_qna = collection_qna.stream()

    distance_dict = {}

    for qna in stream_qna:
        qna = qna.to_dict()
        question = qna['question']
        answer = qna['answer']

        b = question
        _score = _calc_jaacard(a, b)
        distance_dict[answer] = _score

    return OrderedDict(sorted(distance_dict.items(), key=lambda t: t[1], reverse=True))


if __name__ == '__main__':
    test_ui = UserInput('test')
    print(get_response(test_ui))
