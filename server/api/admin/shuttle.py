import json

from flask_jwt_simple import jwt_required
from flask_restplus import Resource, Namespace, reqparse

from engine.services.shuttle import ShuttleBus
from utils import *

ns_admin_shuttle = Namespace("admin/shuttle", description="셔틀버스 조작")


@ns_admin_shuttle.route("/edit")
class Edit(Resource):
    @ns_admin_shuttle.doc("셔틀버스 조작", params={"target": "target"})
    @jwt_required
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("target", type=str, help="", required=False)
        args = parser.parse_args(strict=True)
        return ShuttleBus.get_recipe(args.get("target")), 200

    @ns_admin_shuttle.doc("셔틀버스 조작", params={"target": "target", "data": "data"})
    @jwt_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("target", type=str, help="target")
        parser.add_argument("data", type=str, help="data")
        args = parser.parse_args(strict=True)

        target = args.target
        data = args.data
        if ShuttleBus.make_recipe(target, data):
            return {"target": target, "data": data}, 201
        return 401


@ns_admin_shuttle.route("/manage")
class Manage(Resource):
    @ns_admin_shuttle.doc("현재 설정")
    @jwt_required
    def get(self):
        return ShuttleBus.get_manage(), 200

    @ns_admin_shuttle.doc("설정 하기", params={"target": "target"})
    @jwt_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("target", type=str, help="target", required=True)
        args = parser.parse_args(strict=True)
        manage = ShuttleBus.get_manage()
        manage["target"] = args.target
        with open(f"{Config.SHUTTLE_DIR}/manage.json", mode="w") as f:
            json.dump(manage, f)

        return ShuttleBus.get_manage(), 201
