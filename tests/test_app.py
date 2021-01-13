from fastapi.testclient import TestClient
from wimwb.web import app


client = TestClient(app)


def test_app_init_with_test_sqlite():
    """Test app initialization"""
    response = client.get("/")
    assert response.status_code == 404
    assert response.json() == {"detail": "Not Found"}
