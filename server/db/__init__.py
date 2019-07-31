import config
from mongoengine import connect

MONGODB_CONFIG = config.DataBase

connect(MONGODB_CONFIG.db_name, username=MONGODB_CONFIG.username,
        host=MONGODB_CONFIG.host, port=MONGODB_CONFIG.port,
        password=MONGODB_CONFIG.password, authentication_source='admin')

__all__ = ['answer', 'julimmal', 'query', 'stopword']
