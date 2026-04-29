---
name: verify-wompi-transaction
description: Consulta el estado técnico de un pago en Wompi (Colombia) usando el ID de transacción. Úsala cuando el usuario reporte problemas con pagos de Nequi, PSE o tarjeta, o para depurar fallos en el flujo de facturación.
---

# Skill: Verificar Transacción Wompi

Esta skill permite al agente conectarse con el API de Wompi para validar el estado de una transacción en tiempo real.

## 🛠️ Parámetros Requeridos
- `transaction_id`: El código alfanumérico único de la transacción (ej. 12345-67890-abc).
- `environment`: 'sandbox' (pruebas) o 'production' (real).

## 📝 Instrucciones para el Agente
1. Al recibir un ID de transacción, realiza una petición GET a: `https://sandbox.wompi.co/v1/transactions/{{transaction_id}}` (o el endpoint de producción).
2. Analiza el campo `data.status`:
   - **APPROVED:** El pago fue exitoso. Informa que se puede proceder con el despacho del taxi o factura.
   - **DECLINED:** El pago fue rechazado. Explica la razón (`data.status_message`).
   - **VOIDED / ERROR:** Indica un fallo técnico o anulación.
3. Si el estado es `APPROVED`, verifica también el `data.payment_method_type` (PSE, NEQUI, CARD) para confirmar que coincide con lo esperado por el usuario.

## 💬 Ejemplo de interacción
- **Usuario:** "¿Por qué no se ha confirmado el pago de este viaje? El ID es 'womp_123'."
- **Agente:** (Ejecuta skill) "He verificado en Wompi y la transacción está en estado 'DECLINED'. El banco reporta fondos insuficientes en la cuenta Nequi vinculada."