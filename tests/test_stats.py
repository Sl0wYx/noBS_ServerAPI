from fastapi.testclient import TestClient
from app.main import app
client = TestClient(app)

def test_stats_all():
    response = client.get("/stats/all")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)

def test_specific_stat():
    response = client.get("/stats/32337244-5a74-3143-aa78-ce6736d8f490/Player Name")
    assert response.status_code == 200
    assert isinstance(response.json()["uuid"], str)
    assert isinstance(response.json()["stat_value"], str)

def test_not_existing_stat():
    response = client.get("/stats/32337244-5a74-3143-aa78-ce6736d8f490/not a player")
    assert response.status_code == 404
    assert response.json() == {"detail": "Stats not found"}

def test_stats_existing_uuid():
    response = client.get("/stats/32337244-5a74-3143-aa78-ce6736d8f490")
    assert response.status_code == 200
    assert isinstance(response.json()["uuid"], str)
    assert isinstance(response.json()["Player Name"], str)

def test_stats_uuid_not_found():
    response = client.get("/stats/32337244-5a74-3143-aa78-ce6736d8f290")
    assert response.status_code == 404
    assert response.json() == {"detail": "Account with that uuid not found"}

def test_statsbyname_success():
    response = client.get("/stats_name/Evergetis")
    assert response.status_code == 200
    assert isinstance(response.json()["uuid"], str)

def test_statsbyname_not_found():
    response = client.get("/stats_name/Evergeti")
    assert response.status_code == 404
    assert response.json() == {"detail": "Stats with that player name not found"}