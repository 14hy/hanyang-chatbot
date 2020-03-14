import pytest
from flask.testing import FlaskClient

from config import DevConfig
from main import app


@pytest.fixture
def client():
    app.config.from_object(DevConfig)

    with app.test_client() as client:
        with app.app_context():
            pass
        yield client


@pytest.fixture
def jwt_token(client: FlaskClient):
    res = client.post(
        "/admin/login/",
        query_string=[("username", "username"), ("password", "password")],
    )
    yield res.json["jwt"]


# fmt: off
def test_admin_login(client: FlaskClient):
    res = client.post('/admin/login/', query_string=[('username', 'username'), ('password', 'password')])
    assert res.status_code == 200
    assert res.json.get('jwt') is not None

    jwt_token = res.json['jwt']

    res = client.get('/admin/login/',
                     query_string=[('username', 'username'), ('password', 'password')],
                     headers={'Authorization': f'Bearer {jwt_token}'})
    assert res.status_code == 200


def test_service_food_get(client: FlaskClient):
    assert client.get('/service/food/', query_string=[('restaurant', '교직원식당')]).status_code == 200
    assert client.get('/service/food/', query_string=[('restaurant', '학생식당')]).status_code == 200
    assert client.get('/service/food/', query_string=[('restaurant', '창의인재원식당')]).status_code == 200
    assert client.get('/service/food/', query_string=[('restaurant', '푸드코트')]).status_code == 200
    assert client.get('/service/food/', query_string=[('restaurant', '창업보육센터')]).status_code == 200

    assert client.get('/service/food/', query_string=[('restaurant', '없는')]).status_code == 400


def test_service_shuttle_get(client: FlaskClient):
    assert client.get('/service/shuttle/').status_code == 200


def test_admin_shuttle_edit(client: FlaskClient, jwt_token: str):
    res = client.get('/admin/shuttle/edit', query_string=[('season', '학기중'), ('bus', '순환노선'), ('weekend', '월금')],
                     headers={'Authorization': f'Bearer {jwt_token}'})
    assert res.status_code == 200
    assert res.json.get('data') is not None
