from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class Payment(BaseModel):
    id: str = Field(..., description="ID único del pago")
    user_id: str = Field(..., description="ID del usuario que realiza el pago")
    amount: float = Field(..., description="Monto del pago")
    currency: str = Field(..., description="Moneda del pago")
    status: str = Field(..., description="Estado del pago (pending, approved, rejected, etc.)")
    wompi_transaction_id: Optional[str] = Field(None, description="ID de la transacción en Wompi")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Fecha de creación")
    updated_at: Optional[datetime] = Field(None, description="Fecha de última actualización")
