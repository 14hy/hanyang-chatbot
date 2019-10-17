from lib.flask_restplus import Resource, Namespace
from engine.main import Chatbot
from db.connect import db
from db.user_input import UserInput

# from engine.preprocessor.morph import analyze

# chatbot = Chatbot()
ns = Namespace(name='', description='Restful API')

user_input = db.collection('user_input')


@ns.route('/<string:text>')
class Index(Resource):

    @ns.doc('챗봇 입력')
    def get(self, text):
        ui = UserInput(text=text)

        user_input.add(ui.to_dict())

        return text
