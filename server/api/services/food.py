from lib.flask_restplus import Resource, Namespace, fields, reqparse
from engine.services.food import get_recipe, Restaurants
from datetime import datetime
from threading import Thread
from utils import KST, logger

ns_food = Namespace('service/food', description='Service/food')

cache = {}
pool = []


def _is_corrupted(time: datetime) -> bool:
    now = datetime.now(tz=KST)
    if now.minute - time.minute > 60 or now.day != time.day:
        return True
    return False


def _refresh(restaurant):
    cache[restaurant] = get_recipe(Restaurants[restaurant])
    cache['time'] = datetime.now(KST)
    logger.info(f'refreshed {cache[restaurant]}')


for restaurant in Restaurants:
    _refresh(restaurant.name)


@ns_food.route('/')
class Bus(Resource):

    @ns_food.doc('오늘의 식단을 가져옵니다.', params={'restaurant': '교직원식당, 학생식당, 창의인재원식당, 푸드코트, 창업보육센터'})
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('restaurant', type=str, help='식당')
        args = parser.parse_args(strict=True)
        restaurant = args['restaurant']

        if not hasattr(Restaurants, restaurant):
            return None, 400

        if not restaurant in cache:
            _refresh(restaurant)

        if _is_corrupted(cache['time']):
            pool.append(Thread(target=_refresh, args=[restaurant]))
            pool[-1].start()

        return cache[restaurant]
