from fastapi.testclient import TestClient
from ..app.main import app

import pytest
from ..app import models

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ..app.database import get_db, Base
from ..app.oauth2 import create_access_token

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:123456@localhost:5432/fastapi_test"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture()
def session():
    # Drop all existing instances before testing
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(session):
    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture
def test_user(client):
    user_data = {"email": "hello12235@gmail.com",
                 "password": "123456"
                 }
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user


@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user["id"]})


@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client


@pytest.fixture
def test_posts(test_user, session):
    posts_data = [{
        "title": "first title",
        "content": "random content",
        "user_id": test_user["id"]
    }, {
        "title": "second title",
        "content": "random content2",
        "user_id": test_user["id"]
    }, {
        "title": "third title",
        "content": "random content3",
        "user_id": test_user["id"]
    }]

    def create_post_modes(post):
        return models.Post(**post)

    post_map = map(create_post_modes, posts_data)
    posts = list(post_map)
    session.add_all(posts)
    # session.add_all([models.Post(title="first title", content="random content", owner_id=test_user["id"]),
    #                  models.Post(title="second title", content="random content2", owner_id=test_user["id"]),
    #                  models.Post(title="third title", content="random content3", owner_id=test_user["id"])])

    session.commit()
    new_posts = session.query(models.Post).all()
    return new_posts
