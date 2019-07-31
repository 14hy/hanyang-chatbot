from mongoengine import *


class Answer(Document):
    question = StringField(max_length=50, required=True, unique=True)
    answer = StringField(required=False, null=True)
    category = StringField(required=True, choices=['1', '2'])  # TODO category

    meta = {'collection': 'Answer'}
