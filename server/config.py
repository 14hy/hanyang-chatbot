import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class Config(object):
    """Basic Configuration"""

class DataBase(object):
    """DataBase Configuration"""
    host = 'localhost'
    port = 27017
    username = 'mhlee'
    password = 'mhlee'
    db_name = 'chatbot'
