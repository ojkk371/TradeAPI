from app.database.conn import db
from app.database.schema import Users


def test_registration(client, session):
    user = dict(email="test@examples.com", api_key='test11', secret_key='test22')
    res = client.post("api/auth/register/email", json=user)
    res_body = res.json()
    print(res.json())
    assert res.status_code == 201
    assert "Authorization" in res_body.keys()


def test_registration_exist_email(client, session):
    user = dict(email="test@examples.com", api_key='test11', secret_key="test22")
    db_user = Users.create(session=session, **user)
    session.commit()
    res = client.post("api/auth/register", json=user)
    res_body = res.json()
    assert res.status_code == 400
    assert 'EMAIL_EXISTS' == res_body["msg"]
