from datetime import datetime

from flask_jwt_simple import jwt_required
from flask_restplus import Resource, Namespace, reqparse
from google.cloud.firestore_v1 import CollectionReference, Query

from engine.admin import add_qa, client
from utils import KST

ns_admin_add = Namespace("admin/qa", description="질문을 추가 합니다.")


@ns_admin_add.route("/")
class QA(Resource):
    @ns_admin_add.doc("새로운 질문을 추가합니다.", params={"limit": "limit", "offset": "offset"})
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("limit", type=int, help="limit")
        parser.add_argument("offset", type=int, help="offset")
        args = parser.parse_args(strict=True)
        offset = args.get("offset")
        limit = args.get("limit")

        collection: CollectionReference = client.collection("qna")
        query: Query = collection.order_by("question")
        query = query.offset(offset)
        query = query.limit(limit)

        documents = list(query.stream())
        data = []
        for doc in documents:
            _data = doc._data
            data.append(
                {"id": doc.id, "question": _data["question"], "answer": _data["answer"]}
            )

        count = len(data)
        if not offset or not limit:
            pass
        else:
            data = data[offset : offset + limit]
        return {
            "count": count,
            "data": data,
        }

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

        elapsed_time, doc = add_qa(question=question, answer=answer)
        return (
            {
                "elapsed_time": str(
                    datetime.fromtimestamp(elapsed_time.seconds, tz=KST)
                ),
                "doc_id": doc.id,
            },
            201,
        )

    @ns_admin_add.doc("질문을 삭제 합니다.", params={"doc_id": "id"})
    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument("doc_id", type=str, help="id", required=True)
        args = parser.parse_args(strict=True)
        doc_id = args.get("doc_id")

        collection: CollectionReference = client.collection("qna")
        elapsed_time = collection.document(doc_id).delete()
        return (
            {
                "elapsed_time": str(
                    datetime.fromtimestamp(elapsed_time.seconds, tz=KST)
                ),
                "doc_id": doc_id,
            },
            202,
        )
