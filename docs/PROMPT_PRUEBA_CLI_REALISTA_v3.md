# PROMPT EJECUTABLE REALISTA — PRUEBA CLI HERMES LEGAL PRO v3

> **Objetivo:** Ejecutar prueba end-to-end vía CLI (curl + Python). Documentar qué se puede probar y qué requiere intervención humana.
> **Autor:** Hermes Neo
> **Fecha:** 2026-05-02
> **Repo:** cuentadeservicio377-cell/ws-hermes-legal-pro
> **Commit base:** 9311cbe (master)

---

## INSTRUCCIONES PARA OPENCODE GO

1. Lee este archivo completo antes de ejecutar nada.
2. Ejecuta cada fase en orden. NO saltar pasos.
3. Si algo falla, documenta el error EXACTO y continúa.
4. Guarda TODO el output en un log.
5. Al final, genera `docs/REPORTE_PRUEBA_CLI_v3.md`.

---

## ANTES DE EMPEZAR — VERIFICACIONES

```bash
cd ~/ws-hermes-legal-pro
git log --oneline -1
# Debe mostrar: 9311cbe o más reciente
```

**Si el commit no es 9311cbe o más reciente:**
```bash
git pull origin master
```

---

## FASE 0: PREPARACIÓN (5 minutos)

### Paso 0.1: Verificar archivos críticos
```bash
cd ~/ws-hermes-legal-pro
test -f dashboard/backend/app.py && echo "✅ app.py" || echo "❌ app.py NO EXISTE"
test -f motor_kami/motor_kami.py && echo "✅ motor_kami.py" || echo "❌ motor_kami.py NO EXISTE"
test -f motor_kami/blocks.py && echo "✅ blocks.py" || echo "❌ blocks.py NO EXISTE"
test -f hermes_integration/commands.py && echo "✅ commands.py" || echo "❌ commands.py NO EXISTE"
test -d motor_kami/templates && echo "✅ templates/" || echo "❌ templates/ NO EXISTE"
ls motor_kami/templates/*.json | wc -l | xargs echo "Templates JSON:"
```

**Checkpoint:** Deben existir los 5 archivos/directorios. Debe haber 23+ templates JSON.

### Paso 0.2: Verificar dependencias Python
```bash
python3 -c "import fastapi; print('FastAPI OK')" 2>&1
python3 -c "import uvicorn; print('Uvicorn OK')" 2>&1
python3 -c "import weasyprint; print('WeasyPrint OK')" 2>&1
python3 -c "import pydantic; print('Pydantic OK')" 2>&1
python3 -c "import google.auth; print('Google Auth OK')" 2>&1 || echo "⚠️ Google Auth no disponible"
```

**Checkpoint:** FastAPI, Uvicorn, WeasyPrint, Pydantic deben funcionar. Google Auth puede fallar si no hay token.

### Paso 0.3: Iniciar backend
```bash
cd ~/ws-hermes-legal-pro/dashboard/backend
# Matar proceso anterior si existe
pkill -f "uvicorn app:app" 2>/dev/null || true
sleep 2
# Iniciar en background
nohup uvicorn app:app --host 0.0.0.0 --port 8082 --reload > /tmp/backend.log 2>&1 &
echo "Backend PID: $!"
sleep 3
# Verificar
curl -s http://localhost:8082/api/health | python3 -m json.tool 2>/dev/null || echo "❌ Backend no responde"
```

**Checkpoint:** Health check debe retornar JSON con status.

---

## FASE 1: BACKEND API — CURL COMPLETO (15 minutos)

### Paso 1.1: Health check detallado
```bash
curl -s http://localhost:8082/api/health | python3 -m json.tool
```

**Guardar output.** Verificar:
- `status` == "ok"
- `motor_kami` == "ok"
- `templates_count` >= 23

### Paso 1.2: Crear matter de prueba
```bash
curl -s -X POST http://localhost:8082/api/matters \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "CLIENTE PRUEBA E2E",
    "cliente": "Empresa Prueba SA de CV",
    "area": "Corporativo",
    "materia": "corporativo",
    "prioridad": "alta",
    "descripcion": "Matter de prueba para recorrido CLI",
    "deadline": "2026-12-31"
  }' | tee /tmp/matter_created.json | python3 -m json.tool
```

**Guardar `id` del matter en variable:**
```bash
MATTER_ID=$(cat /tmp/matter_created.json | python3 -c "import sys,json; print(json.load(sys.stdin).get('id',''))")
echo "MATTER_ID=$MATTER_ID"
```

**Checkpoint:** MATTER_ID debe tener formato WIL-XXX. Si está vacío, documentar error.

### Paso 1.3: Listar matters
```bash
curl -s http://localhost:8082/api/matters | python3 -m json.tool | head -60
```

**Verificar:** Matter creado aparece en lista.

### Paso 1.4: Obtener detalle del matter
```bash
curl -s "http://localhost:8082/api/matters/$MATTER_ID" | python3 -m json.tool
```

**Verificar:** Todos los campos completos, carpeta existe.

### Paso 1.5: Actualizar matter
```bash
curl -s -X PUT "http://localhost:8082/api/matters/$MATTER_ID" \
  -H "Content-Type: application/json" \
  -d '{"estado": "Activo", "next_step": "Generar contrato"}' | python3 -m json.tool
```

**Verificar:** Estado cambiado a "Activo".

### Paso 1.6: Crear reunión
```bash
curl -s -X POST http://localhost:8082/api/reuniones \
  -H "Content-Type: application/json" \
  -d "{
    \"matter_id\": \"$MATTER_ID\",
    \"cliente\": \"Empresa Prueba SA de CV\",
    \"fecha\": \"2026-05-02\",
    \"resumen\": \"Reunión inicial\",
    \"acuerdos\": [\"Definir alcance\"],
    \"documentos_necesarios\": [\"Contrato\"]
  }" | tee /tmp/reunion_created.json | python3 -m json.tool
```

**Guardar REUNION_ID.**

### Paso 1.7: Listar templates
```bash
curl -s http://localhost:8082/api/templates | python3 -m json.tool | head -80
```

**Contar templates:**
```bash
curl -s http://localhost:8082/api/templates | python3 -c "import sys,json; d=json.load(sys.stdin); print(f'Templates: {len(d)}')"
```

**Checkpoint:** Debe haber 23 templates.

### Paso 1.8: Obtener template prestacion_servicios
```bash
curl -s http://localhost:8082/api/templates/prestacion_servicios | python3 -m json.tool | head -40
```

**Verificar:** Tiene `metadata`, `recommended_blocks`, `document_data_template`.

### Paso 1.9: Generar PDF (PRUEBA CRÍTICA)
```bash
curl -s -X POST "http://localhost:8082/api/matter/$MATTER_ID/generar-documento" \
  -H "Content-Type: application/json" \
  -d '{
    "template_key": "prestacion_servicios",
    "datos_extra": {
      "prestador": {"nombre": "WS Capital", "rfc": "WSC123456ABC", "domicilio": "CDMX"},
      "cliente": {"nombre": "Empresa Prueba", "rfc": "EPS987654XYZ", "domicilio": "CDMX"},
      "servicios": "Consultoría legal",
      "honorarios": "$50,000 MXN",
      "plazo": "12 meses"
    }
  }' | tee /tmp/doc_generated.json | python3 -m json.tool
```

**Guardar `file_path` del response.**

**Checkpoint CRÍTICO:**
- `success` debe ser `true`
- `file_size_kb` debe ser > 0
- `file_path` debe existir

### Paso 1.10: Verificar PDF físico
```bash
PDF_PATH=$(cat /tmp/doc_generated.json | python3 -c "import sys,json; print(json.load(sys.stdin).get('file_path',''))")
echo "PDF_PATH=$PDF_PATH"
ls -lh "$PDF_PATH" 2>/dev/null || echo "❌ PDF NO EXISTE"
file "$PDF_PATH" 2>/dev/null || echo "❌ No se pudo verificar tipo"
```

**Checkpoint:** Archivo debe existir y ser tipo PDF.

### Paso 1.11: Validar sustancia legal
```bash
curl -s -X POST http://localhost:8082/api/kami/validate \
  -H "Content-Type: application/json" \
  -d '{
    "blocks": [
      {"type": "parties_block", "data": {"prestador": {"nombre": "A"}, "cliente": {"nombre": "B"}}},
      {"type": "clause_section", "data": {"numero": "1", "titulo": "Objeto", "subclausulas": [{"texto": "x"}]}},
      {"type": "signature_block", "data": {"prestador": {}, "cliente": {}}}
    ]
  }' | python3 -m json.tool
```

**Verificar:** Response tiene `valido` (true/false).

### Paso 1.12: Crear plazo
```bash
curl -s -X POST http://localhost:8082/api/plazo \
  -H "Content-Type: application/json" \
  -d "{
    \"matter_id\": \"$MATTER_ID\",
    \"titulo\": \"Entrega propuesta\",
    \"descripcion\": \"Entregar propuesta\",
    \"fecha\": \"2026-05-10\",
    \"prioridad\": \"alta\"
  }" | python3 -m json.tool
```

### Paso 1.13: Listar plazos
```bash
curl -s http://localhost:8082/api/plazos | python3 -m json.tool | head -40
```

### Paso 1.14: Verificar alertas
```bash
curl -s http://localhost:8082/api/alertas | python3 -m json.tool | head -40
```

### Paso 1.15: Dashboard KPIs
```bash
curl -s http://localhost:8082/api/dashboard | python3 -m json.tool
```

---

## FASE 2: MOTOR KAMI STANDALONE (5 minutos)

### Paso 2.1: Generar PDF vía CLI directo
```bash
cd ~/ws-hermes-legal-pro/motor_kami

cat > /tmp/test_kami.json << 'EOF'
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

python3 motor_kami.py --input /tmp/test_kami.json --output /tmp/test_kami_output.pdf 2>&1 | tee /tmp/kami_cli.log
echo "Exit code: $?"
```

**Checkpoint CRÍTICO:**
- Exit code 0
- Archivo `/tmp/test_kami_output.pdf` existe
- Tamaño > 5KB

### Paso 2.2: Verificar PDF generado
```bash
ls -lh /tmp/test_kami_output.pdf
file /tmp/test_kami_output.pdf
```

### Paso 2.3: Verificar templates tienen estructura correcta
```bash
# Verificar que templates tienen recommended_blocks
python3 -c "
import json, sys
for f in ['prestacion_servicios', 'nda', 'contrato_trabajo', 'arrendamiento']:
    try:
        with open(f'templates/{f}.json') as fh:
            d = json.load(fh)
            blocks = d.get('recommended_blocks', [])
            print(f'{f}: {len(blocks)} blocks - {blocks[:3]}...')
    except Exception as e:
        print(f'{f}: ERROR - {e}')
" 2>/dev/null || echo "⚠️ No se pudo verificar estructura de templates"
```

---

## FASE 3: HERMES INTEGRATION — COMANDOS PYTHON (5 minutos)

### Paso 3.1: Importar módulo de comandos
```bash
cd ~/ws-hermes-legal-pro
python3 -c "
from hermes_integration.commands import HermesLegalCommands
cmd = HermesLegalCommands()
print('✅ HermesLegalCommands importado')
print(f'Datos dir: {cmd.datos_dir}')
print(f'Motor dir existe: {cmd.motor_dir.exists()}')
" 2>&1
```

**Checkpoint:** Importación exitosa.

### Paso 3.2: Crear matter vía Python
```bash
python3 -c "
from hermes_integration.commands import HermesLegalCommands
import json
cmd = HermesLegalCommands()
result = cmd.crear_matter('Matter Python Test', area='Laboral', prioridad='media')
print(json.dumps(result, indent=2, ensure_ascii=False))
" 2>&1 | tee /tmp/matter_python.json
```

**Guardar MATTER_ID_PYTHON.**

### Paso 3.3: Listar matters vía Python
```bash
python3 -c "
from hermes_integration.commands import HermesLegalCommands
import json
cmd = HermesLegalCommands()
matters = cmd.listar_matters()
print(f'Matters: {len(matters)}')
for m in matters[-3:]:
    print(f'  {m[\"id\"]}: {m[\"nombre\"]} ({m[\"estado\"]})')
" 2>&1
```

### Paso 3.4: Generar contrato vía Python
```bash
python3 -c "
from hermes_integration.commands import HermesLegalCommands
import json
cmd = HermesLegalCommands()
# Usar último matter creado
matters = cmd.listar_matters()
if matters:
    m = matters[-1]
    result = cmd.generar_contrato(m['id'], 'prestacion_servicios', {
        'prestador': {'nombre': 'WS Capital'},
        'cliente': {'nombre': 'Cliente Python'}
    })
    print(json.dumps(result, indent=2, ensure_ascii=False))
else:
    print('❌ No hay matters')
" 2>&1 | tee /tmp/contrato_python.json
```

**Checkpoint:** Si hay matters, debe generar contrato.

---

## FASE 4: GOOGLE WORKSPACE (Condicional — 5 minutos)

**NOTA:** Esta fase puede fallar si no hay token de Google válido. Documentar el estado.

### Paso 4.1: Verificar token Google
```bash
ls -la ~/.config/gcloud/application_default_credentials.json 2>/dev/null || \
ls -la ~/.hermes/google_token.json 2>/dev/null || \
echo "❌ No hay token Google encontrado"
```

**Si NO hay token:** Saltar toda Fase 4. Documentar: "Google Workspace no configurado".

**Si SÍ hay token:**

### Paso 4.2: Probar Drive Manager
```bash
python3 -c "
from scripts.drive_manager import DriveManager
d = DriveManager()
print('✅ DriveManager inicializado')
# Intentar listar carpetas root
folders = d.list_folders()
print(f'Carpetas en Drive: {len(folders)}')
" 2>&1 | head -20
```

### Paso 4.3: Crear carpeta de prueba
```bash
python3 -c "
from scripts.drive_manager import DriveManager
d = DriveManager()
result = d.create_folder('TEST_HERMES_LEGAL_PRO')
print(json.dumps(result, indent=2, ensure_ascii=False) if hasattr(result, 'items') else str(result))
" 2>&1 | tee /tmp/drive_test.json
```

---

## FASE 5: LIMPIEZA (2 minutos)

### Paso 5.1: Eliminar matters de prueba
```bash
# Identificar matters de prueba
curl -s http://localhost:8082/api/matters | python3 -c "
import json, sys
d = json.load(sys.stdin)
for m in d:
    nombre = m.get('nombre','')
    if any(x in nombre for x in ['PRUEBA', 'Test', 'test', 'PYTHON', 'E2E']):
        print(f'ELIMINAR: {m[\"id\"]} - {nombre}')
" 2>/dev/null

# Eliminar matter principal de prueba
if [ -n "$MATTER_ID" ]; then
    curl -s -X DELETE "http://localhost:8082/api/matters/$MATTER_ID" | python3 -m json.tool
fi
```

### Paso 5.2: Verificar estado limpio
```bash
curl -s http://localhost:8082/api/matters | python3 -c "import json,sys; d=json.load(sys.stdin); print(f'Matters restantes: {len(d)}')"
curl -s http://localhost:8082/api/dashboard | python3 -m json.tool | head -20
```

---

## FASE 6: GENERAR REPORTE (5 minutos)

### Paso 6.1: Compilar resultados
```bash
cat > /tmp/reporte_data.json << 'EOF'
{
  "fecha": "",
  "commit": "",
  "backend_ok": false,
  "motor_kami_ok": false,
  "templates_count": 0,
  "pdf_generated_api": false,
  "pdf_generated_cli": false,
  "matter_created_api": false,
  "matter_created_python": false,
  "reunion_created": false,
  "plazo_created": false,
  "alertas_working": false,
  "dashboard_working": false,
  "google_workspace_ok": false,
  "errores": [],
  "advertencias": [],
  "notas": []
}
EOF
```

### Paso 6.2: Llenar datos del reporte
Ejecutar script Python que lea los archivos temporales (`/tmp/matter_created.json`, `/tmp/doc_generated.json`, `/tmp/kami_cli.log`, etc.) y llene el JSON de reporte.

### Paso 6.3: Generar markdown
Crear `docs/REPORTE_PRUEBA_CLI_v3.md` con:

```markdown
# Reporte de Prueba CLI — Hermes Legal Pro v3

**Fecha:** {fecha}
**Commit:** {commit}
**Tester:** OpenCode Go (automático)

## Resumen Ejecutivo

| Componente | Estado |
|-----------|--------|
| Backend API | ✅/❌ |
| Motor Kami v3 | ✅/❌ |
| Templates (23) | ✅/❌ |
| Generación PDF vía API | ✅/❌ |
| Generación PDF vía CLI | ✅/❌ |
| CRUD Matters | ✅/❌ |
| Reuniones | ✅/❌ |
| Plazos | ✅/❌ |
| Alertas | ✅/❌ |
| Dashboard KPIs | ✅/❌ |
| Hermes Integration (Python) | ✅/❌ |
| Google Workspace | ✅/❌/⚠️ |

## Detalle por Fase

### Fase 0: Preparación
- Archivos críticos: {estado}
- Dependencias: {estado}
- Backend iniciado: {estado}

### Fase 1: Backend API
{output de cada curl}

### Fase 2: Motor Kami CLI
{output de motor_kami.py}

### Fase 3: Hermes Integration
{output de comandos Python}

### Fase 4: Google Workspace
{estado}

## Errores Encontrados

{lista de errores con mensaje exacto}

## Advertencias

{lista de advertencias}

## Lo que NO se pudo probar

- Frontend SPA visual (requiere navegador + screenshots)
- Telegram/Hermes Agent (requiere interacción humana)
- Diseño visual de PDF (requiere visión humana)
- Google Workspace (si no hay token)

## Conclusión

{Sistema completo / Parcial / Incompleto}
```

### Paso 6.4: Commitear reporte
```bash
cd ~/ws-hermes-legal-pro
git add docs/REPORTE_PRUEBA_CLI_v3.md
git commit -m "TEST: Reporte de prueba CLI v3 — $(date +%Y-%m-%d)"
git push origin master
```

---

## NOTAS IMPORTANTES PARA OPENCODE GO

### Lo que ESTE prompt puede probar (CLI):
✅ Backend API vía curl
✅ Motor Kami vía CLI
✅ Hermes Integration vía Python
✅ Generación de PDFs reales
✅ CRUD completo de datos
✅ Google Workspace (si hay token)

### Lo que ESTE prompt NO puede probar:
❌ Frontend SPA visual (necesita navegador)
❌ Screenshots (necesita herramienta de captura)
❌ Telegram/Hermes Agent chat (necesita interacción humana)
❌ Verificación visual de diseño Kami (necesita ojos humanos)
❌ Google Workspace si no hay token configurado

### Si algo falla:
1. Documentar el error EXACTO (copiar stderr)
2. Continuar con el siguiente paso
3. NO detenerse completamente

### Comandos útiles de debug:
```bash
# Ver logs del backend
tail -50 /tmp/backend.log

# Verificar puerto
lsof -i :8082 || netstat -an | grep 8082

# Matar backend si se quedó colgado
pkill -f "uvicorn app:app"
```

---

*Prompt realista generado por Hermes Neo. Enfocado en lo que OpenCode Go SÍ puede ejecutar vía CLI.*
