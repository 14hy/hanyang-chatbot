from engine.services.food import *


def test_get_recipe():
    recipe = get_recipe(Restaurants.교직원식당)
    assert not recipe['restaurant'] == "-1"
    recipe = get_recipe(Restaurants.창업보육센터)
    assert not recipe['restaurant'] == "-1"
    recipe = get_recipe(Restaurants.창의인재원식당)
    assert not recipe['restaurant'] == "-1"
    recipe = get_recipe(Restaurants.푸드코트)
    assert not recipe['restaurant'] == "-1"
    recipe = get_recipe(Restaurants.학생식당)
    assert not recipe['restaurant'] == "-1"
