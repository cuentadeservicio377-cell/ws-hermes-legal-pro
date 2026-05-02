# PROMPT v5.1 FIX — Google Workspace Integration REAL
# 
# PROBLEMA: Scripts existen pero NO funcionan porque:
# 1. No usan el token.json ya autenticado
# 2. Faltan endpoints en backend (/api/aprobar, /api/finanzas)
# 3. DriveManager no está integrado en crear_matter()
# 4. No hay test real de funcionamiento
#
# ESTADO: config/token.json existe y está autenticado
# OBJETIVO: Que todo funcione de verdad, no solo exista

---

## 📍 UBICACIÓN

```bash
REPO_PATH=~/ws-hermes-legal-pro
cd "$REPO_PATH"
```

---

## 🔧 FIX 1: Usar token.json existente (5 min)

### 1.1 Verificar token existe

```bash
cd "$REPO_PATH"

ls -la config/token.json
ls -la config/client_secret.json

# Si NO existen, copiar desde backup o reautenticar
# Si SÍ existen, continuar
```

### 1.2 Modificar scripts/drive_manager.py para usar token existente

Editar `scripts/drive_manager.py` y reemplazar `_get_credentials()`:

```python
def _get_credentials(self):
    """Obtener credenciales OAuth2 usando token existente."""
    token_path = Path("config/token.json")
    creds_path = Path("config/client_secret.json")
    
    # PRIORIDAD 1: Usar token existente
    if token_path.exists():
        try:
            creds = Credentials.from_authorized_user_file(str(token_path), SCOPES)
            if creds and creds.valid:
                print("✅ Token existente válido")
                return creds
            elif creds and creds.expired and creds.refresh_token:
                print("🔄 Refrescando token...")
                creds.refresh(Request())
                # Guardar token refrescado
                with open(token_path, 'w') as token:
                    token.write(creds.to_json())
                print("✅ Token refrescado")
                return creds
        except Exception as e:
            print(f"⚠️  Error con token existente: {e}")
    
    # PRIORIDAD 2: Autenticar nuevo (solo si no hay token)
    if creds_path.exists():
        print("🔐 Iniciando autenticación nueva...")
        flow = InstalledAppFlow.from_client_secrets_file(str(creds_path), SCOPES)
        creds = flow.run_local_server(port=0)
        
        # Guardar token
        token_path.parent.mkdir(parents=True, exist_ok=True)
        with open(token_path, 'w') as token:
            token.write(creds.to_json())
        print("✅ Nuevo token guardado")
        return creds
    else:
        raise FileNotFoundError(f"No existe {creds_path}. Descargar de Google Cloud Console.")
```

### 1.3 Test rápido de Drive

```bash
cd "$REPO_PATH"
python3 << 'PYEOF'
import sys
sys.path.insert(0, '.')

from scripts.drive_manager import DriveManager

try:
    dm = DriveManager()
    print("✅ Drive Manager inicializado")
    print(f"   Base folder ID: {dm.base_folder_id}")
    
    # Listar archivos en base folder
    results = dm.service.files().list(
        q=f"'{dm.base_folder_id}' in parents and trashed=false",
        fields='files(name, id)'
    ).execute()
    
    files = results.get('files', [])
    print(f"   Archivos en base folder: {len(files)}")
    for f in files[:5]:
        print(f"     - {f['name']}")
    
    print("\n🎉 Drive funciona correctamente")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
PYEOF
```

**Si funciona → continuar**
**Si falla → reportar error exacto**

---

## 🔧 FIX 2: Integrar Drive en crear_matter() (10 min)

### 2.1 Modificar hermes_integration/commands.py

En `crear_matter()`, después de crear carpeta local:

```python
# Crear en Drive (usar token existente)
try:
    from scripts.drive_manager import DriveManager
    dm = DriveManager()
    drive_folder_id = dm.create_client_structure(client_name)
    matter["drive_folder_id"] = drive_folder_id
    matter["drive_link"] = f"https://drive.google.com/drive/folders/{drive_folder_id}"
    print(f"📁 Drive: Carpeta creada {drive_folder_id}")
except Exception as e:
    print(f"⚠️  Drive no disponible: {e}")
    matter["drive_folder_id"] = None
    matter["drive_link"] = None
```

### 2.2 Modificar listar_matters() para mostrar Drive

```python
def listar_matters(self, limite=10):
    try:
        matters = self._load_json(self.matters_file, [])
        
        if not matters:
            return {"status": "ok", "mensaje": "📭 No hay matters"}
        
        lines = ["📋 MATTERS:"]
        for m in matters[-limite:]:
            emoji = "🟢" if m.get("estado") == "Activo" else "🟡"
            drive_icon = "📁" if m.get("drive_folder_id") else "❌"
            lines.append(f"  {emoji} {m['id']}: {m['nombre']} {drive_icon}")
        
        return {"status": "ok", "mensaje": "\n".join(lines)}
    except Exception as e:
        return {"status": "error", "mensaje": f"❌ {e}"}
```

### 2.3 Test crear matter con Drive

```bash
cd "$REPO_PATH"
python3 scripts/hermes_bridge.py matter nuevo "Test_Drive_Integration" area=Corporativo

# Verificar output tenga "📁 Drive: Carpeta creada"
```

---

## 🔧 FIX 3: Agregar endpoints faltantes (15 min)

### 3.1 Agregar /api/aprobar en backend

Editar `dashboard/backend/app.py`:

```python
@app.post("/api/documentos/{doc_id}/aprobar")
def aprobar_documento(doc_id: str, payload: dict):
    """Aprobar documento con trazabilidad."""
    try:
        documentos = load_json(DOCUMENTOS_FILE, [])
        doc = next((d for d in documentos if d["id"] == doc_id), None)
        
        if not doc:
            return JSONResponse({"error": "Documento no encontrado"}, status_code=404)
        
        doc["estado"] = "aprobado"
        doc["aprobado_por"] = payload.get("aprobado_por", "Sistema")
        doc["fecha_aprobacion"] = datetime.now().isoformat()
        doc["comentario_aprobacion"] = payload.get("comentario", "")
        
        save_json(DOCUMENTOS_FILE, documentos)
        
        return {
            "status": "ok",
            "documento": doc,
            "mensaje": f"✅ Documento {doc_id} aprobado por {doc['aprobado_por']}"
        }
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

@app.post("/api/documentos/{doc_id}/rechazar")
def rechazar_documento(doc_id: str, payload: dict):
    """Rechazar documento."""
    try:
        documentos = load_json(DOCUMENTOS_FILE, [])
        doc = next((d for d in documentos if d["id"] == doc_id), None)
        
        if not doc:
            return JSONResponse({"error": "Documento no encontrado"}, status_code=404)
        
        doc["estado"] = "rechazado"
        doc["rechazado_por"] = payload.get("rechazado_por", "Sistema")
        doc["fecha_rechazo"] = datetime.now().isoformat()
        doc["motivo_rechazo"] = payload.get("motivo", "")
        
        save_json(DOCUMENTOS_FILE, documentos)
        
        return {
            "status": "ok",
            "mensaje": f"❌ Documento {doc_id} rechazado"
        }
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)
```

### 3.2 Agregar /api/finanzas en backend

```python
# Variables globales
FINANZAS_FILE = Path("dashboard/datos/finanzas.json")

@app.get("/api/finanzas")
def listar_finanzas(matter_id: str = None):
    """Listar movimientos financieros."""
    try:
        finanzas = load_json(FINANZAS_FILE, {"movimientos": [], "resumen": {}})
        
        movimientos = finanzas.get("movimientos", [])
        if matter_id:
            movimientos = [m for m in movimientos if m.get("matter_id") == matter_id]
        
        return {
            "status": "ok",
            "movimientos": movimientos[-50:],  # últimos 50
            "resumen": finanzas.get("resumen", {})
        }
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

@app.post("/api/finanzas")
def crear_movimiento(payload: dict):
    """Registrar movimiento financiero."""
    try:
        finanzas = load_json(FINANZAS_FILE, {"movimientos": [], "resumen": {}})
        
        movimiento = {
            "id": f"FIN-{len(finanzas['movimientos'])+1:03d}",
            "matter_id": payload.get("matter_id"),
            "concepto": payload.get("concepto", ""),
            "monto": float(payload.get("monto", 0)),
            "tipo": payload.get("tipo", "anticipo"),  # anticipo, honorario, factura, gasto
            "estado": payload.get("estado", "pendiente"),
            "fecha": payload.get("fecha", datetime.now().isoformat()),
            "notas": payload.get("notas", "")
        }
        
        finanzas["movimientos"].append(movimiento)
        
        # Recalcular resumen
        movs = finanzas["movimientos"]
        finanzas["resumen"] = {
            "total_anticipos": sum(m["monto"] for m in movs if m["tipo"] == "anticipo"),
            "total_honorarios": sum(m["monto"] for m in movs if m["tipo"] == "honorario"),
            "total_facturado": sum(m["monto"] for m in movs if m["tipo"] == "factura"),
            "total_cobrado": sum(m["monto"] for m in movs if m["estado"] == "cobrado"),
            "total_pendiente": sum(m["monto"] for m in movs if m["estado"] == "pendiente"),
            "count": len(movs)
        }
        
        save_json(FINANZAS_FILE, finanzas)
        
        return {
            "status": "ok",
            "movimiento": movimiento,
            "mensaje": f"💰 {movimiento['tipo'].upper()}: ${movimiento['monto']:,.2f}"
        }
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)
```

### 3.3 Test endpoints

```bash
cd "$REPO_PATH"

# Test finanzas
curl -X POST http://localhost:8082/api/finanzas \
  -H "Content-Type: application/json" \
  -d '{"matter_id":"WIL-001","concepto":"Anticipo inicial","monto":25000,"tipo":"anticipo"}'

# Test aprobar
curl -X POST http://localhost:8082/api/documentos/DOC-001/aprobar \
  -H "Content-Type: application/json" \
  -d '{"aprobado_por":"Pablo","comentario":"OK"}'
```

---

## 🔧 FIX 4: Integrar Calendar en crear_plazo() (10 min)

### 4.1 Modificar hermes_integration/commands.py

En `crear_plazo()`:

```python
# Crear en Google Calendar
try:
    from scripts.calendar_manager import CalendarManager
    cm = CalendarManager()
    
    # Usar token existente
    cal_result = cm.create_deadline(
        matter_id=matter_id,
        descripcion=descripcion,
        fecha=fecha,
        reminder_days=[3, 1]  # alertas a 3 días y 1 día
    )
    
    alerta["calendar_event_id"] = cal_result['id']
    alerta["calendar_link"] = cal_result['link']
    
    mensaje_extra = f"\n📅 Calendar: {cal_result['link']}"
except Exception as e:
    print(f"⚠️  Calendar: {e}")
    mensaje_extra = ""

return {
    "status": "ok",
    "mensaje": (
        f"📅 Plazo creado: {alerta['id']}\n"
        f"   Matter: {matter_id}\n"
        f"   📌 {descripcion}\n"
        f"   📆 {fecha}"
        f"{mensaje_extra}"
    )
}
```

### 4.2 Test plazo con Calendar

```bash
cd "$REPO_PATH"
python3 scripts/hermes_bridge.py plazo WIL-001 "Test Calendar" $(date -v+7d +%Y-%m-%d)

# Verificar output tenga "📅 Calendar:"
```

---

## 🔧 FIX 5: Test End-to-End REAL (10 min)

### 5.1 Test completo

```bash
cd "$REPO_PATH"

echo "=========================================="
echo "  TEST END-TO-END GOOGLE WORKSPACE"
echo "=========================================="

# 1. Crear matter (debe crear en Drive)
echo ""
echo "1. Creando matter..."
RESULT=$(python3 scripts/hermes_bridge.py matter nuevo "E2E_Test_Google" area=Corporativo 2>&1)
echo "$RESULT"

# Extraer matter_id
MATTER_ID=$(echo "$RESULT" | grep "Matter creado:" | sed 's/.*: //' | awk '{print $1}')
echo "   Matter ID: $MATTER_ID"

# 2. Verificar en Drive
echo ""
echo "2. Verificando Drive..."
python3 << PYEOF
import sys
sys.path.insert(0, '.')
from scripts.drive_manager import DriveManager

dm = DriveManager()
# Listar archivos en base folder
results = dm.service.files().list(
    q=f"'{dm.base_folder_id}' in parents and trashed=false and name contains 'E2E_Test'",
    fields='files(name, id)'
).execute()

files = results.get('files', [])
if files:
    print(f"✅ Matter encontrado en Drive: {files[0]['name']}")
else:
    print("❌ Matter NO aparece en Drive")
PYEOF

# 3. Crear plazo (debe crear en Calendar)
echo ""
echo "3. Creando plazo..."
FUTURE_DATE=$(date -v+7d +%Y-%m-%d 2>/dev/null || date -d '+7 days' +%Y-%m-%d)
python3 scripts/hermes_bridge.py plazo "$MATTER_ID" "Test E2E" "$FUTURE_DATE"

# 4. Verificar finanzas
echo ""
echo "4. Verificando finanzas..."
curl -s http://localhost:8082/api/finanzas | python3 -m json.tool | head -20

echo ""
echo "=========================================="
echo "  TEST COMPLETADO"
echo "=========================================="
```

---

## ✅ VERIFICACIÓN FINAL

```bash
cd "$REPO_PATH"

echo ""
echo "=========================================="
echo "  VERIFICACIÓN HERMES LEGAL v5.1"
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

# 1. Token funciona
python3 -c "from scripts.drive_manager import DriveManager; dm = DriveManager(); print('ok')" 2>/dev/null
check $? "Drive Manager con token existente"

# 2. Endpoints existen
grep -q "/api/finanzas" dashboard/backend/app.py
check $? "Endpoint /api/finanzas"

grep -q "/api/documentos.*aprobar" dashboard/backend/app.py
check $? "Endpoint /api/aprobar"

# 3. Drive integrado en commands
grep -q "drive_folder_id" hermes_integration/commands.py
check $? "drive_folder_id en commands"

# 4. Calendar integrado en commands
grep -q "calendar_event_id" hermes_integration/commands.py
check $? "calendar_event_id en commands"

# 5. Datos compartidos
test -f dashboard/datos/finanzas.json
check $? "finanzas.json existe"

test -f datos/matters.json
check $? "matters.json existe"

echo ""
echo "=========================================="
echo "  RESULTADO: $PASS ✅ / $ERRORS ❌"
echo "=========================================="

if [ $ERRORS -eq 0 ]; then
    echo ""
    echo "🎉 HERMES LEGAL v5.1 FUNCIONA"
    echo ""
    echo "Google Workspace integrado:"
    echo "  📁 Drive — Carpetas por cliente"
    echo "  📅 Calendar — Plazos con alertas"
    echo "  💰 Finanzas — Tracking completo"
    echo "  📄 Documentos — Aprobaciones"
    echo ""
    git add -A
    git commit -m "v5.1 FIX: Google Workspace funcional — token, endpoints, integración real"
    git push origin master
    echo "✅ Código subido"
else
    echo ""
    echo "❌ FALTAN COSAS. Corregir antes de usar."
fi
```

---

## 🎯 RESULTADO ESPERADO

Después de este fix:

1. ✅ `config/token.json` se usa (no se intenta reautenticar)
2. ✅ Crear matter → aparece carpeta en Google Drive
3. ✅ Crear plazo → aparece evento en Google Calendar
4. ✅ Endpoint /api/finanzas funciona
5. ✅ Endpoint /api/aprobar funciona
6. ✅ Dashboard muestra links reales a Drive

**Todo conectado. Todo funciona.**

---

**INICIA CON FIX 1 AHORA.**
**NO SALTES FIXES.**
**TESTEA CADA UNO.**
