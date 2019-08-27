import os
import logging


# BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class Logger(object):
    # DEBUG - INFO - WARN - ERROR - CRITICAL
    level = "INFO"

class test(object):
    pass

class DataBase(object):
    host = 'localhost'
    port = 27017
    username = 'mhlee'
    password = 'mhlee'
    db_name = 'chatbot'


class Flask(object):
    host = '0.0.0.0'
    port = 8000
    debug = True
    version = 0.1
    title = 'hanyang-chatbot-dev'
    desc = 'development version'
