import config
from flask_restplus import Api
from api.v3.api import api as api_v3

api = Api(version=config.Flask.version, title=config.Flask.title, description=config.Flask.desc)

# version-3
api.add_namespace(api_v3)
