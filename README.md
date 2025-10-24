# Zaldo — MVP Finanzas Personales

Zaldo es un MVP de plataforma de finanzas personales inspirada en flujos mensuales y reglas automáticas. Incluye un backend FastAPI, frontend Next.js, pipelines de importación de CSV/XLSX, autenticación passwordless y panel admin básico.

## Estructura

```
/frontend      # Next.js + Tailwind + React Query
/backend       # FastAPI + SQLAlchemy + Alembic
/db            # Migraciones
/samples       # Archivos de ejemplo para importaciones
/scripts       # Scripts de seed
```

## Requisitos

- Python 3.11+
- Node.js 20+
- Docker y docker-compose (opcional)

## Configuración rápida

1. Copia `.env.example` a `.env` y ajusta secretos.
2. Instala dependencias del backend:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```
3. Instala dependencias del frontend:
   ```bash
   cd frontend
   npm install
   ```
4. Ejecuta migraciones y seed:
   ```bash
   make migrate
   make seed
   ```
5. Corre ambos servicios en modo desarrollo:
   ```bash
   make backend  # http://localhost:8000/docs
   make frontend # http://localhost:3000
   ```

También puedes levantar todo con Docker:
```bash
docker compose up --build
```

## Scripts útiles

- `make test`: ejecuta pruebas críticas (parser, seguridad, agregaciones).
- `make seed`: inserta UF 2025, categorías base e invitaciones demo.

## Features principales

- **Auth passwordless** con magic links vía Resend (fallback consola).
- **Waitlist e invitaciones** para controlar acceso.
- **Onboarding guiado** (crear cuenta, importar, crear reglas).
- **Importador CSV/XLSX** con vista previa, mapeo flexible y deduplicación por hash SHA256.
- **Dashboard** con KPIs clave, gráficos esenciales y toggle CLP/UF.
- **Feedback in-app** + telemetría PostHog (consentimiento explícito).
- **Admin mínimo** para gestionar usuarios, invitaciones y métricas.

## Tests

```
make test
```

Cubre parsing de fechas/montos, hash de deduplicación y utilidades core.

## Extensiones futuras

- Conexiones directas a bancos chilenos.
- Recomendaciones automáticas de categoría con ML ligero.
- Presupuestos, alertas y objetivos.
- Exportaciones en PDF/CSV y API pública.

## Licencia

MIT
