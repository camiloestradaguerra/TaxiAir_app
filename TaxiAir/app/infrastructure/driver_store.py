from typing import Dict, Optional
from TaxiAir.app.domain.driver import DriverRegisterRequest

class DriverStore:
    def __init__(self):
        self._drivers: Dict[str, DriverRegisterRequest] = {}

    def add_driver(self, driver: DriverRegisterRequest):
        if driver.placa in self._drivers:
            raise ValueError("Registro duplicado para esta placa")
        self._drivers[driver.placa] = driver

    def get_driver(self, placa: str) -> Optional[DriverRegisterRequest]:
        return self._drivers.get(placa)

    def list_drivers(self):
        return list(self._drivers.values())

    def delete_driver(self, placa: str):
        if placa in self._drivers:
            del self._drivers[placa]

    def update_driver(self, placa: str, driver: DriverRegisterRequest):
        if placa not in self._drivers:
            raise ValueError("No existe registro para actualizar")
        self._drivers[placa] = driver

driver_store = DriverStore()
