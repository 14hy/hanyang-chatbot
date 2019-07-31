from mongoengine import *
from datetime import datetime


class Query(Document):
    query = StringField(required=True, max_length=50)
    answer = LazyReferenceField(document_type='Answer', reverse_delete_rule=1)  # NULLIFY
    confidence = FloatField(min_value=0.0, max_value=100.0, required=True)
    added_time = DateField(required=True, default=datetime.utcnow)

    meta = {'collection': 'Query'}
