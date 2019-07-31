from mongoengine import *


class Julimmal(Document):
    orig = StringField(max_length=10, required=True, unique=True)
    sub = StringField(required=True)

    meta = {'collection': 'Julimmal'}

