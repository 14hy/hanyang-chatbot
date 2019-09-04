from lib.flask_restplus import Api
from config import Basic as _CONF
from api.main import ns
from api.services.shuttle import ns_shuttle
from api.rive_dummy import ns_rive_dummy

api = Api(version=_CONF.version, title=_CONF.title, description=_CONF.desc)

api.add_namespace(ns)
api.add_namespace(ns_shuttle)
api.add_namespace(ns_rive_dummy)
