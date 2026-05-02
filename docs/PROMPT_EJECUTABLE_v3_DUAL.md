# PROMPT EJECUTABLE v3 DUAL — OpenCode Go
# Hermes Legal Pro: Modo Dual (Dashboard + Hermes Agent)
# 
# ⚠️  REGLAS ABSOLUTAS:
# 1. Lee TODO este archivo antes de tocar cualquier cosa
# 2. Ejecuta tareas en ORDEN (1 → 2 → 3 → 4 → 5)
# 3. Cada tarea tiene VERIFICACIÓN — si falla, DETENTE y reporta
# 4. NO modificar motor_kami/blocks.py, motor_kami.py, bridge_api.py
# 5. NO modificar dashboard/backend/app.py salvo que se indique
# 6. Si algo no existe, CREALO. Si algo existe, respétalo.
# 7. Usa rutas ABSOLUTAS siempre que sea posible
# 8. Documenta errores en docs/ERRORES_OPENCODE.md
#
# 📍 UBICACIÓN DEL REPO: ~/ws-hermes-legal-pro (o donde esté clonado)
# 📅 FECHA: 2026-05-01
# 🎯 OBJETIVO: Producto legal dual — funciona por Telegram (Hermes) y por Dashboard (Mac)

---

## 🔍 PASO 0: PREPARACIÓN (Obligatorio antes de todo)

### 0.1 Verificar ubicación del repo
```bash
# Buscar el repo si no sabes dónde está
REPO_PATH=$(find ~ -type d -name "ws-hermes-legal-pro" 2>/dev/null | head -1)

if [ -z "$REPO_PATH" ]; then
    echo "❌ ERROR: No se encontró ws-hermes-legal-pro"
    echo "Clonar con: git clone https://github.com/cuentadeservicio377-cell/ws-hermes-legal-pro.git ~/ws-hermes-legal-pro"
    exit 1
fi

echo "✅ Repo encontrado en: $REPO_PATH"
cd "$REPO_PATH"
```

### 0.2 Verificar estructura base existe
```bash
cd "$REPO_PATH"

echo "=== VERIFICACIÓN ESTRUCTURA BASE ==="
[ -d motor_kami ] && [ -f motor_kami/blocks.py ] && echo "✅ motor_kami/" || echo "❌ FALTA motor_kami/"
[ -d dashboard/backend ] && [ -f dashboard/backend/app.py ] && echo "✅ dashboard/" || echo "❌ FALTA dashboard/"
[ -d motor_kami/templates ] && [ $(ls motor_kami/templates/*.json 2>/dev/null | wc -l) -ge 20 ] && echo "✅ templates/" || echo "❌ FALTA templates/"
[ -f datos/matters.json ] && echo "✅ datos/" || echo "⚠️  datos/matters.json no existe (se creará)"
[ -f README.md ] && echo "✅ README.md" || echo "❌ FALTA README.md"

# Si falta algo crítico, detenerse
if [ ! -d motor_kami ] || [ ! -f motor_kami/blocks.py ]; then
    echo "❌ ERROR CRÍTICO: Motor Kami no existe. No se puede continuar."
    exit 1
fi
```

### 0.3 Actualizar repo desde GitHub
```bash
cd "$REPO_PATH"
git pull origin master
echo "✅ Repo actualizado"
```

### 0.4 Verificar plan dual existe
```bash
cd "$REPO_PATH"
if [ ! -f docs/PLAN_MAESTRO_v3_DUAL.md ]; then
    echo "❌ ERROR: No existe docs/PLAN_MAESTRO_v3_DUAL.md"
    echo "Descargar de: https://github.com/cuentadeservicio377-cell/ws-hermes-legal-pro/blob/master/docs/PLAN_MAESTRO_v3_DUAL.md"
    exit 1
fi
echo "✅ Plan v3 dual disponible"
```

**RESULTADO ESPERADO:**
- Repo localizado y actualizado
- Motor Kami presente y funcional
- Plan v3 dual disponible
- Si todo ✅ → Continuar a Tarea 1

---

## 🔧 TAREA 1: Copiar Assets de Paperclip (30 min)

### OBJETIVO
Traer el conocimiento operativo jurídico del repo Paperclip al repo Hermes Legal.

### 1.1 Clonar Paperclip
```bash
cd /tmp
if [ ! -d paperclip-assets ]; then
    git clone https://github.com/cuentadeservicio377-cell/willow-paperclip-portable.git paperclip-assets
    echo "✅ Paperclip clonado"
else
    echo "✅ Paperclip ya existe"
fi
```

### 1.2 Verificar Paperclip tiene lo necesario
```bash
cd /tmp/paperclip-assets

echo "=== VERIFICANDO PAPERCLIP ==="
test -f company/workspace/agents/despacho.md && echo "✅ despacho.md" || echo "❌ FALTA despacho.md"
test -f company/workspace/agents/intake.md && echo "✅ intake.md" || echo "❌ FALTA intake.md"
test -f company/workspace/agents/admin.md && echo "✅ admin.md" || echo "❌ FALTA admin.md"
test -f company/workspace/triggers/willow-triggers.json && echo "✅ triggers.json" || echo "❌ FALTA triggers.json"
test -f company/workspace/library/willow-template-library.json && echo "✅ library.json" || echo "❌ FALTA library.json"

# Contar líneas de cada agente
wc -l company/workspace/agents/*.md
```

**Si algo falta ❌ → Detenerse y reportar**

### 1.3 Crear directorio agents/ y copiar
```bash
cd "$REPO_PATH"

# Crear directorio si no existe
mkdir -p agents/

# Copiar agentes (preservar metadata)
cp /tmp/paperclip-assets/company/workspace/agents/despacho.md agents/
cp /tmp/paperclip-assets/company/workspace/agents/intake.md agents/
cp /tmp/paperclip-assets/company/workspace/agents/admin.md agents/

echo "✅ Agentes copiados"
ls -la agents/
```

### 1.4 Copiar triggers
```bash
cd "$REPO_PATH"

# Crear directorio config/ si no existe
mkdir -p config/

# Copiar triggers
cp /tmp/paperclip-assets/company/workspace/triggers/willow-triggers.json config/triggers.json

echo "✅ Triggers copiados"
test -f config/triggers.json && wc -l config/triggers.json
```

### 1.5 Crear documentación de estructura de carpetas
```bash
cd "$REPO_PATH"

# Extraer de despacho.md la sección de carpetas
grep -A 30 "Regla de carpeta fuente" agents/despacho.md > docs/ESTRUCTURA_CARPETAS.md 2>/dev/null || echo "# ESTRUCTURA DE CARPETAS WILLOW LEGAL" > docs/ESTRUCTURA_CARPETAS.md

# Añadir estructura estándar
cat >> docs/ESTRUCTURA_CARPETAS.md << 'EOF'

## Estructura estándar por asunto

```
CARPETA_DEL_ASUNTO/
├── 00-Insumos crudos/          # Material bruto del cliente
├── 01-Expediente vivo/          # Documentos activos
├── 02-Demanda inicial/          # Para litigio
├── 03-Estrategia de litigio/   # Análisis y estrategia
├── 04-Anexos y evidencia/      # Pruebas
└── 05-Versiones aprobadas/     # Documentos firmados
```

## Estructura del sistema

```
~/WillowLegal/
├── 00_Sistema/                 # Scripts, docs, motor
│   ├── Motor_Kami/
│   ├── scripts/
│   └── docs/
├── 01_Clientes/                # Un directorio por cliente
├── 02_Administracion/          # Templates, formatos
├── 03_Biblioteca_Legal/        # Precedentes, jurisprudencia
├── 04_Agentes_Onyx/            # Fichas de agentes
└── 05_Backups/                 # Respaldos periódicos
```
EOF

echo "✅ ESTRUCTURA_CARPETAS.md creado"
wc -l docs/ESTRUCTURA_CARPETAS.md
```

### 1.6 VERIFICACIÓN TAREA 1
```bash
cd "$REPO_PATH"

echo ""
echo "=========================================="
echo "  VERIFICACIÓN TAREA 1: Assets Paperclip"
echo "=========================================="
echo ""

ERRORS=0

# Verificar agentes
if [ -f agents/despacho.md ]; then
    LINES=$(wc -l < agents/despacho.md)
    if [ "$LINES" -gt 100 ]; then
        echo "✅ despacho.md: $LINES líneas"
    else
        echo "⚠️  despacho.md: solo $LINES líneas (¿completo?)"
    fi
else
    echo "❌ FALTA agents/despacho.md"
    ERRORS=$((ERRORS + 1))
fi

if [ -f agents/intake.md ]; then
    LINES=$(wc -l < agents/intake.md)
    echo "✅ intake.md: $LINES líneas"
else
    echo "❌ FALTA agents/intake.md"
    ERRORS=$((ERRORS + 1))
fi

if [ -f agents/admin.md ]; then
    LINES=$(wc -l < agents/admin.md)
    echo "✅ admin.md: $LINES líneas"
else
    echo "❌ FALTA agents/admin.md"
    ERRORS=$((ERRORS + 1))
fi

# Verificar triggers
if [ -f config/triggers.json ]; then
    TRIGGERS=$(grep -c '"id"' config/triggers.json)
    echo "✅ triggers.json: $TRIGGERS triggers encontrados"
else
    echo "❌ FALTA config/triggers.json"
    ERRORS=$((ERRORS + 1))
fi

# Verificar estructura carpetas
if [ -f docs/ESTRUCTURA_CARPETAS.md ]; then
    echo "✅ ESTRUCTURA_CARPETAS.md existe"
else
    echo "❌ FALTA docs/ESTRUCTURA_CARPETAS.md"
    ERRORS=$((ERRORS + 1))
fi

echo ""
if [ $ERRORS -eq 0 ]; then
    echo "🎉 TAREA 1 COMPLETADA ✅"
    echo ""
    echo "Contenido de agents/:"
    ls -la agents/
    echo ""
    echo "Primeras 5 líneas de despacho.md:"
    head -5 agents/despacho.md
else
    echo "❌ TAREA 1 CON ERRORES ($ERRORS fallos)"
    echo "NO CONTINUAR. Reportar errores."
    exit 1
fi
```

---

## 🔧 TAREA 2: Merge Catálogo Templates (20 min)

### OBJETIVO
Combinar metadata de templates del Paperclip con los templates JSON del Motor Kami.

### 2.1 Verificar catálogos existen
```bash
cd "$REPO_PATH"

echo "=== CATÁLOGOS ==="
test -f motor_kami/templates/index.json && echo "✅ motor_kami/templates/index.json" || echo "❌ FALTA"
test -f /tmp/paperclip-assets/company/workspace/library/willow-template-library.json && echo "✅ paperclip library" || echo "❌ FALTA"
```

### 2.2 Ejecutar script de merge
```bash
cd "$REPO_PATH"

python3 << 'PYEOF'
import json
import sys

print("=== MERGE DE CATÁLOGOS ===")

# Leer catálogo del motor
try:
    with open('motor_kami/templates/index.json', 'r', encoding='utf-8') as f:
        motor_data = json.load(f)
    print("✅ Catálogo motor leído")
except Exception as e:
    print(f"❌ Error leyendo motor_kami/templates/index.json: {e}")
    sys.exit(1)

# Leer catálogo de Paperclip
try:
    with open('/tmp/paperclip-assets/company/workspace/library/willow-template-library.json', 'r', encoding='utf-8') as f:
        paperclip_data = json.load(f)
    print(f"✅ Catálogo Paperclip leído: {len(paperclip_data)} templates")
except Exception as e:
    print(f"❌ Error leyendo Paperclip library: {e}")
    sys.exit(1)

# Crear diccionario Paperclip por key
paperclip_by_key = {}
for t in paperclip_data:
    key = t.get('key', '')
    if key:
        paperclip_by_key[key] = t

print(f"✅ {len(paperclip_by_key)} templates en Paperclip indexados")

# Determinar estructura del catálogo motor
templates_list = []
if isinstance(motor_data, list):
    templates_list = motor_data
    motor_data = {"templates": templates_list}
elif isinstance(motor_data, dict) and 'templates' in motor_data:
    templates_list = motor_data['templates']
else:
    print("⚠️  Estructura de index.json desconocida, creando nueva")
    templates_list = []
    motor_data = {"templates": templates_list}

print(f"✅ {len(templates_list)} templates en motor")

# Mergear
merged_count = 0
new_count = 0
for template in templates_list:
    key = template.get('key', template.get('slug', ''))
    if not key:
        print(f"⚠️  Template sin key: {template.get('label', 'sin label')}")
        continue
    
    if key in paperclip_by_key:
        pc = paperclip_by_key[key]
        # Mergear campos
        fields_merged = []
        for field in ['area', 'materia', 'descripcion', 'estado', 'category']:
            if field not in template or not template[field]:
                if field in pc and pc[field]:
                    template[field] = pc[field]
                    fields_merged.append(field)
        
        if fields_merged:
            print(f"✅ {key}: mergeado {fields_merged}")
            merged_count += 1
        else:
            print(f"✓ {key}: ya completo")
    else:
        print(f"⚠️  {key}: no encontrado en Paperclip")
        new_count += 1

# Guardar resultado
try:
    with open('motor_kami/templates/index.json', 'w', encoding='utf-8') as f:
        json.dump(motor_data, f, indent=2, ensure_ascii=False)
    print(f"\n✅ Catálogo guardado")
    print(f"   Templates totales: {len(templates_list)}")
    print(f"   Mergeados: {merged_count}")
    print(f"   No encontrados en Paperclip: {new_count}")
except Exception as e:
    print(f"❌ Error guardando: {e}")
    sys.exit(1)

print("\n🎉 TAREA 2 COMPLETADA")
PYEOF
```

### 2.3 VERIFICACIÓN TAREA 2
```bash
cd "$REPO_PATH"

echo ""
echo "=========================================="
echo "  VERIFICACIÓN TAREA 2: Merge Templates"
echo "=========================================="
echo ""

python3 << 'PYEOF'
import json

with open('motor_kami/templates/index.json') as f:
    data = json.load(f)

templates = data if isinstance(data, list) else data.get('templates', [])

print(f"Total templates: {len(templates)}")
print("")
print("Primeros 5 templates:")
for t in templates[:5]:
    key = t.get('key', t.get('slug', 'SIN_KEY'))
    area = t.get('area', 'N/A')
    materia = t.get('materia', 'N/A')
    desc = t.get('descripcion', 'N/A')[:50]
    print(f"  {key}: {area}/{materia} - {desc}...")

# Verificar que tienen campos mergeados
complete = sum(1 for t in templates if t.get('area') and t.get('materia'))
print(f"\nTemplates con area+materia: {complete}/{len(templates)}")

if complete == len(templates):
    print("🎉 TAREA 2 VERIFICADA ✅")
else:
    print(f"⚠️  {len(templates) - complete} templates sin metadata completa")
PYEOF
```

---

## 🔧 TAREA 3: Crear Integración Hermes (40 min)

### OBJETIVO
Crear la capa que permite operar el producto vía Telegram con Hermes Agent.

### 3.1 Crear directorio hermes_integration/
```bash
cd "$REPO_PATH"
mkdir -p hermes_integration/templates
echo "✅ Directorio hermes_integration/ creado"
```

### 3.2 Crear commands.py
```bash
cd "$REPO_PATH"

cat > hermes_integration/commands.py << 'PYEOF'
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hermes Legal Commands — Parser de comandos Telegram para operación legal.

Uso:
    from hermes_integration.commands import HermesLegalCommands
    cmd = HermesLegalCommands()
    result = cmd.crear_matter("Innovatech Digital")
    print(result["mensaje"])
"""

import json
import subprocess
import sys
from pathlib import Path
from datetime import datetime


class HermesLegalCommands:
    """
    Interfaz de comandos para operación legal via Hermes Agent.
    
    Mantiene compatibilidad con:
    - Modo Hermes (Telegram): comandos tipo /matter, /contrato
    - Modo Dashboard: mismo backend de datos
    """
    
    def __init__(self, base_dir="~/WillowLegal"):
        """
        Inicializar con directorio base.
        
        Args:
            base_dir: Directorio raíz de WillowLegal (default: ~/WillowLegal)
        """
        self.base_dir = Path(base_dir).expanduser()
        self.datos_dir = self.base_dir / "datos"
        self.datos_dir.mkdir(parents=True, exist_ok=True)
        
        # Archivos de datos
        self.matters_file = self.datos_dir / "matters.json"
        self.documentos_file = self.datos_dir / "documentos.json"
        self.alertas_file = self.datos_dir / "alertas.json"
        
        # Referencia al motor
        self.motor_dir = self.base_dir / "00_Sistema" / "Motor_Kami"
        self.repo_dir = Path(__file__).parent.parent  # ws-hermes-legal-pro
    
    # ============================================================
    # MATTERS
    # ============================================================
    
    def crear_matter(self, nombre: str, **kwargs) -> dict:
        """
        Crear nuevo matter desde comando Telegram.
        
        Args:
            nombre: Nombre del cliente o asunto
            cliente: (opcional) Nombre del cliente si difiere
            area: (opcional) Área legal (default: Mercantil)
            prioridad: (opcional) baja/media/alta (default: media)
            
        Returns:
            dict con status, matter_id, mensaje
        """
        try:
            # Cargar matters existentes
            matters = self._load_json(self.matters_file, [])
            
            # Generar ID
            matter_id = f"WIL-{len(matters)+1:03d}"
            
            # Crear matter
            matter = {
                "id": matter_id,
                "nombre": nombre,
                "cliente": kwargs.get("cliente", nombre),
                "estado": "Intake",
                "area": kwargs.get("area", "Mercantil"),
                "materia": kwargs.get("materia", "corporativo"),
                "prioridad": kwargs.get("prioridad", "media"),
                "creado": datetime.now().isoformat(),
                "actualizado": datetime.now().isoformat(),
                "next_step": "Intake inicial pendiente",
                "blocker": "none",
                "carpeta": str(self.base_dir / "01_Clientes" / self._safe_name(nombre)),
                "deadline": kwargs.get("deadline", None),
                "descripcion": kwargs.get("descripcion", "")
            }
            
            matters.append(matter)
            self._save_json(self.matters_file, matters)
            
            # Crear estructura de carpetas
            self._crear_carpetas_matter(matter["carpeta"])
            
            return {
                "status": "ok",
                "matter_id": matter_id,
                "mensaje": (
                    f"✅ Matter creado: {matter_id}\n"
                    f"📁 Carpeta: {matter['carpeta']}\n"
                    f"📋 Next step: {matter['next_step']}\n"
                    f"🏷️  Área: {matter['area']}"
                )
            }
            
        except Exception as e:
            return {
                "status": "error",
                "mensaje": f"❌ Error creando matter: {str(e)}"
            }
    
    def listar_matters(self, limite: int = 10) -> dict:
        """Listar matters activos para mostrar en Telegram."""
        try:
            matters = self._load_json(self.matters_file, [])
            
            if not matters:
                return {
                    "status": "ok",
                    "mensaje": "📭 No hay matters registrados"
                }
            
            lines = ["📋 MATTERS ACTIVOS:"]
            for m in matters[-limite:]:
                emoji = "🟢" if m.get("estado") == "Activo" else "🟡" if m.get("estado") == "Intake" else "🔴"
                lines.append(f"  {emoji} {m['id']}: {m['nombre']} ({m['estado']})")
            
            return {
                "status": "ok",
                "mensaje": "\n".join(lines),
                "data": matters[-limite:]
            }
            
        except Exception as e:
            return {
                "status": "error",
                "mensaje": f"❌ Error listando matters: {str(e)}"
            }
    
    def ver_matter(self, matter_id: str) -> dict:
        """Ver detalle de un matter específico."""
        try:
            matters = self._load_json(self.matters_file, [])
            
            matter = next((m for m in matters if m["id"] == matter_id), None)
            if not matter:
                return {
                    "status": "error",
                    "mensaje": f"❌ Matter {matter_id} no encontrado"
                }
            
            return {
                "status": "ok",
                "mensaje": (
                    f"📋 {matter['id']}: {matter['nombre']}\n"
                    f"   Estado: {matter['estado']}\n"
                    f"   Área: {matter['area']}\n"
                    f"   Next step: {matter.get('next_step', 'N/A')}\n"
                    f"   Blocker: {matter.get('blocker', 'none')}\n"
                    f"   📁 {matter['carpeta']}"
                ),
                "data": matter
            }
            
        except Exception as e:
            return {
                "status": "error",
                "mensaje": f"❌ Error: {str(e)}"
            }
    
    # ============================================================
    # DOCUMENTOS / CONTRATOS
    # ============================================================
    
    def generar_documento(self, template: str, matter_id: str = None, **kwargs) -> dict:
        """
        Generar documento legal via Motor Kami.
        
        Args:
            template: Key del template (nda, prestacion_servicios, etc.)
            matter_id: (opcional) Matter asociado
            variables: (opcional) Dict con variables adicionales
            
        Returns:
            dict con status, mensaje, path del PDF
        """
        try:
            # Verificar template existe
            template_file = self.repo_dir / "motor_kami" / "templates" / f"{template}.json"
            if not template_file.exists():
                # Listar templates disponibles
                templates_dir = self.repo_dir / "motor_kami" / "templates"
                disponibles = [f.stem for f in templates_dir.glob("*.json") if f.stem != "index"]
                return {
                    "status": "error",
                    "mensaje": (
                        f"❌ Template '{template}' no encontrado\n"
                        f"📋 Disponibles: {', '.join(disponibles[:10])}"
                    )
                }
            
            # Preparar comando al motor
            motor_script = self.repo_dir / "motor_kami" / "motor_kami.py"
            
            cmd = [
                sys.executable,
                str(motor_script),
                "--template", template
            ]
            
            if matter_id:
                cmd.extend(["--matter", matter_id])
            
            # Ejecutar motor
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=str(self.repo_dir / "motor_kami")
            )
            
            if result.returncode != 0:
                return {
                    "status": "error",
                    "mensaje": f"❌ Motor Kami error:\n{result.stderr}"
                }
            
            # Buscar PDF generado
            output_dir = self.repo_dir / "motor_kami" / "output"
            pdfs = sorted(output_dir.glob("*.pdf"), key=lambda p: p.stat().st_mtime, reverse=True)
            
            if pdfs:
                latest_pdf = pdfs[0]
                return {
                    "status": "ok",
                    "mensaje": (
                        f"📝 Documento generado:\n"
                        f"   Template: {template}\n"
                        f"   📄 {latest_pdf.name}\n"
                        f"   📁 {latest_pdf.parent}"
                    ),
                    "pdf_path": str(latest_pdf)
                }
            else:
                return {
                    "status": "ok",
                    "mensaje": f"✅ Documento generado (sin PDF en output)"
                }
                
        except Exception as e:
            return {
                "status": "error",
                "mensaje": f"❌ Error generando documento: {str(e)}"
            }
    
    def listar_templates(self) -> dict:
        """Listar templates disponibles."""
        try:
            templates_dir = self.repo_dir / "motor_kami" / "templates"
            templates = [f.stem for f in templates_dir.glob("*.json") if f.stem != "index"]
            
            lines = ["📋 TEMPLATES DISPONIBLES:"]
            for t in sorted(templates):
                lines.append(f"  • {t}")
            
            return {
                "status": "ok",
                "mensaje": "\n".join(lines)
            }
            
        except Exception as e:
            return {
                "status": "error",
                "mensaje": f"❌ Error: {str(e)}"
            }
    
    # ============================================================
    # PLAZOS / ALERTAS
    # ============================================================
    
    def crear_plazo(self, matter_id: str, descripcion: str, fecha: str, **kwargs) -> dict:
        """Crear plazo con alerta."""
        try:
            alertas = self._load_json(self.alertas_file, [])
            
            alerta = {
                "id": f"ALERT-{len(alertas)+1:03d}",
                "matter_id": matter_id,
                "descripcion": descripcion,
                "fecha": fecha,
                "tipo": kwargs.get("tipo", "plazo"),
                "estado": "pendiente",
                "creado": datetime.now().isoformat()
            }
            
            alertas.append(alerta)
            self._save_json(self.alertas_file, alertas)
            
            return {
                "status": "ok",
                "mensaje": (
                    f"📅 Plazo creado: {alerta['id']}\n"
                    f"   Matter: {matter_id}\n"
                    f"   📌 {descripcion}\n"
                    f"   📆 Fecha límite: {fecha}"
                )
            }
            
        except Exception as e:
            return {
                "status": "error",
                "mensaje": f"❌ Error: {str(e)}"
            }
    
    def ver_alertas(self, matter_id: str = None) -> dict:
        """Ver alertas pendientes."""
        try:
            alertas = self._load_json(self.alertas_file, [])
            
            if matter_id:
                alertas = [a for a in alertas if a.get("matter_id") == matter_id]
            
            pendientes = [a for a in alertas if a.get("estado") == "pendiente"]
            
            if not pendientes:
                return {
                    "status": "ok",
                    "mensaje": "✅ No hay alertas pendientes"
                }
            
            lines = [f"📢 ALERTAS PENDIENTES ({len(pendientes}):"]
            for a in pendientes[-10:]:
                lines.append(f"  • {a['id']}: {a['descripcion']} (vence: {a['fecha']})")
            
            return {
                "status": "ok",
                "mensaje": "\n".join(lines)
            }
            
        except Exception as e:
            return {
                "status": "error",
                "mensaje": f"❌ Error: {str(e)}"
            }
    
    # ============================================================
    # STATUS / REPORTES
    # ============================================================
    
    def status_despacho(self) -> dict:
        """Estado general del despacho."""
        try:
            matters = self._load_json(self.matters_file, [])
            alertas = self._load_json(self.alertas_file, [])
            
            activos = [m for m in matters if m.get("estado") in ["Activo", "Intake"]]
            pendientes = [a for a in alertas if a.get("estado") == "pendiente"]
            
            lines = [
                "📊 ESTADO DEL DESPACHO",
                "",
                f"📁 Matters activos: {len(activos)}",
                f"📢 Alertas pendientes: {len(pendientes)}",
                f"📊 Total matters: {len(matters)}",
                "",
                "🟢 MATTERS RECIENTES:"
            ]
            
            for m in matters[-5:]:
                lines.append(f"   {m['id']}: {m['nombre']} ({m['estado']})")
            
            return {
                "status": "ok",
                "mensaje": "\n".join(lines)
            }
            
        except Exception as e:
            return {
                "status": "error",
                "mensaje": f"❌ Error: {str(e)}"
            }
    
    # ============================================================
    # HELPERS PRIVADOS
    # ============================================================
    
    def _load_json(self, path: Path, default):
        """Cargar JSON o retornar default."""
        if path.exists():
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return default
    
    def _save_json(self, path: Path, data):
        """Guardar JSON con formato."""
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def _safe_name(self, name: str) -> str:
        """Convertir nombre a nombre de carpeta seguro."""
        return "".join(c if c.isalnum() or c in " _-" else "_" for c in name).strip().replace(" ", "_")
    
    def _crear_carpetas_matter(self, carpeta: str):
        """Crear estructura de carpetas para un matter."""
        base = Path(carpeta)
        subdirs = [
            "01_Intake",
            "02_Contratos/Borradores",
            "02_Contratos/Firmados",
            "03_Correspondencia/Entrante",
            "03_Correspondencia/Saliente",
            "04_Litigio",
            "05_Facturacion",
            "06_Entregables/Documentos_Finales",
            "07_Archivo"
        ]
        for sub in subdirs:
            (base / sub).mkdir(parents=True, exist_ok=True)


if __name__ == "__main__":
    # Test básico
    cmd = HermesLegalCommands()
    print(cmd.crear_matter("Test_Hermes_Integration"))
    print(cmd.listar_matters())
    print(cmd.status_despacho())
PYEOF

echo "✅ hermes_integration/commands.py creado"
wc -l hermes_integration/commands.py
```

### 3.3 Crear session_manager.py
```bash
cd "$REPO_PATH"

cat > hermes_integration/session_manager.py << 'PYEOF'
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session Manager — Gestión de contexto entre Hermes y Legal.

Mantiene el matter activo para comandos subsiguientes.
"""

import json
from pathlib import Path
from datetime import datetime


class LegalSessionManager:
    """
    Mantiene contexto de sesión legal activa entre interacciones.
    
    Uso:
        session = LegalSessionManager()
        session.set_matter("WIL-001")  # Fijar contexto
        
        # En comandos subsiguientes:
        matter_id = session.get_matter()  # "WIL-001"
    """
    
    def __init__(self, session_file="~/.hermes/legal_session.json"):
        self.session_file = Path(session_file).expanduser()
        self.session = self._load()
    
    def _load(self) -> dict:
        """Cargar sesión existente o crear nueva."""
        if self.session_file.exists():
            try:
                with open(self.session_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        return {
            "matter_active": None,
            "usuario": "hermes",
            "historial": [],
            "creado": datetime.now().isoformat()
        }
    
    def set_matter(self, matter_id: str):
        """Fijar matter activo."""
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
    
    def clear_matter(self):
        """Limpiar matter activo."""
        self.session["matter_active"] = None
        self.session["historial"].append({
            "accion": "clear_matter",
            "timestamp": datetime.now().isoformat()
        })
        self._save()
    
    def get_historial(self, limite: int = 10) -> list:
        """Obtener últimas acciones."""
        return self.session["historial"][-limite:]
    
    def _save(self):
        """Guardar sesión a disco."""
        self.session_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.session_file, 'w', encoding='utf-8') as f:
            json.dump(self.session, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    # Test
    sm = LegalSessionManager()
    sm.set_matter("WIL-TEST-001")
    print(f"Matter activo: {sm.get_matter()}")
    print(f"Historial: {len(sm.get_historial())} acciones")
    sm.clear_matter()
    print(f"Después de clear: {sm.get_matter()}")
PYEOF

echo "✅ hermes_integration/session_manager.py creado"
wc -l hermes_integration/session_manager.py
```

### 3.4 Crear __init__.py
```bash
cd "$REPO_PATH"

cat > hermes_integration/__init__.py << 'PYEOF'
"""
Hermes Integration — Operación legal via Hermes Agent.

Modo dual: funciona tanto por Telegram (Hermes) como por Dashboard.
"""

from .commands import HermesLegalCommands
from .session_manager import LegalSessionManager

__all__ = ["HermesLegalCommands", "LegalSessionManager"]
__version__ = "1.0.0"
PYEOF

echo "✅ hermes_integration/__init__.py creado"
```

### 3.5 Crear scripts/hermes_bridge.py
```bash
cd "$REPO_PATH"

cat > scripts/hermes_bridge.py << 'PYEOF'
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hermes Bridge — Entry point para comandos desde Hermes Agent.

Uso desde Hermes:
    python3 scripts/hermes_bridge.py matter nuevo "Cliente S.A."
    python3 scripts/hermes_bridge.py contrato nda WIL-001
    python3 scripts/hermes_bridge.py plazo WIL-001 "Audiencia" 2026-05-20
    python3 scripts/hermes_bridge.py status
    python3 scripts/hermes_bridge.py alerta
"""

import sys
import os
from pathlib import Path

# Añadir repo al path
REPO_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(REPO_DIR))

from hermes_integration.commands import HermesLegalCommands
from hermes_integration.session_manager import LegalSessionManager


def print_usage():
    print("""
Uso: hermes_bridge.py <comando> [args...]

Comandos:
  matter nuevo <nombre> [area=...] [prioridad=...]
  matter list
  matter <id>
  
  contrato <template> [matter_id]
  templates
  
  plazo <matter_id> <descripcion> <fecha>
  alerta [matter_id]
  
  status
  
Ejemplos:
  python3 scripts/hermes_bridge.py matter nuevo "Innovatech" area=Corporativo
  python3 scripts/hermes_bridge.py contrato nda
  python3 scripts/hermes_bridge.py plazo WIL-001 "Audiencia" 2026-05-20
  python3 scripts/hermes_bridge.py status
""")


def parse_kwargs(args):
    """Parsear argumentos tipo key=value."""
    kwargs = {}
    clean_args = []
    for arg in args:
        if '=' in arg:
            key, value = arg.split('=', 1)
            kwargs[key] = value
        else:
            clean_args.append(arg)
    return clean_args, kwargs


def main():
    if len(sys.argv) < 2:
        print_usage()
        sys.exit(1)
    
    cmd = sys.argv[1]
    args, kwargs = parse_kwargs(sys.argv[2:])
    
    # Inicializar
    commands = HermesLegalCommands()
    session = LegalSessionManager()
    
    # ============================================================
    # MATTER
    # ============================================================
    if cmd == "matter":
        if not args:
            print("❌ Falta subcomando. Uso: matter nuevo|list|<id>")
            sys.exit(1)
        
        subcmd = args[0]
        
        if subcmd == "nuevo":
            if len(args) < 2:
                print("❌ Falta nombre del matter")
                sys.exit(1)
            nombre = " ".join(args[1:])
            result = commands.crear_matter(nombre, **kwargs)
            if result["status"] == "ok":
                session.set_matter(result["matter_id"])
            print(result["mensaje"])
        
        elif subcmd == "list":
            result = commands.listar_matters()
            print(result["mensaje"])
        
        else:
            # Ver matter específico
            matter_id = subcmd
            result = commands.ver_matter(matter_id)
            print(result["mensaje"])
    
    # ============================================================
    # CONTRATO / DOCUMENTO
    # ============================================================
    elif cmd == "contrato":
        if not args:
            print("❌ Falta template. Uso: contrato <template> [matter_id]")
            sys.exit(1)
        
        template = args[0]
        matter_id = args[1] if len(args) > 1 else session.get_matter()
        
        if not matter_id:
            print("❌ No hay matter activo. Usa 'matter nuevo' primero, o especifica matter_id")
            sys.exit(1)
        
        result = commands.generar_documento(template, matter_id, **kwargs)
        print(result["mensaje"])
    
    elif cmd == "templates":
        result = commands.listar_templates()
        print(result["mensaje"])
    
    # ============================================================
    # PLAZO / ALERTA
    # ============================================================
    elif cmd == "plazo":
        if len(args) < 3:
            print("❌ Uso: plazo <matter_id> <descripcion> <fecha>")
            sys.exit(1)
        
        matter_id = args[0]
        descripcion = args[1]
        fecha = args[2]
        
        result = commands.crear_plazo(matter_id, descripcion, fecha, **kwargs)
        print(result["mensaje"])
    
    elif cmd == "alerta":
        matter_id = args[0] if args else None
        result = commands.ver_alertas(matter_id)
        print(result["mensaje"])
    
    # ============================================================
    # STATUS
    # ============================================================
    elif cmd == "status":
        result = commands.status_despacho()
        print(result["mensaje"])
    
    else:
        print(f"❌ Comando desconocido: {cmd}")
        print_usage()
        sys.exit(1)


if __name__ == "__main__":
    main()
PYEOF

chmod +x scripts/hermes_bridge.py
echo "✅ scripts/hermes_bridge.py creado"
wc -l scripts/hermes_bridge.py
```

### 3.6 Crear config/hermes-commands.json
```bash
cd "$REPO_PATH"
mkdir -p config

cat > config/hermes-commands.json << 'JSONEOF'
{
  "version": "1.0",
  "description": "Comandos Telegram para operación legal via Hermes Agent",
  "prefix": "/",
  "commands": {
    "matter": {
      "description": "Gestionar matters (asuntos legales)",
      "subcommands": {
        "nuevo": {
          "description": "Crear nuevo matter",
          "args": ["nombre"],
          "optional_args": ["area", "prioridad", "cliente"],
          "example": "/matter nuevo Innovatech Digital area=Corporativo"
        },
        "list": {
          "description": "Listar matters activos",
          "example": "/matter list"
        }
      },
      "example": "/matter nuevo Cliente S.A."
    },
    "contrato": {
      "description": "Generar documento legal",
      "args": ["template"],
      "optional_args": ["matter_id"],
      "example": "/contrato nda WIL-001"
    },
    "templates": {
      "description": "Listar templates disponibles",
      "example": "/templates"
    },
    "plazo": {
      "description": "Crear deadline o plazo",
      "args": ["matter_id", "descripcion", "fecha"],
      "example": "/plazo WIL-001 'Audiencia inicial' 2026-05-20"
    },
    "alerta": {
      "description": "Ver alertas pendientes",
      "optional_args": ["matter_id"],
      "example": "/alerta"
    },
    "status": {
      "description": "Estado general del despacho",
      "example": "/status"
    },
    "abrir": {
      "description": "Abrir carpeta del matter",
      "args": ["matter_id"],
      "example": "/abrir WIL-001"
    }
  }
}
JSONEOF

echo "✅ config/hermes-commands.json creado"
```

### 3.7 VERIFICACIÓN TAREA 3
```bash
cd "$REPO_PATH"

echo ""
echo "=========================================="
echo "  VERIFICACIÓN TAREA 3: Integración Hermes"
echo "=========================================="
echo ""

ERRORS=0

# Verificar archivos creados
files=(
    "hermes_integration/__init__.py"
    "hermes_integration/commands.py"
    "hermes_integration/session_manager.py"
    "scripts/hermes_bridge.py"
    "config/hermes-commands.json"
)

for f in "${files[@]}"; do
    if [ -f "$f" ]; then
        lines=$(wc -l < "$f")
        echo "✅ $f ($lines líneas)"
    else
        echo "❌ FALTA $f"
        ERRORS=$((ERRORS + 1))
    fi
done

# Verificar imports funcionan
echo ""
echo "=== TEST DE IMPORTS ==="
python3 -c "
import sys
sys.path.insert(0, '.')
try:
    from hermes_integration.commands import HermesLegalCommands
    print('✅ HermesLegalCommands importa')
except Exception as e:
    print(f'❌ Error importando commands: {e}')
    sys.exit(1)

try:
    from hermes_integration.session_manager import LegalSessionManager
    print('✅ LegalSessionManager importa')
except Exception as e:
    print(f'❌ Error importando session_manager: {e}')
    sys.exit(1)
" || ERRORS=$((ERRORS + 1))

# Test funcional básico
echo ""
echo "=== TEST FUNCIONAL ==="
python3 scripts/hermes_bridge.py matter nuevo "Test_Integracion" 2>&1 | head -5

echo ""
if [ $ERRORS -eq 0 ]; then
    echo "🎉 TAREA 3 COMPLETADA ✅"
else
    echo "❌ TAREA 3 CON ERRORES ($ERRORS fallos)"
    exit 1
fi
```

---

## 🔧 TAREA 4: Actualizar README y Documentación (20 min)

### 4.1 Backup README
```bash
cd "$REPO_PATH"
cp README.md README.md.bak.$(date +%Y%m%d_%H%M%S)
echo "✅ README backup creado"
```

### 4.2 Insertar sección de Modo Dual
```bash
cd "$REPO_PATH"

# Crear archivo temporal con nueva sección
cat > /tmp/README_dual_section.md << 'EOF'

## 🎯 Modo Dual: Telegram + Dashboard

Hermes Legal Pro funciona en **dos modos simultáneos**:

### 🤖 Modo Hermes Agent (Telegram/Voz)

Opera tu despacho desde cualquier lugar via Telegram:

```bash
# Crear matter
/matter nuevo "Innovatech Digital" area=Corporativo

# Generar documento
/contrato nda WIL-001

# Crear plazo
/plazo WIL-001 "Audiencia" 2026-05-20

# Ver estado
/status
```

**Ventajas:**
- 🎤 Voz a texto (Whisper)
- 📱 Desde cualquier lugar
- ⚡ Comandos rápidos
- 🤖 Hermes orquesta agentes automáticamente

### 💻 Modo Dashboard (Mac Local)

Abre tu navegador en `http://localhost:8082`:

- 📊 Dashboard con KPIs en tiempo real
- 📅 Calendario mensual/semanal
- 📁 Matters con documentos y archivos
- 📝 Wizard de generación de documentos
- 📈 Reportes y finanzas

**Ventajas:**
- 👁️ Visual y estructurado
- 📑 Drag & drop de archivos
- 🖨️ Preview y print directo
- 📊 Excel maestro integrado

### 🔄 Sincronización

Ambos modos comparten:
- 💾 Misma base de datos (`datos/matters.json`)
- 📄 Mismo Motor Kami (23 templates)
- 📁 Mismas carpetas (`~/WillowLegal/`)
- 📊 Mismo Excel maestro

**Regla:** Lo que hagas en Telegram aparece en Dashboard, y viceversa.

EOF

# Insertar después de la descripción principal
# (Esto es un ejemplo, adaptar según estructura real del README)
echo "✅ Sección dual creada en /tmp/README_dual_section.md"
echo "⚠️  Insertar manualmente en README.md o usar script de merge"
```

### 4.3 Crear docs/MANUAL_HERMES_INTEGRATION.md
```bash
cd "$REPO_PATH"

cat > docs/MANUAL_HERMES_INTEGRATION.md << 'EOF'
# Manual de Integración Hermes — Hermes Legal Pro

## 🤖 Comandos Disponibles

### Matters

| Comando | Descripción | Ejemplo |
|---------|-------------|---------|
| `/matter nuevo <nombre>` | Crear matter | `/matter nuevo Innovatech` |
| `/matter list` | Listar matters | `/matter list` |
| `/matter <id>` | Ver matter | `/matter WIL-001` |

### Documentos

| Comando | Descripción | Ejemplo |
|---------|-------------|---------|
| `/contrato <template> [matter]` | Generar documento | `/contrato nda WIL-001` |
| `/templates` | Listar templates | `/templates` |

### Plazos

| Comando | Descripción | Ejemplo |
|---------|-------------|---------|
| `/plazo <matter> <desc> <fecha>` | Crear deadline | `/plazo WIL-001 "Audiencia" 2026-05-20` |
| `/alerta [matter]` | Ver alertas | `/alerta` |

### General

| Comando | Descripción | Ejemplo |
|---------|-------------|---------|
| `/status` | Estado despacho | `/status` |
| `/abrir <matter>` | Abrir carpeta | `/abrir WIL-001` |

## 🔧 Configuración

### Variables de entorno

Crear archivo `config/.env`:

```bash
WILLOW_BASE_DIR=~/WillowLegal
WILLOW_REPO_DIR=~/ws-hermes-legal-pro
HERMES_SESSION_FILE=~/.hermes/legal_session.json
```

### Primer uso

```bash
# 1. Ir al repo
cd ~/ws-hermes-legal-pro

# 2. Verificar instalación
python3 scripts/hermes_bridge.py status

# 3. Crear primer matter
python3 scripts/hermes_bridge.py matter nuevo "Test"

# 4. Listar templates
python3 scripts/hermes_bridge.py templates

# 5. Generar documento
python3 scripts/hermes_bridge.py contrato nda
```

## 🏗️ Arquitectura

```
Hermes (Telegram)
    ↓
hermes_bridge.py
    ↓
HermesLegalCommands
    ↓
datos/matters.json ← → Dashboard
    ↓
Motor Kami
    ↓
PDF generado
```

EOF

echo "✅ docs/MANUAL_HERMES_INTEGRATION.md creado"
```

### 4.4 VERIFICACIÓN TAREA 4
```bash
cd "$REPO_PATH"

echo ""
echo "=========================================="
echo "  VERIFICACIÓN TAREA 4: Documentación"
echo "=========================================="
echo ""

ERRORS=0

if [ -f docs/MANUAL_HERMES_INTEGRATION.md ]; then
    echo "✅ Manual Hermes creado"
else
    echo "❌ FALTA manual"
    ERRORS=$((ERRORS + 1))
fi

if [ -f /tmp/README_dual_section.md ]; then
    echo "✅ Sección README dual creada (insertar manualmente)"
else
    echo "⚠️  Sección README no creada"
fi

if [ $ERRORS -eq 0 ]; then
    echo "🎉 TAREA 4 COMPLETADA ✅"
else
    echo "❌ TAREA 4 CON ERRORES"
    exit 1
fi
```

---

## 🔧 TAREA 5: Test End-to-End Dual (20 min)

### 5.1 Test Modo Hermes
```bash
cd "$REPO_PATH"

echo ""
echo "=========================================="
echo "  TEST MODO HERMES"
echo "=========================================="
echo ""

# Test 1: Crear matter
echo "TEST 1: Crear matter"
python3 scripts/hermes_bridge.py matter nuevo "Test_E2E_Hermes" area=Corporativo 2>&1

# Test 2: Listar matters
echo ""
echo "TEST 2: Listar matters"
python3 scripts/hermes_bridge.py matter list 2>&1

# Test 3: Ver templates
echo ""
echo "TEST 3: Listar templates"
python3 scripts/hermes_bridge.py templates 2>&1

# Test 4: Status
echo ""
echo "TEST 4: Status despacho"
python3 scripts/hermes_bridge.py status 2>&1
```

### 5.2 Test Modo Dashboard
```bash
cd "$REPO_PATH"

echo ""
echo "=========================================="
echo "  TEST MODO DASHBOARD"
echo "=========================================="
echo ""

# Verificar backend inicia
echo "TEST: Backend importa correctamente"
python3 -c "import sys; sys.path.insert(0, 'dashboard/backend'); import app; print('✅ Backend importa')" 2>&1

# Verificar datos compartidos
echo ""
echo "TEST: Datos compartidos"
if [ -f datos/matters.json ]; then
    python3 -c "import json; d=json.load(open('datos/matters.json')); print(f'✅ Matters en datos/: {len(d)}')" 2>&1
else
    echo "⚠️  datos/matters.json no existe aún"
fi
```

### 5.3 Test Sync
```bash
cd "$REPO_PATH"

echo ""
echo "=========================================="
echo "  TEST SYNC HERMES ↔ DASHBOARD"
echo "=========================================="
echo ""

# Verificar que matter creado por Hermes está en datos/
python3 << 'PYEOF'
import json

# Cargar matters
with open('datos/matters.json') as f:
    matters = json.load(f)

# Buscar matter de test
test_matters = [m for m in matters if 'Test_E2E' in m.get('nombre', '')]

if test_matters:
    print(f"✅ Matter creado por Hermes encontrado en datos/: {test_matters[0]['id']}")
    print(f"   Nombre: {test_matters[0]['nombre']}")
    print(f"   Estado: {test_matters[0]['estado']}")
    print(f"   SYNC: Hermes ↔ Dashboard ✅")
else:
    print("⚠️  No se encontró matter de test (puede ser normal si no se ejecutó Test 1)")

print(f"\nTotal matters en sistema: {len(matters)}")
PYEOF
```

### 5.4 VERIFICACIÓN FINAL COMPLETA
```bash
cd "$REPO_PATH"

echo ""
echo "=========================================="
echo "  VERIFICACIÓN FINAL HERMES LEGAL PRO v3"
echo "=========================================="
echo ""

ERRORS=0
PASS=0

check() {
    if [ $1 -eq 0 ]; then
        echo "✅ $2"
        PASS=$((PASS + 1))
    else
        echo "❌ $2"
        ERRORS=$((ERRORS + 1))
    fi
}

# Estructura
test -d agents && test -f agents/despacho.md
check $? "Agentes copiados (despacho, intake, admin)"

test -f config/triggers.json
check $? "Triggers configurados"

test -f config/hermes-commands.json
check $? "Comandos Hermes definidos"

# Integración
test -d hermes_integration
test -f hermes_integration/commands.py
test -f hermes_integration/session_manager.py
test -f hermes_integration/__init__.py
check $? "Módulo hermes_integration completo"

test -f scripts/hermes_bridge.py
check $? "Script bridge creado"

# Motor (existente)
test -f motor_kami/blocks.py
check $? "Motor Kami preservado"

test -d motor_kami/templates && [ $(ls motor_kami/templates/*.json 2>/dev/null | wc -l) -ge 20 ]
check $? "Templates disponibles (20+)"

# Dashboard (existente)
test -f dashboard/backend/app.py
check $? "Dashboard backend preservado"

# Documentación
test -f docs/MANUAL_HERMES_INTEGRATION.md
check $? "Manual Hermes creado"

test -f docs/ESTRUCTURA_CARPETAS.md
check $? "Estructura carpetas documentada"

# Funcional
test -f datos/matters.json
check $? "Base de datos matters existe"

echo ""
echo "=========================================="
echo "  RESULTADO: $PASS ✅ / $ERRORS ❌"
echo "=========================================="

if [ $ERRORS -eq 0 ]; then
    echo ""
    echo "🎉🎉🎉 HERMES LEGAL PRO v3 DUAL COMPLETADO 🎉🎉🎉"
    echo ""
    echo "El producto ahora funciona en DOS MODOS:"
    echo "  🤖 Hermes Agent (Telegram): /matter, /contrato, /plazo"
    echo "  💻 Dashboard (Mac): http://localhost:8082"
    echo ""
    echo "Ambos modos comparten:"
    echo "  • Motor Kami (23 templates)"
    echo "  • Base de datos (datos/matters.json)"
    echo "  • Carpetas (~/WillowLegal/)"
    echo ""
    echo "Para commitear:"
    echo "  git add -A"
    echo "  git commit -m 'v3 DUAL: Hermes Agent + Dashboard integrados'"
    echo "  git push origin master"
    exit 0
else
    echo ""
    echo "❌ HAY ERRORES. NO COMMITEAR. Corregir primero."
    exit 1
fi
```

---

## 📝 SI ALGO FALLA

### Documentar error
```bash
cd "$REPO_PATH"
echo "$(date '+%Y-%m-%d %H:%M:%S') — TAREA X — ERROR" >> docs/ERRORES_OPENCODE.md
echo "Comando: $COMANDO_FALLIDO" >> docs/ERRORES_OPENCODE.md
echo "Error: $MENSAJE_ERROR" >> docs/ERRORES_OPENCODE.md
echo "---" >> docs/ERRORES_OPENCODE.md
```

### No continuar
Si una tarea falla, **NO** pasar a la siguiente. Detenerse y reportar.

### Reportar a Hermes Neo
Incluir:
1. Qué tarea falló
2. Qué paso específico
3. Output completo del error
4. Estado actual del repo (`git status`, `ls -la`)

---

## ✅ CHECKLIST FINAL PRE-COMMIT

Antes de hacer git commit, verificar:

```bash
cd "$REPO_PATH"

# 1. Todo archivo creado existe
# 2. No hay archivos vacíos (0 bytes)
# 3. Los .py tienen sintaxis válida
# 4. Los .json son parseables
# 5. No se modificó motor_kami/blocks.py
# 6. No se modificó motor_kami/motor_kami.py
# 7. Tests pasan
```

---

## 🚀 COMANDO FINAL

Cuando TODO esté verificado:

```bash
cd "$REPO_PATH"
git add -A
git commit -m "v3 DUAL: Integración Hermes Agent + Dashboard — $(date '+%Y-%m-%d %H:%M:%S')"
git push origin master
echo "✅ Código subido a GitHub"
```

---

**INICIA AHORA con PASO 0 (Preparación).**
**NO saltes ningún paso.**
**Verifica ANTES de continuar.**

**ÉXITO = Producto dual que funciona tanto por Telegram como por Dashboard.**

