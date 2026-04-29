
from pydantic import BaseModel, Field, validator
from typing import Optional
import time
import re

PLACA_REGEX = r"^[A-Z]{3}\d{3}$"

class DriverRegisterRequest(BaseModel):
    placa: str = Field(..., example="XYZ123")
    id_conductor: str = Field(..., min_length=3, max_length=32, example="driver_001")
    timestamp: Optional[int] = Field(default_factory=lambda: int(time.time()))
    include_hash: bool = False

    @validator('placa')
    def validate_placa(cls, v):
        if not re.match(PLACA_REGEX, v):
            raise ValueError('Formato de placa inválido (ej: ABC123)')
        return v

    @validator('timestamp')
    def validate_timestamp(cls, v):
        if v > int(time.time() + 60):
            raise ValueError('El timestamp no puede ser futuro')
        return v

    @validator('id_conductor')
    def validate_id_conductor(cls, v):
        if not (3 <= len(v) <= 32):
            raise ValueError('id_conductor debe tener entre 3 y 32 caracteres')
        return v

class DriverQRResponse(BaseModel):
    qr_json: str
    qr_url: str
