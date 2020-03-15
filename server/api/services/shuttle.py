from engine.services.shuttle import ShuttleBus
from flask_restplus import Resource, Namespace, reqparse, fields

shuttle_bus = ShuttleBus()
ns_shuttle = Namespace("service/shuttle", description="Service/Shuttle")

station_list = [
    "dorm_cycle",
    "dorm_station",
    "dorm_artin",
    "shuttle_cycle",
    "shuttle_station",
    "shuttle_artin",
    "station",
    "station_artin",
    "artin",
    "shuttle_dorm",
]


@ns_shuttle.route("/")
class Bus(Resource):
    @ns_shuttle.doc(
        "현재 시각을 기준으로 셔틀버스를 조회합니다.",
        params={
            "weekend": "평일, 주말",
            "season": "학기중, 계절학기, 방학중",
            "hours": "int",
            "minutes": "int",
            "seconds": "int",
            "now": "bool (기본값: True)",
        },
    )
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("weekend", type=str, required=False)
        parser.add_argument("season", type=str, required=False)
        parser.add_argument("hours", type=int, required=False)
        parser.add_argument("minutes", type=int, required=False)
        parser.add_argument("seconds", type=int, required=False)
        parser.add_argument("now", type=fields.boolean, required=False, default=True)
        args = parser.parse_args(strict=True)

        if args["now"]:
            return shuttle_bus.get_current()
        return shuttle_bus.get(
            args["season"],
            args["weekend"],
            hours=args["hours"],
            minutes=args["minutes"],
            seconds=args["seconds"],
        )
