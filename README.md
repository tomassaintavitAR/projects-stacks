# Project Stacks

Sistema simple para gestionar **proyectos** y los **stacks tecnológicos** asociados a cada uno (ABM/CRUD), construido para probar el despliegue completo de una aplicación en la web usando distintas plataformas.

- Backend: **Python 3.12 + FastAPI**
- Base de datos: **PostgreSQL** (local vía docker-compose; Supabase en producción)
- Frontend: **HTML/JS vanilla** (SPA estática servida por Vercel)
- Infra: **Docker + docker-compose** en local
- Despliegue: **Vercel** (frontend), **Render** (API), **Supabase** (PostgreSQL)

## Estructura

```
api/          Servicio backend (FastAPI + SQLAlchemy + Alembic)
frontend/     SPA estática (HTML/JS vanilla) que consume la API REST
```

## Flujo de arquitectura

```
Browser (frontend en Vercel)
        │  HTTP/JSON
        ▼
API REST (FastAPI en Render)
        │  SQL
        ▼
PostgreSQL (Supabase / local via docker-compose)
```

## Ejecutar la API en local

1. Levantar PostgreSQL (docker):

   ```bash
   docker compose up -d db
   ```

2. Instalar dependencias:

   ```bash
   cd api
   pip install -r requirements-dev.txt
   ```

3. Configurar variables de entorno (copiar de `.env.example`):

   ```bash
   cp .env.example .env
   ```

4. Aplicar migraciones y levantar el servidor:

   ```bash
   alembic upgrade head
   uvicorn app.main:app --reload
   ```

La API queda disponible en `http://localhost:8000` y su documentación interactiva en `http://localhost:8000/docs`.

## Endpoints de la API

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/health` | Estado del servicio |
| GET | `/projects` | Listar proyectos |
| POST | `/projects` | Crear proyecto |
| GET | `/projects/{id}` | Detalle de un proyecto con sus tecnologías |
| PATCH | `/projects/{id}` | Renombrar proyecto |
| DELETE | `/projects/{id}` | Eliminar proyecto |
| POST | `/projects/{id}/technologies` | Agregar tecnología a un proyecto |
| PATCH | `/projects/{id}/technologies/{tech_id}` | Editar tecnología |
| DELETE | `/projects/{id}/technologies/{tech_id}` | Eliminar tecnología |

## Tests

```bash
cd api
pytest
```

## Branches

Los cambios fluyen en cascada con Pull Requests:

```
desarrollo ──► homologacion ──► production
```

- `desarrollo`: branch de trabajo principal, con su base de datos local.
- `homologacion`: staging, espejo de `production`, con su propia base de datos.
- `production`: producción (protegida). El merge requiere PR aprobado.

## Más información

- Especificación del proyecto: `PROJECT_SPEC.md`
- Estado del proyecto: `PROJECT_STATUS.md`