from flask_restplus import Resource, Namespace
from engine.preprocessor.clean import *
from engine.services.talk import *
from db.connect import client

ns = Namespace(name="", description="Restful API")

user_input = client.collection("user_input")


@ns.route("/<string:text>")
class Index(Resource):
    @ns.doc("챗봇 입력")
    def get(self, text):
        text = clean(text, token=False)
        ui = UserInput(text=text)
        ret: dict = get_response(ui)

        user_input.add(ui.to_dict())

        return {"answer": ret}, 200
