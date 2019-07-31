import config
from flask_restplus import Api
from api.v3.api import api as v3_api


CONFIG = config.FLASK

api = Api(version=CONFIG['version'], title=CONFIG['title'], description=CONFIG['desc'])

# version-3
api.add_namespace(v3_api)
