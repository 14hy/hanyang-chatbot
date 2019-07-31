from db.index import *
from db import convert_to_question, convert_to_document

collection = db[MONGODB_CONFIG['col_questions']]


def insert(question):
    '''
    :param question: Question object
    :return: InsertOneResult.inserted_id
    '''

    if question.feature_vector is None:
        raise Exception('feature feature_vector is None')

    document = convert_to_document(question)

    return collection.update_one(filter={'text': document['text']},
                                 update={'$set': document},
                                 upsert=True)  # update_one -> 중복 삽입을 막기 위해


def find_all():
    questions = []
    cursor = collection.find()

    for document in cursor:
        question = convert_to_question(document)
        questions.append(question)
    # questions = list(cursor)

    return questions


def find(field={}):
    questions = []
    cursor = collection.find({}, field)

    questions = list(cursor)

    return questions


def find_by_text(text):
    '''

    :param text:
    :return: Question object
    '''
    document = collection.find_one({'text': text})
    if document:
        return convert_to_question(document)
    return None


def find_by_keywords(keywords):
    '''

    :param keywords: list, keywords
    :return: list, of Question object
    '''
    output = []

    cursor = collection.find({'keywords': {'$in': keywords}})

    for document in cursor:
        question = convert_to_question(document)
        output.append(question)

    return output


def find_by_category(category):
    '''
    :param category:
    :return: list of Question objects
    '''

    questions = []
    cursor = collection.find({'category': category})

    for document in cursor:
        question = convert_to_question(document)
        questions.append(question)

    return questions


def delete_by_text(text):
    return collection.delete_one({'text': text})


def remove_by_text():
    pass


# a = find_by_text('오늘 메뉴 뭐에요').feature_vector
