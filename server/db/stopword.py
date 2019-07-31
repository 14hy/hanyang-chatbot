from mongoengine import *


class Stopword(Document):
    word = StringField(required=True, max_length=10)

    meta = {'collection': 'Stopword'}
