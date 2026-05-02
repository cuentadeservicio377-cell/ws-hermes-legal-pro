# Manual Técnico — Willow Legal

## 1. Requisitos

### Hardware
- Mac o PC con al menos 8GB RAM
- 500MB de espacio en disco

### Software
- **Python 3.9+** (viene con macOS)
- **Google Chrome** o cualquier navegador moderno
- **Cuenta de Google** (para Drive, Calendar, Docs)
- **pip3** (gestor de paquetes de Python)

### Servicios Google
- Google Drive API habilitada
- Google Calendar API habilitada
- Google Docs API habilitada
- Google Tasks API habilitada
- Client secret OAuth2 configurado

---

## 2. Instalación paso a paso

### 2.1 Clonar el repositorio

```bash
git clone https://github.com/cuentadeservicio377-cell/ws-hermes-legal-pro.git
cd ws-hermes-legal-pro
```

### 2.2 Instalar dependencias Python

```bash
pip3 install fastapi uvicorn weasyprint python-multipart
pip3 install google-api-python-client google-auth-httplib2 google-auth-oauthlib gspread
pip3 install openpyxl  # Para Excel sync
```

### 2.3 Configurar credenciales Google

1. Ve a [Google Cloud Console](https://console.cloud.google.com)
2. Crea un proyecto (o usa "hermes-ws-capital")
3. Habilita las APIs: Drive, Docs, Calendar, Tasks, Sheets
4. Crea credenciales OAuth 2.0 para "Aplicación de escritorio"
5. Descarga el archivo JSON como `config/client_secret.json`

### 2.4 Autenticar con Google

```bash
cd ~/ws-hermes-legal-pro
python3 scripts/drive_manager.py
# Se abrirá una ventana del navegador. Inicia sesión con la cuenta del despacho.
# El token se guarda en config/token.json
```

### 2.5 Iniciar el backend

```bash
cd ~/ws-hermes-legal-pro
python3 dashboard/backend/app.py
# El servidor inicia en http://localhost:8082
```

### 2.6 Abrir el dashboard

Abre tu navegador y ve a: **http://localhost:8082**

---

## 3. Configuración de credenciales

### Variables de entorno

Crear `config/.env` (copiar de `.env.template`):

```env
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

# Telegram (opcional)
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_HOME_CHAT_ID=your_chat_id

# AI Models (opcional)
KIMI_API_KEY=your_kimi_key
```

---

## 4. Estructura de archivos

```
ws-hermes-legal-pro/
├── dashboard/
│   ├── backend/
│   │   └── app.py              # FastAPI server (port 8082)
│   ├── datos/                  # JSON data files
│   │   ├── matters.json
│   │   ├── reuniones.json
│   │   ├── alertas.json
│   │   ├── documentos.json
│   │   ├── finanzas.json
│   │   ├── plazos.json
│   │   └── aprobaciones.json
│   └── frontend/
│       ├── index.html          # SPA shell
│       ├── css/
│       │   └── styles.css      # Design system (villow v7)
│       └── js/
│           ├── api.js           # HTTP client
│           ├── app.js           # Main app logic
│           └── finanzas.js      # Finance module
├── motor_kami/
│   ├── motor_kami.py            # PDF generation engine
│   ├── blocks.py                # Content blocks
│   └── templates/               # 23+ legal templates
├── scripts/
│   ├── drive_manager.py         # Google Drive integration
│   ├── docs_exporter.py         # Google Docs integration
│   ├── sheets_manager.py        # Google Sheets sync
│   ├── calendar_manager.py      # Google Calendar integration
│   ├── tasks_manager.py         # Google Tasks integration
│   ├── sync_excel_json.py       # Excel ↔ JSON sync
│   ├── check_plazos.py          # Deadline notifications
│   ├── sync_drive.py            # Local ↔ Drive sync
│   └── hermes_bridge.py         # CLI for Hermes Agent
├── hermes_integration/
│   ├── commands.py              # Legal command parser
│   └── session_manager.py       # Session persistence
├── config/
│   ├── .env.template            # Environment variables template
│   ├── client_secret.json       # Google OAuth credentials (no committeado)
│   ├── token.json               # Google OAuth token (no committeado)
│   ├── triggers.json            # Paperclip triggers
│   └── hermes-commands.json     # Telegram command definitions
├── agents/
│   ├── despacho.md              # Legal operations agent
│   ├── intake.md                # Client intake agent
│   └── admin.md                 # Admin agent
├── docs/                        # Documentation
└── datos/                       # v1 legacy data (for compatibility)
```

---

## 5. Backup

### Qué copiar

```bash
# Datos esenciales
cp -r dashboard/datos/ ~/Backups/willow/datos/
cp -r datos/ ~/Backups/willow/datos-legacy/

# Documentos generados
cp -r motor_kami/output/ ~/Backups/willow/output/

# Credenciales
cp config/.env ~/Backups/willow/config/
cp config/token.json ~/Backups/willow/config/
```

### Frecuencia recomendada
- **Diario**: `dashboard/datos/` (matters, plazos, finanzas)
- **Semanal**: Todo el proyecto (git push)
- **Mensual**: Carpeta completa `~/WillowLegal/`

---

## 6. Troubleshooting

### 6.1 "Module not found: fastapi"

```bash
pip3 install fastapi uvicorn
```

### 6.2 "Error 405 Method Not Allowed"

El backend necesita reiniciarse después de cambios en los endpoints:
```bash
pkill -f "app.py"
python3 dashboard/backend/app.py
```

### 6.3 "Port 8082 already in use"

```bash
lsof -i :8082
kill -9 [PID]
```

### 6.4 "Token expired or revoked"

```bash
rm config/token.json
python3 scripts/drive_manager.py  # Re-autenticar
```

### 6.5 "Motor Kami not found"

Verifica que motor_kami/ existe en la raíz del proyecto:
```bash
ls motor_kami/motor_kami.py
```

### 6.6 "WeasyPrint error on macOS"

```bash
brew install weasyprint
# O usar:
pip3 install weasyprint
```

### 6.7 "No module named 'scripts'"

Ejecuta comandos desde la raíz del repositorio:
```bash
cd ~/ws-hermes-legal-pro
python3 scripts/drive_manager.py
```

### 6.8 "Excel file not found"

```bash
ls excel/Centro_Operativo_Maestro_Willow_v4.xlsx
# Si no existe, generar uno nuevo con scripts/sync_excel_json.py
```

### 6.9 "Dashboard shows blank page"

1. Abre la consola del navegador (F12)
2. Busca errores en rojo
3. Verifica que el backend esté corriendo:
```bash
curl http://localhost:8082/api/health
```

### 6.10 "404 Documento no encontrado"

El documento fue eliminado o no se generó. Genera uno nuevo desde la interfaz o con:
```bash
python3 scripts/hermes_bridge.py contrato nda [MATTER_ID]
```

### 6.11 "Google API quota exceeded"

Reducir frecuencia de llamadas API o solicitar aumento de cuota en Google Cloud Console.

### 6.12 "files.list() 403 Insufficient Permission"

Verificar scopes de OAuth. Re-autenticar con todos los permisos:
```bash
rm config/token.json
python3 scripts/drive_manager.py
```

### 6.13 "Dashboard no carga bien en iPad"

El modo responsive está diseñado para tablets. Si hay problemas:
- Usar Safari en iPad (mejor compatibilidad)
- Activar "Solicitar sitio de escritorio" en Safari

### 6.14 "No se ve el balance en Finanzas"

El endpoint `/api/finanzas` necesita datos. Registrar al menos un movimiento:
```bash
curl -X POST http://localhost:8082/api/finanzas \
  -H "Content-Type: application/json" \
  -d '{"matter_id":"WIL-001","concepto":"Anticipo inicial","monto":25000,"tipo":"anticipo"}'
```

### 6.15 "Error CORS en el navegador"

El backend ya tiene CORS habilitado para todos los orígenes. Si persiste:
```bash
# Verificar que app.py tenga:
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
```

---

*Willow Legal v7 — Documentación Técnica*
*WS Capital © 2026*
