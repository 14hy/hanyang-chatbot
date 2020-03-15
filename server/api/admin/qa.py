from flask_jwt_simple import jwt_required

from engine.admin import *
from flask_restplus import Resource, Namespace, reqparse

from utils import get_response

ns_admin_add = Namespace("admin/add", description="질문을 추가 합니다.")


@ns_admin_add.route("/")
class QA(Resource):
    @ns_admin_add.doc(
        "새로운 질문을 추가합니다.", params={"question": "question", "answer": "answer"}
    )
    @jwt_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("answer", type=str, help="answer")
        parser.add_argument("question", type=str, help="question")
        args = parser.parse_args(strict=True)

        question = args.question
        answer = args.answer

        ret = add_qa(question=question, answer=answer)
        return get_response(ret), 201
