import httpx
import structlog
from typing import Optional

logger = structlog.get_logger()

class WompiClient:
    def __init__(self, public_key: str, private_key: str, base_url: str = "https://production.wompi.co/v1"):
        self.public_key = public_key
        self.private_key = private_key
        self.base_url = base_url
        self.client = httpx.AsyncClient()

    async def get_transaction_status(self, transaction_id: str) -> Optional[dict]:
        url = f"{self.base_url}/transactions/{transaction_id}"
        headers = {"Authorization": f"Bearer {self.public_key}"}
        try:
            response = await self.client.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()
            logger.info("wompi_transaction_status", transaction_id=transaction_id, status=data.get("data", {}).get("status"))
            return data
        except httpx.HTTPError as e:
            logger.error("wompi_transaction_error", transaction_id=transaction_id, error=str(e))
            return None
