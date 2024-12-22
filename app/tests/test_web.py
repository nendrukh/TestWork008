import random
import time

from fastapi.testclient import TestClient

from config import API_KEY
from web_app import web_app
from models import TransactionStatisticsSchema

client = TestClient(web_app)


def test_post_transactions():
    random_id = random.randint(153570, 99999999)

    response = client.post(
        "/transactions",
        json={
            "transaction_id": str(random_id),
            "user_id": "user_1",
            "amount": 100.01,
            "currency": "USD",
            "timestamp": "2024-12-21T16:00:00"
        },
        headers={"Authorization": f"ApiKey {API_KEY}"}
    )

    assert response.status_code == 201
    assert response.json()["message"] == "Transaction received"


def test_get_statistics():
    time.sleep(0.3)

    response = client.get("/statistics", headers={"Authorization": f"ApiKey {API_KEY}"})

    assert response.status_code == 200
    assert TransactionStatisticsSchema.model_validate(response.json())


def test_delete_transactions():
    response = client.delete("/transactions", headers={"Authorization": f"ApiKey {API_KEY}"})

    assert response.status_code == 200


def test_invalid_api_key():
    response = client.get("/statistics", headers={"Authorization": f"ApiKey api"})

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid API Key"


def test_no_auth_in_headers():
    response = client.get("/statistics")

    assert response.status_code == 422
    assert response.json()["detail"][0]["type"] == "missing"
    assert "header" and "Authorization" in response.json()["detail"][0]["loc"]
