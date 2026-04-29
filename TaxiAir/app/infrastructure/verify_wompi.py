from .wompi_client import WompiClient
import structlog
import asyncio

logger = structlog.get_logger()

async def verify_wompi_transaction(transaction_id: str, public_key: str, private_key: str) -> bool:
    client = WompiClient(public_key, private_key)
    data = await client.get_transaction_status(transaction_id)
    if data and data.get("data", {}).get("status") == "APPROVED":
        logger.info("payment_verified", transaction_id=transaction_id)
        return True
    logger.warning("payment_not_verified", transaction_id=transaction_id, status=data.get("data", {}).get("status"))
    return False

# Ejemplo de uso (debe ejecutarse en un entorno async):
# asyncio.run(verify_wompi_transaction("transaction_id", "public_key", "private_key"))
