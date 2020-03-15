import datetime
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class Config(object):
    BASE_DIR = BASE_DIR
    LOG_LEVEL = None

    # FLASK
    HOST = None
    PORT = None
    DEBUG = None
    VERSION = None
    TITLE = None
    DESC = None
    SECRET_KEY = None

    # FireStore
    PROJECT_ID = "cool-benefit-185923"
    SERVICE_ACCOUNT = ""

    # paths
    SHUTTLE_DIR = "shuttle_files"
    APPLICATION_ROOT = None


class DevConfig(Config):
    LOG_LEVEL = "DEBUG"

    # FLASK
    HOST = "0.0.0.0"
    PORT = 8001
    DEBUG = True
    TESTING = True
    VERSION = 0.3
    TITLE = "hanyang-chatbot-api"
    DESC = ""
    SECRET_KEY = open(f"{BASE_DIR}/cert/secret_key", mode="r").readline()
    JWT_SECRET_KEY = SECRET_KEY

    # FireStore
    PROJECT_ID = ""
    SERVICE_ACCOUNT = f"{BASE_DIR}/cert/service_account.json"

    # paths
    SHUTTLE_DIR = f"{BASE_DIR}/shuttle_files"

    # login
    LOGIN_TOKEN = "baf06612f9fc2e34694ca1b4254e4a8f368ea6c80f0f901743062a3a482b17ff"
    JWT_EXPIRES = datetime.timedelta(days=365)
    APPLICATION_ROOT = "/hanyang-chatbot"


class ProdConfig(Config):
    LOG_LEVEL = "INFO"

    # FLASK
    HOST = "0.0.0.0"
    PORT = 8001
    DEBUG = False
    VERSION = 0.3
    TITLE = "hanyang-chatbot-api"
    DESC = ""
    SECRET_KEY = open(f"{BASE_DIR}/cert/secret_key", mode="r").readline()
    JWT_SECRET_KEY = SECRET_KEY

    # FireStore
    PROJECT_ID = "cool-benefit-185923"
    SERVICE_ACCOUNT = ""

    # paths
    SHUTTLE_DIR = f"{BASE_DIR}/shuttle_files"

    # login
    LOGIN_TOKEN = "4373671fc1e3dd6517f264c30e70e904016f668b422b210f7083453eec1b722d"
    JWT_EXPIRES = datetime.timedelta(hours=1)
    APPLICATION_ROOT = "/hanyang-chatbot"


if __name__ == "__main__":
    print(BASE_DIR)
    print(Config.SECRET_KEY)
