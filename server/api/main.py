from lib.flask_restplus import Resource, Namespace
from pprint import pprint
from engine.preprocessor.clean import *
from engine.services.talk import *

# from engine.preprocessor.morph import analyze

# chatbot = Chatbot()
ns = Namespace(name='', description='Restful API')

user_input = db.collection('user_input')


@ns.route('/<string:text>')
class Index(Resource):

    @ns.doc('챗봇 입력')
    def get(self, text):
        text = clean(text, token=False)
        ui = UserInput(text=text)
        ret: dict = get_response(ui)
        pprint(ret)
        ret = list(ret.items())[0][0]

        user_input.add(ui.to_dict())

        return {'answer': ret}, 200
