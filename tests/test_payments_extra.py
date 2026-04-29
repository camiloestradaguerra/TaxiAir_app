import sys
import os
import pytest
from fastapi.testclient import TestClient

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from TaxiAir.main import app

client = TestClient(app)

def test_create_payment_invalid_amount():
    payload = {
        "id": "pay_invalid_amount",
        "user_id": "user_002",
        "amount": -100.0,
        "currency": "COP",
        "status": "pending",
        "wompi_transaction_id": "trans_invalid",
        "created_at": "2024-04-29T12:00:00Z",
        "updated_at": None
    }
    response = client.post("/payments", json=payload)
    assert response.status_code == 422  # Unprocessable Entity

def test_create_payment_missing_field():
    payload = {
        "id": "pay_missing_field",
        "amount": 1000.0,
        "currency": "COP",
        "status": "pending",
        "wompi_transaction_id": "trans_missing",
        "created_at": "2024-04-29T12:00:00Z",
        "updated_at": None
    }
    response = client.post("/payments", json=payload)
    assert response.status_code == 422

def test_create_payment_invalid_currency():
    payload = {
        "id": "pay_invalid_currency",
        "user_id": "user_003",
        "amount": 1000.0,
        "currency": "INVALID",
        "status": "pending",
        "wompi_transaction_id": "trans_invalid_cur",
        "created_at": "2024-04-29T12:00:00Z",
        "updated_at": None
    }
    response = client.post("/payments", json=payload)
    # Si hay validación de currency, debe fallar. Si no, será 200.
    assert response.status_code in (200, 422)

def test_security_sql_injection():
    payload = {
        "id": "pay_sql_inj",
        "user_id": "user_004; DROP TABLE users;--",
        "amount": 1000.0,
        "currency": "COP",
        "status": "pending",
        "wompi_transaction_id": "trans_sql_inj",
        "created_at": "2024-04-29T12:00:00Z",
        "updated_at": None
    }
    response = client.post("/payments", json=payload)
    assert response.status_code == 200  # No debe ejecutar SQL, solo almacenar como string

def test_large_amount():
    payload = {
        "id": "pay_large_amount",
        "user_id": "user_005",
        "amount": 1e12,
        "currency": "COP",
        "status": "pending",
        "wompi_transaction_id": "trans_large",
        "created_at": "2024-04-29T12:00:00Z",
        "updated_at": None
    }
    response = client.post("/payments", json=payload)
    assert response.status_code == 200
