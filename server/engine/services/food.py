import requests
from enum import Enum
from lxml.html import fromstring
from lxml.cssselect import CSSSelector
from utils import *


class Restaurants(Enum):
    교직원식당 = "11"
    학생식당 = "12"
    창의인재원식당 = "13"
    푸드코트 = "14"
    창업보육센터 = "15"


@log_time
def get_recipe(restaurant, url="https://www.hanyang.ac.kr/web/www/re"):
    """식단 받아오기

    :return:
    {
        "조식": [
            {
                "menu": str,
                "price": int
            },
        ],
        "중":..,
        "석식":..
    }
    """
    ret = {}
    ret["restaurant"] = restaurant.name

    inboxes = CSSSelector("div.in-box")
    h4 = CSSSelector("h4")  # 조식, 중식, 석식
    h3 = CSSSelector("h3")  # menu
    li = CSSSelector("li")
    price = CSSSelector("p.price")
    # get
    try:
        res = requests.get(f"{url}{restaurant.value}")
    except requests.exceptions.RequestException as e:
        logger.error(e)
        ret["restaurant"] = "-1"
        return ret

    tree = fromstring(res.text)
    for inbox in inboxes(tree):
        title = h4(inbox)[0].text_content()
        ret[title] = []
        for l in li(inbox):
            menu = h3(l)[0].text_content().replace("\t", "").replace("\r\n", "")
            p = price(l)[0].text_content()
            ret[title].append({"menu": menu, "price": p})

    return ret
