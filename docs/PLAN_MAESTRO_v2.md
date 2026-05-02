# PLAN MAESTRO: Hermes Legal Pro v2 — Integración Paperclip + Motor Kami

> **Fecha:** 2026-05-01
> **Repo:** cuentadeservicio377-cell/ws-hermes-legal-pro
> **Arquitecto:** Hermes Neo
> **Ejecutor:** OpenCode Go en Mac de Pablo

---

## 🎯 OBJETIVO

Fusionar el **conocimiento operativo jurídico** de Willow Paperclip (agentes, triggers, flujos) con el **Motor Kami funcional** de Hermes Legal Pro para crear un producto legal completo y usable.

---

## 📦 ESTADO ACTUAL DEL REPO

### ✅ Lo que ya funciona (NO tocar)
| Componente | Estado | Archivos |
|---|---|---|
| Motor Kami v3 | ✅ Funcional | `motor_kami/blocks.py`, `motor_kami.py`, `bridge_api.py` |
| 23 Templates JSON | ✅ Con estructura de bloques | `motor_kami/templates/*.json` |
| Validador de sustancia | ✅ 13 elementos | `blocks.py` líneas 60-200 |
| Generador PDF | ✅ WeasyPrint | `motor_kami.py` |
| Dashboard v6 | ✅ 6 fases completas | `dashboard/backend/app.py` + frontend |
| Excel maestro v4 | ✅ 15 hojas | `excel/Centro_Operativo_Maestro_Willow_v4.xlsx` |
| Calendario | ✅ Mensual/semanal | Fase 6 implementada |
| Gestión documentos | ✅ Wizard + preview | Fase 5 implementada |

### ❌ Lo que falta (copiar de Paperclip)
| Componente | Origen | Destino en repo |
|---|---|---|
| Agentes legales (3) | `willow-paperclip/company/workspace/agents/` | `agents/despacho.md`, `intake.md`, `admin.md` |
| Triggers (13) | `willow-paperclip/company/workspace/triggers/` | `config/triggers.json` |
| Catálogo templates | `willow-paperclip/company/workspace/library/` | `motor_kami/templates/index.json` (merge) |
| Flujos de aprobación | `willow-paperclip/app/ui/ApprovalBubble.tsx` | Documentación en `docs/` |
| Estructura carpetas | `willow-paperclip/company/workspace/agents/despacho.md` | `docs/ESTRUCTURA_CARPETAS.md` |

---

## 🏗️ ARQUITECTURA OBJETIVO

```
ws-hermes-legal-pro/
├── README.md                          # Producto completo
├── INSTALL.md                         # Guía instalación Mac
├── actualizar.sh                      # Script de actualización
│
├── agents/                            # NUEVO: Desde Paperclip
│   ├── despacho.md                    # Orquestador principal
│   ├── intake.md                      # Recepcionista
│   └── admin.md                       # Administrador
│
├── config/                            # EXISTENTE + NUEVO
│   ├── .env.template                  # Variables de entorno
│   └── triggers.json                  # NUEVO: 13 triggers de Paperclip
│
├── dashboard/                         # EXISTENTE (funcional)
│   ├── backend/
│   │   └── app.py                     # FastAPI (21KB, funcional)
│   └── frontend/                      # SPA completa (6 fases)
│
├── motor_kami/                        # EXISTENTE (funcional)
│   ├── blocks.py                      # Validador + bloques (29KB)
│   ├── motor_kami.py                  # Generador PDF
│   ├── bridge_api.py                  # API FastAPI motor
│   ├── templates/                     # 23 templates JSON
│   └── output/                        # PDFs generados
│
├── datos/                             # EXISTENTE
│   └── matters.json                   # Estado de matters
│
├── docs/                              # EXISTENTE + NUEVO
│   ├── MANUAL_ABOGADO_COMPLETO.md     # Guía usuario
│   ├── PLAN_CONSTRUCCION.md           # Este plan
│   ├── PROMPT_FASE_*.md               # Prompts ejecutables
│   └── ESTRUCTURA_CARPETAS.md         # NUEVO: Desde Paperclip
│
├── excel/                             # EXISTENTE
│   └── Centro_Operativo_Maestro_Willow_v4.xlsx
│
├── scripts/                           # EXISTENTE
│   └── willow_standalone.py           # Orquestador
│
└── skills/                            # EXISTENTE
    ├── hermes-legal-pro/
    └── willow-legal-complete/
```

---

## 📋 TAREAS PARA OPENCODE GO

### TAREA 1: Copiar assets de Paperclip (30 min)

**Input:** Repo `willow-paperclip-portable` clonado localmente
**Output:** Archivos copiados al repo `ws-hermes-legal-pro`

```bash
# 1. Crear directorio agents/
mkdir -p agents/

# 2. Copiar agentes
cp willow-paperclip/company/workspace/agents/despacho.md agents/
cp willow-paperclip/company/workspace/agents/intake.md agents/
cp willow-paperclip/company/workspace/agents/admin.md agents/

# 3. Copiar triggers
cp willow-paperclip/company/workspace/triggers/willow-triggers.json config/triggers.json

# 4. Documentar estructura de carpetas
grep -A 20 "Regla de carpeta fuente" agents/despacho.md > docs/ESTRUCTURA_CARPETAS.md
```

**Verificación:**
```bash
test -f agents/despacho.md && echo "✅ despacho.md"
test -f agents/intake.md && echo "✅ intake.md"
test -f agents/admin.md && echo "✅ admin.md"
test -f config/triggers.json && echo "✅ triggers.json"
```

---

### TAREA 2: Merge catálogo templates (30 min)

**Input:** 
- `motor_kami/templates/index.json` (catálogo actual)
- `willow-paperclip/company/workspace/library/willow-template-library.json` (catálogo Paperclip)

**Output:** `motor_kami/templates/index.json` actualizado con metadata completa

**Acción:**
```python
# Leer ambos catálogos
# Para cada template en motor_kami:
#   - Si existe en Paperclip, mergear: area, materia, descripcion
#   - Si no existe en Paperclip, mantener como está
# Guardar index.json merged
```

**Verificación:**
```bash
python3 -c "import json; d=json.load(open('motor_kami/templates/index.json')); print(f'{len(d[\"templates\"])} templates con metadata completa')"
```

---

### TAREA 3: Actualizar README con funcionalidades reales (20 min)

**Input:** README actual + conocimiento de Paperclip
**Output:** README.md v2 que refleje todo lo que hace el producto

**Secciones a agregar:**
- Agentes legales (3) con descripción de roles
- Triggers (13) con ejemplos
- Flujo de aprobaciones
- Estructura de carpetas Drive

---

### TAREA 4: Crear script de instalación unificado (30 min)

**Input:** `installer/install-mac.sh` + `actualizar.sh`
**Output:** `install.sh` unificado que:
1. Verifica Python 3.11+
2. Instala dependencias: `weasyprint`, `fastapi`, `uvicorn`
3. Crea estructura de carpetas en `~/WillowLegal/`
4. Copia templates y motor
5. Inicia dashboard en puerto 8082

**Verificación:**
```bash
./install.sh --dry-run  # Verificar sin ejecutar
```

---

### TAREA 5: Test end-to-end de generación de documento (20 min)

**Input:** Motor Kami + templates
**Output:** PDF generado correctamente

```bash
# Test de generación
cd motor_kami
python3 motor_kami.py --template prestacion_servicios --test

# Verificar PDF generado
ls -la output/test_*.pdf
```

**Verificación:**
```bash
test -f output/test_prestacion_servicios.pdf && echo "✅ PDF generado"
```

---

## ✅ CRITERIOS DE ACEPTACIÓN

Antes de declarar "listo", verificar:

```bash
# 1. Estructura completa
[ -d agents ] && [ -f agents/despacho.md ] && echo "✅ Agentes"
[ -f config/triggers.json ] && echo "✅ Triggers"
[ -d motor_kami/templates ] && [ $(ls motor_kami/templates/*.json | wc -l) -eq 23 ] && echo "✅ 23 templates"
[ -f motor_kami/blocks.py ] && echo "✅ Motor Kami"
[ -f dashboard/backend/app.py ] && echo "✅ Dashboard backend"

# 2. Motor funcional
python3 motor_kami/motor_kami.py --template nda --test && echo "✅ Motor genera PDF"

# 3. Dashboard responde
curl -s http://localhost:8082/api/health | grep "ok" && echo "✅ Dashboard online"

# 4. Git limpio
git status --short | wc -l | grep "^0$" && echo "✅ Todo commiteado"
```

---

## 🚀 FLUJO DE TRABAJO CON OPENCODE GO

```
1. Hermes Neo crea plan (este archivo)
   ↓
2. Hermes Neo sube a GitHub como issue/PR
   ↓
3. OpenCode Go lee plan en Mac de Pablo
   ↓
4. OpenCode Go ejecuta tareas 1-5
   ↓
5. Hermes Neo revisa resultado
   ↓
6. Si hay errores → Hermes Neo corrige plan → OpenCode Go reejecuta
   ↓
7. Cuando pasa criterios → Pablo prueba en su Mac
```

---

## 📝 NOTAS PARA OPENCODE GO

**Reglas críticas:**
1. **NO modificar** `motor_kami/blocks.py`, `motor_kami.py`, `bridge_api.py` — ya funcionan
2. **NO modificar** `dashboard/backend/app.py` — a menos que sea para integrar endpoints del motor
3. **SÍ copiar** archivos de Paperclip tal cual — son conocimiento jurídico puro
4. **SÍ mergear** catálogos de templates — mantener ambas fuentes
5. **SÍ verificar** con tests después de cada tarea

**Si algo falla:**
- Documentar error en `docs/ERRORES.md`
- No continuar a siguiente tarea hasta resolver
- Pedir ayuda a Hermes Neo vía comentario en el issue

---

## 🎯 RESULTADO ESPERADO

Al final de este plan, el repo contendrá:
- ✅ Motor Kami funcional (existente)
- ✅ Dashboard v6 funcional (existente)
- ✅ 3 agentes legales con roles definidos (nuevo desde Paperclip)
- ✅ 13 triggers con formatos de entrada (nuevo desde Paperclip)
- ✅ 23 templates con metadata completa (merged)
- ✅ Documentación de estructura de carpetas (nuevo)
- ✅ Script de instalación unificado (nuevo)
- ✅ README actualizado con funcionalidades reales

**El producto será:** Un sistema operativo legal completo que puede:
1. Recibir asuntos via triggers estructurados
2. Operar con agentes especializados (despacho, intake, admin)
3. Generar documentos legales con Motor Kami
4. Gestionar matters, plazos, reuniones, calendario
5. Integrar con Drive y carpetas locales

---

**Creado por:** Hermes Neo
**Fecha:** 2026-05-01
**Versión plan:** 1.0
**Estado:** Listo para ejecutar
