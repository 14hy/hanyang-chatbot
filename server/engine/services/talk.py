import json
import random
from collections import OrderedDict

import pypandoc
from konlpy.tag import Mecab
import pymongo
from pymongo import MongoClient

from db.connect import client
from db.models import UserInput
from engine.preprocessor.n_gram import *
from utils import *
import re

mecab = Mecab()

# Mongo
mongo_client = MongoClient(host=Config.MONGO_HOST, port=Config.MONGO_PORT)
namu_wiki = mongo_client['wiki']['namu']
if not is_dev():
    namu_wiki.create_index([('title', pymongo.TEXT)])

# Firestore
collection_qna = client.collection("qna")
qna_collection = list(collection_qna.stream())


@log_time
@log_fn
def get_response(user_input: UserInput):
    def _get_answers_from_qa():
        ui = user_input.to_dict()
        query = ui["text"]
        global qna_collection
        distance_dict = {}
        top_answers = []
        for qna in qna_collection:
            qna = qna.to_dict()
            question = qna["question"]
            answer = qna["answer"]

            _score = _get_score(query, question)
            distance_dict[answer] = _score

        distance_dict = OrderedDict(
            sorted(distance_dict.items(), key=lambda t: t[1], reverse=True)
        )
        ret = list(distance_dict.items())
        top_answers = []
        for each in ret:
            answer, score = each
            if score < Config.QA_THRESHOLD:
                break
            top_answers.append(answer)
        return top_answers

    answers = _get_answers_from_qa()
    if answers:
        return random.choice(answers)
    return answer_from_wiki(user_input)


def _get_score(a, b):
    def _jaccard(a_grams, b_grams):
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
        score_unigram = _jaccard(grams_a, grams_b)
    grams_a = bigram(a)
    grams_b = bigram(b)
    if len(grams_a) > 1 and len(grams_b) > 1:
        score_bigram = _jaccard(grams_a, grams_b)
    grams_a = trigram(a)
    grams_b = trigram(b)
    if len(grams_a) > 2 and len(grams_b) > 2:
        score_trigram = _jaccard(grams_a, grams_b)

    return score_unigram + score_bigram + score_trigram


@log_fn
@log_time
def answer_from_wiki(user_input):
    def _extract_headers(blocks):
        ret = []
        for each in blocks:
            block_tag = each.get('t')
            block_content = each.get('c')

            if block_tag == 'Header':
                content = block_content[-1][0]['c']
                if isinstance(content, str):
                    ret.append(content)
        return ret

    def _get_paragraphs(blocks, header):
        ret = []

        found = False
        for each in blocks:

            # start extracting paragraphs
            if found and each['t'] == 'Para':
                temp = []
                paragraph_contexts = each['c']
                for pc in paragraph_contexts:
                    if pc['t'] == 'Str':
                        temp.append(pc['c'])
                ret.append(' '.join(temp))

            if each['t'] == 'Header':
                if found:
                    found = False
                elif each['c'][-1][0]['c'] in header:
                    found = True
        return ret

    def _extract_terms():
        terms = []

        pos = mecab.pos(user_input.text)
        for each in pos:
            text, tag = each
            if tag == 'NNG':
                if terms:
                    terms.append(''.join(terms) + text)
                terms.append(text)

        terms.extend(user_input.text.split())
        return terms

    def _find_from_wiki(term):
        target = namu_wiki.find_one({'$text': {'$search': term}})

        if not target:
            return None

        # preprocess raw wiki data
        text = pypandoc.convert_text(target['text'], 'json', 'mediawiki')
        text = json.loads(text)
        return text['blocks']

    def _to_answer(paragraphs):

        answer = ''
        for p in paragraphs:
            p = re.sub(r'[\[\(\{]{1}.*[\]\)\}]{1}', '', p)
            if re.match(r'^>', p):
                continue

            answer_ = answer + p
            if answer and len(answer_) > Config.MAX_ANSWER_LENGTH:
                break
            answer = answer_

        if answer:
            answer = list(answer)
            if answer[-1] == '.':
                answer[-1] = '냥!'
            return ''.join(answer)

        return None

    terms = _extract_terms()

    if terms is None:
        return None

    for term in terms:
        blocks = _find_from_wiki(term)

        if not blocks:
            continue

        headers = _extract_headers(blocks)

        if '개요' not in headers and '소개' not in headers:
            logger.debug(f'header not found! header: {headers}')
            continue

        paragraphs = _get_paragraphs(blocks, ['개요', '소개'])
        return _to_answer(paragraphs)

    return None
