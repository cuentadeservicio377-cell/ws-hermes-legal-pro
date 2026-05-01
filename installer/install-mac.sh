#!/bin/bash
# install-mac.sh — Instalador de Hermes Legal Pro para macOS
# Ejecutar: chmod +x install-mac.sh && ./install-mac.sh

set -e

HERMES_VERSION="0.12.0"
PRODUCT_VERSION="1.0.0"
PROFILE_NAME="legal-pro"

echo "=========================================="
echo "  HERMES LEGAL PRO v${PRODUCT_VERSION}"
echo "  Instalador para macOS"
echo "=========================================="
echo ""

# Verificar macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo "❌ Error: Este instalador es solo para macOS"
    exit 1
fi

# Verificar arquitectura
ARCH=$(uname -m)
echo "✓ Arquitectura detectada: $ARCH"

# Verificar requisitos
echo ""
echo "📋 Verificando requisitos..."

# Python 3.11+
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
    echo "✓ Python: $PYTHON_VERSION"
else
    echo "❌ Python 3 no encontrado. Instálalo con: brew install python@3.11"
    exit 1
fi

# Node.js
if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version)
    echo "✓ Node.js: $NODE_VERSION"
else
    echo "⚠ Node.js no encontrado. Algunas features pueden no funcionar."
    echo "  Instálalo con: brew install node"
fi

# Git
if command -v git &> /dev/null; then
    echo "✓ Git: $(git --version | awk '{print $3}')"
else
    echo "⚠ Git no encontrado."
    echo "  Instálalo con: brew install git"
fi

# Google Chrome (para Meet)
if [ -d "/Applications/Google Chrome.app" ]; then
    echo "✓ Google Chrome: Instalado"
else
    echo "⚠ Google Chrome no encontrado. Necesario para transcripción de Meet."
    echo "  Descárgalo de: https://google.com/chrome"
fi

echo ""
echo "🚀 Instalando Hermes Agent..."

# Instalar Hermes si no está instalado
if ! command -v hermes &> /dev/null; then
    echo "Descargando Hermes Agent..."
    curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash
    export PATH="$HOME/.local/bin:$PATH"
else
    echo "✓ Hermes ya instalado: $(hermes --version)"
fi

# Verificar que hermes está disponible
if ! command -v hermes &> /dev/null; then
    echo "❌ Error: Hermes no se instaló correctamente"
    echo "   Intenta: export PATH=\"$HOME/.local/bin:\$PATH\""
    exit 1
fi

echo ""
echo "📦 Importando perfil legal-pro..."

# Descomprimir perfil
PROFILE_TAR="hermes-legal-pro-profile.tar.gz"
if [ -f "$PROFILE_TAR" ]; then
    tar -xzf "$PROFILE_TAR" -C "$HOME/.hermes/profiles/"
    echo "✓ Perfil importado"
else
    echo "❌ Error: No se encontró $PROFILE_TAR"
    echo "   Asegúrate de ejecutar este script desde el directorio del paquete"
    exit 1
fi

# Activar perfil
hermes profile use "$PROFILE_NAME"
echo "✓ Perfil 'legal-pro' activado"

echo ""
echo "🔧 Configurando plugins..."

# Activar plugins
hermes plugins enable disk-cleanup 2>/dev/null || true
hermes plugins enable google_meet 2>/dev/null || true
echo "✓ Plugins activados"

echo ""
echo "📝 Configuración de API keys..."

# Crear .env si no existe
ENV_FILE="$HOME/.hermes/.env"
if [ ! -f "$ENV_FILE" ]; then
    echo ""
    echo "⚠ IMPORTANTE: Necesitas configurar tus API keys"
    echo ""
    echo "Edita el archivo: $ENV_FILE"
    echo ""
    echo "Variables necesarias:"
    echo "  KIMI_API_KEY=sk-tu-key-aqui"
    echo "  TELEGRAM_BOT_TOKEN=tu-bot-token"
    echo "  GOOGLE_CALENDAR_TOKEN=token-aqui"
    echo ""
    echo "Para obtener keys:"
    echo "  - Kimi: https://platform.moonshot.cn"
    echo "  - Telegram Bot: Busca @BotFather en Telegram"
    echo "  - Google: Sigue la guía en docs/google-setup.md"
    echo ""
    
    # Crear template
    cat > "$ENV_FILE" << 'EOF'
# Hermes Legal Pro — Variables de Entorno
# Edita este archivo con tus API keys

# Modelo principal (Kimi recomendado)
KIMI_API_KEY=

# Fallback (opcional)
OPENAI_CODEX_OAUTH=
NVIDIA_API_KEY=

# Google (para Meet y Calendar)
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=
GOOGLE_CALENDAR_TOKEN=

# Telegram (para gateway)
TELEGRAM_BOT_TOKEN=
TELEGRAM_HOME_CHAT_ID=
EOF
    
    echo "✓ Template de .env creado en $ENV_FILE"
else
    echo "✓ .env ya existe"
fi

echo ""
echo "📁 Creando estructura de carpetas..."

# Crear carpetas legales
mkdir -p "$HOME/WillowLegal"/{00_Sistema,01_Clientes,02_Administracion,03_Biblioteca_Legal,04_Agentes_Onyx,05_Backups}
mkdir -p "$HOME/WillowLegal/02_Administracion"/{Plantillas,Formatos,Manuales,Reportes}

echo "✓ Carpetas creadas en ~/WillowLegal/"

echo ""
echo "🔍 Verificación final..."

# Health check
hermes doctor 2>/dev/null || echo "⚠ Doctor encontró issues (revisa arriba)"

echo ""
echo "=========================================="
echo "  ✅ INSTALACIÓN COMPLETADA"
echo "=========================================="
echo ""
echo "Próximos pasos:"
echo ""
echo "1. Configurar API keys:"
echo "   nano ~/.hermes/.env"
echo ""
echo "2. Configurar Telegram bot:"
echo "   - Busca @BotFather en Telegram"
echo "   - Crea un bot nuevo"
echo "   - Copia el token a ~/.hermes/.env"
echo ""
echo "3. Iniciar gateway:"
echo "   hermes gateway start"
echo ""
echo "4. Probar:"
echo "   hermes chat -q \"Hola, estoy configurando Hermes Legal Pro\""
echo ""
echo "Documentación:"
echo "   README.md      — Overview del producto"
echo "   INSTALL.md     — Guía detallada de instalación"
echo "   USER-GUIDE.md  — Guía de uso para abogados"
echo ""
echo "Soporte: soporte@wscapital.ai"
echo ""
echo "=========================================="
