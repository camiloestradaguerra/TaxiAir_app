import sys
import os
import json
import pytest
from fastapi.testclient import TestClient

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from TaxiAir.main import app

client = TestClient(app)

def test_register_driver_qr_basic():
    payload = {
        "placa": "XYZ123",
        "id_conductor": "driver_001"
    }
    response = client.post("/drivers/register", json=payload)
    assert response.status_code == 200
    data = response.json()
    qr_json = json.loads(data["qr_json"])
    assert qr_json["p"] == "XYZ123"
    assert qr_json["u"] == "driver_001"
    assert isinstance(qr_json["t"], int)
    assert qr_json["v"] == 1
    assert "hash" not in qr_json
    assert data["qr_url"].startswith("https://api.qrserver.com/v1/create-qr-code")

def test_register_driver_qr_with_hash():
    payload = {
        "placa": "ABC456",
        "id_conductor": "driver_002",
        "include_hash": True
    }
    response = client.post("/drivers/register", json=payload)
    assert response.status_code == 200
    data = response.json()
    qr_json = json.loads(data["qr_json"])
    assert qr_json["p"] == "ABC456"
    assert qr_json["u"] == "driver_002"
    assert isinstance(qr_json["t"], int)
    assert qr_json["v"] == 1
    assert "hash" in qr_json
    assert len(qr_json["hash"]) == 64
    assert data["qr_url"].startswith("https://api.qrserver.com/v1/create-qr-code")
