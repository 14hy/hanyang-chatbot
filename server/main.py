from flask import Flask
from lib.flask_restplus import Api
from .config import Basic
from logging import Logger

_CONF = Basic

app = Flask(__name__)

logger: Logger = app.logger
logger.setLevel(Logger.level)
logger.propagate = False

api = Api(version=_CONF.version, title=_CONF.title, description=_CONF.desc)

from api.main import ns
from api.services.shuttle import ns_shuttle

api.add_namespace(ns)
api.add_namespace(ns_shuttle)

api.init_app(app)

if __name__ == "__main__":
    # context = ('/etc/nginx/certificate.crt', '/etc/nginx/private.key') # https 인증서 적용하기
    app.run(host=_CONF.host, port=_CONF.port, debug=_CONF.debug)
