from flask_jwt_simple import jwt_required
from flask_restx import Resource, Namespace, reqparse

from engine.services.shuttle import ShuttleBus

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

        return {"updated": ShuttleBus.set_recipe(data, season, bus, weekend)}
