from engine.data.query import QueryMaker
from db.index import *
from datetime import datetime, timezone
from tqdm import tqdm

collection = db[MONGODB_CONFIG['col_queries']]
_query_maker = QueryMaker()


def insert(query):
    document = convert_to_document(query=query)
    return collection.insert_one(document)


def get_list():
    queries = []
    cursor = collection.find({})

    for document in cursor:
        query = convert_to_query(document)
        queries.append(query)
    return queries


def find_all():
    queries = []
    for document in collection.find({}):
        query = convert_to_query(document)
        queries.append(query)
    return queries


def find_by_category(category):
    queries = []
    for document in collection.find({'category': category}):
        query = convert_to_query(document)
        queries.append(query)
    return queries


def find_by_date(year, month, day, hour=0, minute=0, second=0):
    NOW = datetime(year=year, month=month, day=day,
                   hour=hour, minute=minute, second=second)
    UTC = timezone.utc

    NOW.astimezone(UTC)

    queries = collection.find({'added_time': {'$gte': NOW}})

    return list(queries)


def rebase():
    for document in tqdm(collection.find({}), desc='Rebase query'):
        _id = document['_id']
        chat = document['chat']
        try:
            added_time = document['added_time']
        except KeyError:
            added_time = None

        try:

            query = _query_maker.make_query(chat=chat,
                                            added_time=added_time)
            if query is None:
                collection.delete_one({'_id': _id})
                continue
            insert(query)
            collection.delete_one({'_id': _id})
        except Exception as err:
            print('rebase ERROR: ', err)
            print(document)
            return document


if __name__ == '__main__':
    # rebase()
    a = find_by_date(2019, 5, 29, 0)
