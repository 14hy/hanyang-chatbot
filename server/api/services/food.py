from flask_restplus import Resource, Namespace, reqparse
from engine.services.food import get_recipe, Restaurants
from datetime import datetime
from utils import *

ns_food = Namespace("service/food", description="Service/food")

cache = {}


def _is_corrupted(time: datetime) -> bool:
    now = datetime.now(tz=KST)
    if now.minute - time.minute > 15 or now.day != time.day:
        return True
    return False


def _refresh(restaurant):
    cache[restaurant] = get_recipe(Restaurants[restaurant])
    cache["time"] = datetime.now(KST)
    logger.info(f"refreshed {cache[restaurant]}")


if not is_dev():
    for restaurant in Restaurants:
        _refresh(restaurant.name)


@ns_food.route("/")
class Food(Resource):
    @ns_food.doc(
        "오늘의 식단을 가져옵니다.", params={"restaurant": "교직원식당, 학생식당, 창의인재원식당, 푸드코트, 창업보육센터"}
    )
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("restaurant", type=str, help="식당")
        args = parser.parse_args(strict=True)
        restaurant = args["restaurant"]

        if not hasattr(Restaurants, restaurant):
            return None, 400

        if not restaurant in cache or _is_corrupted(cache["time"]):
            _refresh(restaurant)

        return cache[restaurant]
