# PLAN MAESTRO v3: Hermes Legal Pro — Dual Mode
# Dashboard Local + Hermes Agent (Telegram)

> **Fecha:** 2026-05-01
> **Repo:** cuentadeservicio377-cell/ws-hermes-legal-pro
> **Filosofía:** "Todo funciona por separado. Todo funciona junto."

---

## 🎯 VISIÓN DUAL

Hermes Legal Pro debe operar en **dos modos simultáneos**:

### Modo 1: Hermes Agent (Telegram/Voz)
- Pablo habla con Hermes Neo vía Telegram
- Hermes orquesta agentes, genera documentos, gestiona asuntos
- **Ventaja:** Natural, conversacional, accesible desde cualquier lado

### Modo 2: Dashboard Local (Mac)
- Abre navegador en `localhost:8082`
- Ve matters, calendario, documentos, finanzas
- **Ventaja:** Visual, estructurado, self-service para el equipo

**Regla de oro:** Ambos modos comparten la MISMA base de datos, MISMOS templates, MISMO Motor Kami. No son sistemas separados.

---

## 🏗️ ARQUITECTURA DUAL

```
┌─────────────────────────────────────────────────────────────┐
│                    HERMES LEGAL PRO v3                        │
│                                                              │
│  ┌─────────────────────┐    ┌─────────────────────────────┐ │
│  │   MODO 1: HERMES    │    │    MODO 2: DASHBOARD        │ │
│  │   (Telegram/Voz)    │    │    (Mac Localhost)          │ │
│  │                     │    │                             │ │
│  │  Pablo → Telegram   │    │  Navegador → localhost:8082 │ │
│  │       ↓             │    │       ↓                     │ │
│  │  Hermes Neo         │    │  SPA React/Vanilla          │ │
│  │       ↓             │    │       ↓                     │ │
│  │  Skill: willow-     │    │  FastAPI Backend            │ │
│  │  legal-complete     │    │       ↓                     │ │
│  │       ↓             │    │  Motor Kami API             │ │
│  │  Comandos:          │    │       ↓                     │ │
│  │  /matter, /contrato │    │  PDF + Excel                │ │
│  │  /plazo, /status    │    │                             │ │
│  └──────────┬──────────┘    └─────────────┬───────────────┘ │
│             │                              │                 │
│             └──────────────┬───────────────┘                 │
│                            ▼                                │
│              ┌─────────────────────────┐                     │
│              │     CAPA COMPARTIDA     │                     │
│              │                         │                     │
│              │  • Motor Kami (PDF)     │                     │
│              │  • 23 Templates JSON    │                     │
│              │  • Excel Maestro v4     │                     │
│              │  • Agentes (3)          │                     │
│              │  • Triggers (13)        │                     │
│              │  • datos/matters.json   │                     │
│              │  • Carpetas Windows/Mac │                     │
│              └─────────────────────────┘                     │
│                            ▼                                │
│              ┌─────────────────────────┐                     │
│              │   PERSISTENCIA LOCAL    │                     │
│              │                         │                     │
│              │  ~/WillowLegal/         │                     │
│              │  ├── 00_Sistema/        │                     │
│              │  ├── 01_Clientes/       │                     │
│              │  ├── 02_Administracion/ │                     │
│              │  └── 03_Biblioteca/     │                     │
│              └─────────────────────────┘                     │
└─────────────────────────────────────────────────────────────┘
```

---

## 📦 ESTRUCTURA DE REPO DUAL

```
ws-hermes-legal-pro/
│
├── README.md                          # Producto dual
├── INSTALL.md                         # Instalación Mac
├── actualizar.sh                      # Update script
│
├── agents/                            # 🤖 NUEVO: Para Hermes + Dashboard
│   ├── despacho.md                    # Orquestador (ambos modos)
│   ├── intake.md                      # Recepcionista (ambos modos)
│   └── admin.md                       # Administrador (ambos modos)
│
├── config/
│   ├── .env.template                  # Variables entorno
│   ├── triggers.json                  # 🎯 13 triggers (ambos modos)
│   └── hermes-commands.json           # 🆕 Comandos Telegram
│
├── dashboard/                         # 💻 Modo 2: Dashboard
│   ├── backend/
│   │   └── app.py                     # FastAPI (21KB)
│   └── frontend/                      # SPA 6 fases
│
├── motor_kami/                        # ⚙️  Capa compartida
│   ├── blocks.py                      # Validador + bloques
│   ├── motor_kami.py                  # Generador PDF
│   ├── bridge_api.py                  # API FastAPI
│   ├── templates/                     # 23 templates JSON
│   └── output/                        # PDFs generados
│
├── hermes_integration/                # 🆕 NUEVO: Modo 1
│   ├── commands.py                    # Parser comandos Telegram
│   ├── session_manager.py             # Gestión sesiones Hermes
│   ├── matter_bridge.py               # Bridge Hermes ↔ datos/
│   └── templates/                     # Prompts para agentes
│       ├── generar_contrato.txt
│       ├── crear_matter.txt
│       └── status_matter.txt
│
├── datos/                             # 💾 Persistencia compartida
│   ├── matters.json                   # Estado matters
│   ├── documentos.json              # Tracker documentos
│   └── alertas.json                 # Alertas sistema
│
├── excel/
│   └── Centro_Operativo_Maestro_Willow_v4.xlsx
│
├── scripts/
│   ├── willow_standalone.py           # Orquestador standalone
│   └── hermes_bridge.py               # 🆕 Bridge Hermes ↔ Motor
│
└── docs/
    ├── MANUAL_ABOGADO_COMPLETO.md     # Guía usuario
    ├── MANUAL_HERMES_INTEGRATION.md   # 🆕 Guía modo Hermes
    ├── PLAN_MAESTRO_v3.md             # Este plan
    └── ESTRUCTURA_CARPETAS.md         # Desde Paperclip
```

---

## 🤖 MODO 1: HERMES AGENT (Telegram)

### Comandos Telegram

| Comando | Acción | Equivalente Dashboard |
|---------|--------|----------------------|
| `/matter nuevo [nombre]` | Crear matter | Botón "Nuevo Matter" |
| `/matter list` | Listar matters | Tab "Matters" |
| `/matter [id]` | Ver detalle matter | Click en matter |
| `/contrato [template] [matter]` | Generar contrato | Wizard documentos |
| `/plazo [matter] [desc] [fecha]` | Crear deadline | Tab "Plazos" |
| `/alerta` | Ver alertas | Dashboard KPIs |
| `/status` | Estado despacho | Dashboard general |
| `/reunion [matter]` | Registrar reunión | Tab "Reuniones" |
| `/documento [matter] [tipo]` | Generar documento | Wizard documentos |
| `/calendario` | Ver calendario | Tab "Calendario" |
| `/abrir [matter]` | Abrir carpeta | Botón "Abrir carpeta" |

### Flujo típico por Telegram

```
Pablo: /matter nuevo "Innovatech Digital"

Hermes:
✅ Matter creado: WIL-007
📁 Carpeta: ~/WillowLegal/01_Clientes/Innovatech_Digital/
📋 Next step: Intake inicial

Pablo: /contrato prestacion_servicios WIL-007

Hermes:
📝 Generando contrato...
✅ Contrato generado: Contrato_WIL-007_prestacion_servicios.pdf
📄 Preview: [link localhost]
📁 Guardado en: 06_Entregables/Documentos_Finales/

Pablo: /plazo WIL-007 "Enviar borrador a cliente" 2026-05-15

Hermes:
📅 Plazo creado: 2026-05-15
⏰ Alerta: 3 días antes
📊 Dashboard actualizado
```

### Integración técnica

```python
# hermes_integration/commands.py

class HermesLegalCommands:
    """Parser de comandos Telegram para operación legal."""
    
    def __init__(self, data_dir="~/WillowLegal"):
        self.data_dir = Path(data_dir).expanduser()
        self.motor = MotorKamiBridge()
        self.datos = DatosManager(self.data_dir / "datos")
    
    def handle_matter(self, args: list) -> dict:
        """Crear o listar matters."""
        if args[0] == "nuevo":
            return self.crear_matter(" ".join(args[1:]))
        elif args[0] == "list":
            return self.listar_matters()
        else:
            return self.ver_matter(args[0])
    
    def handle_contrato(self, args: list) -> dict:
        """Generar contrato via Motor Kami."""
        template = args[0]
        matter_id = args[1] if len(args) > 1 else None
        return self.generar_documento(template, matter_id)
    
    def handle_plazo(self, args: list) -> dict:
        """Crear plazo con alerta."""
        matter_id = args[0]
        descripcion = args[1]
        fecha = args[2]
        return self.crear_plazo(matter_id, descripcion, fecha)
```

---

## 💻 MODO 2: DASHBOARD (Mac Local)

### Funcionalidades existentes (ya funcionan)
- ✅ Fase 1: Dashboard general con KPIs
- ✅ Fase 2: Calendario mensual/semanal
- ✅ Fase 3: Matters CRUD completo
- ✅ Fase 4: Reuniones registro y procesamiento
- ✅ Fase 5: Documentos wizard + preview + descarga
- ✅ Fase 6: Calendario con plazos y eventos

### Mejoras para modo dual
1. **Botón "Enviar a Telegram"** en cada matter/documento
2. **Notificaciones** cuando Hermes genera algo via Telegram
3. **Sync bidireccional** de datos entre modos

---

## 🔧 TAREAS PARA OPENCODE GO (v3)

### TAREA 1: Copiar assets Paperclip (igual que v2)
- Copiar `agents/` (despacho, intake, admin)
- Copiar `config/triggers.json`
- Documentar estructura carpetas

### TAREA 2: Crear integración Hermes (NUEVO)
```bash
mkdir -p hermes_integration/
mkdir -p hermes_integration/templates/

# Crear commands.py
cat > hermes_integration/commands.py << 'PYEOF'
#!/usr/bin/env python3
"""Hermes Legal Commands — Parser de comandos Telegram."""

from pathlib import Path
import json
from datetime import datetime

class HermesLegalCommands:
    def __init__(self, base_dir="~/WillowLegal"):
        self.base_dir = Path(base_dir).expanduser()
        self.datos_dir = self.base_dir / "datos"
        self.datos_dir.mkdir(parents=True, exist_ok=True)
    
    def crear_matter(self, nombre: str, **kwargs) -> dict:
        """Crear nuevo matter desde Telegram."""
        matters_file = self.datos_dir / "matters.json"
        matters = json.load(open(matters_file)) if matters_file.exists() else []
        
        matter_id = f"WIL-{len(matters)+1:03d}"
        matter = {
            "id": matter_id,
            "nombre": nombre,
            "cliente": kwargs.get("cliente", nombre),
            "estado": "Intake",
            "area": kwargs.get("area", "Mercantil"),
            "prioridad": kwargs.get("prioridad", "media"),
            "creado": datetime.now().isoformat(),
            "next_step": "Intake inicial pendiente",
            "carpeta": str(self.base_dir / "01_Clientes" / nombre.replace(" ", "_"))
        }
        matters.append(matter)
        json.dump(matters, open(matters_file, "w"), indent=2, ensure_ascii=False)
        
        # Crear carpeta
        Path(matter["carpeta"]).mkdir(parents=True, exist_ok=True)
        
        return {
            "status": "ok",
            "matter_id": matter_id,
            "mensaje": f"✅ Matter creado: {matter_id}\n📁 Carpeta: {matter['carpeta']}"
        }
    
    def listar_matters(self) -> dict:
        """Listar matters para mostrar en Telegram."""
        matters_file = self.datos_dir / "matters.json"
        matters = json.load(open(matters_file)) if matters_file.exists() else []
        
        lines = ["📋 MATTERS ACTIVOS:"]
        for m in matters[-10:]:  # Últimos 10
            lines.append(f"  {m['id']}: {m['nombre']} ({m['estado']})")
        
        return {"status": "ok", "mensaje": "\n".join(lines)}
    
    def generar_documento(self, template: str, matter_id: str = None) -> dict:
        """Generar documento via Motor Kami."""
        # Llamar a motor_kami.py via subprocess
        import subprocess
        result = subprocess.run(
            ["python3", "motor_kami/motor_kami.py", "--template", template, "--matter", matter_id or ""],
            capture_output=True, text=True
        )
        
        if result.returncode == 0:
            return {
                "status": "ok",
                "mensaje": f"📝 Documento generado:\n{result.stdout}"
            }
        else:
            return {
                "status": "error",
                "mensaje": f"❌ Error: {result.stderr}"
            }
PYEOF

# Crear session_manager.py
cat > hermes_integration/session_manager.py << 'PYEOF'
#!/usr/bin/env python3
"""Session Manager — Gestión de contexto entre Hermes y Legal."""

import json
from pathlib import Path
from datetime import datetime

class LegalSessionManager:
    """Mantiene contexto de sesión legal activa."""
    
    def __init__(self, session_file="~/.hermes/legal_session.json"):
        self.session_file = Path(session_file).expanduser()
        self.session = self._load()
    
    def _load(self) -> dict:
        if self.session_file.exists():
            return json.load(open(self.session_file))
        return {"matter_active": None, "historial": []}
    
    def set_matter(self, matter_id: str):
        """Fijar matter activo para comandos subsiguientes."""
        self.session["matter_active"] = matter_id
        self.session["historial"].append({
            "accion": "set_matter",
            "matter_id": matter_id,
            "timestamp": datetime.now().isoformat()
        })
        self._save()
    
    def get_matter(self) -> str:
        """Obtener matter activo actual."""
        return self.session.get("matter_active")
    
    def _save(self):
        self.session_file.parent.mkdir(parents=True, exist_ok=True)
        json.dump(self.session, open(self.session_file, "w"), indent=2)
PYEOF

# Crear hermes_bridge.py en scripts/
cat > scripts/hermes_bridge.py << 'PYEOF'
#!/usr/bin/env python3
"""Hermes Bridge — Conexión entre Hermes Agent y Motor Kami."""

import sys
from pathlib import Path

# Añadir motor_kami al path
sys.path.insert(0, str(Path(__file__).parent.parent / "motor_kami"))

from hermes_integration.commands import HermesLegalCommands
from hermes_integration.session_manager import LegalSessionManager

def main():
    """Entry point para comandos desde Hermes."""
    if len(sys.argv) < 2:
        print("Uso: hermes_bridge.py <comando> [args...]")
        sys.exit(1)
    
    cmd = sys.argv[1]
    args = sys.argv[2:]
    
    commands = HermesLegalCommands()
    session = LegalSessionManager()
    
    if cmd == "matter":
        if args[0] == "nuevo":
            result = commands.crear_matter(" ".join(args[1:]))
            if result["status"] == "ok":
                session.set_matter(result["matter_id"])
            print(result["mensaje"])
        elif args[0] == "list":
            result = commands.listar_matters()
            print(result["mensaje"])
    
    elif cmd == "contrato":
        template = args[0]
        matter_id = args[1] if len(args) > 1 else session.get_matter()
        result = commands.generar_documento(template, matter_id)
        print(result["mensaje"])
    
    elif cmd == "status":
        result = commands.listar_matters()
        print(result["mensaje"])
    
    else:
        print(f"Comando desconocido: {cmd}")
        print("Comandos: matter, contrato, status")

if __name__ == "__main__":
    main()
PYEOF

chmod +x scripts/hermes_bridge.py
```

### TAREA 3: Crear config/hermes-commands.json
```json
{
  "version": "1.0",
  "prefix": "/",
  "commands": {
    "matter": {
      "description": "Gestionar matters",
      "subcommands": ["nuevo", "list", "ver"],
      "examples": ["/matter nuevo Innovatech", "/matter list"]
    },
    "contrato": {
      "description": "Generar documento legal",
      "args": ["template", "matter_id"],
      "examples": ["/contrato nda WIL-001", "/contrato prestacion_servicios"]
    },
    "plazo": {
      "description": "Crear deadline",
      "args": ["matter_id", "descripcion", "fecha"],
      "examples": ["/plazo WIL-001 'Enviar borrador' 2026-05-15"]
    },
    "alerta": {
      "description": "Ver alertas del sistema",
      "examples": ["/alerta"]
    },
    "status": {
      "description": "Estado general del despacho",
      "examples": ["/status"]
    },
    "abrir": {
      "description": "Abrir carpeta del matter",
      "args": ["matter_id"],
      "examples": ["/abrir WIL-001"]
    }
  }
}
```

### TAREA 4: Actualizar README dual
Agregar sección:
```markdown
## 🤖 Modo Hermes Agent (Telegram)

Opera el despacho via Telegram con comandos naturales:

```bash
/matter nuevo "Cliente S.A."        # Crear matter
/contrato nda WIL-001               # Generar NDA
/plazo WIL-001 "Audiencia" 2026-05-20  # Crear deadline
/status                              # Ver estado despacho
```

**Ventajas:**
- 🎤 Voz a texto (Whisper)
- 📱 Desde cualquier lugar
- 🤖 Hermes orquesta agentes automáticamente
- 📊 Sync con Dashboard en tiempo real

## 💻 Modo Dashboard (Mac Local)

Abre navegador en `http://localhost:8082`:
- 📊 Dashboard con KPIs
- 📅 Calendario mensual/semanal
- 📁 Matters con documentos
- 📝 Wizard de generación de documentos
- 📈 Reportes y finanzas

**Ventajas:**
- 👁️ Visual y estructurado
- 📑 Drag & drop de archivos
- 🖨️ Preview y print directo
- 📊 Excel maestro integrado
```

### TAREA 5: Test dual end-to-end
```bash
# Test 1: Hermes mode
python3 scripts/hermes_bridge.py matter nuevo "Test_Client"
# Debe crear matter + carpeta

# Test 2: Dashboard mode
curl http://localhost:8082/api/health
# Debe responder "ok"

# Test 3: Sync
# Verificar que matter creado por Hermes aparece en datos/matters.json
# y es visible en Dashboard
```

---

## ✅ CRITERIOS DE ÉXITO DUAL

```bash
cd ~/ws-hermes-legal-pro

echo "=== MODO HERMES ==="
python3 scripts/hermes_bridge.py matter nuevo "Test_Dual" && echo "✅ Hermes mode funciona"

echo "=== MODO DASHBOARD ==="
curl -s http://localhost:8082/api/health | grep "ok" && echo "✅ Dashboard funciona"

echo "=== SYNC ==="
grep -q "Test_Dual" datos/matters.json && echo "✅ Datos compartidos"

echo "=== ESTRUCTURA ==="
[ -d hermes_integration ] && [ -f hermes_integration/commands.py ] && echo "✅ Integración Hermes"
[ -f config/hermes-commands.json ] && echo "✅ Comandos configurados"

echo ""
echo "🎉 HERMES LEGAL PRO v3 DUAL LISTO"
```

---

## 🎯 RESULTADO ESPERADO

Producto que funciona en **ambos modos simultáneamente**:

| Escenario | Modo | Ejemplo |
|-----------|------|---------|
| Pablo en el coche | Hermes Telegram | "Crea matter para Innovatech" |
| Pablo en la oficina | Dashboard | Click en "Nuevo Matter", formulario |
| Paola necesita contrato | Hermes Telegram | "/contrato nda WIL-005" |
| Revisión de documentos | Dashboard | Preview PDF, click firmar |
| Alerta de plazo | Ambos | Notificación Telegram + Dashboard rojo |
| Reporte semanal | Hermes Telegram | "/status" → resumen |
| Reporte semanal | Dashboard | Tab "Reportes" → gráficas |

---

**Creado por:** Hermes Neo  
**Fecha:** 2026-05-01  
**Versión:** 3.0 Dual Mode  
**Estado:** Listo para ejecutar
