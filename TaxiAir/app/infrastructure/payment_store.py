from typing import Dict, Optional
from TaxiAir.app.domain.payment import Payment

class PaymentStore:
    def __init__(self):
        self._payments: Dict[str, Payment] = {}

    def add_payment(self, payment: Payment):
        self._payments[payment.id] = payment

    def get_payment(self, payment_id: str) -> Optional[Payment]:
        return self._payments.get(payment_id)

    def list_payments(self):
        return list(self._payments.values())

# Instancia global para demo (en producción usar DB)
payment_store = PaymentStore()
