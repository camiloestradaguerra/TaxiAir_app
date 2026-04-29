
import sys
import os
import pytest
from fastapi.testclient import TestClient

# Asegura que la raíz del proyecto esté en el sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from TaxiAir.main import app
from TaxiAir.app.domain.payment import Payment

client = TestClient(app)


def test_verify_payment_rejected():
    # Mock WompiClient para simular respuesta de pago no aprobado
    class MockWompiClient:
        async def get_transaction_status(self, transaction_id):
            return {"data": {"status": "REJECTED"}}

    from TaxiAir.main import app, get_wompi_client
    app.dependency_overrides[get_wompi_client] = lambda: MockWompiClient()

    payload = {
        "id": "pay_123456",
        "user_id": "user_001",
        "amount": 15000.0,
        "currency": "COP",
        "status": "pending",
        "wompi_transaction_id": "trans_abcdef123456",
        "created_at": "2024-04-29T12:00:00Z",
        "updated_at": None
    }
    response = client.post("/payments/verify", json=payload)
    assert response.status_code == 400
    assert response.json()["detail"] == "Pago no aprobado"


def test_verify_payment_approved():
    # Mock WompiClient para simular respuesta de pago aprobado
    class MockWompiClient:
        async def get_transaction_status(self, transaction_id):
            return {"data": {"status": "APPROVED"}}

    from TaxiAir.main import app, get_wompi_client
    app.dependency_overrides[get_wompi_client] = lambda: MockWompiClient()

    payload = {
        "id": "pay_123456",
        "user_id": "user_001",
        "amount": 15000.0,
        "currency": "COP",
        "status": "pending",
        "wompi_transaction_id": "trans_abcdef123456",
        "created_at": "2024-04-29T12:00:00Z",
        "updated_at": None
    }
    response = client.post("/payments/verify", json=payload)
    assert response.status_code == 200
    assert response.json()["id"] == payload["id"]
