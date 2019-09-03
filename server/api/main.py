from flask_restplus import Resource, Namespace, Api
import config
from engine.main import Chatbot
from app import logger
from engine.preprocessor.morph import analyze

chatbot = Chatbot()
ns = Namespace(name='', description='Restful API')


@ns.route('/<string:text>')
class Index(Resource):

    @ns.doc('챗봇 입력', params={'text': '입력'})
    def get(self, text):
        logger.info(text)

        return analyze(text)


api = Api(version=config.Flask.version, title=config.Flask.title, description=config.Flask.desc)

from .services.shuttle import ns_shuttle

api.add_namespace(ns)
api.add_namespace(ns_shuttle)
