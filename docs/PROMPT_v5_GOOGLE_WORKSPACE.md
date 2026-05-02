# PROMPT EJECUTABLE v5 — OpenCode Go
# Integración Total Google Workspace + Fix UX/UI
# 
# ⚠️  REGLAS:
# 1. Lee TODO este archivo antes de empezar
# 2. Ejecuta fases en ORDEN (A → B → C → D → E → F → G)
# 3. Cada fase tiene VERIFICACIÓN — si falla, DETENTE
# 4. Usa Google Workspace API (gws CLI o Google API Python client)
# 5. Todo documento generado DEBE ir a Drive
# 6. Todo plazo DEBE ir a Calendar
# 7. Todo task DEBE ir a Google Tasks

---

## 📍 UBICACIÓN

```bash
REPO_PATH=~/ws-hermes-legal-pro
cd "$REPO_PATH"
git pull origin master
```

---

## 🔧 FASE A: Fix Backend CRUD + UX/UI (20 min)

### A.1 Agregar PUT/DELETE matters en backend

Editar `dashboard/backend/app.py` y agregar:

```python
@app.put("/api/matters/{matter_id}")
def update_matter(matter_id: str, payload: dict):
    """Actualizar matter existente."""
    try:
        matters = load_matters()
        matter = next((m for m in matters if m["id"] == matter_id), None)
        if not matter:
            return JSONResponse({"error": "Matter not found"}, status_code=404)
        
        # Actualizar campos permitidos
        allowed_fields = ["nombre", "cliente", "estado", "area", "materia", 
                         "prioridad", "next_step", "blocker", "deadline", "descripcion"]
        for field in allowed_fields:
            if field in payload:
                matter[field] = payload[field]
        
        matter["actualizado"] = datetime.now().isoformat()
        save_matters(matters)
        
        # Sync a Excel
        sync_to_excel(matter)
        
        return {"status": "ok", "matter": matter}
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

@app.delete("/api/matters/{matter_id}")
def delete_matter(matter_id: str):
    """Eliminar matter (soft delete)."""
    try:
        matters = load_matters()
        matter = next((m for m in matters if m["id"] == matter_id), None)
        if not matter:
            return JSONResponse({"error": "Matter not found"}, status_code=404)
        
        matter["estado"] = "Eliminado"
        matter["actualizado"] = datetime.now().isoformat()
        save_matters(matters)
        
        return {"status": "ok", "mensaje": f"Matter {matter_id} eliminado"}
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)
```

### A.2 Crear datos/finanzas.json

```bash
cd "$REPO_PATH"
mkdir -p dashboard/datos

cat > dashboard/datos/finanzas.json << 'JSONEOF'
{
  "version": "1.0",
  "movimientos": [],
  "resumen": {
    "total_anticipos": 0,
    "total_honorarios": 0,
    "total_facturado": 0,
    "total_cobrado": 0,
    "total_pendiente": 0
  }
}
JSONEOF

echo "✅ dashboard/datos/finanzas.json creado"
```

### A.3 Agregar DRIVE_FOLDER_ID a .env.template

```bash
cd "$REPO_PATH"

cat >> config/.env.template << 'ENVEOF'

# Google Workspace Integration
DRIVE_FOLDER_ID=your_drive_folder_id_here
GOOGLE_CLIENT_SECRET_PATH=config/client_secret.json
GOOGLE_TOKEN_PATH=config/token.json

# Google Workspace APIs
ENABLE_DRIVE_SYNC=true
ENABLE_CALENDAR_SYNC=true
ENABLE_TASKS_SYNC=true
ENABLE_SHEETS_SYNC=true
ENABLE_DOCS_EXPORT=true
ENVEOF

echo "✅ Variables Google Workspace agregadas a .env.template"
```

### A.4 Verificación

```bash
cd "$REPO_PATH"

echo "=== FASE A VERIFICACIÓN ==="

# Verificar PUT/DELETE en backend
grep -q "@app.put" dashboard/backend/app.py && echo "✅ PUT endpoint" || echo "❌ FALTA PUT"
grep -q "@app.delete" dashboard/backend/app.py && echo "✅ DELETE endpoint" || echo "❌ FALTA DELETE"

# Verificar finanzas.json
test -f dashboard/datos/finanzas.json && echo "✅ finanzas.json" || echo "❌ FALTA finanzas.json"

# Verificar .env.template
grep -q "DRIVE_FOLDER_ID" config/.env.template && echo "✅ DRIVE_FOLDER_ID en .env" || echo "❌ FALTA DRIVE_FOLDER_ID"

# Test funcional
python3 -c "import json; d=json.load(open('dashboard/datos/finanzas.json')); print(f\"✅ Finanzas JSON válido: {len(d['movimientos'])} movimientos\")"
```

---

## 🔧 FASE B: Google Drive como Filesystem Principal (40 min)

### B.1 Instalar dependencias Google

```bash
cd "$REPO_PATH"
pip3 install google-api-python-client google-auth-httplib2 google-auth-oauthlib gspread
```

### B.2 Crear scripts/drive_manager.py

```python
#!/usr/bin/env python3
"""
Drive Manager — Google Drive como filesystem principal del despacho.

Todo documento generado se sube automáticamente a Drive.
Estructura:
    WillowLegal/
    ├── 01_Clientes/
    │   └── {Cliente}/
    │       ├── 01_Intake/
    │       ├── 02_Contratos/
    │       │   ├── Borradores/
    │       │   └── Firmados/
    │       ├── 03_Correspondencia/
    │       ├── 04_Litigio/
    │       ├── 05_Facturacion/
    │       ├── 06_Entregables/
    │       │   └── Documentos_Finales/
    │       └── 07_Archivo/
    └── 02_Administracion/
"""

import os
import json
from pathlib import Path
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = [
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/documents',
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/calendar',
    'https://www.googleapis.com/auth/tasks'
]

class DriveManager:
    def __init__(self, base_folder_name="WillowLegal"):
        self.creds = self._get_credentials()
        self.service = build('drive', 'v3', credentials=self.creds)
        self.base_folder_id = self._get_or_create_folder(base_folder_name)
        
    def _get_credentials(self):
        """Obtener credenciales OAuth2."""
        token_path = Path("config/token.json")
        creds_path = Path("config/client_secret.json")
        
        if token_path.exists():
            creds = Credentials.from_authorized_user_file(str(token_path), SCOPES)
        else:
            creds = None
            
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not creds_path.exists():
                    raise FileNotFoundError(f"No existe {creds_path}. Descargar de Google Cloud Console.")
                flow = InstalledAppFlow.from_client_secrets_file(str(creds_path), SCOPES)
                creds = flow.run_local_server(port=0)
            
            # Guardar token
            token_path.parent.mkdir(parents=True, exist_ok=True)
            with open(token_path, 'w') as token:
                token.write(creds.to_json())
        
        return creds
    
    def _get_or_create_folder(self, name, parent_id=None):
        """Obtener o crear carpeta en Drive."""
        query = f"mimeType='application/vnd.google-apps.folder' and name='{name}' and trashed=false"
        if parent_id:
            query += f" and '{parent_id}' in parents"
        
        results = self.service.files().list(q=query, spaces='drive', fields='files(id, name)').execute()
        items = results.get('files', [])
        
        if items:
            return items[0]['id']
        
        # Crear carpeta
        metadata = {
            'name': name,
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': [parent_id] if parent_id else []
        }
        folder = self.service.files().create(body=metadata, fields='id').execute()
        return folder['id']
    
    def create_client_structure(self, client_name):
        """Crear estructura completa de carpetas para un cliente."""
        # Carpeta del cliente
        client_folder_id = self._get_or_create_folder(client_name, self.base_folder_id)
        
        # Subcarpetas
        subfolders = [
            "01_Intake",
            "02_Contratos",
            "03_Correspondencia",
            "04_Litigio",
            "05_Facturacion",
            "06_Entregables",
            "07_Archivo"
        ]
        
        for subfolder in subfolders:
            self._get_or_create_folder(subfolder, client_folder_id)
        
        # Subcarpetas especiales
        contratos_id = self._get_or_create_folder("02_Contratos", client_folder_id)
        self._get_or_create_folder("Borradores", contratos_id)
        self._get_or_create_folder("Firmados", contratos_id)
        
        entregables_id = self._get_or_create_folder("06_Entregables", client_folder_id)
        self._get_or_create_folder("Documentos_Finales", entregables_id)
        
        return client_folder_id
    
    def upload_pdf(self, pdf_path, client_name, subfolder="06_Entregables/Documentos_Finales"):
        """Subir PDF a carpeta del cliente en Drive."""
        from googleapiclient.http import MediaFileUpload
        
        # Navegar a subcarpeta
        client_folder_id = self._get_or_create_folder(client_name, self.base_folder_id)
        current_id = client_folder_id
        for part in subfolder.split('/'):
            current_id = self._get_or_create_folder(part, current_id)
        
        # Subir archivo
        file_metadata = {
            'name': Path(pdf_path).name,
            'parents': [current_id]
        }
        media = MediaFileUpload(pdf_path, mimetype='application/pdf')
        file = self.service.files().create(body=file_metadata, media_body=media, fields='id, webViewLink').execute()
        
        return {
            'id': file['id'],
            'link': file.get('webViewLink', ''),
            'mensaje': f"📄 PDF subido a Drive: {file['webViewLink']}"
        }
    
    def list_client_files(self, client_name):
        """Listar archivos de un cliente."""
        client_folder_id = self._get_or_create_folder(client_name, self.base_folder_id)
        
        query = f"'{client_folder_id}' in parents and trashed=false"
        results = self.service.files().list(q=query, fields='files(id, name, mimeType, webViewLink, modifiedTime)').execute()
        
        return results.get('files', [])

if __name__ == "__main__":
    # Test
    dm = DriveManager()
    print(f"✅ Drive Manager inicializado. Base folder: {dm.base_folder_id}")
    
    # Crear estructura de prueba
    test_folder = dm.create_client_structure("Test_Cliente")
    print(f"✅ Estructura creada: {test_folder}")
```

### B.3 Modificar Motor Kami para subir a Drive

Editar `motor_kami/motor_kami.py` y agregar al final de generación:

```python
# Al final del método generate() o main():

# Subir a Drive si está configurado
try:
    from scripts.drive_manager import DriveManager
    dm = DriveManager()
    result = dm.upload_pdf(output_pdf_path, client_name)
    print(f"📤 Drive: {result['mensaje']}")
except Exception as e:
    print(f"⚠️  Drive no configurado: {e}")
```

### B.4 Modificar hermes_bridge.py para crear estructura Drive

```python
# En crear_matter(), después de crear carpeta local:

# Crear en Drive
try:
    from scripts.drive_manager import DriveManager
    dm = DriveManager()
    drive_folder_id = dm.create_client_structure(client_name)
    matter["drive_folder_id"] = drive_folder_id
    print(f"📁 Drive: Carpeta creada")
except Exception as e:
    print(f"⚠️  Drive no disponible: {e}")
```

### B.5 Verificación

```bash
cd "$REPO_PATH"

echo "=== FASE B VERIFICACIÓN ==="

# Verificar drive_manager existe
test -f scripts/drive_manager.py && echo "✅ drive_manager.py" || echo "❌ FALTA"

# Verificar dependencias
python3 -c "from googleapiclient.discovery import build; print('✅ Google API client')" 2>/dev/null || echo "❌ FALTA google-api-python-client"

# Test de Drive (requiere auth)
python3 scripts/drive_manager.py 2>&1 | head -5
```

---

## 🔧 FASE C: Google Docs para Documentos Editables (30 min)

### C.1 Crear scripts/docs_exporter.py

```python
#!/usr/bin/env python3
"""
Docs Exporter — Convertir documentos legales a Google Docs editables.
"""

from googleapiclient.discovery import build
from scripts.drive_manager import DriveManager

class DocsExporter:
    def __init__(self):
        self.dm = DriveManager()
        self.docs_service = build('docs', 'v1', credentials=self.dm.creds)
        self.drive_service = self.dm.service
    
    def create_from_template(self, title, content_html, client_folder_id):
        """Crear Google Doc desde contenido HTML."""
        # Crear documento vacío
        doc = self.docs_service.documents().create(body={'title': title}).execute()
        doc_id = doc['documentId']
        
        # Insertar contenido (simplificado)
        requests = [{
            'insertText': {
                'location': {'index': 1},
                'text': content_html
            }
        }]
        
        self.docs_service.documents().batchUpdate(documentId=doc_id, body={'requests': requests}).execute()
        
        # Mover a carpeta del cliente
        self.drive_service.files().update(fileId=doc_id, addParents=client_folder_id).execute()
        
        return {
            'id': doc_id,
            'link': f"https://docs.google.com/document/d/{doc_id}/edit",
            'mensaje': f"📝 Google Doc creado: https://docs.google.com/document/d/{doc_id}/edit"
        }
    
    def convert_pdf_to_doc(self, pdf_path, title, client_name):
        """Convertir PDF existente a Google Doc."""
        client_folder_id = self.dm._get_or_create_folder(client_name, self.dm.base_folder_id)
        
        # Subir como Google Doc (Drive hace conversión)
        from googleapiclient.http import MediaFileUpload
        
        file_metadata = {
            'name': title,
            'mimeType': 'application/vnd.google-apps.document',
            'parents': [client_folder_id]
        }
        media = MediaFileUpload(pdf_path, mimetype='application/pdf')
        file = self.drive_service.files().create(body=file_metadata, media_body=media, fields='id, webViewLink').execute()
        
        return {
            'id': file['id'],
            'link': file['webViewLink'],
            'mensaje': f"📝 PDF convertido a Google Doc: {file['webViewLink']}"
        }

if __name__ == "__main__":
    de = DocsExporter()
    print("✅ Docs Exporter inicializado")
```

### C.2 Integrar en Motor Kami

Editar `motor_kami/motor_kami.py`:

```python
# Después de generar PDF, también crear Google Doc:

try:
    from scripts.docs_exporter import DocsExporter
    de = DocsExporter()
    
    # Leer HTML generado
    html_path = output_pdf_path.replace('.pdf', '.html')
    if os.path.exists(html_path):
        with open(html_path, 'r') as f:
            html_content = f.read()
        
        doc_result = de.create_from_template(
            title=f"{template_name} - {client_name}",
            content_html=html_content,
            client_folder_id=matter.get('drive_folder_id')
        )
        print(f"📄 {doc_result['mensaje']}")
except Exception as e:
    print(f"⚠️  Docs export no disponible: {e}")
```

---

## 🔧 FASE D: Google Sheets para Datos (30 min)

### D.1 Crear scripts/sheets_manager.py

```python
#!/usr/bin/env python3
"""
Sheets Manager — Sincronizar datos con Google Sheets maestro.
"""

import gspread
from google.oauth2.credentials import Credentials
from scripts.drive_manager import DriveManager

class SheetsManager:
    def __init__(self):
        self.dm = DriveManager()
        self.gc = gspread.authorize(self.dm.creds)
        self.sheet_id = self._get_or_create_sheet()
    
    def _get_or_create_sheet(self):
        """Obtener o crear Sheet maestro."""
        sheet_name = "WillowLegal_Maestro"
        
        # Buscar en Drive
        query = f"mimeType='application/vnd.google-apps.spreadsheet' and name='{sheet_name}' and trashed=false"
        results = self.dm.service.files().list(q=query, fields='files(id, name)').execute()
        items = results.get('files', [])
        
        if items:
            return items[0]['id']
        
        # Crear nuevo
        spreadsheet = self.gc.create(sheet_name)
        
        # Configurar hojas
        spreadsheet.add_worksheet(title="Matters", rows=1000, cols=20)
        spreadsheet.add_worksheet(title="Finanzas", rows=1000, cols=10)
        spreadsheet.add_worksheet(title="Plazos", rows=1000, cols=10)
        
        # Headers Matters
        matters_ws = spreadsheet.worksheet("Matters")
        matters_ws.append_row(["ID", "Nombre", "Cliente", "Estado", "Área", "Materia", 
                                "Prioridad", "Next Step", "Blocker", "Deadline", "Creado", "Drive Folder"])
        
        # Headers Finanzas
        finanzas_ws = spreadsheet.worksheet("Finanzas")
        finanzas_ws.append_row(["ID", "Matter ID", "Concepto", "Monto", "Tipo", "Estado", "Fecha"])
        
        # Headers Plazos
        plazos_ws = spreadsheet.worksheet("Plazos")
        plazos_ws.append_row(["ID", "Matter ID", "Descripción", "Fecha", "Estado", "Días Restantes"])
        
        return spreadsheet.id
    
    def sync_matter(self, matter):
        """Sincronizar matter a Sheets."""
        spreadsheet = self.gc.open_by_key(self.sheet_id)
        matters_ws = spreadsheet.worksheet("Matters")
        
        # Buscar fila existente
        cell = matters_ws.find(matter['id'])
        
        row_data = [
            matter['id'],
            matter['nombre'],
            matter['cliente'],
            matter['estado'],
            matter.get('area', ''),
            matter.get('materia', ''),
            matter.get('prioridad', ''),
            matter.get('next_step', ''),
            matter.get('blocker', ''),
            matter.get('deadline', ''),
            matter.get('creado', ''),
            matter.get('drive_folder_id', '')
        ]
        
        if cell:
            # Actualizar
            matters_ws.update(f'A{cell.row}:L{cell.row}', [row_data])
        else:
            # Insertar
            matters_ws.append_row(row_data)
        
        return {"status": "ok", "mensaje": f"✅ Matter {matter['id']} sincronizado a Sheets"}
    
    def sync_finanza(self, movimiento):
        """Sincronizar movimiento financiero."""
        spreadsheet = self.gc.open_by_key(self.sheet_id)
        finanzas_ws = spreadsheet.worksheet("Finanzas")
        
        finanzas_ws.append_row([
            movimiento['id'],
            movimiento['matter_id'],
            movimiento['concepto'],
            movimiento['monto'],
            movimiento['tipo'],
            movimiento['estado'],
            movimiento['fecha']
        ])
        
        return {"status": "ok"}

if __name__ == "__main__":
    sm = SheetsManager()
    print(f"✅ Sheets Manager inicializado. Sheet ID: {sm.sheet_id}")
```

### D.2 Integrar sync en commands.py

```python
# En HermesLegalCommands.crear_matter():

# Sync a Sheets
try:
    from scripts.sheets_manager import SheetsManager
    sm = SheetsManager()
    sm.sync_matter(matter)
except Exception as e:
    print(f"⚠️  Sheets sync: {e}")
```

---

## 🔧 FASE E: Google Calendar para Plazos (20 min)

### E.1 Crear scripts/calendar_manager.py

```python
#!/usr/bin/env python3
"""
Calendar Manager — Plazos legales en Google Calendar.
"""

from googleapiclient.discovery import build
from scripts.drive_manager import DriveManager
from datetime import datetime, timedelta

class CalendarManager:
    def __init__(self):
        self.dm = DriveManager()
        self.calendar_service = build('calendar', 'v3', credentials=self.dm.creds)
        self.calendar_id = 'primary'  # Calendar principal
    
    def create_deadline(self, matter_id, descripcion, fecha, reminder_days=[3, 1]):
        """Crear evento de deadline en Calendar."""
        
        event = {
            'summary': f'[Willow] {descripcion}',
            'description': f'Matter: {matter_id}\nDescripción: {descripcion}',
            'start': {
                'date': fecha,
                'timeZone': 'America/Mexico_City',
            },
            'end': {
                'date': fecha,
                'timeZone': 'America/Mexico_City',
            },
            'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'email', 'minutes': days * 24 * 60}
                    for days in reminder_days
                ] + [
                    {'method': 'popup', 'minutes': 60}  # 1 hora antes
                ],
            },
            'colorId': '11',  # Rojo para deadlines
        }
        
        event = self.calendar_service.events().insert(calendarId=self.calendar_id, body=event).execute()
        
        return {
            'id': event['id'],
            'link': event.get('htmlLink', ''),
            'mensaje': f"📅 Plazo creado en Calendar: {event.get('htmlLink', '')}"
        }
    
    def list_upcoming(self, days=7):
        """Listar plazos próximos."""
        now = datetime.utcnow().isoformat() + 'Z'
        future = (datetime.utcnow() + timedelta(days=days)).isoformat() + 'Z'
        
        events_result = self.calendar_service.events().list(
            calendarId=self.calendar_id,
            timeMin=now,
            timeMax=future,
            q='[Willow]',
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        
        return events_result.get('items', [])

if __name__ == "__main__":
    cm = CalendarManager()
    print("✅ Calendar Manager inicializado")
```

### E.2 Integrar en commands.py

```python
# En crear_plazo():

# Crear en Calendar
try:
    from scripts.calendar_manager import CalendarManager
    cm = CalendarManager()
    cal_result = cm.create_deadline(matter_id, descripcion, fecha)
    alerta["calendar_event_id"] = cal_result['id']
    print(f"📅 {cal_result['mensaje']}")
except Exception as e:
    print(f"⚠️  Calendar no disponible: {e}")
```

---

## 🔧 FASE F: Google Tasks para Tareas (20 min)

### F.1 Crear scripts/tasks_manager.py

```python
#!/usr/bin/env python3
"""
Tasks Manager — Tareas legales en Google Tasks.
"""

from googleapiclient.discovery import build
from scripts.drive_manager import DriveManager

class TasksManager:
    def __init__(self):
        self.dm = DriveManager()
        self.tasks_service = build('tasks', 'v1', credentials=self.dm.creds)
        self.tasklist_id = self._get_or_create_tasklist()
    
    def _get_or_create_tasklist(self):
        """Obtener o crear lista de tareas."""
        tasklists = self.tasks_service.tasklists().list().execute()
        items = tasklists.get('items', [])
        
        for item in items:
            if item['title'] == 'WillowLegal':
                return item['id']
        
        # Crear nueva
        tasklist = self.tasks_service.tasklists().insert(body={'title': 'WillowLegal'}).execute()
        return tasklist['id']
    
    def create_task(self, matter_id, descripcion, due_date=None, notes=""):
        """Crear tarea en Google Tasks."""
        
        task = {
            'title': f'[{matter_id}] {descripcion}',
            'notes': notes or f'Matter: {matter_id}',
        }
        
        if due_date:
            task['due'] = f"{due_date}T00:00:00.000Z"
        
        result = self.tasks_service.tasks().insert(tasklist=self.tasklist_id, body=task).execute()
        
        return {
            'id': result['id'],
            'mensaje': f"✅ Tarea creada: {result['title']}"
        }
    
    def complete_task(self, task_id):
        """Marcar tarea como completada."""
        self.tasks_service.tasks().update(
            tasklist=self.tasklist_id,
            task=task_id,
            body={'status': 'completed'}
        ).execute()
        
        return {"status": "ok", "mensaje": "✅ Tarea completada"}

if __name__ == "__main__":
    tm = TasksManager()
    print(f"✅ Tasks Manager inicializado. Tasklist: {tm.tasklist_id}")
```

---

## 🔧 FASE G: UX/UI Polish - Dashboard conectado (30 min)

### G.1 Modificar Dashboard para mostrar Drive

Editar `dashboard/frontend/index.html`:

```html
<!-- Agregar en nav o sidebar -->
<div class="nav-item">
    <span>📁 Drive</span>
    <a id="drive-link" href="#" target="_blank">Abrir en Google Drive</a>
</div>

<div class="nav-item">
    <span>📅 Calendar</span>
    <a id="calendar-link" href="https://calendar.google.com" target="_blank">Ver plazos</a>
</div>

<div class="nav-item">
    <span>📝 Docs</span>
    <a id="docs-link" href="#" target="_blank">Documentos editables</a>
</div>
```

### G.2 Modificar frontend/js/api.js

```javascript
// Agregar funciones Drive

async function getDriveFolder(matterId) {
    const response = await fetch(`/api/matters/${matterId}/drive-folder`);
    return await response.json();
}

async function openInDrive(matterId) {
    const result = await getDriveFolder(matterId);
    if (result.link) {
        window.open(result.link, '_blank');
    }
}

async function openInDocs(docId) {
    window.open(`https://docs.google.com/document/d/${docId}/edit`, '_blank');
}
```

### G.3 Agregar endpoints en backend

```python
@app.get("/api/matters/{matter_id}/drive-folder")
def get_drive_folder(matter_id: str):
    """Obtener link de carpeta en Drive."""
    matters = load_matters()
    matter = next((m for m in matters if m["id"] == matter_id), None)
    
    if not matter or not matter.get("drive_folder_id"):
        return {"status": "error", "mensaje": "No hay carpeta en Drive"}
    
    return {
        "status": "ok",
        "folder_id": matter["drive_folder_id"],
        "link": f"https://drive.google.com/drive/folders/{matter['drive_folder_id']}"
    }

@app.get("/api/matters/{matter_id}/documents")
def get_drive_documents(matter_id: str):
    """Listar documentos en Drive del matter."""
    try:
        from scripts.drive_manager import DriveManager
        dm = DriveManager()
        
        matters = load_matters()
        matter = next((m for m in matters if m["id"] == matter_id), None)
        
        if not matter:
            return JSONResponse({"error": "Matter not found"}, status_code=404)
        
        files = dm.list_client_files(matter["cliente"])
        return {"status": "ok", "files": files}
        
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)
```

---

## ✅ VERIFICACIÓN FINAL COMPLETA

```bash
cd "$REPO_PATH"

echo ""
echo "=========================================="
echo "  VERIFICACIÓN HERMES LEGAL PRO v5"
echo "  Google Workspace Integration"
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

# Fase A
grep -q "@app.put" dashboard/backend/app.py
check $? "PUT endpoint"

grep -q "@app.delete" dashboard/backend/app.py
check $? "DELETE endpoint"

test -f dashboard/datos/finanzas.json
check $? "finanzas.json"

# Fase B
test -f scripts/drive_manager.py
check $? "Drive Manager"

python3 -c "from googleapiclient.discovery import build; print('ok')" 2>/dev/null
check $? "Google API client"

# Fase C
test -f scripts/docs_exporter.py
check $? "Docs Exporter"

# Fase D
test -f scripts/sheets_manager.py
check $? "Sheets Manager"

python3 -c "import gspread; print('ok')" 2>/dev/null
check $? "gspread"

# Fase E
test -f scripts/calendar_manager.py
check $? "Calendar Manager"

# Fase F
test -f scripts/tasks_manager.py
check $? "Tasks Manager"

# Fase G
grep -q "drive-folder" dashboard/backend/app.py
check $? "Endpoint drive-folder"

echo ""
echo "=========================================="
echo "  RESULTADO: $PASS ✅ / $ERRORS ❌"
echo "=========================================="

if [ $ERRORS -eq 0 ]; then
    echo ""
    echo "🎉🎉🎉 HERMES LEGAL PRO v5 COMPLETO 🎉🎉🎉"
    echo ""
    echo "Integraciones Google Workspace:"
    echo "  📁 Google Drive — Carpetas y archivos"
    echo "  📝 Google Docs — Documentos editables"
    echo "  📊 Google Sheets — Datos maestros"
    echo "  📅 Google Calendar — Plazos y deadlines"
    echo "  ✅ Google Tasks — Tareas pendientes"
    echo ""
    echo "Modos de operación:"
    echo "  🤖 Telegram (Hermes) — /matter, /contrato, /plazo"
    echo "  💻 Dashboard (Mac) — Visual, drag & drop"
    echo "  📱 Google Apps — Drive, Docs, Calendar, Tasks"
    echo ""
    exit 0
else
    echo ""
    echo "❌ HAY ERRORES. Corregir antes de usar."
    exit 1
fi
```

---

## 🎉 RESULTADO ESPERADO

Al finalizar, el abogado podrá:

1. **Recibir cliente** → `/matter nuevo` → Crea carpeta local + Drive + Sheets
2. **Generar contrato** → Motor Kami → PDF local + PDF en Drive + Google Doc editable
3. **Ver plazos** → Calendar con alertas en celular
4. **Tareas** → Google Tasks integrado con Gmail
5. **Finanzas** → Sheets con fórmulas + Dashboard
6. **Editar documento** → Abrir en Google Docs desde celular
7. **Reporte** → `/status` o Dashboard con datos de Sheets

**Todo conectado. Todo funciona. Todo en Google Workspace.**

---

**INICIA CON FASE A AHORA.**
**NO SALTES FASES.**
**VERIFICA CADA UNA.**

**ÉXITO = Sistema legal completo integrado a Google Workspace.**
