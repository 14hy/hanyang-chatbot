import os
import logging


# BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class Logger(object):
    # DEBUG - INFO - WARN - ERROR - CRITICAL
    level = "DEBUG"


class DataBase(object):
    host = '35.236.158.57'
    port = 27017
    username = 'postgres'
    password = 'password'
    db_name = 'postgres'


class Flask(object):
    host = '0.0.0.0'
    port = 8000
    debug = True
    version = 0.1
    title = 'hanyang-chatbot-dev'
    desc = 'development version'
