from fastapi.testclient import TestClient
from ..app.main import app

import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ..app.database import get_db, Base

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

