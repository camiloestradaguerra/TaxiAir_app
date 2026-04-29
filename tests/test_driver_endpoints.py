import sys
import os
import json
import pytest
from fastapi.testclient import TestClient

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from TaxiAir.main import app

client = TestClient(app)

@pytest.fixture(autouse=True)
def clear_drivers():
    # Limpiar el store antes de cada test
    yield
    client.delete("/drivers/XYZ123")
    client.delete("/drivers/ABC456")
    client.delete("/drivers/DEF789")

# --- Registro y validaciones ---
def test_register_driver_valid():
    payload = {"placa": "XYZ123", "id_conductor": "driver_001"}
    r = client.post("/drivers/register", json=payload)
    assert r.status_code == 200
    data = r.json()
    qr_json = json.loads(data["qr_json"])
    assert qr_json["p"] == "XYZ123"
    assert qr_json["u"] == "driver_001"

def test_register_driver_duplicate():
    payload = {"placa": "XYZ123", "id_conductor": "driver_001"}
    client.post("/drivers/register", json=payload)
    r = client.post("/drivers/register", json=payload)
    assert r.status_code == 409

def test_register_driver_invalid_placa():
    payload = {"placa": "ZZ123", "id_conductor": "driver_001"}
    r = client.post("/drivers/register", json=payload)
    assert r.status_code == 422

def test_register_driver_invalid_timestamp():
    import time
    payload = {"placa": "DEF789", "id_conductor": "driver_003", "timestamp": int(time.time()) + 3600}
    r = client.post("/drivers/register", json=payload)
    assert r.status_code == 422

def test_register_driver_empty_fields():
    payload = {"placa": "", "id_conductor": ""}
    r = client.post("/drivers/register", json=payload)
    assert r.status_code == 422

# --- Listar y consultar ---
def test_list_drivers():
    client.post("/drivers/register", json={"placa": "XYZ123", "id_conductor": "driver_001"})
    client.post("/drivers/register", json={"placa": "ABC456", "id_conductor": "driver_002"})
    r = client.get("/drivers/list")
    assert r.status_code == 200
    data = r.json()
    assert any(d["placa"] == "XYZ123" for d in data)
    assert any(d["placa"] == "ABC456" for d in data)

def test_get_driver_by_placa():
    client.post("/drivers/register", json={"placa": "XYZ123", "id_conductor": "driver_001"})
    r = client.get("/drivers/XYZ123")
    assert r.status_code == 200
    data = r.json()
    assert data["placa"] == "XYZ123"
    assert data["id_conductor"] == "driver_001"

def test_get_driver_not_found():
    r = client.get("/drivers/NOPE00")
    assert r.status_code == 404

# --- Eliminar y actualizar ---
def test_delete_driver():
    client.post("/drivers/register", json={"placa": "XYZ123", "id_conductor": "driver_001"})
    r = client.delete("/drivers/XYZ123")
    assert r.status_code == 200
    r2 = client.get("/drivers/XYZ123")
    assert r2.status_code == 404

def test_update_driver():
    client.post("/drivers/register", json={"placa": "XYZ123", "id_conductor": "driver_001"})
    payload = {"placa": "XYZ123", "id_conductor": "driver_002"}
    r = client.put("/drivers/XYZ123", json=payload)
    assert r.status_code == 200
    r2 = client.get("/drivers/XYZ123")
    assert r2.json()["id_conductor"] == "driver_002"

def test_update_driver_placa_mismatch():
    client.post("/drivers/register", json={"placa": "XYZ123", "id_conductor": "driver_001"})
    payload = {"placa": "ABC456", "id_conductor": "driver_002"}
    r = client.put("/drivers/XYZ123", json=payload)
    assert r.status_code == 400

def test_update_driver_not_found():
    payload = {"placa": "XYZ123", "id_conductor": "driver_002"}
    r = client.put("/drivers/XYZ123", json=payload)
    assert r.status_code == 404
