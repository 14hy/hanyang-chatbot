from flask_restplus import Resource, Namespace, Api
import config
from engine.main import Chatbot
from main import logger

# from engine.preprocessor.morph import analyze

chatbot = Chatbot()
ns = Namespace(name='', description='Restful API')


@ns.route('/<string:text>')
class Index(Resource):

    @ns.doc('챗봇 입력', params={'text': '입력'})
    def get(self, text):
        logger.info(text)

        return chatbot.get_response(text)
