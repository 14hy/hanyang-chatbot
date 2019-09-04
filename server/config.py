# BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class Basic(object):
    # DEBUG - INFO - WARN - ERROR - CRITICAL
    level = "DEBUG"

    # FLASK
    host = '0.0.0.0'
    port = 8001
    debug = True
    version = 0.1
    title = 'hanyang-chatbot-api'
    desc = '2019 SW 학술대회 챗봇 빌더 API 서버'

    # FireStore
    project_id = 'cool-benefit-185923'
    serviceAccount = 'cool-benefit-185923.json'
