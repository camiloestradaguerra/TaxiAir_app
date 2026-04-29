

import sys
import os
import structlog
import asyncio
import json

# Asegura que el workspace esté en el sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, HTTPException, Depends, Request
import uuid


app = FastAPI()

def get_request_id(request: Request):
    rid = request.headers.get("X-Request-ID")
    if not rid:
        rid = str(uuid.uuid4())
    return rid


from TaxiAir.app.domain.payment import Payment
from TaxiAir.app.domain.driver import DriverRegisterRequest, DriverQRResponse
from TaxiAir.app.infrastructure.wompi_client import WompiClient
from TaxiAir.app.infrastructure.logging_config import configure_logging
from TaxiAir.app.infrastructure.payment_store import payment_store
from TaxiAir.app.infrastructure.qr_generator import generate_qr_json, generate_qr_url
from TaxiAir.app.infrastructure.driver_store import driver_store

configure_logging()
logger = structlog.get_logger()

# Configuración de llaves Wompi (usar variables de entorno en producción)
WOMPI_PUBLIC_KEY = os.getenv("WOMPI_PUBLIC_KEY", "tu_public_key")
WOMPI_PRIVATE_KEY = os.getenv("WOMPI_PRIVATE_KEY", "tu_private_key")

def get_wompi_client():
    return WompiClient(WOMPI_PUBLIC_KEY, WOMPI_PRIVATE_KEY)

# Endpoint para crear un nuevo pago

@app.post("/payments", response_model=Payment)
def create_payment(payment: Payment, request: Request):
    payment_store.add_payment(payment)
    request_id = get_request_id(request)
    logger.info("payment_created", payment_id=payment.id, user_id=payment.user_id, amount=payment.amount, request_id=request_id)
    return payment



# Endpoint para registrar conductor y generar QR (con validación de unicidad)

@app.post("/drivers/register", response_model=DriverQRResponse)
def register_driver_qr(request_body: DriverRegisterRequest, request: Request):
    request_id = get_request_id(request)
    if driver_store.get_driver(request_body.placa):
        logger.warning("driver_duplicate", placa=request_body.placa, request_id=request_id)
        raise HTTPException(status_code=409, detail="Ya existe un registro para esta placa")
    driver_store.add_driver(request_body)
    qr_data = generate_qr_json(
        placa=request_body.placa,
        id_conductor=request_body.id_conductor,
        timestamp=request_body.timestamp,
        include_hash=request_body.include_hash
    )
    qr_json = json.dumps(qr_data, separators=(",", ":"))
    qr_url = generate_qr_url(qr_data)
    logger.info("driver_qr_generated", placa=request_body.placa, id_conductor=request_body.id_conductor, timestamp=request_body.timestamp, include_hash=request_body.include_hash, request_id=request_id)
    return DriverQRResponse(qr_json=qr_json, qr_url=qr_url)

# Endpoint para listar conductores
@app.get("/drivers/list")
def list_drivers():
    return [d.dict() for d in driver_store.list_drivers()]

# Endpoint para consultar conductor por placa
@app.get("/drivers/{placa}")
def get_driver(placa: str):
    driver = driver_store.get_driver(placa)
    if not driver:
        raise HTTPException(status_code=404, detail="Conductor no encontrado")
    return driver.dict()

# Endpoint para eliminar conductor

@app.delete("/drivers/{placa}")
def delete_driver(placa: str, request: Request):
    request_id = get_request_id(request)
    driver = driver_store.get_driver(placa)
    if not driver:
        raise HTTPException(status_code=404, detail="Conductor no encontrado")
    driver_store.delete_driver(placa)
    logger.info("driver_deleted", placa=placa, request_id=request_id)
    return {"detail": "Conductor eliminado"}

# Endpoint para actualizar datos de conductor

@app.put("/drivers/{placa}")
def update_driver(placa: str, request_body: DriverRegisterRequest, request: Request):
    request_id = get_request_id(request)
    if placa != request_body.placa:
        raise HTTPException(status_code=400, detail="La placa en la URL y el body deben coincidir")
    if not driver_store.get_driver(placa):
        raise HTTPException(status_code=404, detail="Conductor no encontrado")
    driver_store.update_driver(placa, request_body)
    logger.info("driver_updated", placa=placa, request_id=request_id)
    return {"detail": "Conductor actualizado"}

# Endpoint para consultar un pago por ID

@app.get("/payments/{payment_id}", response_model=Payment)
def get_payment(payment_id: str, request: Request):
    request_id = get_request_id(request)
    payment = payment_store.get_payment(payment_id)
    if not payment:
        logger.warning("payment_not_found", payment_id=payment_id, request_id=request_id)
        raise HTTPException(status_code=404, detail="Pago no encontrado")
    return payment


@app.post("/payments/verify", response_model=Payment)
async def verify_payment(payment: Payment, request: Request, client: WompiClient = Depends(get_wompi_client)):
    request_id = get_request_id(request)
    data = await client.get_transaction_status(payment.wompi_transaction_id)
    if not data or data.get("data", {}).get("status") != "APPROVED":
        logger.warning("payment_not_verified", transaction_id=payment.wompi_transaction_id, status=(data or {}).get("data", {}).get("status"), request_id=request_id)
        raise HTTPException(status_code=400, detail="Pago no aprobado")
    logger.info("payment_verified", transaction_id=payment.wompi_transaction_id, request_id=request_id)
    return payment

@app.get("/health")
def health():
    return {"status": "ok"}
