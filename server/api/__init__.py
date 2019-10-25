from lib.flask_restplus import Api
from config import Basic as _CONF
from api.main import ns
from api.services.shuttle import ns_shuttle
from api.services.food import ns_food
from api.admin.main import ns_admin_add

# from api.rive_dummy import ns_rive_dummy

api = Api(version=_CONF.version, title=_CONF.title, description=_CONF.desc)

api.add_namespace(ns)
api.add_namespace(ns_shuttle)
api.add_namespace(ns_food)
api.add_namespace(ns_admin_add)
# api.add_namespace(ns_rive_dummy)
