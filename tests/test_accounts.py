from fastapi.testclient import TestClient
from app.main import app
import os
from dotenv import load_dotenv
from pathlib import Path
client = TestClient(app)

load_dotenv(Path("app/data/private/.env"))
API_TOKEN = os.getenv("API_TOKEN")

def test_get_nonexisting_ID():
    response = client.get("/accounts/2")
    assert response.status_code == 404
    assert response.json() == {"detail": "Account with that ID does not exist"}

def test_get_account_success():
    response = client.get("/accounts/934533956244742194")
    assert response.status_code == 200
    assert isinstance(response.json()["DiscordID"], int)
    assert isinstance(response.json()["PlayerUUID"], str)

def test_get_online_success():
    response = client.get("/online")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

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

def test_existing_uuid():
    response = client.get("/stats/32337244-5a74-3143-aa78-ce6736d8f490")
    assert response.status_code == 200
    assert isinstance(response.json()["uuid"], str)
    assert isinstance(response.json()["Player Name"], str)

def test_uuid_not_found():
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
    
def test_get_image():
    response = client.get("/get_image/2026-03-26_18-06-09")
    assert response.status_code == 200
    assert response.headers["content-type"] == "image/png"

def test_get_image_not_found():
    response = client.get("/get_image/2026-03-26_18-06-0")
    assert response.status_code == 404
    assert response.json() == {"detail": "Image not found"}

def test_receive_message_right_token():
    response = client.post(
        "/receive_message",
        headers={"authorization": f"{API_TOKEN}"},
        json={"message": "Hi this is a test message!", "date": f"21-12-32"}
    )
    assert response.status_code == 200

def test_receive_message_false_token():
    response = client.post(
            "/receive_message",
            headers={"authorization": f"false_token1000"},
            json={"message": "Hi this is a bad message!", "date": f"21-12-32"}
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid API Token"}


def test_receive_message_with_image():
    response = client.post(
        "/receive_message",
        headers={"authorization": f"{API_TOKEN}"},
        json={"message": "Hi this is a test message!", "date": f"21-12-32", "image": True}
    )
    assert response.status_code == 200

def test_receive_message_with_image_wrong_token():
    response = client.post(
        "/receive_message",
        headers={"authorization": f"really_cool_token2"},
        json={"message": "Hi this is a test message!", "date": f"21-12-32", "image": True}
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid API Token"}

