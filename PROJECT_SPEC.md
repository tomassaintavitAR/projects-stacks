# Project Specification

Version: 0.1.0

## Purpose

This document defines the context, objectives, constraints, and technical decisions of this project.

AI agents MUST read this document before planning or implementing changes.

---

# Project Overview

## Project Name

Project Stacks

---

## Problem Statement

Probar el flujo completo de construir un sistema simple y desplegarlo en la web usando diferentes servicios y plataformas (Vercel, Render, Supabase).

El sistema gestiona proyectos y los stacks tecnológicos asociados a cada uno, mediante un ABM/CRUD sencillo.

---

## Objectives

1. Crear un proyecto.
2. Visualizar proyectos en una lista o tabla.
3. Seleccionar un proyecto.
4. Agregar tecnologías (stacks) dentro de un proyecto.
5. Volver a la sección de todos los proyectos.
6. CRUD completo: crear/renombrar/eliminar proyectos; agregar/editar/eliminar tecnologías.

---

## Non-Objectives

Este proyecto NO incluye:

- Autenticación ni gestión de usuarios.
- Roles, permisos ni multi-tenancy.
- Manejo de datos sensibles.
- Optimizaciones de desempeño o escalabilidad.
- Cualquier complejidad adicional más allá de un CRUD simple.

---

# Users and Stakeholders

## Target Users

El autor y cualquier usuario que tenga la URL del sitio. Uso exclusivamente para pruebas.

---

## Stakeholders

Ninguno. Proyecto de prueba personal sin impacto en otros equipos o sistemas.

---

# Technical Context

## Technology Stack

Backend:
- Python 3.12
- FastAPI

Frontend:
- HTML/JS vanilla (SPA estática, servida por Vercel)

Database:
- PostgreSQL (local via docker-compose; Supabase en producción)

Infrastructure:
- Docker + docker-compose (ejecución local)
- Despliegue: Vercel (frontend), Render (API), Supabase (PostgreSQL)

---

## Architecture Overview

Arquitectura de microservicios con dos servicios:

- `frontend`: SPA estática (HTML/JS vanilla) que consume la API REST.
- `api`: FastAPI que expone la API REST y gestiona el acceso a PostgreSQL.

Flujo de datos:

```
Browser (frontend en Vercel)
        │  HTTP/JSON
        ▼
API REST (FastAPI en Render)
        │  SQL
        ▼
PostgreSQL (Supabase)
```

Las credenciales y llaves de Supabase, Render y Vercel serán provistas por el autor en variables de entorno (`.env`) una vez creadas las cuentas.

---

# Development Constraints

## Mandatory Technologies

- Python 3.12 + FastAPI
- PostgreSQL
- Docker + docker-compose
- Frontend estático simple (HTML/JS vanilla)
- Todos los servicios en planes gratuitos

---

## Forbidden Technologies

No hay tecnologías explícitamente prohibidas, pero no se agregarán dependencias o complejidad innecesaria (principio de simplicidad).

---

## Performance Requirements

Ninguna. El aprendizaje y la simplicidad son prioritarios.

---

## Security Requirements

- Sin autenticación: el CRUD es público para cualquier usuario con la URL.
- No se procesan datos sensibles.
- Las claves/llaves de servicios externos se gestionan mediante variables de entorno.

---

# Branching Strategy and Delivery

## Branches

Se trabaja con 3 branches long-lived:

- `desarrollo`: branch de trabajo principal. El código se edita aquí y debe funcionar en local con docker-compose y su propia base de datos local (PostgreSQL).
- `homologacion`: espejo de `production`. Entorno de staging con su propia base de datos.
- `production`: branch base/protegida que representa el entorno de producción con su propia base de datos.

## Flow

Los cambios fluyen en cascada, cada subida se hace mediante un Pull Request:

```
desarrollo ──► homologacion ──► production
```

- Para pushear a `production` se requiere un PR que debe ser revisado y aprobado por la persona designada (el propio autor, actuando como revisor).
- Cada branch tiene su base de datos independiente.

## GitHub Actions

CI/CD automatizado con GitHub Actions:

- Testing automático del código.
- Migraciones de base de datos (esquema por branch/environment).
- Deploy automático al mergear:
  - Merge a `homologacion` → deploy staging.
  - Merge a `production` → deploy producción.

---

# Success Criteria

- Un usuario puede crear, eliminar y renombrar proyectos.
- Un usuario puede agregar, editar y eliminar tecnologías dentro de cada proyecto.
- Un usuario puede visualizar los proyectos en una lista o tabla, seleccionar uno y volver a la lista.
- El sistema se puede ejecutar localmente con docker-compose.
- El sistema se puede desplegar en Vercel + Render + Supabase.

---

# Project Status

This document describes the project contract: what the project is and why.

For the live project state — completed/in-progress features, decisions log, technical
debt, blockers, and metrics — see `PROJECT_STATUS.md`.