---
name: check-dian-status-validator
description: Valida la estructura del JSON de facturación electrónica según los estándares de la DIAN (Anexo 1.8/1.9). Úsala antes de realizar envíos masivos o para depurar errores de validación de proveedores como Siigo o FacturaDirecta.
---

# Skill: Validador de Factura Electrónica (DIAN)

Esta skill actúa como un linter especializado para asegurar que los datos del viaje y del pasajero cumplen con los requisitos legales colombianos para la generación de facturas electrónicas.

## 🛠️ Parámetros Requeridos
- `json_payload`: El objeto JSON que se pretende enviar al proveedor tecnológico.
- `document_type`: Tipo de documento (01 para Factura, 03 para Boleta de transporte).

## 📝 Instrucciones para el Agente
1. **Verificación de Campos Obligatorios:** Comprueba que el JSON incluya:
   - `Customer`: NIT o Cédula (con dígito de verificación si aplica).
   - `TaxTotal`: Cálculo correcto del IVA (o exención si aplica a transporte).
   - `PaymentMeans`: Método de pago (efectivo, tarjeta, transferencia).
2. **Validación de Unidades:** Verificar que el concepto de "Transporte de pasajeros" use el código de unidad estándar (ej. `94` para servicios).
3. **Sandbox Check:** Si el usuario lo solicita, simula una respuesta de éxito/error basada en las respuestas típicas del API de la DIAN, identificando posibles `RejectCodes`.

## 💬 Ejemplo de interacción
- **Usuario:** "Revisa si este JSON para Siigo está bien construido para un viaje al aeropuerto."
- **Agente:** (Ejecuta skill) "He validado el JSON. Falta el campo `IdentificationType` en el objeto `Customer`. Sin este código, la DIAN rechazará la factura por no identificar si el pasajero usó Cédula o NIT."