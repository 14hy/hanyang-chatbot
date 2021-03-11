from flask_restx import Resource, Namespace, reqparse, fields
from flask_jwt_simple import jwt_required

ns_notice = Namespace("service/notice", description="Service/Notice")

parser = ns_notice.parser()
parser.add_argument(
    "Authorization",
    type=str,
    location="headers",
    help="Bearer jwt token",
    required=True,
)

NOTICE = None

@ns_notice.route("/")
class Bus(Resource):
    @ns_notice.doc(
        "태욱아 받아라",
        params={
        },
    )
    def get(self):
        return NOTICE if NOTICE else None

    @ns_notice.doc(
        "공지 등록.",
        params={"notice": "question"},
        parser=parser,
    )
    @jwt_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("notice", type=str, help="notice")
        args = parser.parse_args(strict=True)

        global NOTICE
        NOTICE = args.notice
        return "OK"
