
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum

class CurrencyEnum(str, Enum):
    COP = "COP"
    USD = "USD"
    EUR = "EUR"

class StatusEnum(str, Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"

class Payment(BaseModel):
    id: str = Field(..., description="ID único del pago")
    user_id: str = Field(..., description="ID del usuario que realiza el pago")
    amount: float = Field(..., gt=0, description="Monto del pago (debe ser mayor a cero)")
    currency: CurrencyEnum = Field(..., description="Moneda del pago")
    status: StatusEnum = Field(..., description="Estado del pago (pending, approved, rejected, etc.)")
    wompi_transaction_id: Optional[str] = Field(None, description="ID de la transacción en Wompi")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Fecha de creación")
    updated_at: Optional[datetime] = Field(None, description="Fecha de última actualización")
