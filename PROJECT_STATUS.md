# Project Status

Version: 0.1.0

## Purpose

This document tracks the current state of the project. It is updated by the AI agent after completing significant tasks.

---

# Overview

| Field | Value |
|-------|-------|
| Project Name | Project Stacks |
| Last Updated | 2026-09-11 |
| Current Phase | Development |
| Overall Progress | 40% |

---

# Features

## Completed

- [x] API REST con CRUD de proyectos (crear, listar, renombrar, eliminar) — Completed 2026-09-11
- [x] API REST con CRUD de tecnologías por proyecto (agregar, editar, eliminar) — Completed 2026-09-11
- [x] Frontend SPA (HTML/JS vanilla) que consume la API — Completed 2026-09-11
- [x] Ejecución local con docker-compose (PostgreSQL + API + frontend en nginx) — Completed 2026-09-11
- [x] Migraciones de base de datos con Alembic — Completed 2026-09-11
- [x] Suite de tests de la API (19 tests, cobertura 99%) — Completed 2026-09-11

## In Progress

- [ ] Nada en curso actualmente.

## Planned

- [ ] CI/CD con GitHub Actions (tests automáticos) — Priority: High
- [ ] Deploy automático en homologación y producción — Priority: High
- [ ] Despliegue en Vercel (frontend), Render (API) y Supabase (PostgreSQL) — Priority: High
- [ ] Proyecto local en la branch `desarrollo` con su base de datos local — In place
- [ ] Credenciales de servicios en variables de entorno (Supabase, Render, Vercel) — Priority: High

---

# Technical Debt

| Item | Severity | Description | Target Resolution |
|------|----------|-------------|-------------------|
| TD-001 | Low | Los tests de la API usan SQLite in-memory como fake de DB; el esquema real (PostgreSQL) se valida manualmente | Con CI + Postgres en el pipeline |
| TD-002 | Low | El frontend no tiene suite de tests automatizados (vanilla sin framework) | Evaluar tests e2e livianos |

---

# Decisions Log

| ADR | Title | Status | Date |
|-----|-------|--------|------|
| ADR-001 | Arquitectura de 2 servicios: `frontend` (SPA estática) + `api` (FastAPI REST) | Accepted | 2026-09-11 |
| ADR-002 | SQLAlchemy (sync) + Alembic para el acceso y las migraciones a PostgreSQL | Accepted | 2026-09-11 |
| ADR-003 | Ejecución local con docker-compose: `db` + `api` + `frontend` | Accepted | 2026-09-11 |
| ADR-004 | Estrategia de branches: `desarrollo` → `homologacion` → `production` | Accepted | 2026-09-11 |

---

# Blockers & Risks

| ID | Description | Impact | Mitigation | Owner |
|----|-------------|--------|------------|-------|
| R-001 | Credenciales de Supabase, Render y Vercel aún no creadas | High | El autor crea las cuentas y completa el `.env` | Autor |
| R-002 | La branch `production` debe quedar protegida en GitHub y los PR aprobados | Medium | Configurar reglas de protección en GitHub | Autor |

---

# Metrics

| Metric | Current | Target | Trend |
|--------|---------|--------|-------|
| Test Coverage | 99% | >80% | ↑ |
| Test Suite | 19 tests | — | → |
| Servicios en local | 3 (db, api, frontend) | 3 | → |

---

# Notes

- El proyecto sigue el flujo: primero funcional en local sobre `desarrollo`; el despliegue en la nube (Vercel + Render + Supabase) se realiza en una etapa posterior.
- Las llaves de servicios se manejan por variables de entorno (`.env`), nunca se commitean (SECURITY_RULES).
- Update this file after each significant task completion (see DEFINITION_OF_DONE.md DONE-040).