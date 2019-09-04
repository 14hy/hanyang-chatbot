from db.connect import db
from db.rive_qa import RiveQA
from lib.flask_restplus import Resource, Namespace, fields

rive_qa = db.collection('rive_qa')

ns_rive_dummy = Namespace('rive_dummy', description='rive_dummy')


# resource_q = ns_rive_dummy.model(name='q',
#                                  model={'msg': fields.String(example="you can call my <star1> number at 1 (888) 555-5555.", description='사용자 질문 RAW 텍스트'),
#                                         'star*': fields.List(fields.String, description='star1, star2... 에 해당하는 preset string list', example=['happy', 'merry'])})
#
# resource_a = ns_rive_dummy.model(name='q',
#                                  model={'msg': fields.String(example="you can call my <star1> number at 1 (888) 555-5555.", description='사용자 질문 RAW 텍스트'),
#                                         'star*': fields.List(fields.String, description='star1, star2... 에 해당하는 preset string list', example=['happy', 'merry'])})
#
# resource_dummy = ns_rive_dummy.model(
#     name='rive-script-dummy data',
#     model={
#         'q': fields.List(fields.Nested(resource_q))
#     }
# )


@ns_rive_dummy.route('/')
class Route(Resource):

    # @ns_rive_dummy.marshal_with(resource_dummy, as_list=True)
    @ns_rive_dummy.doc('현재 시각을 기준으로 셔틀버스를 조회합니다.')
    def get(self):
        stream = rive_qa.stream()

        ret = []

        for qa in stream:
            qa = RiveQA.from_dict(qa.to_dict())
            ret.append(qa.to_sj())

        return ret
