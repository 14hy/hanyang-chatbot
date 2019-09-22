from lib.flask_restplus import Resource, Namespace, fields, reqparse
from engine.services.food import get_recipe, Restaurants

ns_food = Namespace('service/food', description='Service/food')


@ns_food.route('/')
class Bus(Resource):

    @ns_food.doc('현재 시각을 기준으로 셔틀버스를 조회합니다.', params={'restaurant': '교직원식당, 학생식당, 창의인재원식당, 푸드코트, 창업보육센터'})
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('restaurant', type=str, help='식당이')
        args = parser.parse_args(strict=True)

        restaurant = args['restaurant']

        if hasattr(Restaurants, restaurant):
            return get_recipe(Restaurants[restaurant])
        return 400
