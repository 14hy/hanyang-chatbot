from flask_restplus import Resource, Namespace
from engine.main import Chatbot
from app import logger

chatbot = Chatbot()
api = Namespace(name='v3', description='version-3')


@api.route('/<string:text>')
class Index(Resource):

    @api.doc('챗봇 입력', params={'text': '입력'})
    def get(self, text):
        logger.debug(text)

        chatbot.get_response(text)
