from flask import Flask
from config import Basic
from logging import Logger
from flask_cors import CORS
from api import api

_CONF = Basic

app = Flask(__name__)
CORS(app)

logger: Logger = app.logger
logger.setLevel(Basic.level)
logger.propagate = False

# from main import app
api.init_app(app)

if __name__ == "__main__":
    logger.info(f'starting app from local environment...')
    # context = ('/etc/nginx/certificate.crt', '/etc/nginx/private.key') # https 인증서 적용하기
    app.run(host=_CONF.host, port=_CONF.port, debug=_CONF.debug)
