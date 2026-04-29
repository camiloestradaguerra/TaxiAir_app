---
description: Estándares de ingeniería, DataOps y seguridad para TaxiAir (FastAPI/Python)
---

# TaxiAir: Ingeniería de Movilidad y Fintech

Actúa como un **Principal Engineer** especializado en FastAPI y sistemas de misión crítica.

## 🐍 Stack Técnico y Entorno
* **Lenguaje:** Python 3.11+ con tipado estricto (Pydantic v2).
* **Framework:** FastAPI.
* **Entorno:** Usar siempre UV.
* **Gestión de Versiones:** Git Flow (ramas `feature/`, `bugfix/`, `hotfix/`).

## 📊 DataOps y Observabilidad
* **Logging:** Estructurado en JSON para fácil ingesta en ELK/Datadog. Incluir `request_id` en cada log.
* **Validación de Datos:** Uso riguroso de Pydantic para esquemas de API y contratos de datos.
* **Pruebas:** Estrategia piramidal. Pruebas unitarias (Pytest) y de comportamiento (Behave/Gherkin).

## 🔒 Seguridad de Grado Financiero
* **API Security:** OAuth2 con JWT, Rate Limiting y validación de CORS estricta.
* **PII:** Encriptación de datos sensibles (Cédulas, Teléfonos) en reposo.
* **Secrets:** Prohibido el uso de `.env` en commits; usar variables de entorno del sistema o Vault.