import sys
import os
import pytest
from fastapi.testclient import TestClient

# Asegura que la raíz del proyecto esté en el sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from TaxiAir.main import app
from TaxiAir.app.domain.payment import Payment

client = TestClient(app)

def test_create_and_get_payment():
    payload = {
        "id": "pay_999",
        "user_id": "user_999",
        "amount": 5000.0,
        "currency": "COP",
        "status": "pending",
        "wompi_transaction_id": "trans_xyz",
        "created_at": "2024-04-29T12:00:00Z",
        "updated_at": None
    }
    # Crear pago
    response = client.post("/payments", json=payload)
    assert response.status_code == 200
    assert response.json()["id"] == payload["id"]

    # Consultar pago
    response = client.get(f"/payments/{payload['id']}")
    assert response.status_code == 200
    assert response.json()["user_id"] == payload["user_id"]

def test_get_payment_not_found():
    response = client.get("/payments/no_existe")
    assert response.status_code == 404
    assert response.json()["detail"] == "Pago no encontrado"
