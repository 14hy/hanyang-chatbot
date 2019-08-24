from flask import Flask
from flask_cors import CORS
import config
import logging

app = Flask(__name__)
logger: logging.Logger = app.logger
logger.setLevel(config.Logger.level)
logger.propagate = False
# 기본 Flask handler 를 사용합니다.
# https://docs.python.org/2/library/logging.html#logging.Logger.propagate
CORS(app)

if __name__ == '__main__':
    from api import api

    api.init_app(app=app)

    # context = ('/etc/nginx/certificate.crt', '/etc/nginx/private.key') # https 인증서 적용하기
    app.run(host=config.Flask.host, port=config.Flask.port, debug=config.Flask.debug)
