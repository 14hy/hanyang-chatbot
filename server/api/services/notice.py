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
DEFAULT_NOTICE = """
안녕하냥~ 하냥이다냥~!! <br>
<img src="https://blog.mhlee.dev/wp-content/uploads/2021/03/image-4.png"> <br>
개선사항이 있으면 스토어에서 리뷰를 써달라냥!! 🙏<br><br>
그리고!! <br>
셔틀 시간표가 자주 바뀌므로 😭 <br>
공식 시간표 및 공지도 참고해달라냥! <br>
<img src="https://www.hanyang.ac.kr/documents/20182/6049116/20190923-bus3.png"> <br>


https://www.hanyang.ac.kr/<br>web/www/shuttle_bus_timetable <br>
"""


@ns_notice.route("/")
class Bus(Resource):
    @ns_notice.doc(
        params={
        },
    )
    def get(self):
        return NOTICE if NOTICE else DEFAULT_NOTICE

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
