import requests
from config import Basic as _CONF
import json


def get_dummy():
    res = requests.get(f'http://localhost:{_CONF.port}/rive_dummy/')
    res = json.loads(res.text)
    return res
