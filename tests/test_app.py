# pylint: disable=redefined-outer-name
import json
import datetime

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from wimwb.web import app
from wimwb.models import WhatismybrowserUseragentModel


SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)


def convert_datetime(datetime_str):
    """Convert datetime"""
    result = None
    try:
        result = datetime.datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        try:
            result = datetime.datetime.strptime(
                datetime_str, "%Y-%m-%d %H:%M:%S.%f"
            )
        except ValueError:
            pass
    return result


def import_db_dump(db):
    """Import data from dump into the database"""
    with open("tests/db_dump.json") as json_file:
        rows = json.loads(json_file.read())
        for row in rows[2:3]:
            # convert dates
            # 2010-03-23 10:42:17"
            if row["first_seen_at"]:
                row["first_seen_at"] = convert_datetime(row["first_seen_at"])
            if row["last_seen_at"]:
                row["last_seen_at"] = convert_datetime(row["last_seen_at"])
            # 2020-02-25 02:10:17.649732
            if row["updated_at"]:
                row["updated_at"] = convert_datetime(row["updated_at"])

            obj = WhatismybrowserUseragentModel(**row)
            db.add(obj)
        db.commit()


@pytest.fixture(scope="function")
def get_db():
    """Fixture to create inmemory sqlite database"""
    WhatismybrowserUseragentModel.metadata.create_all(engine)
    try:
        db = TestingSessionLocal()
        import_db_dump(db)  # import database from json dump
        yield db
    finally:
        WhatismybrowserUseragentModel.__table__.drop(
            engine
        )  # pylint: disable=no-member
        db.close()  # pylint: disable=no-member


client = TestClient(app)


def test_app_init_with_test_sqlite():
    """Test app initialization"""
    response = client.get("/")
    assert response.status_code == 404
    assert response.json() == {"detail": "Not Found"}


def test_database_import(get_db):
    """Check database imported"""
    obj = get_db.query(WhatismybrowserUseragentModel).first()

    print(obj)
    assert obj is not None


def test_database_can_connect():
    """Check app able to connect to database"""
    from wimwb.web import settings

    assert "sqlite" in settings.database_uri


def test_app_random_uas_return_results(get_db):
    """Test endpoint to fetch random results return"""

    # lazyloading fixture, need to fetch first
    obj = get_db.query(WhatismybrowserUseragentModel).first()
    assert obj is not None

    response = client.get("/user-agents/?limit=10")
    assert response.status_code == 200
    json_data = response.json()

    assert len(json_data) == 10
