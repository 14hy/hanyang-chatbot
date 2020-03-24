from logging import Logger

from flask import Flask
from flask_cors import CORS
from flask_jwt_simple import JWTManager

from api import api
from utils import Config, is_dev

app = Flask(__name__)
app.config.from_object(Config)
jwt = JWTManager(app)
CORS(app)

logger: Logger = app.logger
logger.setLevel(Config.LOG_LEVEL)
logger.propagate = False

api.init_app(app)

if __name__ == "__main__":
    logger.info(f"running app in {'Dev' if is_dev() else 'Production'}")
    context = (
        f"{Config.BASE_DIR}/cert/mhlee.engineer.crt",
        f"{Config.BASE_DIR}/cert/mhlee.engineer.key",
    )
    app.run(host=Config.HOST, port=Config.PORT, debug=Config.DEBUG, ssl_context=context)
