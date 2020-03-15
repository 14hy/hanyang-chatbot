from flask_restx import Resource, Namespace

from db.connect import client
from engine.preprocessor.clean import *
from engine.services.talk import *

ns = Namespace(name="", description="Restful API")

user_input = client.collection("user_input")


@ns.route("/<string:text>")
class Index(Resource):
    @ns.doc("챗봇 입력")
    def get(self, text):
        text = clean(text, token=False)
        ui = UserInput(text=text)
        ret: dict = get_response(ui)
        ui.answer = ret
        user_input.add(ui.to_dict())

        return {"answer": ret or "잘 모르겠다냥.."}, 200
