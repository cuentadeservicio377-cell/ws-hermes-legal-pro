# PROMPT FIX MOTOR KAMI — Hacer que todo funcione por completo
## Para OpenCode Go | Hermes Legal Pro v3.0

---

## 🎯 OBJETIVO

El frontend de Documentos (FASE 5) y el wizard de generación están listos, pero **no pueden generar PDFs reales** porque el backend reporta `"motor_kami": "no_encontrado"`. 

Necesito que arregles la integración del **Motor Kami** en la Mac para que:
1. El backend encuentre el motor Kami
2. Los templates estén disponibles
3. La generación de PDFs funcione
4. Los documentos aparezcan en la lista con estado "generado"
5. Previsualizar y descargar PDFs funcionen

---

## 🔍 DIAGNÓSTICO DEL PROBLEMA

El backend (`dashboard/backend/app.py`) busca el motor en:
```python
MOTOR_DIR = BASE_DIR / "motor_kami"
```

Donde `BASE_DIR = Path(__file__).parent.parent` → es `~/ws-hermes-legal-pro/`

Pero el `install-mac.sh` copia el motor a:
```
~/WillowLegal/00_Sistema/Motor_Kami/
```

**Resultado:** El backend no encuentra `~/ws-hermes-legal-pro/motor_kami/` → reporta `"no_encontrado"`

---

## 🔧 SOLUCIÓN

Hay **dos opciones**. Elige la más simple:

### Opción A (Recomendada): Copiar motor al repo
Copiar `motor_kami/` desde `~/WillowLegal/00_Sistema/Motor_Kami/` (o donde esté) al directorio base del repo `~/ws-hermes-legal-pro/motor_kami/`

### Opción B: Cambiar ruta en backend
Modificar `dashboard/backend/app.py` para que busque en `~/WillowLegal/00_Sistema/Motor_Kami/`

**Usa Opción A.** Es más limpia y mantiene todo el proyecto autocontenido.

---

## 📋 PASOS A EJECUTAR

### PASO 1: Verificar dónde está el motor

```bash
# Buscar motor_kami en el sistema
find ~ -name "motor_kami.py" -type f 2>/dev/null

# Verificar si está en WillowLegal
ls -la ~/WillowLegal/00_Sistema/Motor_Kami/ 2>/dev/null || echo "No está en WillowLegal"

# Verificar si está en el repo
ls -la ~/ws-hermes-legal-pro/motor_kami/ 2>/dev/null || echo "No está en el repo"
```

### PASO 2: Copiar motor al repo (Opción A)

```bash
cd ~/ws-hermes-legal-pro

# Si el motor está en WillowLegal, copiarlo
if [ -d ~/WillowLegal/00_Sistema/Motor_Kami ]; then
    cp -r ~/WillowLegal/00_Sistema/Motor_Kami ./motor_kami
    echo "✓ Motor copiado desde WillowLegal"
fi

# Si no está en ningún lado, crear la estructura mínima
if [ ! -d ./motor_kami ]; then
    mkdir -p motor_kami/templates motor_kami/output
    echo "⚠ Motor no encontrado en el sistema. Se creó estructura vacía."
    echo "   Necesitarás copiar manualmente los archivos del motor."
fi

# Verificar que ahora existe
ls -la motor_kami/
```

### PASO 3: Verificar dependencias de Python

```bash
# Verificar que weasyprint está instalado
python3 -c "from weasyprint import HTML, CSS; print('✓ WeasyPrint OK')" 2>/dev/null || echo "❌ WeasyPrint no instalado"

# Verificar otras dependencias
python3 -c "import fastapi; print('✓ FastAPI OK')" 2>/dev/null || echo "❌ FastAPI no instalado"
python3 -c "import pydantic; print('✓ Pydantic OK')" 2>/dev/null || echo "❌ Pydantic no instalado"

# Instalar si faltan
pip3 install weasyprint fastapi uvicorn pydantic python-docx openpyxl
```

### PASO 4: Verificar templates

```bash
# Debe haber templates JSON en motor_kami/templates/
ls -la ~/ws-hermes-legal-pro/motor_kami/templates/

# Debe haber al menos index.json
if [ ! -f ~/ws-hermes-legal-pro/motor_kami/templates/index.json ]; then
    echo "❌ No hay templates. El motor no funcionará."
fi
```

### PASO 5: Probar generación de PDF manualmente

```bash
cd ~/ws-hermes-legal-pro

# Crear test JSON
 cat > /tmp/test_kami.json << 'EOF'
{
  "blocks": [
    {"type": "header", "content": "Documento de Prueba"},
    {"type": "paragraph", "content": "Este es un documento generado por Motor Kami."},
    {"type": "signature", "content": "Firma digital"}
  ],
  "options": {"titulo": "Test Document"}
}
EOF

# Ejecutar motor
python3 motor_kami/motor_kami.py --input /tmp/test_kami.json --output /tmp/test_output.pdf

# Verificar que se generó
if [ -f /tmp/test_output.pdf ]; then
    ls -lh /tmp/test_output.pdf
    echo "✓ Motor Kami funciona correctamente"
else
    echo "❌ Error generando PDF"
fi
```

### PASO 6: Probar endpoint del backend

```bash
# Iniciar backend (en otra terminal o background)
cd ~/ws-hermes-legal-pro/dashboard/backend
python3 app.py &

# Esperar 3 segundos
sleep 3

# Verificar health
 curl -s http://localhost:8082/api/health | python3 -m json.tool

# Debe mostrar:
# {
#   "status": "ok",
#   "motor_kami": "ok",
#   ...
# }

# Verificar templates
curl -s http://localhost:8082/api/templates | python3 -m json.tool

# Debe mostrar lista de templates, no vacío
```

### PASO 7: Probar generación vía API

```bash
# Crear un matter primero (si no hay)
curl -s -X POST http://localhost:8082/api/matters \
  -H "Content-Type: application/json" \
  -d '{
    "id": "TEST-001",
    "cliente": "Cliente Prueba",
    "area_practica": "Corporativo",
    "prioridad": "media",
    "estado": "activo"
  }'

# Generar documento
curl -s -X POST http://localhost:8082/api/matter/TEST-001/generar-documento \
  -H "Content-Type: application/json" \
  -d '{
    "template_key": "confidencialidad",
    "output_filename": "test_doc.pdf"
  }' | python3 -m json.tool

# Debe devolver success: true con file_path
```

### PASO 8: Verificar en el frontend

```bash
# Abrir navegador
open http://localhost:8082

# Ir a Documentos → Debe mostrar templates disponibles
# Click "Generar Documento" → Wizard debe funcionar
# Al generar → Debe descargar PDF real
```

---

## 🧪 TESTS DE VERIFICACIÓN

### Test 1: Health check reporta motor ok
```bash
curl -s http://localhost:8082/api/health | grep -q '"motor_kami": "ok"' && echo "✓ PASS" || echo "❌ FAIL"
```

### Test 2: Templates disponibles
```bash
curl -s http://localhost:8082/api/templates | python3 -c "import sys,json; d=json.load(sys.stdin); print('✓ PASS' if d.get('templates') else '❌ FAIL')"
```

### Test 3: Generar PDF vía API
```bash
curl -s -X POST http://localhost:8082/api/matter/TEST-001/generar-documento \
  -H "Content-Type: application/json" \
  -d '{"template_key":"confidencialidad"}' | python3 -c "import sys,json; d=json.load(sys.stdin); print('✓ PASS' if d.get('success') else '❌ FAIL: '+str(d))"
```

### Test 4: PDF existe en disco
```bash
ls -la ~/ws-hermes-legal-pro/motor_kami/output/*.pdf 2>/dev/null && echo "✓ PASS" || echo "❌ FAIL"
```

### Test 5: Frontend muestra documento generado
```bash
# Abrir navegador, ir a Documentos, verificar que aparece el documento
# con estado "generado" y botones "Ver" y "Descargar"
echo "Verificar manualmente en el navegador"
```

---

## ✅ CHECKLIST PARA DAR POR TERMINADO

- [ ] `motor_kami/` existe en `~/ws-hermes-legal-pro/motor_kami/`
- [ ] `motor_kami/motor_kami.py` existe y es ejecutable
- [ ] `motor_kami/templates/` tiene archivos `.json`
- [ ] `motor_kami/templates/index.json` existe
- [ ] WeasyPrint instalado (`python3 -c "from weasyprint import HTML"`)
- [ ] Backend health reporta `"motor_kami": "ok"`
- [ ] Endpoint `/api/templates` devuelve lista no vacía
- [ ] Generar PDF vía API devuelve `success: true`
- [ ] Archivo PDF se crea en `motor_kami/output/`
- [ ] Frontend Documentos muestra templates en el wizard
- [ ] Generar documento desde frontend descarga PDF real
- [ ] Previsualizar PDF abre el documento
- [ ] Descargar PDF guarda el archivo

---

## 📤 ENTREGA

```bash
cd ~/ws-hermes-legal-pro

# Si creaste/copiaste archivos nuevos
git add motor_kami/ dashboard/backend/
git commit -m "FIX: Motor Kami integrado correctamente - generacion de PDFs funcional"
git push origin master
```

**Notificar:** "Motor Kami arreglado. Generación de PDFs funcionando al 100%. Documentos, previsualización y descarga operativos."

---

## 🆘 SI NO FUNCIONA

### Problema: WeasyPrint no instala en Mac M1/M2/M3
```bash
# Solución: Instalar con Homebrew primero
brew install libffi cairo pango gdk-pixbuf libxml2 libxslt

# Luego instalar weasyprint
pip3 install weasyprint

# Verificar
python3 -c "from weasyprint import HTML; print('OK')"
```

### Problema: `libffi` o `cairo` no encontrado
```bash
# Para Mac M1/M2/M3 (ARM64)
export DYLD_LIBRARY_PATH="/opt/homebrew/lib:$DYLD_LIBRARY_PATH"

# Para Mac Intel (x86_64)
export DYLD_LIBRARY_PATH="/usr/local/lib:$DYLD_LIBRARY_PATH"

# Agregar a ~/.zshrc para persistir
echo 'export DYLD_LIBRARY_PATH="/opt/homebrew/lib:$DYLD_LIBRARY_PATH"' >> ~/.zshrc
```

### Problema: No hay templates JSON
```bash
# Si el motor está vacío, copiar desde el repo original o crear mínimo:
mkdir -p motor_kami/templates
cat > motor_kami/templates/index.json << 'EOF'
{
  "templates": [
    {"key": "confidencialidad", "label": "Acuerdo de Confidencialidad (NDA)", "area": "Corporativo"},
    {"key": "prestacion_servicios", "label": "Contrato de Prestación de Servicios", "area": "Laboral"},
    {"key": "arrendamiento", "label": "Contrato de Arrendamiento", "area": "Inmobiliario"}
  ]
}
EOF
```

### Problema: Backend no encuentra motor después de copiar
```bash
# Reiniciar backend completamente
pkill -f "python3 app.py" 2>/dev/null || true
sleep 2
cd ~/ws-hermes-legal-pro/dashboard/backend
python3 app.py
```

---

*Prompt FIX MOTOR KAMI — Diseñado para OpenCode Go*
*Hermes Legal Pro v3.0*
