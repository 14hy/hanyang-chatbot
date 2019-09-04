from lib.flask_restplus import Resource, Namespace, fields
from engine.services.shuttle import ShuttleBus

shuttle_bus = ShuttleBus()
ns_shuttle = Namespace('service/shuttle', description='Service/Shuttle')

station_list = ['dorm_cycle', 'dorm_station', 'dorm_artin', 'shuttle_cycle', 'shuttle_station',
                'shuttle_artin', 'station', 'station_artin', 'artin', 'shuttle_dorm']

resource_station = [ns_shuttle.model(name='station', model={
    'status': fields.Boolean,
    'minutes': fields.Integer,
    'seconds': fields.Integer
}) for station in station_list]

resource_shuttle = ns_shuttle.model(name='shuttle',
                                    model={station: fields.Nested(resource)
                                           for station, resource in
                                           zip(station_list, resource_station)})


@ns_shuttle.route('/')
class Bus(Resource):

    @ns_shuttle.marshal_with(resource_shuttle, as_list=True)
    @ns_shuttle.doc('현재 시각을 기준으로 셔틀버스를 조회합니다.')
    def get(self): \
            return shuttle_bus.response()
