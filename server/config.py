import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class Config(object):
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


class DevConfig(Config):
    LOG_LEVEL = "DEBUG"

    # FLASK
    HOSTS = "0.0.0.0"
    PORT = 8001
    SERVER_NAME = f"{HOSTS}:{PORT}"
    DEBUG = True
    TESTING = True
    VERSION = 0.3
    TITLE = "hanyang-chatbot-api"
    DESC = ""
    SECRET_KEY = open(f"{BASE_DIR}/cert/secret_key", mode="r").readline()

    # FireStore
    PROJECT_ID = ""
    SERVICE_ACCOUNT = f"{BASE_DIR}/cert/service_account.json"

    # paths
    SHUTTLE_DIR = "shuttle_files"


class ProdConfig(Config):
    LOG_LEVEL = None

    # FLASK
    HOST = "0.0.0.0"
    PORT = 8001
    DEBUG = False
    VERSION = 0.3
    TITLE = "hanyang-chatbot-api"
    DESC = ""
    SECRET_KEY = open(f"{BASE_DIR}/cert/secret_key", mode="r").readline()

    # FireStore
    PROJECT_ID = "cool-benefit-185923"
    SERVICE_ACCOUNT = ""

    # paths
    SHUTTLE_DIR = "shuttle_files"


if __name__ == "__main__":
    print(BASE_DIR)
    print(Config.SECRET_KEY)
