from flask_restx import Api

from api.admin.login import ns_admin_login
from api.admin.qa import ns_admin_add
from api.admin.shuttle import ns_admin_shuttle
from api.admin.user_input import ns_admin_userinput
from api.main import ns
from api.services.food import ns_food
from api.services.shuttle import ns_shuttle
from utils import Config

api = Api(version=Config.VERSION, title=Config.TITLE, description=Config.DESC,)

api.add_namespace(ns)
api.add_namespace(ns_shuttle)
api.add_namespace(ns_food)
api.add_namespace(ns_admin_add)
api.add_namespace(ns_admin_login)
api.add_namespace(ns_admin_shuttle)
api.add_namespace(ns_admin_userinput)
