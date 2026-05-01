---
name: willow-legal-complete
description: Sistema completo Willow Legal — frontend en Onyx, motor de documentos Kami v3, y arquitectura de integración. Genera contratos y documentos legales mexicanos con validación de sustancia + diseño editorial profesional, dentro del producto Onyx chat-first.
trigger: Cuando el usuario necesite construir, operar o mejorar cualquier parte de Willow Legal — ya sea en modo standalone (dashboard propio, Excel local, sin Onyx) o en modo integrado con Onyx (frontend Onyx, PostgreSQL, chat-first). También cuando se detecte que Onyx está caído y se necesite operar Willow de forma independiente.
version: 2.1.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [willow, legal, onyx, kami, document-engine, mexican-law, contracts, frontend, bridge-api]
---

# Willow Legal — Sistema Completo

Skill consolidada que cubre los 3 pilares de Willow Legal:

1. **Frontend en Onyx** — Producto legal construido dentro del frontend real de Onyx (chat-first UI)
2. **Motor Kami v3** — Generación de documentos legales con validación de sustancia + diseño editorial
3. **Arquitectura de Integración** — Bridge API, agentes legales, carpetas Windows, flujo end-to-end

---

## PARTE 1: Frontend en Onyx (Onyx-First Legal UI)

### Principio fundamental

El producto legal debe existir **dentro del frontend real de Onyx**, no como un dashboard paralelo. Hermes Workspace debe tratarse como capa de integración futura, no como runtime primario.

### UX Anchor: Chat-First

- El modelo mental es **chat-first**, no dashboard-first
- El abogado debe sentirse dentro del producto Onyx principal
- El contexto legal envuelve el flujo de conversación
- Plazos, despacho, templates, memoria y entregables extienden el lenguaje del chat

### Audit antes de construir

**Nunca asumir que no existe nada.** Antes de planificar cualquier build, auditar los contenedores Docker desplegados:

```bash
# 1. Contenedores corriendo?
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" | grep onyx

# 2. Páginas legales en el build Next.js?
docker exec onyx-web_server-1 find /app/.next -type f | grep -i "legal" | sort
# Esperado: /app/.next/server/app/app/legal/page.js
#           /app/.next/server/app/app/legal/desk/page.js
#           /app/.next/server/app/app/legal/deadlines/page.js
#           /app/.next/server/app/app/legal/matters/[matterId]/page.js
#           /app/.next/server/app/app/legal/chat/[matterId]/page.js

# 3. Entrada en sidebar?
docker exec onyx-web_server-1 grep -o "Legal Runtime" /app/.next/server/chunks/ssr/*.js | head -1

# 4. Tablas en DB?
docker exec onyx-relational_db-1 psql -U postgres -c "\dt willow_*"

# 5. Agentes sembrados?
docker exec onyx-relational_db-1 psql -U postgres -c "SELECT name, is_public, builtin_persona FROM persona WHERE deleted = false AND (name ILIKE '%legal%' OR name ILIKE '%despacho%' OR name ILIKE '%intake%' OR name ILIKE '%biblioteca%' OR name ILIKE '%arquitecto%' OR name ILIKE '%plazos%');"

# 6. Templates cargados?
docker exec onyx-relational_db-1 psql -U postgres -c "SELECT id, label, category, area, state FROM willow_legal_template WHERE state = 'active';"

# 7. Proveedor LLM configurado?
docker exec onyx-relational_db-1 psql -U postgres -c "SELECT name, provider, default_model_name, is_default_provider FROM llm_provider;"

# 8. Matters existen?
docker exec onyx-relational_db-1 psql -U postgres -c "SELECT id, client_name, status, practice_area, office_path FROM willow_legal_matter;"
```

### Interpretación de resultados del audit

| Hallazgo | Significado | Acción |
|---|---|---|
| Las 5 páginas legales en `.next/server/app/app/legal/` | Frontend fue construido y desplegado | ✅ Verificar haciendo login y clickeando "Legal Runtime" |
| Tablas `willow_legal_*` existen con datos | Schema DB está listo | ✅ Usar tablas existentes, no recrear |
| 5 agentes legales en tabla `persona` | Agentes sembrados y listos para chat | ✅ Probarlos en el chat UI |
| 20+ templates en `willow_legal_template` | Librería de templates cargada | ✅ Usar templates existentes |
| `office_path` / `obsidian_path` vacíos | Sin integración filesystem aún | ⚠️ Construir Bridge + folder sync |
| No existe `legal_api.py` en ningún lado | Bridge API no existe | ⚠️ Construir FastAPI bridge |

### Rutas recomendadas

Crear un lane legal dedicado bajo el shell real de Onyx:
- `/app/legal` — legal home
- `/app/legal/matters/[matterId]` — matter workspace
- `/app/legal/chat/[matterId]` — matter chat
- `/app/legal/deadlines` — plazos
- `/app/legal/desk` — despacho/biblioteca/admin

### Orden de implementación

1. **Añadir entrada legal al sidebar real** — `AppSidebar.tsx` apuntando a `/app/legal`
2. **Crear legal home dentro de Onyx** — Orientar al abogado, mostrar matters activos, rutear al matter workspace
3. **Hacer el matter workspace el centro operativo** — Resumen, status, next step, blocker, deadline, conversación
4. **Añadir deadlines y desk como subvistas legales nativas** — Dentro del mismo modelo de interacción Onyx
5. **Mover de mock state hacia chat consciente de matter** — El matter seleccionado impulsa contexto legal

### Componentes reutilizables del substrate Onyx

Inspeccionar y reusar piezas reales ya en Onyx:
- `web/src/app/app/page.tsx`
- `web/src/refresh-pages/AppPage.tsx`
- `web/src/sections/sidebar/AppSidebar.tsx`
- `web/src/sections/input/AppInputBar.tsx`
- `web/src/sections/document-sidebar/DocumentsSidebar.tsx`
- `web/src/app/app/components/projects/ProjectContextPanel.tsx`
- `web/src/app/app/components/projects/ProjectChatSessionList.tsx`
- `web/src/providers/ProjectsContext.tsx`

### Construcción pragmática: SPA Fallback

Cuando el build Next.js está bloqueado por dependencias, pnpm workspace, errores Opal, o restricciones de tiempo:

1. Crear `legal_spa/index.html` junto a `legal_api.py`
2. Montar en FastAPI:
   ```python
   from fastapi.staticfiles import StaticFiles
   app.mount("/spa", StaticFiles(directory="legal_spa", html=True), name="spa")
   ```
3. La SPA llama a `/api/legal/*` y abre Onyx chat en nuevas pestañas

La SPA debe incluir:
- Lista de matters con formulario de creación
- Matter detail con tabs: Overview, Chat, Files, Contracts
- Chat tab: lista sesiones Onyx + botón "New chat"
- Files tab: upload + lista
- Contracts tab: selector de template + generar + download
- Agents sidebar: lista de personas legales con links

### Integración chat sin rebuild del controlador

En lugar de cablear chat UI custom dentro de `/app/legal`, **aprovechar el chat nativo de Onyx** abriendo `/chat?projectId={project_id}&chatId={chat_session_id}` en nueva pestaña o embed.

Esto permite usar el chat real Onyx con contexto legal (archivos scoped, selección de persona, citaciones) sin reescribir `AppPage.tsx`.

### Build loop WSL + Docker (crítico)

El contenedor `onyx-web_server` es una imagen Docker con output standalone compilado. No monta el código fuente del host.

**Lo que funciona:**
1. Copiar fuente a path Linux puro: `cp -r /mnt/c/.../onyx/web /tmp/onyx-web`
2. Usar `pnpm` en lugar de `npm`: `cd /tmp/onyx-web && pnpm install`
3. Aprobar build scripts: `echo -e "a\ny\n" | pnpm approve-builds`
4. Build: `pnpm run build`
5. Copiar `.next/standalone` y `.next/static` al contenedor

**Build canonical desde fuente:**
```bash
cd /mnt/c/Users/.../onyx/deployment/docker_compose
docker compose -f docker-compose.yml -f docker-compose.onyx-lite.yml build web_server
```

### Restricciones Opal (bloqueadores de build críticos)

- `Text` de `@/refresh-components/texts/Text` solo acepta `as?: "p" | "span" | "li"` — ❌ `as="h1"` o `as="h2"` → error TypeScript
- `Button` de `@opal/components` **no acepta `className`** — envolver en `<div className="mt-2">`
- `Divider` de `@opal/components` **no acepta `className`** — envolver en `<div className="my-5">`
- IDs de matter son `number` pero params de ruta Next.js son `string` — castear: `String(matter.id) === String(selectedMatterId)`

### Creación de usuarios (fastapi_users)

Onyx usa `fastapi_users` con bcrypt. El endpoint de login es `/api/auth/login` y espera `application/x-www-form-urlencoded`.

```bash
# Generar hash bcrypt
docker exec onyx-api_server-1 python3 -c "from passlib.context import CryptContext; ctx = CryptContext(schemes=['bcrypt'], deprecated='auto'); print(ctx.hash('Legal'))"

# Login
curl -s -X POST http://localhost:3000/api/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=hola@welaw.com.mx&password=Legal"
```

Campos críticos NOT NULL en tabla `user`:
- `role` — MUST be uppercase `'ADMIN'` (enum `userrole`)
- `is_active`, `is_superuser`, `is_verified` — booleans NOT NULL
- `default_app_mode` — NOT NULL varchar, default `'CHAT'`
- `account_type` — NOT NULL varchar, default `'STANDARD'`

---

## PARTE 2: Motor Kami v3 — Generación de Documentos Legales

### Filosofía

> **Primero la sustancia, luego el diseño.**

Secuencia obligatoria:
```
1. VALIDAR SUSTANCIA → 2. COMPONER BLOQUES → 3. APLICAR DISEÑO → 4. OUTPUT PDF
```

### Regla fundamental: Kami es SOLO capa estética

**Kami NUNCA es capa de contenido.** NO:
- Añadir metáforas explicativas ("sastre", "CFE", "mancha de Excel")
- Insertar cajas didácticas dentro de cláusulas legales
- Reemplazar numeralia legal con secciones narrativas
- Convertir un contrato de 3 páginas en una guía de 10 páginas

**Test Blanco-y-Negro:** Un contrato Kami debe seguir siendo legalmente válido si se imprime en blanco y negro con Times New Roman, cero color, cero cajas. Si no lo es, la estructura legal está rota.

### Estructura requerida para contratos mexicanos de servicios

```
1.  TÍTULO
2.  SUBTÍTULO (opcional)
3.  Fecha y Número de Contrato
4.  PARTES (ambas partes con datos legales completos)
    - Razón social / Nombre completo
    - RFC
    - Domicilio fiscal
    - Representante legal
    - Email
5.  ANTECEDENTES (1 párrafo seco, máx)
6.  1. OBJETO Y ALCANCE (1.1, 1.2, 1.3...)
7.  2. FORMA DE PAGO (2.1, 2.2 a/b/c/d, 2.3, 2.4, 2.5)
8.  3. PLAZO (cláusula separada, no mezclada con entregables)
9.  4. ENTREGABLES Y ACEPTACIÓN
10. 5. PROPIEDAD INTELECTUAL
11. 6. CONFIDENCIALIDAD
12. 7. LIMITACIÓN DE RESPONSABILIDAD
13. 8. SUSPENSIÓN Y TERMINACIÓN
14. 9. MEDIACIÓN Y JURISDICCIÓN
15. 10. DISPOSICIONES GENERALES (siempre incluir)
16. FIRMAS (ambas partes + Testigo 1 + Testigo 2)
17. Pie de documento
```

### Reglas de numeralia

- Decimal: `1.`, `1.1`, `1.2`, `1.3`
- Letras para sub-items: `a)`, `b)`, `c)`
- NUNCA saltar números
- NUNCA mezclar encabezados narrativos con numeralia legal
- Si una sección necesita explicación, ponerla en un ANEXO, no en la cláusula

### Validación de sustancia (13 elementos)

Antes de generar CUALQUIER PDF, validar:

| # | Elemento | Bloque |
|---|---------|-------|
| 1 | PARTES (nombre, RFC, domicilio, representante, email) | `parties_block` |
| 2 | ANTECEDENTES — non-empty, mínimo 20 chars | `clause_section` (num 0) |
| 3 | OBJETO Y ALCANCE — cláusula con "objeto" o "alcance" | `clause_section` |
| 4 | FORMA DE PAGO — cláusula con "pago" | `clause_section` + `payment_table` |
| 5 | PLAZO — cláusula con "plazo" | `clause_section` |
| 6 | ENTREGABLES — cláusula o anexo | `clause_section` o `annex_section` |
| 7 | PROPIEDAD INTELECTUAL | `clause_section` |
| 8 | CONFIDENCIALIDAD | `clause_section` |
| 9 | LIMITACIÓN DE RESPONSABILIDAD | `clause_section` |
| 10 | SUSPENSIÓN Y TERMINACIÓN | `clause_section` |
| 11 | MEDIACIÓN Y JURISDICCIÓN | `clause_section` |
| 12 | DISPOSICIONES GENERALES | `clause_section` |
| 13 | FIRMAS + TESTIGOS (2+2) | `signature_block` |

También validar:
- **Tono:** Sin metáforas ("como la CFE", "sastre a medida", "mancha de Excel")
- **Límite de palabras:** Máximo 3,000 palabras para contratos estándar

Si la validación falla → **RECHAZAR** con lista de errores + checklist. No se genera PDF.

### Catálogo de bloques

| Bloque | Propósito | Cuándo usar |
|--------|-----------|-------------|
| `header_brand` | Logo + marca + número de documento | Todo documento formal |
| `cover_page` | Portada editorial | Contratos principales, propuestas |
| `parties_block` | Identificación formal de partes con borde izquierdo | Todo contrato |
| `clause_section` | Cláusula numerada con estilo editorial | Cuerpo del contrato |
| `payment_table` | Tabla de pagos con bordes sólidos | Cláusula de pago |
| `comparison_table` | Comparativa 3-columnas (concepto / A / B) | Obligaciones vs responsabilidades |
| `flow_diagram` | Diagrama de flujo SVG con cajas y flechas | Procesos, fases, workflows |
| `signature_block` | Grilla 2×2 con bordes + testigos | Final de todo contrato |
| `footer_block` | Disclaimer + números de página | Todo documento |
| `annex_section` | Anexo con encabezado y tabla | Anexos técnicos |
| `data_grid` | Tabla de datos (canales, catálogos) | Tablas de comunicación |
| `highlight_rule` | Regla horizontal con texto centrado | Separadores de sección |
| `checklist_block` | Lista de checkboxes | Requisitos, validaciones |
| `timeline_block` | Línea de tiempo visual | Cronogramas, calendarios |

### Sistema de diseño v3 (Editorial Robusto)

#### Tipografía
- **Playfair Display** (400–800) — títulos, cuerpo, firmas
- **Inter** (400–700) — tablas, metadata, encabezados

#### Colores
- **Primary:** `#1a1a18` (negro editorial, NO azul)
- **Background:** `#faf8f0` (pergamino cálido)
- **Secondary:** `#3d3d3a`
- **Metadata:** `#9a9a96`
- **Accent:** `#8B0000` (solo para penalizaciones)

#### Espaciado
- Márgenes: 25mm
- Interlineado: 1.65
- Numerales oldstyle proporcionales

#### Elementos visuales
- Partes: borde izquierdo 3pt sólido negro + indentación
- Cláusulas: numeral grande (18pt Inter bold) + título subrayado + borde izquierdo en subcláusulas
- Tablas: borde exterior 1pt sólido, header negro, fondos alternados sutiles
- Firmas: grilla 2×2 con bordes 1pt, línea de firma gruesa (1.5pt)
- Diagramas de flujo: cajas SVG negras con texto blanco, conectores flecha

### Motor Kami — Arquitectura centralizada

Desde abril 2026, TODOS los documentos legales DEBEN generarse a través del **Motor Kami** — un servicio Python centralizado. Sin scripts standalone, sin generadores .docx, sin creación ad-hoc de PDFs.

**Por qué centralizado:**
- Hermes Neo lo invoca vía CLI: `python3 motor_kami.py --input datos.json --output contrato.pdf`
- Agentes Onyx lo invocan vía `LegalDocumentTool` → Bridge API → Motor Kami
- Cron jobs lo invocan vía CLI para recordatorios y reportes automatizados
- Todo documento sale con estructura legal consistente + diseño Kami consistente

**Input del Motor Kami (v3, actual):**
```json
{
  "blocks": [
    { "type": "cover_page", "data": {"marca": "Pragma", "titulo": "...", ...} },
    { "type": "parties_block", "data": {"prestador": {...}, "cliente": {...}} },
    { "type": "clause_section", "data": {"numero": "1", "titulo": "Objeto", "subclausulas": [...]} },
    { "type": "payment_table", "data": {"headers": [...], "rows": [...]} },
    { "type": "flow_diagram", "data": {"titulo": "Flujo", "steps": ["Firma", "Fase 1", "Fase 2", "Entrega"]} },
    { "type": "comparison_table", "data": {"titulo": "Obligaciones", "left_label": "Prestador", "right_label": "Cliente", "items": [...]} },
    { "type": "signature_block", "data": {"prestador": {...}, "cliente": {...}} }
  ],
  "options": {
    "color_primary": "#1a1a18",
    "color_bg": "#faf8f0",
    "titulo": "Contrato..."
  }
}
```

**Workflow del Motor Kami:**
```
JSON datos → Validación SUSTANCIA (13 elementos) → Validación ESTRUCTURA →
Composición de bloques → Render HTML → Aplicar CSS Kami → PDF
```

Si la validación falla, el motor RECHAZA la generación y devuelve lista de elementos faltantes. El agente debe corregir el JSON antes de reintentar.

### Regla FORZOSA

> **Todo documento legal DEBE pasar por Motor Kami.** Sin excepciones. Sin .docx sin diseño. Sin PDFs generados fuera del motor.

### Anti-patrón crítico: Generación directa sin agentes

**NUNCA generar documentos legales directamente con Python scripts o python-docx sin mediación de agentes.**

El anti-patrón incorrecto:
```python
# ❌ MAL: Hermes genera docx directamente
from docx import Document
doc = Document()
doc.add_heading("Contrato")
doc.add_paragraph("El prestador...")
doc.save("Contrato.docx")
```

Esto produce documentos estériles, basados en templates genéricos, que los clientes rechazan.

**La forma correcta: generación mediada por agentes con sistema de diseño:**
```
1. Agentes Onyx (chat) generan contenido:
   - Paralegal de Intake extrae datos del cliente de notas de sesión
   - Despacho Legal define estrategia y prioridades
   - Bibliotecario Legal propone cláusulas y templates
   - Arquitecto Legal diseña estructura y dependencias

2. Hermes (Neo) ORQUESTA:
   - Recolecta outputs de agentes de sesiones de chat
   - Estructura contenido en HTML semántico/markdown
   - Mapea variables desde datos del matter

3. Sistema de diseño (Kami) RENDERIZA:
   - Aplica canvas pergamino + acento ink blue
   - Genera diagramas SVG inline (flujos de proceso, timelines, swimlanes)
   - Produce output PDF profesional

4. Bridge almacena en carpeta Windows:
   - PDF final → 06_Entregables/Documentos_Finales/
   - Source HTML → 02_Contratos/Borradores/
   - Registra qué agente propuso cada sección en metadata
```

### Inventario de templates (23 tipos)

| # | Key | Área | Materia |
|---|-----|------|---------|
| 1 | nda | Contratos | corporativo |
| 2 | confidencialidad | Contratos | corporativo |
| 3 | prestacion_servicios | Contratos | corporativo |
| 4 | terminos_condiciones | Contratos | corporativo |
| 5–8 | acta_asamblea, poder_notarial, estatutos_sociales, convenio_accionistas | Corporativo | corporativo |
| 9–12 | contrato_trabajo, reglamento_interior, finiquito, nda_laboral | Laboral | laboral |
| 13–18 | convenio_pagos, garantias, arrendamiento, calendario_cobranza, carta_cobranza, pagare | Cobranza/Contratos | civil/mercantil |
| 19 | bitacora_entregas | Documentación | corporativo |
| 20–21 | expediente_materialidad, carta_sat | Fiscal | fiscal |
| 22–23 | aviso_privacidad, formato_arco | Privacidad | privacidad |

### Qué va dónde

| Tipo de contenido | Ubicación |
|---|---|
| Obligaciones, derechos, sanciones | CUERPO del contrato |
| Montos, porcentajes de pago | CUERPO del contrato (tabla dentro de cláusula) |
| Deadlines, fechas | CUERPO del contrato |
| Descripciones de proceso, rituales | ANEXO TÉCNICO |
| Explicaciones, metáforas, por qué hacemos esto | GUÍA DEL CLIENTE (documento separado) |
| Tabla detallada de entregables | ANEXO TÉCNICO (nunca en cuerpo del contrato) |
| Reglas de canales de comunicación | CUERPO del contrato (breve) o ANEXO |

### Lista de verificación antes de entregar

- [ ] Sección PARTES existe con datos legales completos de ambas partes
- [ ] Numeralia completa y consistente (1 → 1.1, 1.2)
- [ ] PLAZO es cláusula separada
- [ ] DISPOSICIONES GENERALES existe
- [ ] FIRMAS incluye 2 testigos
- [ ] Sin cajas de highlight, warning boxes, o tags en el cuerpo
- [ ] Sin metáforas o explicaciones didácticas en el cuerpo
- [ ] Tono imperativo ("se obliga", "faculta", "se reserva")
- [ ] Longitud proporcional (3-5 páginas para contrato estándar)
- [ ] Contenido de transcripts está LEGALIZADO, no pegado narrativamente
- [ ] **Generado a través de Motor Kami (servicio centralizado)**
- [ ] **Comparado contra documentos existentes del cliente para match de estructura**
- [ ] **Input JSON validado (check estructural de 13 elementos)**
- [ ] **Composición de bloques apropiada para el tipo de documento**
- [ ] **Validación de sustancia pasada antes de aplicar diseño**

---

## PARTE 3: Arquitectura de Integración

### Bridge API (FastAPI)

No construir una base de datos separada para Willow. Crear un **servicio bridge FastAPI** que reuse la PostgreSQL existente de Onyx y sus tablas nativas:

- `user_project` → crear un proyecto por matter legal
- `chat_session` → crear sesiones de chat ligadas al `project_id` del matter
- `user_file` + `project__user_file` → subir archivos ligados al proyecto del matter
- `persona` → sembrar agentes legales (Despacho Legal, Intake Legal, Biblioteca Legal)
- Tablas custom prefix `willow_legal_*` solo para campos que Onyx no tiene nativamente (practice_area, blocker, next_step, priority, deadline, etc.)

**Endpoints útiles del Bridge:**
- `POST /api/legal/matters` — crea tanto un `user_project` de Onyx como una fila `willow_legal_matter`, ligándolas
- `POST /api/legal/matters/{id}/chat-sessions` — crea una `chat_session` real de Onyx atada al `project_id` del matter
- `POST /api/legal/matters/{id}/files` — envuelve el upload de archivos de Onyx y liga vía `project__user_file`
- `POST /api/legal/contracts/generate` — llena un `willow_legal_template` usando datos del matter y devuelve texto generado
- `POST /api/legal/agents/seed` — inserta personas legales en la tabla `persona` de Onyx con `starter_messages` JSON

### Schema exacto para crear chat sessions

```sql
INSERT INTO chat_session (
    id, user_id, persona_id, description, project_id,
    time_created, time_updated,
    deleted, shared_status, onyxbot_flow
) VALUES (
    gen_random_uuid(),
    '<user_uuid>',
    <persona_id>,       -- 0 para default Assistant
    '<description>',
    <project_id>,
    NOW(), NOW(),
    false, 'private', false
);
```

Campos NOT NULL críticos descubiertos:
- `deleted` — boolean, NOT NULL, default false
- `shared_status` — varchar(7), NOT NULL, values: `'private' | 'public'`
- `onyxbot_flow` — boolean, NOT NULL, default false
- `time_created` — timestamptz, NOT NULL
- `time_updated` — timestamptz, NOT NULL

### Schema exacto para sembrar agentes legales (personas)

```sql
INSERT INTO persona (
    name, deleted, description, is_listed, is_public,
    builtin_persona, system_prompt, starter_messages,
    datetime_aware, replace_base_system_prompt
) VALUES (
    'Despacho Legal',
    false,
    'Agente de gestión operativa del despacho...',
    true, true, false,
    'Eres el agente de Despacho Legal...',
    '[{"name": "Resumen del despacho", "message": "..."}]'::jsonb,
    true, false
);
```

Personas confirmadas en un despliegue funcional (5 agentes):
- **Despacho Legal** — priorización de workload, deadlines, tracking de tareas, aprobaciones
- **Paralegal de Intake** — intake de cliente, definición de scope, documentos requeridos, setup de matter
- **Bibliotecario Legal** — templates, precedentes, sugerencias de cláusulas, evolución de librería
- **Arquitecto Legal** — diseño de paquete de contratos, dependencias, variables compartidas, secuencia de ejecución
- **Coordinador de Plazos** — deadlines, milestones procesales, audiencias, blockers, follow-ups

### Bridge de carpetas Windows + filesystem legal

Cuando el usuario necesita ver **documentos finales (Word, PowerPoint, Excel)** en una carpeta Windows real, no solo dentro de Onyx:

**Estructura de carpetas:**
```
C:\WillowLegal\
├── 00_Sistema\              # Scripts bridge, guías, docs de conexión
│   ├── willow_bridge.py
│   ├── Guia_Operativa.md
│   ├── Conexion_Onyx.md
│   └── Checklist_Apertura_Matter.md
├── 01_Clientes\             # Una carpeta por cliente/matter
│   └── Cliente_Nuevo_1\     # Template — copiar y renombrar para cada cliente
│       ├── 01_Intake\       # Datos_Cliente.xlsx, Ficha_Matter.md, Checklist_Intake.md
│       ├── 02_Contratos\    # Borradores, Firmados, Anexos
│       ├── 03_Correspondencia\  # Entrante, Saliente
│       ├── 04_Litigio\      # Demandas, Contestaciones, Pruebas, Audiencias
│       ├── 05_Facturacion\  # Cotizaciones, Facturas, Pagos
│       ├── 06_Entregables\  # Documentos_Finales, Presentaciones, Reportes
│       └── 07_Archivo\      # Cerrado
├── 02_Administracion\       # Templates, formatos, manuales, reportes
│   ├── Plantillas\          # Espejo de categorías willow_legal_template
│   ├── Formatos\
│   ├── Manuales\
│   └── Reportes\
├── 03_Biblioteca_Legal\     # Precedentes, Jurisprudencia, Doctrina, Cláusulas
├── 04_Agentes_Onyx\         # Fichas de cada agente con prompts de ejemplo
└── 05_Backups\              # Target de backup periódico
```

**Archivos clave por carpeta de cliente:**

| Archivo | Propósito |
|---|---|
| `01_Intake/Datos_Cliente.xlsx` | Datos estructurados del cliente (3 hojas: datos, contactos, documentos) |
| `01_Intake/Ficha_Matter.md` | Matter card editable por humanos sincronizada a campos Onyx |
| `01_Intake/Checklist_Intake.md` | Checklist de validación antes de apertura formal de matter |
| `01_Intake/Notas_Recepcion.md` | Log de cada interacción con el cliente |
| `02_Contratos/Borradores/` | Contratos work-in-progress |
| `02_Contratos/Firmados/` | Contratos finales ejecutados |
| `06_Entregables/Documentos_Finales/` | **Entregables finales** — Word, PDF |
| `06_Entregables/Presentaciones/` | Archivos PowerPoint |
| `06_Entregables/Reportes/` | Excel, CSV reports |

**Script bridge: willow_bridge.py**

```python
#!/usr/bin/env python3
"""Willow Bridge — sync Onyx DB con carpetas Windows. Sin dependencias externas."""
import argparse, subprocess
from pathlib import Path

DB_CONTAINER = "onyx-relational_db-1"
DB_USER = "postgres"
CLIENTES_DIR = Path("C:/WillowLegal/01_Clientes")

def psql(query):
    cmd = ["docker", "exec", DB_CONTAINER, "psql", "-U", DB_USER, "-t", "-A", "-c", query]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return [l.strip().split("|") for l in result.stdout.strip().split("\n") if l.strip()]

def create_matter(client_name, practice_area="Mercantil", deadline=None, priority="medium"):
    # Crear proyecto Onyx
    rows = psql(f"INSERT INTO user_project (name, description) VALUES ('{client_name}', 'Matter: {client_name}') RETURNING id;")
    project_id = rows[0][0]

    # Crear willow matter
    dl = f"'{deadline}'" if deadline else "NULL"
    rows = psql(f"INSERT INTO willow_legal_matter (project_id, client_name, status, practice_area, deadline, priority, blocker, next_step) VALUES ({project_id}, '{client_name}', 'active', '{practice_area}', {dl}, '{priority}', 'none', 'Intake inicial pendiente') RETURNING id;")
    matter_id = rows[0][0]

    # Crear carpeta física
    safe = "".join(c for c in client_name if c.isalnum() or c in " _-").strip()
    d = CLIENTES_DIR / safe
    d.mkdir(parents=True, exist_ok=True)
    for sf in ["01_Intake", "02_Contratos/Borradores", "02_Contratos/Firmados", "02_Contratos/Anexos", "03_Correspondencia/Entrante", "03_Correspondencia/Saliente", "04_Litigio/Demandas", "04_Litigio/Contestaciones", "04_Litigio/Pruebas", "04_Litigio/Audiencias", "05_Facturacion/Cotizaciones", "05_Facturacion/Facturas", "05_Facturacion/Pagos", "06_Entregables/Documentos_Finales", "06_Entregables/Presentaciones", "06_Entregables/Reportes", "07_Archivo/Cerrado"]:
        (d / sf).mkdir(parents=True, exist_ok=True)

    # Link path en Onyx
    path = str(d).replace("/", "\\\\")
    psql(f"UPDATE willow_legal_matter SET office_path = '{path}' WHERE id = {matter_id};")

    print(f"✅ Matter {matter_id} | Project {project_id} | Folder: {d}")
```

**Operaciones:**
```bash
# Listar matters
python3 willow_bridge.py --list-matters

# Crear matter + carpeta simultáneamente
python3 willow_bridge.py --create-matter "Cliente Real SA" --area "Corporativo" --deadline "2026-06-30"

# Verificar que cada matter tiene su carpeta
python3 willow_bridge.py --sync-matters
```

**Reglas doradas para operación de carpetas:**
1. **Todo cliente nuevo empieza copiando `Cliente_Nuevo_1` y renombrando**
2. **Todo documento final vive en `06_Entregables/Documentos_Finales/`**
3. **Todo contrato fluye: Borrador → Revisión → Firmado**
4. **Onyx trackea el qué/cuándo/quién. La carpeta almacena el archivo físico.**
5. **Matters cerrados se mueven a `07_Archivo/Cerrado/` y obtienen status `closed` en Onyx**

### Principio de independencia Onyx + Hermes

**Onyx y Hermes deben funcionar cada uno independientemente. Son aditivos, no sustractivos.**

| Capacidad | Onyx (nativo) | Hermes (operador externo) |
|---|---|---|
| **Quién inicia** | Usuario en chat Onyx | Pablo vía Telegram/voz |
| **Quién orquesta** | Agentes Onyx + auto-flows | Hermes (Neo) + subagentes |
| **Generación de documentos** | Agent chat → Document Engine → PDF | Session notes → Agent chat → Document Engine → PDF |
| **Dónde se almacena** | `user_file` en Onyx + carpeta Windows | Carpeta Windows + sync a Onyx |
| **Documentación** | Auto-loggeada en tabla `willow_legal_document` | Manual escrito en `00_Sistema/Manual_Procesamiento.md` |
| **Experiencia de usuario** | Self-service para abogados usando Onyx | Servicio asistido con guía de Hermes |

**El Document Engine** (Kami + Legal Design + templates) es un **servicio independiente único** (ej. FastAPI en puerto 9100) consumido por ambos:

```
┌─────────────────────────────────────────┐
│         DOCUMENT ENGINE                 │
│  Kami Renderer + Legal Design Rules     │
│  Templates ES + SVG Diagram Generator   │
│            Port 9100                    │
└─────────────────────────────────────────┘
                    ▲
        ┌───────────┴───────────┐
        │                       │
   ┌────▼────┐            ┌─────▼─────┐
   │  ONYX   │            │  HERMES   │
   │ agents  │            │  (Neo)    │
   │ chat    │            │ Telegram  │
   └─────────┘            └───────────┘
```

### Flujo de procesamiento de caso real (transcript → documentos)

**Paso 1: Recibir materiales brutos**
- Notas de sesión (`.docx` o `.txt` de Gemini/Google Meet)
- Documentos del cliente, emails, fotos
- Todo almacenado en `01_Clientes/{Cliente}/01_Intake/`

**Paso 2: Extraer datos estructurados**
Usar **Paralegal de Intake** (chat Onyx) para:
- Leer el transcript
- Extraer: nombre del cliente, tipo de negocio, contacto, scope del proyecto
- Identificar: problemas, disputas, riesgos, documentos requeridos
- Detectar información faltante

**Crítico:** NO usar templates genéricos. La voz del transcript importa. Si el cliente dice "órale", "chingón", "estudio boutique", "pausas que pulverizan proyecciones" — los documentos legales deben reflejar este contexto específico.

**Paso 3: Definir estrategia**
Usar **Despacho Legal** (chat Onyx) para:
- Establecer prioridades (resolución de disputa = urgente, contrato = importante)
- Asignar next steps
- Identificar blockers
- Definir el paquete documental necesario

**Paso 4: Diseñar estructura de documentos**
Usar **Arquitecto Legal** (chat Onyx) para:
- Mapear dependencias entre documentos
- Definir nombres de variables para templates
- Secuenciar orden de ejecución

**Paso 5: Generar contenido con agentes**
Cada agente contribuye contenido:
- **Bibliotecario Legal** → propone cláusulas desde templates + precedentes
- **Arquitecto Legal** → diseña estructura y dependencias
- **Despacho Legal** → aprueba estrategia legal y posiciones de riesgo
- **Coordinador de Plazos** → define deadlines y triggers

**Paso 6: Hermes ORQUESTA (si se usa flujo Hermes)**
Hermes recolecta todos los outputs de agentes, los estructura en HTML compatible Kami, y llama al Document Engine.

**Paso 7: Sistema de diseño renderiza**
Kami aplica:
- Canvas pergamino + acento ink blue
- Jerarquía tipográfica serif
- Diagramas SVG inline (flujo de proceso, timeline, swimlane)
- Output PDF

**Paso 8: Almacenar en filesystem + Onyx**
- PDF final → `06_Entregables/Documentos_Finales/`
- Source/borrador → `02_Contratos/Borradores/`
- Registrar en tabla `willow_legal_document` con `generated_by` = nombre del agente
- Subir copia a Onyx vía `/api/user/projects/file/upload`

**Paso 9: Demo guiado con el usuario**
NO optimizar en aislamiento. Hacer que el usuario:
1. Abra el PDF
2. Verifique que la voz coincide con las sesiones
3. Chequee que preocupaciones específicas (ej. "penalización por pausa como la CFE") estén atendidas
4. Itere basado en feedback en vivo

### Configuración de proveedor LLM para Onyx Lite

Onyx Lite deshabilita vector DB y background workers pero mantiene chat funcional. **Chat requiere un proveedor LLM configurado** con API key válida.

**Distinción crítica: OAuth token vs API key**

| Tipo de token | Ubicación | Se ve como | Funciona con Onyx? |
|---|---|---|---|
| OAuth access token | `auth.json` bajo `"openai": { "type": "oauth", "access": "eyJhb..." }` | JWT (`eyJhbG...`) | ❌ No |
| API key | `platform.openai.com/api-keys` | `sk-...` | ✅ Sí |

Onyx espera un campo `api_key` pasado a `openai.Client(api_key=...)`. Los OAuth tokens de login web ChatGPT son para un sistema de autenticación diferente y **no funcionarán**.

**Configurar proveedor alternativo (ej. NVIDIA):**
```sql
INSERT INTO llm_provider (
    name, provider, api_base, api_key, default_model_name,
    is_default_provider, is_public, is_auto_mode
) VALUES (
    'NVIDIA',
    'openai',
    'https://integrate.api.nvidia.com/v1',
    '<nvidia_api_key>',
    'nvidia/llama-3.1-nemotron-70b-instruct',
    true, true, false
)
ON CONFLICT (name) DO UPDATE SET
    api_key = EXCLUDED.api_key,
    api_base = EXCLUDED.api_base;
```

### Upload de archivos reuse

Onyx ya tiene `/api/user/projects/file/upload` (multipart/form-data, acepta `project_id`). El bridge API puede recibir el archivo, reenviarlo al endpoint nativo de Onyx, y devolver el resultado. Sin storage custom necesario.

---

## Señales de que estás en el camino equivocado

Detenerse y corregir curso si:
- El legal home se está convirtiendo en un dashboard que margina el chat
- La implementación copia layout/estilo de Hermes Workspace dentro de Onyx
- El producto legal ya no se siente como un modo nativo de Onyx
- El sidebar, input bar, y document context se evaden en lugar de reusarse
- Estás describiendo Onyx mientras en realidad construyes un shell custom en otro lado
- Te encuentras escribiendo `from docx import Document` para generar un contrato legal
- El contrato generado es 4x más largo que el borrador existente del cliente

## Señales de que estás en el camino correcto

- La ruta vive dentro de `/app/...` en el codebase real de Onyx
- El sidebar tiene una entrada legal
- El matter workspace centra el flujo de conversación
- Deadlines/desk/memory/output se sienten como extensiones del UX chat de Onyx
- El producto facing lawyers se ve como Onyx Cloud adaptado para trabajo legal
- Todo documento legal pasa por Motor Kami con validación de sustancia
- Los agentes generan el contenido; Kami solo aplica diseño
- Onyx y Hermes pueden operar independientemente

---

---

## PARTE 4: Modo Standalone — Operación Sin Onyx

### Cuándo usar este modo

- Onyx está caído (Docker no responde, contenedores apagados)
- No hay conectividad a PostgreSQL
- Se necesita operar Willow **ahora**, sin depender de infraestructura externa
- Pablo pide "que funcione como Paola Meneses" — es decir: dashboard propio, Excel local, scripts standalone

### Principio: Onyx es aditivo, no requerido

> **Onyx y Hermes deben funcionar cada uno independientemente. Son aditivos, no sustractivos.**

| Capacidad | Onyx (cuando está arriba) | Standalone (cuando Onyx está abajo) |
|---|---|---|
| **Quién inicia** | Usuario en chat Onyx | Pablo vía Telegram/voz |
| **Quién orquesta** | Agentes Onyx + auto-flows | Hermes (Neo) + subagentes |
| **Frontend** | Páginas `/app/legal` en Next.js | SPA HTML en FastAPI (puerto :8081) |
| **Backend** | Bridge API reusa PostgreSQL | FastAPI + Excel + JSON en disco |
| **Base de datos** | PostgreSQL (`willow_legal_*`) | Excel maestro + `matters.json` + `documentos.json` |
| **Generación de documentos** | Agent chat → Document Engine → PDF | Session notes → Motor Kami CLI → PDF |
| **Dónde se almacena** | `user_file` en Onyx + carpeta Windows | Carpeta Windows + sync a Onyx cuando vuelva |
| **Persistencia** | PostgreSQL | JSON en disco (`/root/ws-willow-standalone/datos/`) |
| **Comandos** | Chat UI nativo | `/matter`, `/contrato`, `/plazo`, `/alerta`, `/status` vía Telegram |

### Arquitectura Standalone

```
┌─────────────────────────────────────────────────────────────┐
│                    HERMES NEO (Telegram)                   │
│  ┌─────────────────────────────────────────────────────┐  │
│  │  Skill: willow-legal-standalone                      │  │
│  │  - Comandos: /matter, /contrato, /plazo, /alerta     │  │
│  │  - Orquesta todo el sistema                         │  │
│  └─────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│              WILLOW DASHBOARD (FastAPI + SPA)              │
│                    Puerto :8081                            │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐ │
│  │  Backend    │  │  Frontend   │  │  Motor Documentos   │ │
│  │  FastAPI    │  │  SPA HTML   │  │  Kami v3 (blocks.py)│ │
│  │  + Excel    │  │  (igual que  │  │  23 templates       │ │
│  │  como DB    │  │   Paola)     │  │  PDF output         │ │
│  └─────────────┘  └─────────────┘  └─────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│              PERSISTENCIA LOCAL (Standalone)                 │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────┐  │
│  │  Excel Maestro  │  │  JSON Estado    │  │  Carpetas   │  │
│  │  v4.0 (15 hojas)│  │  matters.json   │  │  Windows    │  │
│  │  - Matters      │  │  alertas.json   │  │  por cliente│  │
│  │  - Contratos    │  │  documentos.json│  │             │  │
│  │  - Plazos       │  │  finanzas.json  │  │             │  │
│  │  - Finanzas     │  │                 │  │             │  │
│  └─────────────────┘  └─────────────────┘  └─────────────┘  │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼ (cuando Onyx está arriba)
┌─────────────────────────────────────────────────────────────┐
│              INTEGRACIÓN ONYX (Opcional)                     │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  - Bridge API reusa datos locales                   │   │
│  │  - Sync bidireccional: Excel ↔ PostgreSQL            │   │
│  │  - Agentes Onyx leen desde API Willow              │   │
│  │  - Documentos suben a user_file de Onyx            │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

### Diagnóstico: ¿Standalone o Integrado?

Ejecutar este checklist al inicio de cada sesión:

```bash
# 1. ¿Onyx responde?
curl -s http://localhost:3000/api/health | head -c 100 || echo "Onyx DOWN"

# 2. ¿Docker está corriendo?
docker ps --format "table {{.Names}}\t{{.Status}}" | grep onyx || echo "Docker sin Onyx"

# 3. ¿PostgreSQL accesible?
docker exec onyx-relational_db-1 psql -U postgres -c "SELECT 1;" 2>/dev/null || echo "PostgreSQL DOWN"

# 4. ¿Bridge API responde?
curl -s http://localhost:8080/health || echo "Bridge API DOWN"
```

| Resultado | Modo recomendado | Acción |
|---|---|---|
| Todo responde | **Integrado** (Onyx + Bridge) | Usar Parte 1-3 de esta skill |
| Onyx/PostgreSQL caído | **Standalone** | Usar Parte 4 de esta skill |
| Solo Bridge caído | **Semi-standalone** | Levantar Bridge API local (puerto 8081) |

### Estructura de archivos Standalone

```
ws-willow-standalone/
├── dashboard/
│   ├── app.py              # FastAPI backend (copiar patrón de Paola)
│   ├── spa/
│   │   └── index.html      # Frontend completo (copiar patrón de Paola)
│   └── ejecutor_kami.py    # Wrapper de Motor Kami
├── motor_kami/             # Copiado de C:\WillowLegal\00_Sistema\Motor_Kami
│   ├── blocks.py
│   ├── templates/
│   └── output/
├── scripts/
│   ├── willow_standalone_bridge.py  # Sin Docker, sin PostgreSQL
│   ├── generar_contrato.py          # Genera contrato desde template
│   ├── generar_carta.py             # Genera carta legal
│   └── sync_excel.py                # Sync Excel ↔ JSON
├── datos/
│   ├── matters.json        # Estado de matters
│   ├── documentos.json     # Tracker de documentos
│   └── alertas.json        # Alertas del sistema
├── docs/
│   └── *.md                # Documentación
├── excel/
│   └── Centro_Operativo_Maestro_Willow_v4.xlsx
└── schemas/
    └── willow_schema.sql   # Schema PostgreSQL (para cuando Onyx vuelva)
```

### Excel Maestro v4.0 — Hojas requeridas

| # | Hoja | Propósito | Patrón Paola |
|---|------|-----------|--------------|
| 1 | Dashboard | Métricas + alertas + navegación | Dashboard |
| 2 | Matters | Tracker con status coloreado, deadline, área | Eventos |
| 3 | Contratos | Versiones con estado (borrador, revisión, firmado) | Cotizaciones |
| 4 | Clientes | Directorio con datos legales completos | Clientes |
| 5 | Plazos | Timeline con deadlines, audiencias, milestones | Timeline |
| 6 | Finanzas | Ingresos/egresos por matter | Finanzas |
| 7 | Facturación | Cotizaciones, facturas, pagos | Pagos |
| 8 | Documentos | Tracker de documentos generados | Documentos |
| 9 | Templates | Catálogo de 23 templates con metadata | Catálogo |
| 10 | Agentes | Estado de 5 agentes legales | Agentes |
| 11 | Checklist | Tareas por fase con dependencias | Checklist |
| 12 | Biblioteca | Precedentes, jurisprudencia, cláusulas | — |
| 13 | Proveedores | Aliados comerciales (notarías, peritos) | Proveedores |
| 14 | Métricas | KPIs automáticos | Métricas |
| 15 | Guía de Uso | Documentación embebida para el usuario | Guía de Uso |

### Backend API Standalone — Endpoints mínimos

| Endpoint | Método | Descripción | Patrón Paola |
|----------|--------|-------------|--------------|
| `/api/health` | GET | Health check | ✅ Igual |
| `/api/dashboard` | GET | KPIs, alertas, matters activos | ✅ Igual |
| `/api/matters` | GET | Lista matters con filtros | `/api/eventos` |
| `/api/matter/{id}` | GET | Detalle completo del matter | `/api/evento/{pao_id}` |
| `/api/matter/{id}/plazos` | GET | Timeline de plazos | Timeline de Paola |
| `/api/matter/{id}/documentos` | GET | Documentos del matter | `/api/cliente/{pao_id}/documentos` |
| `/api/matter/{id}/generar-documento` | POST | Genera PDF con Kami | `/api/cliente/{pao_id}/generar-documento` |
| `/api/matter/{id}/abrir-carpeta` | POST | Abre carpeta en Windows | `/api/cliente/{pao_id}/abrir-carpeta` |
| `/api/matter` | POST | Crear nuevo matter | Crear evento en Paola |
| `/api/matter/{id}/actualizar` | POST | Guarda datos operativos | `/api/evento/{pao_id}/actualizar` |
| `/api/contratos` | GET | Lista contratos | Similar a catálogo |
| `/api/contratos/{key}/generar` | POST | Genera contrato desde template | Generar cotización en Paola |
| `/api/finanzas` | GET | Datos financieros reales | ✅ Igual |
| `/api/alertas` | GET | Alertas accionables | ✅ Igual |
| `/api/templates` | GET | Catálogo de 23 templates | `/api/catalogo/servicios` |
| `/api/agentes/estado` | GET | Estado de 5 agentes legales | ✅ Igual |

### Frontend SPA Standalone — Vistas mínimas

| Vista | Descripción | Patrón Paola |
|-------|-------------|--------------|
| **Dashboard** | KPIs, alertas, matters activos, finanzas ocultas | Dashboard v4.2 de Paola |
| **Calendario/Matters** | Vista lista + mensual de matters y deadlines | Calendario operativo de Paola |
| **Detalle Matter** | Resumen, timeline, documentos, finanzas, edición | Detalle evento de Paola |
| **Contratos** | Selector de template, generar, preview, download | Catálogo de Paola |
| **Agentes** | Estado de 5 agentes, activar, ver prompts | Agentes ejecutores de Paola |
| **Finanzas** | Dashboard oculto con KPIs reales | Finanzas ocultas de Paola |
| **Biblioteca** | Precedentes, templates, cláusulas | — Nuevo para Willow |

### Comandos Telegram Standalone

| Comando | Descripción | Patrón Paola |
|---------|-------------|--------------|
| `/matter [nombre]` | Crear nuevo matter | `/cotizar` |
| `/contrato [template] [matter]` | Generar contrato | `/cotizar` |
| `/plazo [matter] [descripción] [fecha]` | Crear deadline | — Nuevo |
| `/alerta` | Ver alertas del día | `/alertas` |
| `/status [matter]` | Estado del matter | `/status` |
| `/documento [matter] [tipo]` | Generar documento | `/bookdate` |
| `/finanzas` | Dashboard financiero | — Nuevo |
| `/abrir [matter]` | Abrir carpeta en Windows | — Nuevo |

### Script `willow_standalone_bridge.py` — Sin Docker

```python
#!/usr/bin/env python3
"""Willow Standalone Bridge — Sin Docker, sin PostgreSQL.
Usa Excel + JSON como fuente de verdad."""
import json
from pathlib import Path
import openpyxl

EXCEL_PATH = Path("/mnt/c/WillowLegal/02_Administracion/Centro_Operativo_Maestro_Willow_v4.xlsx")
DATOS_DIR = Path("/root/ws-willow-standalone/datos")
CLIENTES_DIR = Path("/mnt/c/WillowLegal/01_Clientes")

def load_matters_from_excel():
    """Carga matters desde Excel maestro (hoja 'Matters')."""
    wb = openpyxl.load_workbook(EXCEL_PATH)
    ws = wb["Matters"]
    matters = []
    for row in ws.iter_rows(min_row=2, values_only=True):
        if not row[0]:
            continue
        matters.append({
            "id": row[0],
            "client_name": row[1] or "",
            "status": row[2] or "Intake",
            "practice_area": row[3] or "Mercantil",
            "deadline": row[4] or None,
            "priority": row[5] or "medium",
            "next_step": row[6] or "Intake inicial pendiente",
            "blocker": row[7] or "none",
        })
    return matters

def save_matters_to_json(matters):
    DATOS_DIR.mkdir(parents=True, exist_ok=True)
    with open(DATOS_DIR / "matters.json", "w", encoding="utf-8") as f:
        json.dump(matters, f, indent=2, ensure_ascii=False)

def create_matter_standalone(client_name, practice_area="Mercantil", deadline=None, priority="medium"):
    """Crea matter + carpeta física. NO requiere Docker ni Onyx."""
    # 1. Agregar a Excel
    wb = openpyxl.load_workbook(EXCEL_PATH)
    ws = wb["Matters"]
    next_row = ws.max_row + 1
    ws.cell(row=next_row, column=1, value=f"WIL-{next_row-1:03d}")
    ws.cell(row=next_row, column=2, value=client_name)
    ws.cell(row=next_row, column=3, value="Intake")
    ws.cell(row=next_row, column=4, value=practice_area)
    ws.cell(row=next_row, column=5, value=deadline)
    ws.cell(row=next_row, column=6, value=priority)
    ws.cell(row=next_row, column=7, value="Intake inicial pendiente")
    ws.cell(row=next_row, column=8, value="none")
    wb.save(EXCEL_PATH)
    
    # 2. Crear carpeta física
    safe = "".join(c for c in client_name if c.isalnum() or c in " _-").strip()
    client_dir = CLIENTES_DIR / safe
    client_dir.mkdir(parents=True, exist_ok=True)
    for sf in ["01_Intake", "02_Contratos/Borradores", "02_Contratos/Firmados", 
               "02_Contratos/Anexos", "03_Correspondencia/Entrante", 
               "03_Correspondencia/Saliente", "04_Litigio/Demandas",
               "04_Litigio/Contestaciones", "04_Litigio/Pruebas", 
               "04_Litigio/Audiencias", "05_Facturacion/Cotizaciones",
               "05_Facturacion/Facturas", "05_Facturacion/Pagos",
               "06_Entregables/Documentos_Finales", "06_Entregables/Presentaciones",
               "06_Entregables/Reportes", "07_Archivo/Cerrado"]:
        (client_dir / sf).mkdir(parents=True, exist_ok=True)
    
    # 3. Guardar en JSON
    matters = load_matters_from_excel()
    save_matters_to_json(matters)
    
    print(f"✅ Matter creado: WIL-{next_row-1:03d} | Cliente: {client_name}")
    print(f"   Carpeta: {client_dir}")
    return f"WIL-{next_row-1:03d}"
```

### Fases de implementación Standalone

| Fase | Objetivo | Tiempo estimado |
|------|----------|-----------------|
| 1 | Fundamentos: workspace, Motor Kami, app.py básico, Excel v4.0 | 1-2 sesiones |
| 2 | Backend API: 15+ endpoints, persistencia JSON | 2-3 sesiones |
| 3 | Frontend SPA: dashboard, calendario, detalle matter, contratos | 2-3 sesiones |
| 4 | Comandos Telegram + Skill | 1 sesión |
| 5 | Integración Onyx opcional (sync bidireccional) | 1-2 sesiones |

### Regla de oro

> **"Todo funciona por separado. Todo funciona junto."**
> 
> — Principio confirmado por Pablo en Paola Meneses, aplicable a Willow.

- Excel maestro = funciona sin internet, sin Onyx, sin BD
- Scripts = funcionan standalone leyendo JSON/YAML
- BD/Onyx = se agrega después, opcional para MVP
- Skill de Hermes = opera cualquiera de los 3 modos (Onyx, standalone, semi)

---

## Señales de que estás en el camino equivocado

Detenerse y corregir curso si:
- El legal home se está convirtiendo en un dashboard que margina el chat
- La implementación copia layout/estilo de Hermes Workspace dentro de Onyx
- El producto legal ya no se siente como un modo nativo de Onyx
- El sidebar, input bar, y document context se evaden en lugar de reusarse
- Estás describiendo Onyx mientras en realidad construyes un shell custom en otro lado
- Te encuentras escribiendo `from docx import Document` para generar un contrato legal
- El contrato generado es 4x más largo que el borrador existente del cliente
- **NUEVO:** Estás forzando a usar Onyx cuando está caído en lugar de activar modo standalone
- **NUEVO:** El bridge `willow_bridge.py` falla porque Docker no responde y no hay fallback

## Señales de que estás en el camino correcto

- La ruta vive dentro de `/app/...` en el codebase real de Onyx (modo integrado)
- **O** el sistema tiene dashboard propio en FastAPI + SPA (modo standalone)
- El sidebar tiene una entrada legal (modo integrado)
- **O** hay navegación por tabs en SPA propia (modo standalone)
- El matter workspace centra el flujo de conversación
- Deadlines/desk/memory/output se sienten como extensiones del UX chat de Onyx
- El producto facing lawyers se ve como Onyx Cloud adaptado para trabajo legal
- Todo documento legal pasa por Motor Kami con validación de sustancia
- Los agentes generan el contenido; Kami solo aplica diseño
- Onyx y Hermes pueden operar independientemente
- **NUEVO:** Cuando Onyx cae, el sistema sigue operando vía Excel + JSON + FastAPI
- **NUEVO:** Cuando Onyx vuelve, los datos se sincronizan sin pérdida

---

## Estructura de archivos consolidada (modo integrado)

```
WillowLegal/
├── 00_Sistema/
│   ├── Motor_Kami/
│   │   ├── blocks.py              # Motor core + validador
│   │   ├── bridge_api.py          # FastAPI (puerto 8080/9100)
│   │   ├── motor_kami.py          # Legacy v2
│   │   ├── templates/             # 23 JSON templates
│   │   │   ├── index.json
│   │   │   ├── prestacion_servicios.json
│   │   │   └── ...
│   │   └── output/                # PDFs generados
│   ├── willow_bridge.py           # Script de sync DB ↔ carpetas (requiere Docker)
│   ├── REGLAS_SUSTANCIA_LEGAL_KAMI.md
│   ├── DOCUMENTACION_TECNICA.md
│   └── DOCUMENTACION_ABOGADOS.md
├── 01_Clientes/
├── 02_Administracion/
├── 03_Biblioteca_Legal/
├── 04_Agentes_Onyx/
└── 05_Backups/
```

## Estructura de archivos consolidada (modo standalone)

```
ws-willow-standalone/              # En /root/ (workspace de Hermes)
├── dashboard/
│   ├── app.py                     # FastAPI backend
│   ├── spa/
│   │   └── index.html             # Frontend completo
│   └── ejecutor_kami.py           # Wrapper de Motor Kami
├── motor_kami/                    # Copiado de C:\WillowLegal\00_Sistema\Motor_Kami
│   ├── blocks.py
│   ├── templates/
│   └── output/
├── scripts/
│   ├── willow_standalone_bridge.py
│   ├── generar_contrato.py
│   ├── generar_carta.py
│   └── sync_excel.py
├── datos/
│   ├── matters.json
│   ├── documentos.json
│   └── alertas.json
├── docs/
│   └── *.md
├── excel/
│   └── Centro_Operativo_Maestro_Willow_v4.xlsx
└── schemas/
    └── willow_schema.sql
```
