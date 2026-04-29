import sys
import os
import pytest
from fastapi.testclient import TestClient

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from TaxiAir.main import app

client = TestClient(app)

def test_create_payment_invalid_currency_enum():
    payload = {
        "id": "pay_enum_cur",
        "user_id": "user_enum",
        "amount": 1000.0,
        "currency": "ARS",  # No permitido
        "status": "pending",
        "wompi_transaction_id": "trans_enum_cur",
        "created_at": "2024-04-29T12:00:00Z",
        "updated_at": None
    }
    response = client.post("/payments", json=payload)
    assert response.status_code == 422

def test_create_payment_invalid_status_enum():
    payload = {
        "id": "pay_enum_status",
        "user_id": "user_enum2",
        "amount": 1000.0,
        "currency": "COP",
        "status": "processing",  # No permitido
        "wompi_transaction_id": "trans_enum_status",
        "created_at": "2024-04-29T12:00:00Z",
        "updated_at": None
    }
    response = client.post("/payments", json=payload)
    assert response.status_code == 422
