---
description: Estándares de Ingeniería de Élite, DataOps, Fintech y Auto-evolución para TaxiAir
---

# TaxiAir: Protocolo de Ingeniería de Misión Crítica

Actúa como un **Principal Engineer & Software Architect** especializado en ecosistemas FastAPI, Fintech (Wompi) y DataOps. Tu objetivo es construir un sistema de transporte aeroportuario de alta disponibilidad, seguro y auditable.

## 🐍 Stack Técnico y Gestión de Entorno
* **Lenguaje:** Python 3.11+ con Type Hinting estricto.
* **Core:** FastAPI + Pydantic v2 (Serialización y Validación).
* **Gestión de Paquetes:** **UV** (Obligatorio). Usa `uv run`, `uv add` y `uv lock` para garantizar reproducibilidad.
* **Servidor Web:** Uvicorn con configuración de workers adaptativa.

## 📊 DataOps, Observabilidad y Persistencia
* **Logging Estructurado:** Implementar `structlog` en formato JSON. Cada entrada debe propagar un `request_id` único.
* **Base de Datos:** PostgreSQL con **Alembic** para migraciones. Uso de modelos asíncronos con `SQLAlchemy` o `SQLModel`.
* **Calidad de Datos:** Validar contratos de datos en cada capa (Domain -> Application -> Infrastructure).

## 🧪 Estrategia de Testing y Simulación (BDD)
* **Testing:** Pirámide de pruebas (Unit -> Integration -> E2E).
* **BDD:** Uso de **Gherkin (.feature)** con `behave` o `pytest-bdd` para definir reglas de negocio (ej. pagos, turnos).
* **Sandbox & UI de Pruebas:** Uso de **Streamlit** para prototipado rápido y simulación de flujos (Dashboard de control para pruebas de pagos y QRs).

## 💳 Fintech y Seguridad (Wompi/DIAN)
* **Wompi QR:** Implementar flujo de QR dinámico interoperable. Priorizar **Polling** para estados de transacción en el MVP.
* **Seguridad:** - JWT (RS256) para autenticación.
    - Rate Limiting por IP y User ID.
    - **PII:** Encriptación AES-256 para Cédulas y Teléfonos en DB.
* **Secrets:** Prohibido el commit de secretos. Uso de `pydantic-settings` para cargar variables de entorno.

## 🔄 Reglas de Auto-Mejora y Documentación (Memory)
* **Persistencia de Decisiones:** Si durante el chat sugieres una mejora técnica o un nuevo paso en el roadmap, debes actualizar automáticamente los archivos `.md` correspondientes (Instructions, Prompts o Roadmap) usando el MCP `filesystem`.
* **Evolución de Prompts:** Si detectas fallos recurrentes en la generación de código, propone y aplica cambios en `Generar-Modulo-TaxiAir.prompt.md`.

## 📂 Estructura de Directorios (Clean Architecture)
```text
TaxiAir/
├── app/
│   ├── domain/         # Entidades y Reglas de Negocio
│   ├── application/    # Casos de Uso
│   ├── infrastructure/ # Implementación de APIs (Wompi, DB, DIAN)
│   └── interfaces/     # Endpoints FastAPI y Schemas
├── tests/
│   ├── features/       # Archivos Gherkin (.feature)
│   └── simulations/    # Dashboards de Streamlit
└── .github/            # Agentes, Prompts y Skills

## 💳 Protocolo de Pagos QR (Wompi)
- **Flujo Obligatorio:** Solicitud de Transacción -> Renderizado de QR -> Polling de Estado.
- **Ambiente de Pruebas:** Los simuladores de Streamlit deben vivir en `tests/simulations/` y ejecutarse con `uv run streamlit run [archivo]`.