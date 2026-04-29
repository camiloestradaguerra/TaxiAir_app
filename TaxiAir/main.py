
import sys
import os
import structlog
import asyncio

# Asegura que el workspace esté en el sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, HTTPException, Depends

app = FastAPI()

from TaxiAir.app.domain.payment import Payment
from TaxiAir.app.infrastructure.wompi_client import WompiClient
from TaxiAir.app.infrastructure.logging_config import configure_logging
from TaxiAir.app.infrastructure.payment_store import payment_store

configure_logging()
logger = structlog.get_logger()

# Configuración de llaves Wompi (usar variables de entorno en producción)
WOMPI_PUBLIC_KEY = os.getenv("WOMPI_PUBLIC_KEY", "tu_public_key")
WOMPI_PRIVATE_KEY = os.getenv("WOMPI_PRIVATE_KEY", "tu_private_key")

def get_wompi_client():
    return WompiClient(WOMPI_PUBLIC_KEY, WOMPI_PRIVATE_KEY)

# Endpoint para crear un nuevo pago
@app.post("/payments", response_model=Payment)
def create_payment(payment: Payment):
    payment_store.add_payment(payment)
    logger.info("payment_created", payment_id=payment.id, user_id=payment.user_id, amount=payment.amount)
    return payment

# Endpoint para consultar un pago por ID
@app.get("/payments/{payment_id}", response_model=Payment)
def get_payment(payment_id: str):
    payment = payment_store.get_payment(payment_id)
    if not payment:
        logger.warning("payment_not_found", payment_id=payment_id)
        raise HTTPException(status_code=404, detail="Pago no encontrado")
    return payment

@app.post("/payments/verify", response_model=Payment)
async def verify_payment(payment: Payment, client: WompiClient = Depends(get_wompi_client)):
    data = await client.get_transaction_status(payment.wompi_transaction_id)
    if not data or data.get("data", {}).get("status") != "APPROVED":
        logger.warning("payment_not_verified", transaction_id=payment.wompi_transaction_id, status=(data or {}).get("data", {}).get("status"))
        raise HTTPException(status_code=400, detail="Pago no aprobado")
    logger.info("payment_verified", transaction_id=payment.wompi_transaction_id)
    return payment

@app.get("/health")
def health():
    return {"status": "ok"}
