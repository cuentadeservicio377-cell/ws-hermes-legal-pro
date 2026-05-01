# WILLOW LEGAL — Plan de Construcción: Sistema Standalone para Firma Legal
## (No es migrar Onyx. Es crear Willow desde cero, pensado para abogados.)

**Fecha:** 30 Abr 2026
**Autor:** Hermes Neo / WS Capital
**Versión:** 1.0 — Pre-aprobación

---

## 🎯 COMPRENSIÓN DEL NEGOCIO REAL

### Willow Legal = We Law S.C.
Una firma legal mexicana que atiende a Pragma Studio (y futuros clientes). El cliente real es **Juan Antonio Angel Ramirez** de Pragma Studio, un estudio de arquitectura para restaurantes.

### Problemas reales documentados (de la Ficha de Matter)
| # | Problema | Impacto | Documento requerido |
|---|----------|---------|---------------------|
| 1 | Contrato de 24 páginas "hostil" | Clientes reacios a firmar | Contrato ligero + Términos y Condiciones |
| 2 | Sin actas de entrega por etapa | Disputas de pago | 3 actas de entrega (conceptual, desarrollo, constructiva) |
| 3 | Sin protocolo de cobranza | Clientes no pagan a tiempo | Protocolo de cobranza + plantillas |
| 4 | Sin cláusula de intereses moratorios | Deuda no genera costo | Contrato con intereses |
| 5 | Sin contrato de subcontratistas | Riesgo propiedad intelectual | Contrato de subcontratación |
| 6 | Disputa activa con "Andy" | $80,000-$200,000 en riesgo | Estrategia de respuesta + correo formal |
| 7 | Sin acta de cierre | Proyectos "colgados" | Acta de cierre |
| 8 | Clientes USA sin mediación | Riesgo litigio internacional | Cláusula ICC/medición |

### Datos del cliente real
- **Cliente:** Pragma Studio (Juan Antonio Angel Ramirez)
- **Email:** juan@pragmaestudio.com
- **Área:** Mercantil / Contratos / Cobranza
- **Matter ID:** PRAG-001
- **Status:** Active, prioridad HIGH
- **Deadline principal:** Entrega paquete legal completo
- **Disputa activa:** Cliente "Andy", $353,080 MXN total, $122,871 anticipo recibido

---

## 🏛️ PRINCIPIOS DE DISEÑO (aprendidos de la operación real)

### 1. Primero la sustancia, luego el diseño
> "Kami no escribe el contrato por ti. Tú escribes el contrato, Kami lo hace ver impecable."

- El abogado es el autor. El sistema es el asistente.
- Validación de sustancia ANTES de generar PDF.
- Sin metáforas, sin cajas didácticas, sin explicaciones en el cuerpo legal.

### 2. Chat-first, no dashboard-first
> El modelo mental del abogado es conversacional. No formularios.

- Telegram = modo rápido (en movimiento, con cliente)
- Dashboard = modo profundo (en oficina, revisando)
- Onyx = modo estructurado (cuando exista)

### 3. Todo funciona por separado. Todo funciona junto.
> Excel maestro = funciona sin internet, sin Onyx, sin BD.

- Standalone primero. Integración después.
- Si cae Onyx, el despacho sigue operando.
- Si cae Hermes, el abogado sigue con su Excel y carpetas.

### 4. Un matter = un cliente = una carpeta
> "Todo cliente nuevo comienza copiando Cliente_Nuevo_1 y renombrando."

- Estructura de carpetas inmutable.
- Documentos finales SIEMPRE en `06_Entregables/Documentos_Finales/`.
- Contratos fluyen: Borrador → Revisión → Firmado.

---

## 🏗️ ARQUITECTURA WILLOW STANDALONE v1.0

```
┌─────────────────────────────────────────────────────────────┐
│                    HERMES NEO (Telegram)                    │
│  ┌─────────────────────────────────────────────────────┐  │
│  │  Skill: willow-legal-standalone                      │  │
│  │  - Comandos por voz/texto para abogados en movimiento│  │
│  │  - "Genera contrato para Pragma" → valida → PDF      │  │
│  │  - "Status de Andy" → resumen del matter             │  │
│  │  - "Alertas de hoy" → deadlines próximos             │  │
│  └─────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│              WILLOW DASHBOARD (FastAPI + SPA)              │
│                    Puerto :8081                            │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐ │
│  │  Backend    │  │  Frontend   │  │  Motor Documentos     │ │
│  │  FastAPI    │  │  SPA HTML   │  │  Kami v3            │ │
│  │  + Excel    │  │  (abogado-  │  │  23 templates       │ │
│  │  como DB    │  │   first)    │  │  Validación sustancia │ │
│  └─────────────┘  └─────────────┘  └─────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│              PERSISTENCIA LOCAL (Standalone)                 │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────┐  │
│  │  Excel Maestro  │  │  JSON Estado    │  │  Carpetas   │  │
│  │  v4.0 (12 hojas)│  │  matters.json   │  │  Windows    │  │
│  │  - Matters      │  │  alertas.json   │  │  por cliente│  │
│  │  - Documentos    │  │  plazos.json    │  │             │  │
│  │  - Plazos       │  │  finanzas.json  │  │             │  │
│  │  - Finanzas     │  │                 │  │             │  │
│  │  - Templates    │  │                 │  │             │  │
│  └─────────────────┘  └─────────────────┘  └─────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

## 📊 MODELO DE DATOS: Matter Legal

```json
{
  "matter_id": "PRAG-001",
  "cliente": {
    "razon_social": "Pragma Studio",
    "representante": "Juan Antonio Angel Ramirez",
    "email": "juan@pragmaestudio.com",
    "rfc": "...",
    "domicilio_fiscal": "...",
    "telefono": "...",
    "sector": "Arquitectura / Restaurantes",
    "tamano": "SME"
  },
  "asunto": {
    "area_practica": "Mercantil / Contratos / Cobranza",
    "tipo": "contrato",
    "descripcion": "Formalizar infraestructura legal de Pragma Studio",
    "status": "active",
    "prioridad": "high",
    "fecha_apertura": "2025-09-29",
    "deadline_principal": "2025-12-15"
  },
  "problemas": [
    {
      "id": 1,
      "descripcion": "Contrato de 24 páginas hostil",
      "impacto": "Fricción en venta",
      "documento_requerido": "Contrato ligero + Términos y Condiciones",
      "status": "pendiente"
    }
  ],
  "documentos": [
    {
      "tipo": "contrato_prestacion_servicios",
      "status": "pendiente",
      "ubicacion": "02_Contratos/Borradores/",
      "fecha_limite": "2025-12-15",
      "template": "prestacion_servicios"
    }
  ],
  "plazos": [
    {
      "descripcion": "Entrega correo respuesta Andy",
      "fecha": "2025-11-05",
      "tipo": "contractual",
      "status": "urgente",
      "dias_restantes": -176
    }
  ],
  "finanzas": {
    "total_proyecto": 353080,
    "anticipo_recibido": 122871,
    "adeudo": 230209,
    "honorarios_will": 0,
    "pagos_recibidos": 0,
    "total_pendiente": 0
  },
  "estrategia": {
    "objetivo": "Formalizar infraestructura legal para prevenir disputas",
    "proximo_paso": "Generar contrato ligero + Términos y Condiciones + Actas",
    "bloqueo_actual": "Disputa Andy requiere respuesta formal inmediata",
    "riesgos": ["Andy podría escalar a litigio", "Futuros clientes sin contrato = más disputas"]
  },
  "historial_sesiones": [
    {
      "fecha": "2025-09-29",
      "tipo": "Design Thinking",
      "contenido": "Mapeo de proceso, metodología, contratos previos"
    }
  ],
  "carpeta_fisica": "C:\\WillowLegal\\01_Clientes\\Pragma Studio",
  "agentes_activos": ["Despacho Legal", "Paralegal de Intake", "Arquitecto Legal", "Coordinador de Plazos"]
}
```

---

## 🗂️ ESTRUCTURA DE CARPETAS (ya existe, se mantiene)

```
C:\WillowLegal\
├── 00_Sistema\              # Scripts, guías, motor Kami
│   ├── Motor_Kami\          # blocks.py, templates/, output/
│   ├── willow_standalone.py # Script principal (NUEVO)
│   ├── Guia_Operativa.md
│   └── Checklist_Apertura_Matter.md
├── 01_Clientes\             # Un folder por cliente/matter
│   └── Pragma Studio\       # Cliente real actual
│       ├── 01_Intake\       # Datos_Cliente.xlsx, Ficha_Matter.md, Checklist_Intake.md
│       ├── 02_Contratos\    # Borradores, Firmados, Anexos
│       ├── 03_Correspondencia\  # Entrante, Saliente
│       ├── 04_Litigio\      # Demandas, Contestaciones, Pruebas, Audiencias
│       ├── 05_Facturacion\  # Cotizaciones, Facturas, Pagos
│       ├── 06_Entregables\  # Documentos_Finales, Presentaciones, Reportes
│       └── 07_Archivo\      # Cerrado
├── 02_Administracion\       # Templates, formatos, manuales, reportes
│   ├── Plantillas\          # 23 templates JSON de Kami
│   ├── Formatos\
│   ├── Manuales\
│   └── Centro_Operativo_Maestro_Willow_v4.xlsx  # (NUEVO)
├── 03_Biblioteca_Legal\     # Precedentes, Jurisprudencia, Doctrina, Cláusulas
├── 04_Agentes_Onyx\         # Fichas de cada agente (mantenido para referencia)
└── 05_Backups\              # Respaldo periódico
```

---

## 📋 FASES DE IMPLEMENTACIÓN

### FASE 1: Fundamentos — "El Motor" (2-3 horas)
**Objetivo:** Crear el workspace y el backend mínimo funcional.

| # | Tarea | Output |
|---|-------|--------|
| 1.1 | Crear `/root/ws-willow-standalone/` | Workspace limpio |
| 1.2 | Copiar Motor Kami v3 (`blocks.py`, `templates/`, `output/`) | Motor documentos funcional |
| 1.3 | Crear `app.py` FastAPI con health check + 5 endpoints | Backend base |
| 1.4 | Crear `spa/index.html` con estructura abogado-first | Frontend base |
| 1.5 | Crear `matters.json` con datos reales de Pragma Studio | Datos iniciales |
| 1.6 | Probar generación de contrato de prueba | Motor Kami verificado |

**Endpoints FASE 1:**
- `GET /api/health` — Health check
- `GET /api/matters` — Lista matters
- `GET /api/matter/{id}` — Detalle del matter
- `POST /api/matter/{id}/generar-documento` — Genera PDF con Kami
- `GET /api/templates` — Lista 23 templates

### FASE 2: Dashboard Operativo — "La Vista del Abogado" (3-4 horas)
**Objetivo:** Frontend completo que un abogado use todos los días.

| # | Tarea | Output |
|---|-------|--------|
| 2.1 | Vista "Matters" — lista con status, prioridad, deadline | Tabla operativa |
| 2.2 | Vista "Detalle Matter" — ficha completa editable | Formularios inline |
| 2.3 | Vista "Documentos" — tracker de 8 documentos de Pragma | Progreso visual |
| 2.4 | Vista "Plazos" — timeline con alertas de colores | Calendario legal |
| 2.5 | Vista "Generar" — selector de template → datos → preview → PDF | Flujo Kami integrado |
| 2.6 | Botón "Abrir Carpeta" — abre `C:\WillowLegal\01_Clientes\{cliente}` | Integración Windows |

**Diseño abogado-first:**
- Colores sobrios: negro editorial `#1a1a18`, pergamino `#faf8f0`, dorado `#d4a574`
- Tipografía serif para títulos (Playfair Display), sans para datos (Inter)
- Layout limpio, sin distracciones. Información legal primero.
- Botones de acción grandes: "Generar Contrato", "Abrir Carpeta", "Marcar Listo"

### FASE 3: Excel Maestro v4.0 — "El Respaldo Tangible" (2 horas)
**Objetivo:** Excel que funcione sin internet, sin Onyx, sin nada.

| Hoja | Contenido | Fórmulas |
|------|-----------|----------|
| Dashboard | Métricas + alertas + navegación | `=COUNTIF()`, `=HOY()` |
| Matters | Tracker con status coloreado | Validación dropdown |
| Documentos | Tracker de 8 docs de Pragma | Colores condicionales |
| Plazos | Deadlines con días restantes | `=FECHA-HOY()` |
| Finanzas | Ingresos/egresos por matter | `=SUMPRODUCT()` |
| Clientes | Directorio con datos legales | — |
| Templates | Catálogo 23 templates | — |
| Agentes | Estado 5 agentes | — |
| Disputas | Tracker de disputas activas | — |
| Biblioteca | Precedentes y cláusulas | — |
| Facturación | Cotizaciones, facturas, pagos | — |
| Guía de Uso | Documentación embebida | — |

### FASE 4: Comandos Telegram — "El Abogado en Movimiento" (2 horas)
**Objetivo:** Operar Willow desde Telegram, por voz, en cualquier lado.

| Comando | Ejemplo | Qué hace |
|---------|---------|----------|
| `/matter` | `/matter "Nuevo Cliente SA"` | Crea matter + carpeta + Excel |
| `/contrato` | `/contrato prestacion_servicios PRAG-001` | Genera contrato con datos del matter |
| `/plazo` | `/plazo PRAG-001 "Respuesta Andy" 2025-11-05` | Crea deadline |
| `/alerta` | `/alerta` | Muestra deadlines próximos y urgentes |
| `/status` | `/status PRAG-001` | Resumen del matter |
| `/documento` | `/documento PRAG-001 acta_entrega` | Genera documento específico |
| `/validar` | `/validar [pega texto de contrato]` | Valida sustancia legal |
| `/abrir` | `/abrir PRAG-001` | Abre carpeta del cliente en Windows |

### FASE 5: Integración Onyx (cuando exista) — "La Capa Adicional" (futuro)
**Objetivo:** Cuando Onyx esté arriba, sincronizar sin romper standalone.

| Función | Descripción |
|---------|-------------|
| Sync bidireccional | Excel ↔ PostgreSQL (matters, documentos, plazos) |
| Agentes Onyx | Los 5 agentes legales leen desde API Willow |
| Documentos Onyx | PDFs suben a `user_file` de Onyx |
| Bridge API v2 | Reusa datos locales, no requiere Onyx para funcionar |

---

## 🎨 DISEÑO VISUAL: Identidad Willow Legal

### Paleta (del sistema Kami v3)
- **Primary:** `#1a1a18` — Negro editorial (NO azul corporativo)
- **Background:** `#faf8f0` — Pergamino cálido
- **Secondary:** `#3d3d3a` — Gris oscuro
- **Metadata:** `#9a9a96` — Gris medio
- **Accent:** `#8B0000` — Rojo vino (solo para penalizaciones/urgencias)
- **Gold:** `#d4a574` — Dorado sobrio (acento principal)

### Tipografía
- **Títulos:** Playfair Display (serif, 400-800)
- **Datos/tablas:** Inter (sans, 400-700)

### Elementos visuales
- Partes: borde izquierdo 3pt sólido negro + indentación
- Cláusulas: numeral grande + título subrayado
- Tablas: borde exterior 1pt, header negro, fondos alternados
- Firmas: grilla 2×2 con bordes, línea gruesa
- Alertas: badge de color según urgencia (verde/naranja/rojo)

---

## ✅ CHECKLIST DE ÉXITO

Al terminar FASE 4, el sistema debe poder:

- [ ] Crear un matter nuevo desde Telegram → crea carpeta + Excel + JSON
- [ ] Generar un contrato de prestación de servicios → valida sustancia → PDF en carpeta
- [ ] Ver status de Pragma Studio → deadlines, documentos pendientes, disputa Andy
- [ ] Abrir carpeta de Pragma Studio desde Telegram → se abre en Windows
- [ ] Dashboard en :8081 muestra matters, documentos, plazos, finanzas
- [ ] Excel maestro v4.0 funciona offline con datos reales
- [ ] Todo funciona SIN Onyx, SIN Docker, SIN PostgreSQL
- [ ] Cuando Onyx esté arriba, se sincroniza opcionalmente

---

## 🚀 PRÓXIMA ACCIÓN

**¿Arrancamos FASE 1 ahora?**

1. Crear workspace `/root/ws-willow-standalone/`
2. Copiar Motor Kami
3. Crear `app.py` con 5 endpoints
4. Crear `spa/index.html` base
5. Crear `matters.json` con datos reales de Pragma

**Tiempo estimado:** 2-3 horas de trabajo intenso.

¿Sí?
