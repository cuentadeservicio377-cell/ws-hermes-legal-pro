# PROMPT AUTO-CONTENIDO — HERMES LEGAL PRO SE PRUEBA A SÍ MISMO

> **Objetivo:** El agente Hermes Legal Pro (perfil legal-pro) ejecuta un recorrido de prueba completo de su propio sistema, documenta resultados, y genera un reporte.
> **Fecha:** 2026-05-02
> **Repo:** cuentadeservicio377-cell/ws-hermes-legal-pro

---

## INSTRUCCIONES PARA EL AGENTE HERMES

Eres Hermes Legal Pro. Vas a probar tu propio sistema. Tienes acceso a:
- Terminal (bash/zsh)
- Navegador (para screenshots)
- Python 3
- Tu propio backend en localhost:8082
- Tu motor Kami en ~/ws-hermes-legal-pro/motor_kami/
- Tus templates en ~/ws-hermes-legal-pro/motor_kami/templates/

---

## FASE 0: AUTO-DIAGNÓSTICO (2 minutos)

Ejecuta en terminal:

```bash
echo "=== HERMES LEGAL PRO — AUTO-DIAGNÓSTICO ==="
echo "Fecha: $(date)"
echo "Usuario: $(whoami)"
echo "Hostname: $(hostname)"
echo ""

# 1. Verificar repo
cd ~/ws-hermes-legal-pro 2>/dev/null && echo "✅ Repo existe" || echo "❌ Repo NO existe en ~/ws-hermes-legal-pro"

# 2. Verificar archivos críticos
test -f dashboard/backend/app.py && echo "✅ app.py" || echo "❌ app.py"
test -f motor_kami/motor_kami.py && echo "✅ motor_kami.py" || echo "❌ motor_kami.py"
test -f motor_kami/blocks.py && echo "✅ blocks.py" || echo "❌ blocks.py"
test -f hermes_integration/commands.py && echo "✅ commands.py" || echo "❌ commands.py"

# 3. Contar templates
ls motor_kami/templates/*.json 2>/dev/null | wc -l | xargs echo "Templates:"

# 4. Verificar backend corriendo
curl -s http://localhost:8082/api/health 2>/dev/null | head -1 || echo "❌ Backend no responde en :8082"

# 5. Verificar perfil Hermes
hermes config get profile 2>/dev/null || cat ~/.hermes/config.yaml 2>/dev/null | grep profile || echo "⚠️ No se pudo verificar perfil"

echo ""
echo "=== FIN AUTO-DIAGNÓSTICO ==="
```

**Si el backend NO responde:**
```bash
cd ~/ws-hermes-legal-pro/dashboard/backend
nohup uvicorn app:app --host 0.0.0.0 --port 8082 > /tmp/backend.log 2>&1 &
sleep 3
curl -s http://localhost:8082/api/health | python3 -m json.tool
```

---

## FASE 1: PRUEBA BACKEND API (10 minutos)

### Paso 1.1: Health check
```bash
curl -s http://localhost:8082/api/health | python3 -m json.tool
```
**Verificar:** status=ok, motor_kami=ok, templates_count>=23

### Paso 1.2: Crear matter de prueba
```bash
curl -s -X POST http://localhost:8082/api/matters \
  -H "Content-Type: application/json" \
  -d '{"nombre":"TEST_AUTO_HERMES","cliente":"Cliente Auto","area":"Corporativo","materia":"corporativo","prioridad":"alta","descripcion":"Matter de auto-prueba","deadline":"2026-12-31"}' \
  | tee /tmp/matter_test.json | python3 -m json.tool
```
**Guardar ID del matter.**

### Paso 1.3: Listar matters
```bash
curl -s http://localhost:8082/api/matters | python3 -c "import sys,json; d=json.load(sys.stdin); print(f'Total matters: {len(d)}'); [print(f'  {m[\"id\"]}: {m[\"nombre\"]}') for m in d[-3:]]"
```

### Paso 1.4: Generar PDF (PRUEBA CRÍTICA)
```bash
MATTER_ID=$(cat /tmp/matter_test.json | python3 -c "import sys,json; print(json.load(sys.stdin).get('id',''))")
echo "MATTER_ID=$MATTER_ID"

curl -s -X POST "http://localhost:8082/api/matter/$MATTER_ID/generar-documento" \
  -H "Content-Type: application/json" \
  -d '{"template_key":"prestacion_servicios","datos_extra":{"prestador":{"nombre":"WS Capital","rfc":"WSC123","domicilio":"CDMX"},"cliente":{"nombre":"Cliente Auto","rfc":"CLI123","domicilio":"CDMX"},"servicios":"Consultoría","honorarios":"$50,000","plazo":"12 meses"}}' \
  | tee /tmp/doc_test.json | python3 -m json.tool
```

**Verificar:** success=true, file_size_kb > 0

### Paso 1.5: Verificar PDF físico
```bash
PDF_PATH=$(cat /tmp/doc_test.json | python3 -c "import sys,json; print(json.load(sys.stdin).get('file_path',''))")
ls -lh "$PDF_PATH" 2>/dev/null && file "$PDF_PATH" || echo "❌ PDF no encontrado"
```

### Paso 1.6: Validar sustancia
```bash
curl -s -X POST http://localhost:8082/api/kami/validate \
  -H "Content-Type: application/json" \
  -d '{"blocks":[{"type":"parties_block","data":{"prestador":{"nombre":"A"},"cliente":{"nombre":"B"}}},{"type":"clause_section","data":{"numero":"1","titulo":"Objeto","subclausulas":[{"texto":"x"}]}},{"type":"signature_block","data":{"prestador":{},"cliente":{}}}]}' \
  | python3 -m json.tool
```

### Paso 1.7: Dashboard KPIs
```bash
curl -s http://localhost:8082/api/dashboard | python3 -m json.tool
```

---

## FASE 2: PRUEBA MOTOR KAMI CLI (5 minutos)

```bash
cd ~/ws-hermes-legal-pro/motor_kami

# Crear input de prueba
cat > /tmp/kami_test.json << 'EOF'
{
  "blocks": [
    {"type": "header_brand", "data": {"marca": "WS Capital Legal", "numero_documento": "DOC-TEST-001"}},
    {"type": "parties_block", "data": {
      "prestador": {"nombre": "WS Capital", "rfc": "WSC123", "domicilio": "CDMX", "representante": "Lic. Pablo", "email": "p@wsc.com"},
      "cliente": {"nombre": "Cliente Test", "rfc": "CLI123", "domicilio": "CDMX", "representante": "Ing. Juan", "email": "j@cliente.com"}
    }},
    {"type": "clause_section", "data": {"numero": "1", "titulo": "OBJETO", "subclausulas": [
      {"numero": "1.1", "texto": "El PRESTADOR se obliga a prestar servicios."},
      {"numero": "1.2", "texto": "El CLIENTE se obliga a pagar."}
    ]}},
    {"type": "payment_table", "data": {"headers": ["Concepto", "Monto"], "rows": [["Mensual", "$50,000"]]}},
    {"type": "signature_block", "data": {
      "prestador": {"nombre": "Lic. Pablo", "puesto": "Director"},
      "cliente": {"nombre": "Ing. Juan", "puesto": "CEO"},
      "testigo1": {"nombre": "Testigo 1", "puesto": "Notario"},
      "testigo2": {"nombre": "Testigo 2", "puesto": "Abogado"}
    }}
  ],
  "options": {"titulo": "Contrato de Prueba Kami v3"}
}
EOF

# Generar PDF
python3 motor_kami.py --input /tmp/kami_test.json --output /tmp/kami_output.pdf 2>&1 | tee /tmp/kami_cli.log
echo "Exit code: $?"
ls -lh /tmp/kami_output.pdf 2>/dev/null && file /tmp/kami_output.pdf || echo "❌ Fallo generación CLI"
```

---

## FASE 3: PRUEBA FRONTEND (Navegador + Screenshots) (10 minutos)

Abrir navegador y navegar a `http://localhost:8082`

### Paso 3.1: Screenshot del Dashboard
Navegar a localhost:8082, tomar screenshot.
Verificar: KPIs visibles, sidebar cargado, sin errores 404.

### Paso 3.2: Navegar a Matters
Click en "Matters" en sidebar.
Tomar screenshot.
Verificar: Tabla cargada, matter de prueba visible.

### Paso 3.3: Generar documento desde frontend
Click en "Documentos" → seleccionar template → generar.
Tomar screenshot del resultado.
Verificar: Toast de éxito, documento en lista.

### Paso 3.4: Ver PDF generado
Click en "Descargar PDF" o abrir PDF generado.
Tomar screenshot del PDF abierto.
Verificar: Diseño Kami aplicado (tipografía, colores, estructura).

### Paso 3.5: Vista Calendario
Click en "Calendario".
Tomar screenshot.
Verificar: Calendario mensual renderizado.

### Paso 3.6: Vista Finanzas
Click en "Finanzas".
Tomar screenshot.
Verificar: Formulario y lista visibles.

---

## FASE 4: PRUEBA HERMES AGENT (Comandos) (5 minutos)

### Paso 4.1: Importar commands.py
```bash
python3 -c "
from hermes_integration.commands import HermesLegalCommands
cmd = HermesLegalCommands()
print('✅ Import OK')
print(f'Matters file: {cmd.matters_file}')
print(f'Motor dir: {cmd.motor_dir}')
"
```

### Paso 4.2: Crear matter vía Python
```bash
python3 -c "
from hermes_integration.commands import HermesLegalCommands
import json
cmd = HermesLegalCommands()
r = cmd.crear_matter('Matter Python Auto', area='Laboral')
print(json.dumps(r, indent=2, ensure_ascii=False))
" | tee /tmp/matter_py.json
```

### Paso 4.3: Generar contrato vía Python
```bash
python3 -c "
from hermes_integration.commands import HermesLegalCommands
import json
cmd = HermesLegalCommands()
matters = cmd.listar_matters()
if matters:
    r = cmd.generar_contrato(matters[-1]['id'], 'prestacion_servicios', {
        'prestador': {'nombre': 'WS Capital'},
        'cliente': {'nombre': 'Cliente Python'}
    })
    print(json.dumps(r, indent=2, ensure_ascii=False))
"
```

---

## FASE 5: LIMPIEZA (2 minutos)

```bash
# Eliminar matters de prueba
cd ~/ws-hermes-legal-pro

# Listar matters de prueba
curl -s http://localhost:8082/api/matters | python3 -c "
import json, sys
d = json.load(sys.stdin)
for m in d:
    n = m.get('nombre','')
    if any(x in n for x in ['TEST', 'test', 'AUTO', 'Python']):
        print(f'ELIMINAR: {m[\"id\"]} - {n}')
"

# Eliminar (uno por uno si es necesario)
```

---

## FASE 6: GENERAR REPORTE (5 minutos)

Crear archivo `~/ws-hermes-legal-pro/docs/REPORTE_AUTO_PRUEBA_v3.md`

Estructura:
```markdown
# Reporte de Auto-Prueba — Hermes Legal Pro v3

**Fecha:** {fecha}
**Agente:** Hermes Legal Pro (auto-prueba)
**Commit:** {git log --oneline -1}

## Resumen

| Fase | Estado | Notas |
|------|--------|-------|
| 0. Auto-diagnóstico | ✅/❌ | |
| 1. Backend API | ✅/❌ | |
| 2. Motor Kami CLI | ✅/❌ | |
| 3. Frontend SPA | ✅/❌ | |
| 4. Hermes Agent | ✅/❌ | |
| 5. Limpieza | ✅/❌ | |

## Detalles

### Fase 1: Backend API
{pegar outputs de curls}

### Fase 2: Motor Kami
{pegar output de motor_kami.py}

### Fase 3: Frontend
{describir screenshots tomados}

### Fase 4: Hermes Agent
{pegar outputs de Python}

## Errores
{listar errores encontrados}

## Screenshots
{listar screenshots tomados}

## Conclusión
{Sistema operativo / Parcial / Requiere atención}
```

Commitear y pushear:
```bash
cd ~/ws-hermes-legal-pro
git add docs/REPORTE_AUTO_PRUEBA_v3.md
git commit -m "TEST: Reporte auto-prueba v3 — $(date +%Y-%m-%d)"
git push origin master
```

---

## NOTAS PARA EL AGENTE

1. **Si el backend no responde:** Iniciarlo con `uvicorn app:app --host 0.0.0.0 --port 8082`
2. **Si Motor Kami falla:** Verificar WeasyPrint instalado: `python3 -c "import weasyprint"`
3. **Si falta dependencia:** Documentar en reporte, NO detenerse
4. **Screenshots:** Tomar con herramienta disponible (screencapture en Mac, o browser screenshot)
5. **Si no puedes tomar screenshot:** Describir visualmente lo que ves

---

*Prompt auto-contenido para que Hermes Legal Pro se pruebe a sí mismo.*
