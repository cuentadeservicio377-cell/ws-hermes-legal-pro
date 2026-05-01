# INSTALL.md — Guía de Instalación para Técnicos
# Hermes Legal Pro v1.0.0

---

## 📋 REQUISITOS

### Hardware
- **MacBook Air M2** (o superior)
- **RAM:** 8GB mínimo, 16GB recomendado
- **Almacenamiento:** 50GB libres
- **Internet:** Conexión estable

### Software
- **macOS:** 13.0 (Ventura) o superior
- **Python:** 3.11 o superior
- **Node.js:** 18 o superior
- **Homebrew:** Instalado
- **Git:** Instalado

### Cuentas necesarias
- **API Key de Kimi** (o OpenAI, Anthropic)
- **Cuenta Google** (para Meet y Calendar)
- **Bot de Telegram** (para gateway)

---

## 🚀 INSTALACIÓN PASO A PASO

### Paso 1: Instalar Hermes Agent

```bash
# Instalar Hermes Agent (si no está instalado)
curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash

# Verificar instalación
hermes --version
```

### Paso 2: Importar perfil legal-pro

```bash
# Descomprimir el perfil exportado
tar -xzf hermes-legal-pro-profile.tar.gz -C ~/.hermes/profiles/

# Verificar que se creó el perfil
hermes profile list
# Debe aparecer: legal-pro

# Activar perfil
hermes profile use legal-pro
```

### Paso 3: Configurar API keys

```bash
# Copiar template de variables de entorno
cp config/.env.template ~/.hermes/.env

# Editar ~/.hermes/.env con tus keys
nano ~/.hermes/.env
```

**Variables requeridas:**
```bash
# Modelo principal (Kimi recomendado)
KIMI_API_KEY=sk-tu-key-aqui

# Modelo fallback (OpenAI Codex)
OPENAI_CODEX_OAUTH=oauth-token-aqui

# Google (para Meet y Calendar)
GOOGLE_CLIENT_ID=tu-client-id
GOOGLE_CLIENT_SECRET=tu-client-secret
GOOGLE_CALENDAR_TOKEN=token-de-calendar

# Telegram (para gateway)
TELEGRAM_BOT_TOKEN=tu-bot-token
TELEGRAM_HOME_CHAT_ID=tu-chat-id

# Opcional: NVIDIA (fallback)
NVIDIA_API_KEY=nvapi-tu-key
```

### Paso 4: Instalar plugins

```bash
# Activar google_meet plugin
hermes plugins enable google_meet

# Activar disk-cleanup
hermes plugins enable disk-cleanup

# Verificar plugins activos
hermes plugins list
```

### Paso 5: Configurar Google Meet

```bash
# El plugin google_meet requiere Chrome instalado
# Verificar que Chrome está instalado
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --version

# Configurar cuenta Google
# El plugin usará la cuenta Google ya logueada en Chrome
# Asegurarse de estar logueado en meet.google.com en Chrome
```

**Modos de google_meet:**
- `transcribe` — Solo transcribe (default, recomendado)
- `realtime` — Transcribe + habla en tiempo real (requiere audio setup)
- `remote` — Nodo remoto (para setups avanzados)

### Paso 6: Configurar Telegram Gateway

```bash
# Crear bot en Telegram
# 1. Buscar @BotFather en Telegram
# 2. Enviar /newbot
# 3. Seguir instrucciones
# 4. Guardar el token

# Configurar en Hermes
hermes config set telegram.bot_token tu-bot-token
hermes config set telegram.home_chat_id tu-chat-id

# Iniciar gateway
hermes gateway start
```

### Paso 7: Configurar Google Calendar MCP

```bash
# Agregar MCP server de Google Calendar
hermes mcp add google-calendar --url https://mcp.google.com/calendar

# Configurar autorización
# Seguir flujo OAuth de Google
```

### Paso 8: Verificar instalación

```bash
# Health check completo
hermes doctor

# Verificar status
hermes status

# Debe mostrar:
# - Model: configurado
# - Plugins: google_meet enabled, disk-cleanup enabled
# - Gateway: running
# - Tools: todos activos
```

### Paso 9: Crear estructura de carpetas

```bash
# Ejecutar script de setup
./scripts/setup-carpetas.sh

# Esto crea:
# ~/WillowLegal/
# ├── 00_Sistema/
# ├── 01_Clientes/
# ├── 02_Administracion/
# ├── 03_Biblioteca_Legal/
# ├── 04_Agentes_Onyx/
# └── 05_Backups/
```


### Paso 11: Iniciar Dashboard Visual

```bash
# Navegar al dashboard
cd dashboard

# Instalar dependencias (primera vez)
pip install fastapi uvicorn

# Iniciar backend
cd backend && python app.py

# En otra terminal, abrir frontend
open frontend/index.html
```

El dashboard estará disponible en:
- **Backend API:** http://localhost:8082
- **Frontend:** file://.../frontend/index.html (o servir con cualquier servidor)

### Paso 10: Testear sistema

```bash
# Test 1: Hermes responde
hermes chat -q "Hola, estoy configurando Hermes Legal Pro"

# Test 2: Plugins cargan
hermes plugins list

# Test 3: Gateway responde en Telegram
# Enviar mensaje al bot, debe responder

# Test 4: Generar documento de prueba
hermes chat -q "/documento-generar TEST prestacion_servicios"
```

---

## 🔧 CONFIGURACIÓN AVANZADA

### Cambiar modelo principal

```bash
# Si prefieres Claude en lugar de Kimi
hermes config set model.default claude-sonnet-4
hermes config set model.provider anthropic
```

### Configurar múltiples abogados

```bash
# Crear perfil por abogado
hermes profile create abogado-maria --clone-from legal-pro
hermes profile create abogado-juan --clone-from legal-pro

# Cada abogado tiene su propio contexto y matters
```

### Backup automático

```bash
# Agregar cron job para backup diario
hermes cron create "0 2 * * *" "Backup diario de Hermes Legal Pro"

# Script de backup incluido en scripts/backup-system.sh
```

---

## 🐛 TROUBLESHOOTING

### Problema: Google Meet no transcribe
**Causa:** Chrome no está abierto o no está logueado
**Solución:**
1. Abrir Google Chrome
2. Loguearse en meet.google.com
3. Verificar que el plugin tiene permisos

### Problema: Telegram no responde
**Causa:** Bot token incorrecto o gateway no iniciado
**Solución:**
1. Verificar token: `hermes config path` → revisar config.yaml
2. Reiniciar gateway: `hermes gateway restart`
3. Verificar logs: `hermes logs errors`

### Problema: Documentos no se generan
**Causa:** Motor Kami no configurado o template no encontrado
**Solución:**
1. Verificar que Motor Kami está instalado: `ls ~/WillowLegal/00_Sistema/Motor_Kami/`
2. Verificar templates: `ls templates/`
3. Revisar logs de generación

### Problema: Costos altos de API
**Causa:** Modelo principal muy caro o uso excesivo
**Solución:**
1. Cambiar a modelo más económico: `hermes config set model.default kimi-k2.6`
2. Activar smart routing: `hermes config set smart_model_routing.enabled true`
3. Revisar insights: `hermes insights --days 7`

---

## 📞 SOPORTE TÉCNICO

- **Documentación:** docs/ folder
- **Logs:** `hermes logs`
- **Status:** `hermes status`
- **Email:** soporte@wscapital.ai

---

## 🔄 ACTUALIZACIONES

### Verificar actualizaciones
```bash
hermes update
```

### Actualizar skills
```bash
hermes skills check
hermes skills update
```

### Backup antes de actualizar
```bash
./scripts/backup-system.sh
```

---

*Hermes Legal Pro — Instalación v1.0*
*Para técnicos y administradores de sistemas*
