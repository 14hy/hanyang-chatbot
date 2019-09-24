from lib.flask_restplus import Resource, Namespace, reqparse, fields
from engine.services.shuttle import ShuttleBus

shuttle_bus = ShuttleBus()
ns_shuttle = Namespace('service/shuttle', description='Service/Shuttle')

station_list = ['dorm_cycle', 'dorm_station', 'dorm_artin', 'shuttle_cycle', 'shuttle_station',
                'shuttle_artin', 'station', 'station_artin', 'artin', 'shuttle_dorm']

# station_list = ['dorm_cycle', 'dorm_station', 'dorm_artin', 'shuttle_cycle', 'shuttle_station',
#                 'shuttle_artin', 'station', 'station_artin', 'artin', 'shuttle_dorm']
#
# resource_station = [ns_shuttle.model(name='station', model={
#     'status': fields.Boolean,
#     'minutes': fields.Integer,
#     'seconds': fields.Integer
# }) for station in station_list]
#
# resource_shuttle = ns_shuttle.model(name='shuttle',
#                                     model={station: fields.Nested(resource)
#                                            for station, resource in
#                                            zip(station_list, resource_station)})


@ns_shuttle.route('/')
class Bus(Resource):

    # @ns_shuttle.marshal_with(resource_shuttle, as_list=True)
    @ns_shuttle.doc('현재 시각을 기준으로 셔틀버스를 조회합니다.', params={'weekend': '평일, 주말',
                                                        'season': '학기중, 계절학기, 방학중',
                                                        'hours': 'int',
                                                        'minutes': 'int',
                                                        'seconds': 'int',
                                                        'now': 'bool (기본값: True)'})
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('weekend', type=str, required=False)
        parser.add_argument('season', type=str, required=False)
        parser.add_argument('hours', type=int, required=False)
        parser.add_argument('minutes', type=int, required=False)
        parser.add_argument('seconds', type=int, required=False)
        parser.add_argument('now', type=fields.boolean, required=False, default=True)
        args = parser.parse_args(strict=True)

        if args['now']:
            return shuttle_bus.response()
        else:
            return shuttle_bus.custom_response(args['weekend'], args['season'], args['hours'], args['minutes'],
                                               args['seconds'])
