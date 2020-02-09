from lib.flask_restplus import Api
from config import Config as _CONF
from api.main import ns
from api.services.shuttle import ns_shuttle
from api.services.food import ns_food
from api.admin.main import ns_admin_add

api = Api(version=_CONF.VERSION, title=_CONF.TITLE, description=_CONF.DESC)

api.add_namespace(ns)
api.add_namespace(ns_shuttle)
api.add_namespace(ns_food)
api.add_namespace(ns_admin_add)
