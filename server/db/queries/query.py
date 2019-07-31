import pickle

import numpy as np

from db.questions.index import find_by_text


class Query(object):
    def __init__(self, chat, feature_vector, keywords,
                 matched_question, manhattan_similarity,
                 jaccard_similarity, category=None, added_time=None, answer=None, morphs=None, measurement=None):
        self.chat = chat
        self.feature_vector = feature_vector
        self.keywords = keywords
        self.matched_question = matched_question  # 어떤 질문과 매칭 되었었는지.
        self.manhattan_similarity = manhattan_similarity  # 거리는 어떠 하였는 지
        self.jaccard_similarity = jaccard_similarity
        self.category = category
        self.added_time = added_time
        self.answer = answer
        self.morphs = morphs
        self.measurement = measurement


def convert_to_query(document):
    feature_vector = pickle.loads(np.array(document['feature_vector']))
    matched_question = find_by_text(document['matched_question'])
    query = Query(chat=document['chat'],
                  feature_vector=feature_vector,
                  keywords=document['keywords'],
                  matched_question=matched_question,
                  manhattan_similarity=document['manhattan_similarity'],
                  jaccard_similarity=document['jaccard_similarity'],
                  added_time=document['added_time'],
                  answer=document['answer'],
                  morphs=document['morphs'],
                  measurement=document['measurement'],
                  category=document['category'])
    return query


def convert_to_document(query):
    query.feature_vector = pickle.dumps(query.feature_vector)
    if query.matched_question is not None:
        query.matched_question = query.matched_question.text
    return query.__dict__
