---
name: willow-legal-standalone
category: ws
description: >
  Sistema standalone de Willow Legal para firma We Law S.C.
  Funciona sin Onyx, sin Docker, sin PostgreSQL.
  Dashboard web en :8081, comandos CLI, generación de documentos con Motor Kami v3.
author: Hermes Neo / WS Capital
version: 1.0.0
trigger: Cuando el usuario necesite operar Willow Legal, generar documentos legales, revisar matters, plazos, o usar el sistema de gestión legal.
---

# Willow Legal — Sistema Standalone v1.0

## Estado del Sistema
- **Dashboard:** http://localhost:8081
- **Backend:** FastAPI + JSON local
- **Motor Documentos:** Kami v3 (23 templates)
- **Base de datos:** JSON en disco + Excel maestro v4.0
- **Cliente actual:** Pragma Studio (PRAG-001)

## Links críticos
- Dashboard: `http://localhost:8081`
- Workspace: `/root/ws-willow-standalone/`
- Datos: `/root/ws-willow-standalone/datos/matters.json`
- Motor Kami: `/root/ws-willow-standalone/motor_kami/`
- Scripts: `/root/ws-willow-standalone/scripts/willow_standalone.py`
- Excel Maestro: `/mnt/c/WillowLegal/02_Administracion/Centro_Operativo_Maestro_Willow_v4.xlsx`

## Comandos CLI
```bash
cd /root/ws-willow-standalone/scripts

# Ver status de matter
python3 willow_standalone.py --status PRAG-001

# Ver alertas
python3 willow_standalone.py --alertas

# Generar documento
python3 willow_standalone.py --generar PRAG-001 prestacion_servicios

# Listar templates
python3 willow_standalone.py --listar-templates

# Listar matters
python3 willow_standalone.py --listar-matters

# Abrir carpeta
python3 willow_standalone.py --abrir PRAG-001

# Crear matter nuevo
python3 willow_standalone.py --crear-matter "Nuevo Cliente" --representante "Nombre" --email "email@ej.com" --area "Mercantil"
```

## API Endpoints
| Endpoint | Descripción |
|----------|-------------|
| `GET /api/health` | Health check |
| `GET /api/matters` | Lista matters |
| `GET /api/matter/{id}` | Detalle matter |
| `GET /api/templates` | Lista templates |
| `POST /api/matter/{id}/generar-documento` | Genera PDF |
| `POST /api/matter/{id}/abrir-carpeta` | Abre carpeta Windows |
| `POST /api/matter/{id}/actualizar` | Actualiza campo |
| `GET /api/alertas` | Alertas |
| `GET /api/finanzas` | Finanzas |
| `GET /api/agentes` | Estado de 5 agentes legales |
| `POST /api/agentes/{agente}/accion` | Ejecuta acción de agente |

## Agentes Legales (operados por Hermes)
Los 5 agentes documentados en `04_Agentes_Onyx/` ahora son **capacidades de Hermes**:

| Agente | Acciones disponibles | Cómo usar con Hermes |
|--------|---------------------|----------------------|
| **Despacho Legal** | `proximo_paso`, `estrategia` | "Despacho Legal, ¿cuál es el siguiente paso para PRAG-001?" |
| **Paralegal Intake** | `faltantes`, `estructurar` | "Paralegal, ¿qué datos faltan del cliente?" |
| **Bibliotecario** | `listar_templates`, `proponer` | "Bibliotecario, ¿qué template necesito para un NDA?" |
| **Arquitecto** | `paquete_documentos`, `dependencias` | "Arquitecto, diseña el paquete para este matter" |
| **Coordinador Plazos** | `alertas`, `registrar_deadline` | "Coordinador, ¿hay plazos críticos esta semana?" |

**Nota:** Hermes lee `matters.json` y ejecuta la lógica de cada agente directamente. No requiere Onyx ni PostgreSQL.

## Principios
1. **Primero la sustancia, luego el diseño** — Kami valida antes de generar
2. **Chat-first** — Telegram para rápido, dashboard para profundo
3. **Todo funciona por separado. Todo funciona junto.** — Standalone primero
4. **Un matter = un cliente = una carpeta** — Estructura inmutable
5. **Hermes es el Control Plane** — Los agentes son capacidades de Hermes, no servicios separados

## Patrón de Construcción: "Paolizar" (de producto dependiente a standalone)

Este sistema fue construido siguiendo el patrón probado en `paola-meneses-eventos`:

### Fases de construcción (reutilizable)
| Fase | Qué se construye | Output |
|------|-------------------|--------|
| **1. Fundamentos** | Workspace, backend base, datos reales | `app.py` + `matters.json` |
| **2. Dashboard** | Frontend SPA completo con vistas operativas | `spa/index.html` |
| **3. Excel Maestro** | Excel offline con fórmulas y validaciones | `.xlsx` con 12+ hojas |
| **4. CLI/Telegram** | Comandos para operar en movimiento | `willow_standalone.py` |
| **5. Integración** | Sync opcional cuando la plataforma madre esté arriba | Bridge API v2 |

### Arquitectura reutilizable
```
Hermes (Telegram) ←→ FastAPI Backend (:8081) ←→ Motor de Negocio
                              ↓
                    JSON local + Excel Maestro + Carpetas Windows
```

### Lección clave: Auditoría de honestidad
Antes de declarar "completo", auditar TODO el sistema:
- 69 ítems auditados → 19% completos, 26% parciales, 55% faltantes
- Documentar gaps honestamente
- Definir qué tipo de negocio puede operar con el MVP actual

## Cliente actual: Pragma Studio
- **Matter:** PRAG-001
- **Representante:** Juan Antonio Angel Ramirez
- **Email:** contacto@wscapital.ai
- **Área:** Mercantil / Contratos / Cobranza
- **Problemas:** 8 identificados (disputa Andy, contrato hostil, actas, etc.)
- **Documentos pendientes:** 8
- **Plazos vencidos:** 3 (requieren atención)

## Nota sobre completitud
Este sistema es un **MVP funcional para firma boutique** (contratos, cobranza, consultoría). Para firma full-service (litigio, fiscal, laboral completo), faltan ~55% de funcionalidades: calendario judicial, expediente digital, facturación CFDI, firma electrónica, roles de usuario, etc. Ver `docs/RESUMEN_ENTREGA_v1.md` en workspace para auditoría completa.

## Skills relacionadas
- `paola-meneses-eventos` — Patrón arquitectónico de referencia (standalone con Excel + JSON + FastAPI)
- `willow-legal-complete` — Documentación técnica completa del sistema Onyx-dependiente original
- **Nota de consolidación futura:** `willow-legal-standalone` y `willow-legal-complete` podrían fusionarse cuando Onyx esté estable
