import random
from collections import OrderedDict

from db.connect import client
from db.models import UserInput
from engine.preprocessor.n_gram import *
from utils import *


@log_time
@log_fn
def get_response(user_input: UserInput):
    ui = user_input.to_dict()
    a = ui["text"]
    global stream_qna

    distance_dict = {}

    for qna in stream_qna:
        qna = qna.to_dict()
        question = qna["question"]
        answer = qna["answer"]

        b = question
        _score = _calc_jaacard(a, b)
        distance_dict[answer] = _score

    distance_dict = OrderedDict(
        sorted(distance_dict.items(), key=lambda t: t[1], reverse=True)
    )
    ret = list(distance_dict.items())

    top_score = 0
    top_answers = []
    for each in ret:
        if top_score == 0:
            if each[1] != 0:
                top_score = each[1]
                top_answers.append(each[0])
        else:
            if top_score == each[1]:
                top_answers.append(each[0])
            else:
                break

    if not top_answers:
        return "잘 모르겠다냥~"
    else:
        ret = random.choice(top_answers)
        return ret


collection_qna = client.collection("qna")


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

    # Scores
    score_unigram = 0
    score_bigram = 0
    score_trigram = 0

    # Get scores

    grams_a = unigram(a)
    grams_b = unigram(b)
    if len(grams_a) > 0 and len(grams_b) > 0:
        score_unigram = __calc_jaccard(grams_a, grams_b)
    grams_a = bigram(a)
    grams_b = bigram(b)
    if len(grams_a) > 1 and len(grams_b) > 1:
        score_bigram = __calc_jaccard(grams_a, grams_b)
    grams_a = trigram(a)
    grams_b = trigram(b)
    if len(grams_a) > 2 and len(grams_b) > 2:
        score_trigram = __calc_jaccard(grams_a, grams_b)

    return score_unigram + score_bigram + score_trigram


stream_qna = list(collection_qna.stream())

if __name__ == "__main__":
    test_ui = UserInput("너 뭐냐")
    print(get_response(test_ui))
