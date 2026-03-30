from fastapi.testclient import TestClient
from app.main import app
client = TestClient(app)

def test_get_online_success():
    response = client.get("/online")
    assert response.status_code == 200
    assert isinstance(response.json(), list)