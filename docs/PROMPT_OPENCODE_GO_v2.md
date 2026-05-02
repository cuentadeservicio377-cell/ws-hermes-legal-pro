# PROMPT EJECUTABLE: OpenCode Go — Hermes Legal Pro v2

> **Modelo:** gpt-5.4-mini (o el disponible en OpenCode Go)
> **Contexto:** MacBook Air M2 de Pablo, repo clonado localmente
> **Plan:** docs/PLAN_MAESTRO_v2.md
> **Fecha:** 2026-05-01

---

## 🎯 TU MISIÓN

Eres OpenCode Go. Debes ejecutar el **PLAN MAESTRO v2** en el repo `ws-hermes-legal-pro` que está clonado en la Mac de Pablo.

**Regla #1:** Lee el plan completo antes de empezar: `docs/PLAN_MAESTRO_v2.md`
**Regla #2:** Ejecuta las tareas en ORDEN (1 → 2 → 3 → 4 → 5)
**Regla #3:** Verifica cada tarea antes de pasar a la siguiente
**Regla #4:** Si algo falla, documenta el error y PIDE AYUDA, no improvises

---

## 📁 UBICACIÓN DEL REPO

```
~/ws-hermes-legal-pro/          (o donde Pablo lo haya clonado)
```

Si no sabes dónde está:
```bash
find ~ -type d -name "ws-hermes-legal-pro" 2>/dev/null | head -1
```

---

## 🔧 TAREA 1: Copiar assets de Paperclip

### Paso 1.1: Clonar Paperclip (si no está)
```bash
cd /tmp
git clone https://github.com/cuentadeservicio377-cell/willow-paperclip-portable.git paperclip-assets
```

### Paso 1.2: Crear directorios y copiar
```bash
cd ~/ws-hermes-legal-pro

# Crear directorio agents/
mkdir -p agents/

# Copiar agentes
cp /tmp/paperclip-assets/company/workspace/agents/despacho.md agents/
cp /tmp/paperclip-assets/company/workspace/agents/intake.md agents/
cp /tmp/paperclip-assets/company/workspace/agents/admin.md agents/

# Copiar triggers
cp /tmp/paperclip-assets/company/workspace/triggers/willow-triggers.json config/triggers.json

# Documentar estructura de carpetas
grep -A 30 "Regla de carpeta fuente" agents/despacho.md > docs/ESTRUCTURA_CARPETAS.md
echo "" >> docs/ESTRUCTURA_CARPETAS.md
echo "## Estructura mínima de carpeta por asunto" >> docs/ESTRUCTURA_CARPETAS.md
grep -A 20 "Estructura de carpetas" agents/despacho.md >> docs/ESTRUCTURA_CARPETAS.md || true
```

### Paso 1.3: Verificar
```bash
cd ~/ws-hermes-legal-pro

echo "=== VERIFICACIÓN TAREA 1 ==="
test -f agents/despacho.md && echo "✅ despacho.md" || echo "❌ FALTA despacho.md"
test -f agents/intake.md && echo "✅ intake.md" || echo "❌ FALTA intake.md"
test -f agents/admin.md && echo "✅ admin.md" || echo "❌ FALTA admin.md"
test -f config/triggers.json && echo "✅ triggers.json" || echo "❌ FALTA triggers.json"
test -f docs/ESTRUCTURA_CARPETAS.md && echo "✅ ESTRUCTURA_CARPETAS.md" || echo "❌ FALTA ESTRUCTURA_CARPETAS.md"

# Contar líneas de cada agente
wc -l agents/*.md
```

**Si todo está ✅ → Continuar a Tarea 2**
**Si algo falta ❌ → Documentar error y detenerse**

---

## 🔧 TAREA 2: Merge catálogo templates

### Paso 2.1: Leer ambos catálogos
```bash
cd ~/ws-hermes-legal-pro

# Verificar que existen ambos
ls motor_kami/templates/index.json
ls /tmp/paperclip-assets/company/workspace/library/willow-template-library.json
```

### Paso 2.2: Ejecutar script de merge
```bash
cd ~/ws-hermes-legal-pro
python3 << 'EOF'
import json

# Leer catálogo actual del motor
with open('motor_kami/templates/index.json') as f:
    motor_catalog = json.load(f)

# Leer catálogo de Paperclip
with open('/tmp/paperclip-assets/company/workspace/library/willow-template-library.json') as f:
    paperclip_catalog = json.load(f)

# Crear diccionario de Paperclip por key
paperclip_by_key = {t['key']: t for t in paperclip_catalog}

# Para cada template en motor, mergear metadata de Paperclip
merged_count = 0
for template in motor_catalog.get('templates', motor_catalog if isinstance(motor_catalog, list) else []):
    key = template.get('key', template.get('slug', ''))
    if key in paperclip_by_key:
        pc = paperclip_by_key[key]
        # Mergear campos que no existan
        if 'area' not in template and 'area' in pc:
            template['area'] = pc['area']
        if 'materia' not in template and 'materia' in pc:
            template['materia'] = pc['materia']
        if 'descripcion' not in template and 'descripcion' in pc:
            template['descripcion'] = pc['descripcion']
        if 'estado' not in template and 'estado' in pc:
            template['estado'] = pc['estado']
        merged_count += 1
        print(f"✅ Mergeado: {key}")
    else:
        print(f"⚠️  No encontrado en Paperclip: {key}")

# Guardar resultado
with open('motor_kami/templates/index.json', 'w') as f:
    json.dump(motor_catalog, f, indent=2, ensure_ascii=False)

print(f"\n=== RESUMEN ===")
print(f"Templates en motor: {len(motor_catalog if isinstance(motor_catalog, list) else motor_catalog.get('templates', []))}")
print(f"Mergeados con Paperclip: {merged_count}")
EOF
```

### Paso 2.3: Verificar
```bash
cd ~/ws-hermes-legal-pro
python3 -c "import json; d=json.load(open('motor_kami/templates/index.json')); templates = d if isinstance(d, list) else d.get('templates', []); print(f'{len(templates)} templates con metadata completa'); [print(f'  {t.get(\"key\", t.get(\"slug\"))}: {t.get(\"area\", \"N/A\")}/{t.get(\"materia\", \"N/A\")}') for t in templates[:5]]"
```

**Si todo está ✅ → Continuar a Tarea 3**
**Si algo falla ❌ → Documentar error y detenerse**

---

## 🔧 TAREA 3: Actualizar README

### Paso 3.1: Backup y editar
```bash
cd ~/ws-hermes-legal-pro
cp README.md README.md.bak
```

### Paso 3.2: Agregar sección de Agentes
Insertar después de "### Funcionalidades principales":

```markdown
### 🤖 Agentes Legales Integrados

- **Despacho Legal** — Orquestador principal del despacho. Gestiona asuntos, delega a especialistas, mantiene expediente vivo.
- **Recepcionista Jurídico (Intake)** — Operador de metadatos y estructura. Abre/reusa clientes y matters, crea carpetas, registra en Sheets.
- **Administrador del Despacho** — Biblioteca, estándares, reportes, compounding de lecciones aprendidas.

### 🎯 Triggers Operativos (13)

| Trigger | Agente | Uso |
|---------|--------|-----|
| nuevo_asunto | intake | Alta de cliente/matter |
| generar_documento | documentos | Crear contrato/NDA/carta |
| generar_paquete | documentos | Paquete documental completo |
| tarea | asuntos | Tarea con deadline |
| plazo_judicial | asuntos | Plazo procesal |
| actualizacion | asuntos | Estado del asunto |
| cerrar_asunto | asuntos | Cierre operativo |
| anticipo_recibido | cobranza | Registro de pago |
| abono_recibido | cobranza | Abono parcial |
| pago_final_recibido | cobranza | Liquidación |
| reporte_semanal | admin | Reporte operativo |
| reporte_matter | admin | Reporte específico |
| leccion_aprendida | admin | Mejora continua |

### 📁 Estructura de Carpetas

Cada asunto mantiene esta estructura en Drive/local:
```
00-Insumos crudos
01-Expediente vivo
02-Demanda inicial
03-Estrategia de litigio
04-Anexos y evidencia
05-Versiones aprobadas
```
```

### Paso 3.3: Verificar
```bash
cd ~/ws-hermes-legal-pro
grep -c "Agentes Legales" README.md && echo "✅ Agentes agregados"
grep -c "Triggers Operativos" README.md && echo "✅ Triggers agregados"
grep -c "Estructura de Carpetas" README.md && echo "✅ Carpetas agregadas"
```

**Si todo está ✅ → Continuar a Tarea 4**
**Si algo falla ❌ → Documentar error y detenerse**

---

## 🔧 TAREA 4: Script de instalación unificado

### Paso 4.1: Crear install.sh
```bash
cd ~/ws-hermes-legal-pro

cat > install.sh << 'EOF'
#!/bin/bash
# install.sh — Instalación unificada de Hermes Legal Pro v2
# Uso: ./install.sh [--dry-run]

set -e

DRY_RUN=false
if [ "$1" == "--dry-run" ]; then
    DRY_RUN=true
    echo "🔍 DRY RUN — No se ejecutarán cambios"
fi

echo "⚖️  Instalando Hermes Legal Pro v2..."

# 1. Verificar Python
PYTHON_VERSION=$(python3 --version 2>/dev/null | grep -o '3\.[0-9]*' || echo "")
if [ -z "$PYTHON_VERSION" ]; then
    echo "❌ Python 3 no encontrado. Instalar: brew install python@3.11"
    exit 1
fi
echo "✅ Python $PYTHON_VERSION"

# 2. Verificar pip
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 no encontrado"
    exit 1
fi

# 3. Instalar dependencias Python
DEPS="weasyprint fastapi uvicorn python-multipart sqlalchemy pydantic"
if [ "$DRY_RUN" = false ]; then
    echo "📦 Instalando dependencias..."
    pip3 install $DEPS
else
    echo "🔍 Instalaría: $DEPS"
fi

# 4. Crear estructura de carpetas
WILLOW_DIR="$HOME/WillowLegal"
if [ "$DRY_RUN" = false ]; then
    mkdir -p "$WILLOW_DIR"/{00_Sistema,01_Clientes,02_Administracion,03_Biblioteca_Legal,04_Agentes_Onyx,05_Backups}
    mkdir -p "$WILLOW_DIR/00_Sistema"/{Motor_Kami,scripts,docs}
    mkdir -p "$WILLOW_DIR/01_Clientes/Cliente_Nuevo_1"/{01_Intake,02_Contratos/Borradores,02_Contratos/Firmados,03_Correspondencia,04_Litigio,05_Facturacion,06_Entregables,07_Archivo}
    echo "✅ Carpetas creadas en $WILLOW_DIR"
else
    echo "🔍 Crearía carpetas en $WILLOW_DIR"
fi

# 5. Copiar motor y templates
if [ "$DRY_RUN" = false ]; then
    cp -r motor_kami "$WILLOW_DIR/00_Sistema/Motor_Kami/"
    cp -r agents "$WILLOW_DIR/00_Sistema/"
    cp -r config "$WILLOW_DIR/00_Sistema/"
    echo "✅ Motor y templates copiados"
fi

# 6. Verificar Motor Kami
if [ "$DRY_RUN" = false ]; then
    cd "$WILLOW_DIR/00_Sistema/Motor_Kami"
    python3 motor_kami.py --template nda --test && echo "✅ Motor Kami funcional"
fi

# 7. Iniciar dashboard
if [ "$DRY_RUN" = false ]; then
    cd ~/ws-hermes-legal-pro/dashboard/backend
    echo "🚀 Iniciando dashboard en http://localhost:8082"
    python3 -m uvicorn app:app --host 0.0.0.0 --port 8082 &
fi

echo ""
echo "🎉 Hermes Legal Pro v2 instalado"
echo "📊 Dashboard: http://localhost:8082"
echo "📁 Carpetas: $WILLOW_DIR"
echo ""
EOF

chmod +x install.sh
```

### Paso 4.2: Verificar
```bash
cd ~/ws-hermes-legal-pro
test -f install.sh && echo "✅ install.sh creado"
bash -n install.sh && echo "✅ Sintaxis válida"
```

**Si todo está ✅ → Continuar a Tarea 5**
**Si algo falla ❌ → Documentar error y detenerse**

---

## 🔧 TAREA 5: Test end-to-end

### Paso 5.1: Test de Motor Kami
```bash
cd ~/ws-hermes-legal-pro/motor_kami

# Test generación de NDA
python3 motor_kami.py --template nda --test 2>&1 | head -20

# Verificar PDF generado
ls -la output/test_*.pdf 2>/dev/null || echo "⚠️ No hay PDFs de test"

# Si no hay script de test, crear uno mínimo
python3 << 'PYEOF'
import sys
sys.path.insert(0, '.')
try:
    from blocks import validar_sustancia
    print("✅ blocks.py importa correctamente")
except Exception as e:
    print(f"❌ Error importando blocks.py: {e}")
    sys.exit(1)

try:
    import motor_kami
    print("✅ motor_kami.py importa correctamente")
except Exception as e:
    print(f"❌ Error importando motor_kami.py: {e}")
    sys.exit(1)

print("\n✅ Motor Kami importable")
PYEOF
```

### Paso 5.2: Test de Dashboard
```bash
# Verificar que backend inicia
cd ~/ws-hermes-legal-pro/dashboard/backend
python3 -c "import app; print('✅ Backend importa correctamente')" 2>&1 | head -5

# Verificar endpoints principales (si está corriendo)
curl -s http://localhost:8082/api/health 2>/dev/null | head -c 100 || echo "⚠️ Dashboard no está corriendo (normal si no se inició)"
```

### Paso 5.3: Verificación final
```bash
cd ~/ws-hermes-legal-pro

echo ""
echo "=========================================="
echo "  VERIFICACIÓN FINAL HERMES LEGAL PRO v2"
echo "=========================================="
echo ""

# 1. Estructura
[ -d agents ] && [ -f agents/despacho.md ] && echo "✅ Agentes" || echo "❌ Agentes"
[ -f config/triggers.json ] && echo "✅ Triggers" || echo "❌ Triggers"
[ -d motor_kami/templates ] && [ $(ls motor_kami/templates/*.json 2>/dev/null | wc -l) -ge 20 ] && echo "✅ Templates (20+)" || echo "❌ Templates"
[ -f motor_kami/blocks.py ] && echo "✅ Motor Kami" || echo "❌ Motor Kami"
[ -f dashboard/backend/app.py ] && echo "✅ Dashboard" || echo "❌ Dashboard"
[ -f install.sh ] && echo "✅ Script instalación" || echo "❌ Script instalación"

# 2. Motor funcional
python3 -c "import sys; sys.path.insert(0, 'motor_kami'); from blocks import validar_sustancia; print('✅ Motor importable')" 2>/dev/null || echo "❌ Motor no importable"

# 3. Git
git status --short | wc -l | grep -q "^0$" && echo "✅ Git limpio" || echo "⚠️ Hay cambios sin commitear"

echo ""
echo "=========================================="
```

---

## 📝 SI ALGO FALLA

1. **Documentar error:**
```bash
echo "$(date): TAREA X falló — descripción" >> docs/ERRORES.md
```

2. **No continuar** a la siguiente tarea

3. **Reportar a Hermes Neo:**
   - Qué tarea falló
   - Mensaje de error exacto
   - Output del comando que falló

---

## ✅ CRITERIO DE ÉXITO

Al finalizar, esto debe ser verdadero:

```bash
cd ~/ws-hermes-legal-pro
[ -d agents ] && [ -f agents/despacho.md ] && \
[ -f config/triggers.json ] && \
[ -d motor_kami/templates ] && \
[ -f motor_kami/blocks.py ] && \
[ -f dashboard/backend/app.py ] && \
[ -f install.sh ] && \
echo "🎉 HERMES LEGAL PRO v2 LISTO" || echo "❌ Faltan componentes"
```

---

**Inicia con la TAREA 1 ahora.**
**Lee el plan completo antes de tocar cualquier archivo.**
**Verifica cada paso antes de continuar.**

