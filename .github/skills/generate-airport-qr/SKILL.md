---
name: generate-airport-qr
description: Genera la lógica o el recurso visual de un código QR para el registro de taxis en el acopio. Úsala al diseñar el flujo de check-in del conductor o para crear datos de prueba (Mock data).
---

# Skill: Generador de QR para Acopio Aeropuerto

Esta skill permite crear el token de datos que vincula a un taxista con un servicio de transporte en el punto de despacho.

## 🛠️ Parámetros Requeridos
- `placa`: La placa del vehículo (ej. XYZ123).
- `id_conductor`: Identificador único del conductor en la base de datos.
- `timestamp`: Fecha y hora de llegada al acopio (opcional para seguridad).

## 📝 Instrucciones para el Agente
1. **Estructura del Contenido:** El QR debe contener un objeto JSON codificado o una URL firmada con el siguiente formato:
   `{"v": 1, "p": "{{placa}}", "u": "{{id_conductor}}", "t": "{{timestamp}}"}`
2. **Generación de Código:**
   - Si el usuario solicita código, usa la librería `qrcode` para Node.js o `qr_flutter` para el frontend.
   - Si el usuario solicita una prueba visual, genera una URL de imagen usando una API pública (ej. `https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=...`).
3. **Seguridad:** Sugiere siempre al usuario que el contenido del QR debe estar firmado con un JWT o un Hash de seguridad para evitar que conductores dupliquen registros manualmente.

## 💬 Ejemplo de interacción
- **Usuario:** "Necesito un QR de prueba para la placa ABC456."
- **Agente:** (Ejecuta skill) "He generado la lógica para el QR de la placa ABC456. Aquí tienes el enlace visual de prueba y el código en Flutter para renderizarlo en la app del conductor."