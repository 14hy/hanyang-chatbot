from datetime import datetime

from flask_jwt_simple import jwt_required
from flask_restx import Resource, Namespace, reqparse
from google.cloud.firestore_v1 import CollectionReference, Query

from db.connect import client
from utils import KST

ns_admin_userinput = Namespace("admin/userinput", description="유저 입")

parser = ns_admin_userinput.parser()
parser.add_argument(
    "Authorization",
    type=str,
    location="headers",
    help="Bearer jwt token",
    required=True,
)


@ns_admin_userinput.route("/")
class Edit(Resource):
    @ns_admin_userinput.doc(
        "유저 입력 보기", params={"offset": "offset", "limit": "limit"}, parser=parser
    )
    @jwt_required
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("offset", type=int, required=True)
        parser.add_argument("limit", type=int, required=True)
        args = parser.parse_args(strict=True)

        offset = args.get("offset")
        limit = args.get("limit")

        collection: CollectionReference = client.collection("user_input")
        query: Query = collection.order_by("create_time", direction=Query.DESCENDING)
        query = query.offset(offset)
        query = query.limit(limit)

        documents = list(query.stream())
        data = []
        for doc in documents:
            _data = doc._data
            create_time = None
            if _data.get("create_time"):
                create_time = datetime.fromtimestamp(
                    _data["create_time"], tz=KST
                ).strftime("%Y-%m-%d %H:%M:%S")
            data.append(
                {
                    "id": doc.id,
                    "userInput": _data["text"],
                    "answer": _data.get("answer"),
                    "create_time": create_time,
                }
            )

        count = len(data)
        return {"count": count, "data": data}, 200
