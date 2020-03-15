import pytest
from dateutil.parser import parse
from flask.testing import FlaskClient

from app import app
from config import DevConfig as Config


@pytest.fixture
def client():
    app.config.from_object(Config)

    with app.test_client() as client:
        with app.app_context():
            pass
        yield client


@pytest.fixture
def jwt_token(client: FlaskClient):
    res = client.post(
        "/admin/login/",
        query_string=[("username", "dev"), ("password", "dev")],
    )
    yield res.json["jwt"]


# fmt: off
def test_admin_login(client: FlaskClient):
    res = client.post('/admin/login/', query_string=[('username', 'wrong'), ('password', 'wrong')])
    assert res.status_code == 401

    res = client.post('/admin/login/', query_string=[('username', 'dev'), ('password', 'dev')])
    assert res.status_code == 200
    assert res.json.get('jwt') is not None

    jwt_token = res.json['jwt']

    res = client.get(f'/admin/login/',
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


def test_qa_get(client: FlaskClient, jwt_token: str):
    res = client.get('/admin/qa/', query_string=[('offset', 0), ('limit', 5)],
                     headers={'Authorization': f'Bearer {jwt_token}'})
    assert res.status_code == 200
    assert res.json.get('data') is not None
    assert len(res.json.get('data')) == 5


def test_qa_add_delete(client: FlaskClient, jwt_token: str):
    res = client.post("/admin/qa/", query_string=[('question', 'test'), ('answer', 'test')],
                      headers={'Authorization': f'Bearer {jwt_token}'})
    assert res.status_code == 201

    doc_id = res.json.get('doc_id')
    assert doc_id is not None
    res = client.delete("/admin/qa/", query_string=[('doc_id', doc_id)],
                        headers={'Authorization': f'Bearer {jwt_token}'})
    assert res.status_code == 202


def test_admin_userinput(client: FlaskClient, jwt_token: str):
    res = client.get("/admin/userinput/", query_string=[('offset', 0), ('limit', 5)],
                     headers={'Authorization': f'Bearer {jwt_token}'})
    assert res.status_code == 200
    assert res.json.get('data') is not None
    assert len(res.json.get('data')) == 5
    a = parse(res.json.get('data')[0]['create_time'])
    b = parse(res.json.get('data')[1]['create_time'])
    assert a > b
