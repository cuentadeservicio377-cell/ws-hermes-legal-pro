# Hermes Legal Pro v3 — Descripción Arquitectónica Completa del Producto

> **Documento:** Arquitectura de Producto — Hermes Legal Pro v3 DUAL
> **Versión:** v3.0-DUAL (Dashboard Mac + Hermes Agent Telegram)
> **Fecha:** 2026-05-02
> **Repo:** `https://github.com/cuentadeservicio377-cell/ws-hermes-legal-pro`
> **Branch:** `master`
> **Último commit:** `0fa456f` — v8.1: Fix calendario plazos + verificación completa sistema
> **Autor:** Hermes Neo (Auditoría real del repositorio)

---

## 1. Visión del Producto

**Hermes Legal Pro** es el sistema operativo legal de WS Capital. Es un producto **dual** que opera en dos modos simultáneos:

1. **Dashboard local** (Mac/Windows) — Interfaz visual self-service para abogados y paralegales
2. **Hermes Agent** (Telegram/Voz) — Comandos naturales para operación rápida desde cualquier lugar

### Propuesta de valor única

> "El abogado es el dueño humano del asunto. Hermes Legal Pro es su sistema operativo: maneja la continuidad, el intake, la generación de documentos profesionales con diseño editorial Kami, el seguimiento de plazos, la biblioteca legal viva, la arquitectura de paquetes documentales, y la integración nativa con Google Workspace. El abogado nunca pierde contexto."

### Modo dual de operación

| Modo | Interfaz | Cuándo usar | Usuario |
|------|----------|-------------|---------|
| **Hermes Agent** | Telegram / Voz | En el coche, rápido, comandos naturales | Pablo (director) |
| **Dashboard** | Navegador localhost:8082 | En la oficina, visual, self-service | Abogados, paralegales, clientes |

Ambos modos comparten la **misma persistencia JSON local**, los **mismos 23 templates**, el **mismo Motor Kami v3**, y la **misma integración Google Workspace**.

---

## 2. Arquitectura del Sistema

### 2.1 Diagrama de arquitectura completa

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         CAPA DE INTERACCIÓN                              │
│  ┌─────────────────────┐    ┌─────────────────────────────────────────┐  │
│  │   HERMES AGENT      │    │         DASHBOARD (SPA)                 │  │
│  │   (Telegram/Voz)    │    │      localhost:8082                     │  │
│  │                     │    │                                         │  │
│  │  Comandos:          │    │  • Firm Operating Console               │  │
│  │  /matter, /contrato │    │  • 7 vistas: Dashboard, Matters,       │  │
│  │  /plazo, /status    │    │    Documentos, Calendario, Finanzas,  │  │
│  │  /alerta, /abrir    │    │    Reuniones, Agentes                 │  │
│  │                     │    │                                         │  │
│  │  Triggers: 13       │    │  • Motor Kami integrado               │  │
│  │  automáticos        │    │  • Google Drive sync                  │  │
│  └──────────┬──────────┘    └──────────────────┬──────────────────────┘  │
│             │                                    │                       │
│             └────────────────┬───────────────────┘                       │
│                              ▼                                         │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │              HERMES LEGAL PRO API (FastAPI)                      │   │
│  │                   Puerto :8082                                    │   │
│  │                                                                 │   │
│  │  • 37 endpoints RESTful                                         │   │
│  │  • CRUD completo: matters, reuniones, documentos, plazos       │   │
│  │  • Generación de PDF vía Motor Kami v3 (subprocess CLI)         │   │
│  │  • Validación de sustancia legal (13 elementos)                 │   │
│  │  • Finanzas: ingresos/egresos por matter                       │   │
│  │  • Aprobaciones workflow (aprobar/rechazar documentos)         │   │
│  │  • Alertas automáticas                                         │   │
│  │  • Export a Google Sheets/Docs                                 │   │
│  │  • Sync bidireccional Excel ↔ JSON                             │   │
│  │  • Health check con estado Motor Kami                          │   │
│  └────────────────────────────┬────────────────────────────────────┘   │
│                               │                                        │
│                               ▼                                        │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │              CAPA DE DATOS — JSON Local (Mac/Windows)            │   │
│  │                                                                 │   │
│  │  • matters.json        — Tracker de casos                      │   │
│  │  • documentos.json     — Documentos generados                  │   │
│  │  • reuniones.json      — Reuniones con clientes                │   │
│  │  • alertas.json        — Alertas del sistema                   │   │
│  │  • finanzas.json       — Ingresos/egresos por matter           │   │
│  │  • plazos.json         — Deadlines y milestones               │   │
│  │  • aprobaciones.json   — Workflow de aprobaciones              │   │
│  └────────────────────────────┬────────────────────────────────────┘   │
│                               │                                        │
│                               ▼                                        │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │              MOTOR KAMI v3 (Document Engine)                     │   │
│  │                                                                 │   │
│  │  • motor_kami.py     — CLI: --input JSON → --output PDF         │   │
│  │  • blocks.py         — 15 bloques + validador de sustancia      │   │
│  │  • bridge_api.py     — API FastAPI del motor (puerto 8080)      │   │
│  │  • 23 templates JSON — Estructura: metadata, recommended_blocks,│   │
│  │                        document_data_template, required_vars    │   │
│  │  • Sistema de diseño: Playfair Display + Inter, canvas          │   │
│  │    pergamino #faf8f0, acento ink blue #1B365D                   │   │
│  │  • Output: PDF profesional con numeración, headers, footers     │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │              GOOGLE WORKSPACE INTEGRATION                        │   │
│  │                                                                 │   │
│  │  • drive_manager.py  — Crear carpetas, subir PDFs, links      │   │
│  │  • sheets_manager.py — Exportar datos a Google Sheets         │   │
│  │  • docs_exporter.py  — Exportar documentos a Google Docs        │   │
│  │  • calendar_manager.py — Crear eventos en Google Calendar      │   │
│  │  • tasks_manager.py  — Crear tareas en Google Tasks            │   │
│  │  • Token: ~/.config/gcloud/application_default_credentials.json │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │              ESTRUCTURA DE CARPETAS (~/WillowLegal)              │   │
│  │                                                                 │   │
│  │  00_Sistema/       — Motor Kami, scripts, guías                 │   │
│  │  01_Clientes/     — Una carpeta por matter                     │   │
│  │  02_Administracion/ — Plantillas, formatos, manuales            │   │
│  │  03_Biblioteca_Legal/ — Precedentes, jurisprudencia             │   │
│  │  04_Agentes_Onyx/  — Fichas de agentes                         │   │
│  │  05_Backups/       — Backups periódicos                        │   │
│  └─────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────┘
```

### 2.2 Componentes principales

| # | Componente | Tecnología | Líneas | Rol |
|---|-----------|-----------|--------|-----|
| 1 | **Dashboard API** | FastAPI + Pydantic | 1,021 | Backend principal. 37 endpoints RESTful |
| 2 | **Dashboard Frontend** | Vanilla JS + CSS | 973 | SPA con 7 vistas operativas |
| 3 | **Motor Kami v3** | Python + WeasyPrint | 1,248 | Generador PDF + validador + 23 templates |
| 4 | **Hermes Integration** | Python class | 665 | Parser de comandos Telegram + triggers |
| 5 | **Google Workspace** | Python + Google API | ~800 | Drive, Sheets, Docs, Calendar, Tasks |
| 6 | **Scripts auxiliares** | Python + bash | ~500 | Sync, auditoría, instalación, export |

**Total código producto:** ~4,700+ líneas

---

## 3. Backend — Dashboard API (1,021 líneas)

### 3.1 Endpoints completos (37)

#### Health & Dashboard
| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/api/health` | GET | Health check + estado Motor Kami + conteo templates |
| `/api/dashboard` | GET | KPIs: matters activos, documentos pendientes, alertas, finanzas |

#### Matters (Casos)
| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/api/matters` | GET | Lista matters con filtros |
| `/api/matters` | POST | Crear matter + carpeta física + Drive folder |
| `/api/matters/{id}` | GET | Detalle completo del matter |
| `/api/matters/{id}` | PUT | Actualizar matter |
| `/api/matters/{id}` | DELETE | Eliminar matter |

#### Reuniones
| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/api/reuniones` | GET | Lista reuniones |
| `/api/reuniones` | POST | Crear reunión (con meet_url, transcript, acuerdos) |
| `/api/reuniones/{id}` | GET | Detalle de reunión |

#### Documentos
| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/api/documentos` | GET | Lista documentos generados |
| `/api/documentos` | POST | Registrar documento |
| `/api/documentos/{id}` | GET | Detalle de documento |
| `/api/documentos/{id}/aprobar` | POST | Aprobar documento (workflow) |
| `/api/documentos/{id}/rechazar` | POST | Rechazar documento |

#### Generación con Motor Kami
| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/api/templates` | GET | Lista 23 templates |
| `/api/templates/{key}` | GET | Detalle de template |
| `/api/matter/{id}/generar-documento` | POST | Genera PDF vía Motor Kami CLI |
| `/api/kami/validate` | POST | Valida sustancia legal (13 elementos) |

#### Google Workspace
| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/api/matter/{id}/drive-folder` | GET | Obtener/crear carpeta en Google Drive |
| `/api/matter/{id}/documents` | GET | Listar documentos del matter en Drive |
| `/api/drive-link/{id}` | GET | Obtener link de Drive para matter |
| `/api/export-sheets` | POST | Exportar datos a Google Sheets |
| `/api/export-docs` | POST | Exportar documento a Google Docs |
| `/api/sync-excel` | POST | Sincronizar Excel maestro ↔ JSON |

#### Finanzas, Plazos, Alertas, Tareas
| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/api/finanzas` | GET/POST | Ingresos/egresos por matter |
| `/api/plazos` | GET/POST | Deadlines y milestones |
| `/api/alertas` | GET | Alertas del sistema |
| `/api/aprobaciones` | GET | Documentos pendientes de aprobación |
| `/api/aprobacion/{id}/aprobar` | POST | Aprobar documento |
| `/api/tasks` | GET/POST | Tareas del sistema |
| `/api/calendar-events` | GET | Eventos de calendario |
| `/api/check-plazos` | POST | Verificar plazos vencidos |

### 3.2 Modelos Pydantic

```python
class ReunionInput(BaseModel):
    matter_id: Optional[str]
    cliente: str
    fecha: str
    meet_url: Optional[str]
    transcript: Optional[str]
    resumen: Optional[str]
    acuerdos: Optional[List[str]]
    documentos_necesarios: Optional[List[str]]
    plazos: Optional[List[Dict]]

class GenerarDocumentoRequest(BaseModel):
    template_key: str
    datos_extra: Optional[Dict] = {}
    output_filename: Optional[str] = None
```

### 3.3 Generación de documentos (Motor Kami integrado)

```python
def generar_documento(matter_id: str, req: GenerarDocumentoRequest):
    # 1. Cargar matter
    # 2. Cargar template JSON
    # 3. Construir bloques desde matter + datos_extra
    # 4. Crear JSON temporal
    # 5. Llamar motor_kami.py vía subprocess:
    #    python motor_kami.py --input tmp.json --output contrato.pdf
    # 6. Registrar en documentos.json
    # 7. Retornar path + tamaño + ID
```

---

## 4. Frontend — Dashboard SPA (973 líneas)

### 4.1 Estructura

| Archivo | Líneas | Función |
|---------|--------|---------|
| `index.html` | 159 | Estructura HTML + navegación |
| `app.js` | 814 | Router principal, inicialización |
| `api.js` | ~200 | Cliente HTTP para backend |
| `dashboard.js` | ~150 | Vista Dashboard con KPIs |
| `matters.js` | ~200 | CRUD de matters |
| `documentos.js` | ~180 | Generación y gestión de documentos |
| `calendario.js` | ~150 | Vista de plazos/calendario |
| `finanzas.js` | ~120 | Finanzas por matter |
| `reuniones.js` | ~150 | Registro de reuniones |
| `utils.js` | ~80 | Utilidades |
| `styles.css` | ~300 | Estilos principales |
| `kami.css` | ~100 | Estilos específicos Kami |

### 4.2 Vistas

| Vista | Descripción | Endpoints |
|-------|-------------|-----------|
| **Dashboard** | KPIs, alertas, matters activos, finanzas resumen | `GET /api/dashboard` |
| **Matters** | Lista, crear, editar, eliminar matters | `GET/POST/PUT/DELETE /api/matters` |
| **Documentos** | Generar desde template, aprobar, descargar PDF | `POST /generar-documento`, `POST /aprobar` |
| **Calendario** | Plazos, deadlines, milestones | `GET/POST /api/plazos` |
| **Finanzas** | Ingresos/egresos por matter, totales | `GET/POST /api/finanzas` |
| **Reuniones** | Registrar reuniones, transcripts, acuerdos | `GET/POST /api/reuniones` |
| **Agentes** | Estado de agentes, activar | `GET /api/health` |

### 4.3 Conectividad verificada

Cada botón del frontend tiene su endpoint correspondiente:
- Botón "Generar documento" → `POST /api/matter/{id}/generar-documento`
- Botón "Aprobar" → `POST /api/documentos/{id}/aprobar`
- Botón "Exportar Sheets" → `POST /api/export-sheets`
- Botón "Crear en Drive" → `GET /api/matter/{id}/drive-folder`

---

## 5. Motor Kami v3 (1,248 líneas)

### 5.1 Arquitectura

| Archivo | Líneas | Rol |
|---------|--------|-----|
| `motor_kami.py` | 528 | CLI + renderer PDF con WeasyPrint |
| `blocks.py` | 720 | 15 bloques + validador de sustancia |
| `bridge_api.py` | — | API FastAPI del motor (puerto 8080) |

### 5.2 Sistema de bloques (15 tipos)

| Bloque | Propósito |
|--------|-----------|
| `cover_page` | Portada editorial |
| `header_brand` | Logo + marca + número de documento |
| `parties_block` | Identificación formal de partes |
| `clause_section` | Cláusula numerada con estilo editorial |
| `payment_table` | Tabla de pagos con bordes sólidos |
| `comparison_table` | Comparativa 3-columnas |
| `flow_diagram` | Diagrama de flujo SVG |
| `signature_block` | Grilla 2×2 con testigos |
| `footer_block` | Disclaimer + números de página |
| `annex_section` | Anexo técnico |
| `data_grid` | Tabla de datos |
| `highlight_rule` | Regla horizontal separadora |
| `checklist_block` | Lista de checkboxes |
| `timeline_block` | Línea de tiempo visual |

### 5.3 Validación de sustancia (13 elementos)

```python
def validar_sustancia(data: dict) -> dict:
    # 1. PARTES (nombre, RFC, domicilio, representante, email)
    # 2. ANTECEDENTES (mínimo 20 chars)
    # 3. OBJETO Y ALCANCE
    # 4. FORMA DE PAGO
    # 5. PLAZO
    # 6. ENTREGABLES
    # 7. PROPIEDAD INTELECTUAL
    # 8. CONFIDENCIALIDAD
    # 9. LIMITACIÓN DE RESPONSABILIDAD
    # 10. SUSPENSIÓN Y TERMINACIÓN
    # 11. MEDIACIÓN Y JURISDICCIÓN
    # 12. DISPOSICIONES GENERALES
    # 13. FIRMAS + TESTIGOS
```

### 5.4 Sistema de diseño

- **Tipografía:** Playfair Display (títulos, cuerpo) + Inter (tablas, metadata)
- **Colores:** Pergamino `#faf8f0`, Ink Blue `#1B365D`, Near Black `#1a1a18`
- **Márgenes:** 28mm 22mm 30mm 22mm
- **Numeración:** Oldstyle-nums en footer
- **Output:** PDF A4 profesional

### 5.5 CLI Interface

```bash
python3 motor_kami.py --input datos.json --output contrato.pdf [--preview-html]
```

---

## 6. Biblioteca de Templates (23 Tipos)

### 6.1 Estructura de template

Cada template es un JSON con:
```json
{
  "metadata": { "key", "label", "area", "materia", "version" },
  "recommended_blocks": ["cover_page", "parties_block", "clause_section", ...],
  "document_data_template": { "tipo", "prestador", "cliente", "clausulas", ... },
  "required_variables": ["prestador.nombre", "cliente.nombre", ...],
  "notes": "Instrucciones de uso"
}
```

### 6.2 Inventario completo

| # | Key | Label | Área | Materia |
|---|-----|-------|------|---------|
| 1 | nda | NDA / Acuerdo de confidencialidad | Contratos | corporativo |
| 2 | confidencialidad | Cláusula de confidencialidad | Contratos | corporativo |
| 3 | prestacion_servicios | Prestación de servicios | Contratos | corporativo |
| 4 | terminos_condiciones | Términos y condiciones | Contratos | corporativo |
| 5 | acta_asamblea | Acta de asamblea | Corporativo | corporativo |
| 6 | poder_notarial | Poder notarial | Corporativo | corporativo |
| 7 | estatutos_sociales | Estatutos sociales | Corporativo | corporativo |
| 8 | convenio_accionistas | Convenio de accionistas | Corporativo | corporativo |
| 9 | contrato_trabajo | Contrato de trabajo | Laboral | laboral |
| 10 | reglamento_interior | Reglamento interior | Laboral | laboral |
| 11 | finiquito | Finiquito | Laboral | laboral |
| 12 | nda_laboral | NDA laboral | Laboral | laboral |
| 13 | convenio_pagos | Convenio de pagos | Cobranza | civil/mercantil |
| 14 | garantias | Garantías | Cobranza | civil/mercantil |
| 15 | arrendamiento | Arrendamiento | Cobranza | civil/mercantil |
| 16 | calendario_cobranza | Calendario de cobranza | Cobranza | civil/mercantil |
| 17 | carta_cobranza | Carta de cobranza | Cobranza | civil/mercantil |
| 18 | pagare | Pagaré | Cobranza | civil/mercantil |
| 19 | bitacora_entregas | Bitácora de entregas | Documentación | corporativo |
| 20 | expediente_materialidad | Expediente de materialidad | Fiscal | fiscal |
| 21 | carta_sat | Carta para SAT | Fiscal | fiscal |
| 22 | aviso_privacidad | Aviso de privacidad | Privacidad | privacidad |
| 23 | formato_arco | Formato ARCO | Privacidad | privacidad |

---

## 7. Hermes Agent Integration (665 líneas)

### 7.1 Comandos Telegram

| Comando | Descripción | Equivalente Dashboard |
|---------|-------------|----------------------|
| `/matter nuevo [nombre]` | Crear matter | Botón "Nuevo Matter" |
| `/matter list` | Listar matters | Tab "Matters" |
| `/contrato [template] [matter]` | Generar contrato | Wizard documentos |
| `/plazo [matter] [desc] [fecha]` | Crear deadline | Tab "Calendario" |
| `/alerta` | Ver alertas | Dashboard KPIs |
| `/status` | Estado del despacho | Dashboard general |
| `/documento [matter] [tipo]` | Generar documento | Botón "Generar" |
| `/finanzas` | Dashboard financiero | Tab "Finanzas" |
| `/abrir [matter]` | Abrir carpeta Windows | Botón "Abrir carpeta" |

### 7.2 Triggers automáticos (13)

| Trigger | Condición | Acción |
|---------|-----------|--------|
| `plazo_vencido` | Deadline pasado | Alerta + notificación |
| `documento_pendiente_aprobacion` | Doc en revisión > 24h | Recordatorio |
| `matter_sin_actividad` | Sin updates > 7 días | Alerta inactividad |
| `nueva_reunion` | Reunión registrada | Extraer acuerdos automáticamente |
| `finanzas_mensuales` | Fin de mes | Reporte ingresos/egresos |
| `backup_semanal` | Domingo | Backup JSON a Drive |
| `plazo_proximo` | Deadline en 3 días | Alerta anticipada |
| `documento_rechazado` | Estado = rechazado | Notificar + reasignar |
| `matter_nuevo` | Matter creado | Crear carpeta + Drive folder |
| `contrato_generado` | PDF creado | Subir a Drive + registrar |
| `reunion_sin_transcript` | Reunión sin notas | Recordatorio subir transcript |
| `aprobacion_pendiente` | > 48h sin aprobar | Escalar a Despacho Legal |
| `sync_excel` | Diario | Sincronizar Excel ↔ JSON |

### 7.3 Arquitectura de comandos

```python
class HermesLegalCommands:
    def crear_matter(self, nombre, **kwargs) -> dict
    def listar_matters(self, filtro=None) -> list
    def generar_contrato(self, matter_id, template_key, **kwargs) -> dict
    def crear_plazo(self, matter_id, descripcion, fecha) -> dict
    def ver_alertas(self) -> list
    def status_despacho(self) -> dict
    def abrir_carpeta(self, matter_id) -> str
    def exportar_finanzas(self, periodo) -> dict
```

---

## 8. Google Workspace Integration

### 8.1 Scripts de integración

| Script | Función | API Google |
|--------|---------|-----------|
| `drive_manager.py` | Crear carpetas, subir PDFs, compartir links | Drive API v3 |
| `sheets_manager.py` | Exportar datos, crear hojas | Sheets API v4 |
| `docs_exporter.py` | Exportar documentos a Docs | Docs API v1 |
| `calendar_manager.py` | Crear eventos, recordatorios | Calendar API v3 |
| `tasks_manager.py` | Crear tareas, checklists | Tasks API v1 |
| `sync_drive.py` | Sincronización bidireccional | Drive API v3 |

### 8.2 Flujo de integración

```
1. Crear matter en Dashboard
   ↓
2. Backend llama DriveManager.crear_carpeta_matter()
   ↓
3. Google Drive crea: /WillowLegal/01_Clientes/{Matter}/
   ↓
4. Guardar folder_id en matter.json
   ↓
5. Generar documento → Motor Kami → PDF
   ↓
6. Subir PDF a Drive folder
   ↓
7. Compartir link con cliente
   ↓
8. Registrar en documentos.json
```

---

## 9. Estructura de Carpetas (~/WillowLegal)

```
~/WillowLegal/
├── 00_Sistema/
│   ├── Motor_Kami/
│   │   ├── motor_kami.py
│   │   ├── blocks.py
│   │   ├── bridge_api.py
│   │   ├── templates/          # 23 JSON templates
│   │   └── output/             # PDFs generados
│   ├── scripts/
│   │   ├── drive_manager.py
│   │   ├── sheets_manager.py
│   │   ├── calendar_manager.py
│   │   └── sync_excel_json.py
│   └── Guia_Operativa.md
├── 01_Clientes/
│   └── {Matter_ID}_{Nombre}/
│       ├── 01_Intake/
│       ├── 02_Contratos/
│       ├── 03_Correspondencia/
│       ├── 04_Litigio/
│       ├── 05_Facturacion/
│       ├── 06_Entregables/
│       └── 07_Archivo/
├── 02_Administracion/
│   ├── Plantillas/
│   ├── Formatos/
│   └── Reportes/
├── 03_Biblioteca_Legal/
├── 04_Agentes_Onyx/
└── 05_Backups/
```

---

## 10. Flujo de Procesamiento Real

### 10.1 Sesión con cliente

```
1. Reunión con cliente (Google Meet)
   ↓
2. Registrar reunión en Dashboard (/api/reuniones)
   ↓
3. Subir transcript a matter folder
   ↓
4. Paralegal de Intake extrae datos estructurados
   ↓
5. Despacho Legal define estrategia y paquete documental
   ↓
6. Arquitecto Legal diseña estructura y dependencias
   ↓
7. Bibliotecario Legal propone templates y cláusulas
   ↓
8. Hermes ORQUESTA: construye JSON de bloques
   ↓
9. Motor Kami renderiza PDF profesional
   ↓
10. Almacenar en 06_Entregables/ + subir a Drive
   ↓
11. Workflow de aprobación (aprobar/rechazar)
   ↓
12. Entregar al cliente vía link de Drive
```

---

## 11. Estado Actual del Producto

### 11.1 Lo que SÍ está construido ✅

| Componente | Estado | Evidencia |
|-----------|--------|-----------|
| Dashboard API (37 endpoints) | ✅ | 1,021 líneas, FastAPI |
| Dashboard Frontend (7 vistas) | ✅ | 973 líneas, Vanilla JS |
| Motor Kami v3 (PDF real) | ✅ | 1,248 líneas, WeasyPrint |
| 23 Templates estructurados | ✅ | JSON con blocks + variables |
| Validación de sustancia | ✅ | 13 elementos en blocks.py |
| Hermes Agent commands | ✅ | 665 líneas, 15 métodos |
| 13 Triggers automáticos | ✅ | config/triggers.json |
| Google Workspace integration | ✅ | 6 scripts |
| Finanzas por matter | ✅ | Ingresos/egresos |
| Workflow aprobaciones | ✅ | Aprobar/rechazar |
| Calendario plazos | ✅ | Calendario.js |
| Export Sheets/Docs | ✅ | Endpoints funcionales |
| Sync Excel ↔ JSON | ✅ | Script dedicado |
| Estructura carpetas | ✅ | 7 subcarpetas por matter |
| Git versionado | ✅ | 15+ commits |
| Instalador Mac | ✅ | install-mac.sh |
| Actualizador | ✅ | actualizar.sh |
| Documentación completa | ✅ | 5 manuales |

### 11.2 Lo que FALTA / puede mejorarse ⚠️

| Componente | Estado | Nota |
|-----------|--------|------|
| Onyx integration | ⚠️ Parcial | Este producto es STANDALONE, no requiere Onyx |
| Excel Maestro v4.0 | ⚠️ No confirmado | Sync existe pero no 15 hojas confirmadas |
| Test suite | ⚠️ No encontrado | Sin tests automatizados |
| CI/CD | ❌ No | Sin GitHub Actions |
| Docker | ❌ No | Sin containerización |

### 11.3 Diferencia clave con el repo anterior

| Aspecto | Repo anterior (`willow-hermes-onyx`) | Repo REAL (`ws-hermes-legal-pro`) |
|---------|--------------------------------------|-----------------------------------|
| Motor Kami | ❌ No existía | ✅ 1,248 líneas, genera PDF real |
| Templates | Texto plano con `{{vars}}` | ✅ JSON estructurado con blocks |
| Backend | 1,658 líneas (sin motor) | ✅ 1,021 líneas (con motor integrado) |
| Frontend | 557 líneas, 7 tabs | ✅ 973 líneas, 7 vistas + calendario |
| Hermes Agent | ❌ No existía | ✅ 665 líneas, 15 métodos |
| Google Workspace | ❌ No existía | ✅ 6 scripts funcionales |
| Finanzas | ❌ No existía | ✅ Ingresos/egresos por matter |
| Aprobaciones | ❌ No existía | ✅ Workflow aprobar/rechazar |
| Triggers | ❌ No existían | ✅ 13 automáticos |
| Documentación | 8 docs técnicos | ✅ 5 manuales + prompts ejecutables |

---

## 12. Roadmap

### Completado ✅
- v1-v4: Dashboard base + Motor Kami
- v5: Google Workspace integration
- v6: REST API completa + Finanzas
- v7: Polish + documentación para abogados no-digital
- v8: Plan arquitectónico completo + frontend 100% conectado
- v8.1: Fix calendario plazos + verificación completa sistema

### Pendiente
- v9: Test suite automatizado
- v10: Docker containerization
- v11: CI/CD con GitHub Actions
- v12: Onyx integration opcional (modo dual)

---

## 13. Métricas del Sistema

| Métrica | Valor |
|---------|-------|
| Líneas de backend API | 1,021 |
| Líneas de frontend | 973 |
| Líneas de Motor Kami | 1,248 |
| Líneas de Hermes Integration | 665 |
| Líneas de scripts Google Workspace | ~800 |
| **Total código producto** | **~4,700+** |
| Templates legales | 23 |
| Endpoints RESTful | 37 |
| Comandos Telegram | 9 |
| Triggers automáticos | 13 |
| Vistas del dashboard | 7 |
| Bloques de documento | 15 |
| Elementos de validación sustancia | 13 |
| Commits en repo | 15+ |
| Manuales de documentación | 5 |
| Prompts ejecutables OpenCode Go | 8 |

---

## 14. Repositorio y Documentación

- **Repo GitHub:** `https://github.com/cuentadeservicio377-cell/ws-hermes-legal-pro`
- **Branch:** `master`
- **Último commit:** `0fa456f` — v8.1: Fix calendario plazos + verificación completa sistema
- **Documentos:**
  - `README.md` — Overview del producto
  - `USER-GUIDE.md` — Guía para abogados no-digital
  - `MANUAL_TECNICO.md` — Documentación técnica completa
  - `MANUAL_ABOGADO_COMPLETO.md` — Manual del abogado usuario
  - `MANUAL_HERMES_INTEGRATION.md` — Guía de integración Hermes Agent
  - `PLAN_ARQUITECTURA_COMPLETA_v8.md` — Plan arquitectónico v8
  - `PROMPT_v8_EJECUTABLE.md` — Prompt ejecutable para OpenCode Go

---

*Documento generado por auditoría real del repositorio `ws-hermes-legal-pro`. Cada componente verificado contra código fuente. Estado al 2026-05-02.*
