import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class Config(object):
    LOG_LEVEL = None

    # FLASK
    HOST = "0.0.0.0"
    PORT = 8001
    DEBUG = None
    VERSION = 0.3
    TITLE = "hanyang-chatbot-api"
    DESC = ""

    # FireStore
    PROJECT_ID = "hanyang-chatbot-7008b48daaa9"
    SERVICE_ACCOUNT = "hanyang-chatbot-7008b48daaa9.json"

    # paths
    SHUTTLE_DIR = "shuttle_files"

    # os.urandom(12).hex()
    SECRET_KEY = open(f"{BASE_DIR}/secret_key", mode="r").readline()


class DevConfig(Config):
    LOG_LEVEL = "DEBUG"
    DEBUG = True


class ProdConfig(Config):
    LOG_LEVEL = "DEBUG"
    DEBUG = False


if __name__ == "__main__":
    print(BASE_DIR)
    print(Config.SECRET_KEY)
