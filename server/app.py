from logging import Logger

from flask import Flask
from flask_cors import CORS
from flask_jwt_simple import JWTManager

from api import api
from utils import Config

app = Flask(__name__)
app.config.from_object(Config)
jwt = JWTManager(app)
CORS(app)

logger: Logger = app.logger
logger.setLevel(Config.LOG_LEVEL)
logger.propagate = False

api.init_app(app)

if __name__ == "__main__":
    logger.info(f"starting app from local environment...")
    app.run(host=Config.HOST, port=Config.PORT, debug=Config.DEBUG)
