from flask_jwt_simple import jwt_required
from flask_restx import Resource, Namespace, reqparse

import ast
from engine.services.shuttle import ShuttleBus, to_str, from_str

ns_admin_shuttle = Namespace("admin/shuttle", description="셔틀버스 조작")

parser = ns_admin_shuttle.parser()
parser.add_argument(
    "Authorization",
    type=str,
    location="headers",
    help="Bearer jwt token",
    required=True,
)


@ns_admin_shuttle.route("/edit")
class Edit(Resource):

    @staticmethod
    def to_ret(data):

        ret = []
        for each in data or []:
            if len(each) == 5:
                ret.append(to_str(each))
            elif len(each) == 3:
                _ret = []
                for x in each[:2]:
                    _ret.extend(from_str(x))
                _ret.append(each[2])
                ret.append(_ret)
            else:
                raise Exception
        return ret

    @ns_admin_shuttle.doc(
        "셔틀버스 조작",
        params={"season": "학기중, 계절, 방학", "bus": "순환노선, 한대앞, 예술인", "weekend": "월금, 휴일"},
        parser=parser,
    )
    @jwt_required
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("season", type=str, required=True)
        parser.add_argument("bus", type=str, required=True)
        parser.add_argument("weekend", type=str, required=True)
        args = parser.parse_args(strict=True)
        season = args.get("season")
        bus = args.get("bus")
        weekend = args.get("weekend")
        table = ShuttleBus.get_table(season, bus, weekend)

        table = Edit.to_ret(table)
        return {"data": table}, 200

    @ns_admin_shuttle.doc(
        "셔틀버스 조작",
        params={
            "data": "table data, list of list",
            "season": "학기중, 계절, 방학",
            "bus": "순환노선, 한대앞, 예술인",
            "weekend": "월금, 휴일",
        },
        parser=parser,
    )
    @jwt_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("data", type=str, help="data", required=True)
        parser.add_argument("season", type=str, required=True)
        parser.add_argument("bus", type=str, required=True)
        parser.add_argument("weekend", type=str, required=True)
        args = parser.parse_args(strict=True)

        season = args.get("season")
        bus = args.get("bus")
        weekend = args.get("weekend")
        data = args.get("data")
        data = ast.literal_eval(data)

        data = Edit.to_ret(data)
        updated = ShuttleBus.set_recipe(data, season, bus, weekend)
        updated = Edit.to_ret(updated)
        return {"updated": updated}, 201
