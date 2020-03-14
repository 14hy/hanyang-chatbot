from engine.services.food import *

# fmt: off
def test_get_recipe():
    assert not get_recipe(Restaurants.교직원식당)["restaurant"] == "-1"
    assert not get_recipe(Restaurants.창업보육센터)["restaurant"] == "-1"
    assert not get_recipe(Restaurants.창의인재원식당)["restaurant"] == "-1"
    assert not get_recipe(Restaurants.푸드코트)["restaurant"] == "-1"
    assert not get_recipe(Restaurants.학생식당)["restaurant"] == "-1"
