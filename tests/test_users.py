from fastapi import FastAPI
from fastapi.testclient import TestClient
from ..app.main import app
from ..app import schemas

import pytest

from ..app.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from ..app.database import get_db, Base

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:123456@localhost:5432/fastapi_test"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture
def client():
    # something before the test
    Base.metadata.create_all(bind=engine) # Create the tables before the code runs
    yield TestClient(app)
    # something after the test
    Base.metadata.drop_all(bind=engine) # Drop all the tables


def test_root(client):
    res = client.get("/")
    print(res.json().get("message"))
    assert res.json().get("message") == "hello"
    assert res.status_code == 200


def test_create_user(client):
    res = client.post("/users/",
                      json={
                          "email": "hello12235@gmail.com",
                          "password": "123456"

                      })
    new_user = schemas.UserOut(**res.json())
    assert new_user.email == "hello12235@gmail.com"
    assert res.status_code == 201
