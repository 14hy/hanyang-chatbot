from logging import Logger

from flask import Flask
from flask_cors import CORS
from flask_jwt_simple import JWTManager
from werkzeug.middleware.proxy_fix import ProxyFix

from api import api
from utils import Config, is_dev


app = Flask(__name__)
app.config.from_object(Config)

# Proxy middleware
# swagger fix
app.wsgi_app = ProxyFix(app.wsgi_app)

jwt = JWTManager(app)
CORS(app)

logger = app.logger
logger.setLevel(Config.LOG_LEVEL)
logger.propagate = False

api.init_app(app)

if __name__ == "__main__":
    app.run(host=Config.HOST, port=Config.PORT, debug=Config.DEBUG)
