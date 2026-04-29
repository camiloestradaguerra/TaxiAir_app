import re
from pydantic import validator
from TaxiAir.app.domain.driver import DriverRegisterRequest

PLACA_REGEX = r"^[A-Z]{3}\d{3}$"

@validator('placa')
def validate_placa(cls, v):
    if not re.match(PLACA_REGEX, v):
        raise ValueError('Formato de placa inválido (ej: ABC123)')
    return v

@validator('timestamp')
def validate_timestamp(cls, v):
    import time
    if v > int(time.time() + 60):
        raise ValueError('El timestamp no puede ser futuro')
    return v

@validator('id_conductor')
def validate_id_conductor(cls, v):
    if not (3 <= len(v) <= 32):
        raise ValueError('id_conductor debe tener entre 3 y 32 caracteres')
    return v
