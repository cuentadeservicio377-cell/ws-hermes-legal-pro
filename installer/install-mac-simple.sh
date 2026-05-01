#!/bin/bash
# install-mac-simple.sh — Instalador SIMPLIFICADO para Mac
# Este script evita el problema de Telegram bloqueando la instalación
# El gateway de Telegram se configura DESPUÉS de que todo lo demás funcione

set -e

HERMES_VERSION="0.12.0"
PRODUCT_VERSION="1.0.0"
PROFILE_NAME="legal-pro"

echo "=========================================="
echo "  HERMES LEGAL PRO v${PRODUCT_VERSION}"
echo "  Instalador Simplificado para macOS"
echo "=========================================="
echo ""
echo "Este instalador configura TODO excepto Telegram."
echo "Telegram se configura al final, por separado."
echo ""

# Verificar macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo "❌ Error: Este instalador es solo para macOS"
    exit 1
fi

ARCH=$(uname -m)
echo "✓ Arquitectura: $ARCH"

# Verificar requisitos mínimos
echo ""
echo "📋 Verificando requisitos mínimos..."

# Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 no encontrado. Instálalo primero:"
    echo "   /bin/bash -c '\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)'"
    echo "   brew install python@3.11"
    exit 1
fi
echo "✓ Python: $(python3 --version 2>&1)"

# pip
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 no encontrado. Instálalo:"
    echo "   python3 -m ensurepip --upgrade"
    exit 1
fi
echo "✓ pip3: OK"

# curl
if ! command -v curl &> /dev/null; then
    echo "❌ curl no encontrado. Necesario para descargar Hermes."
    exit 1
fi
echo "✓ curl: OK"

echo ""
echo "🚀 PASO 1: Instalar Hermes Agent..."

# Instalar Hermes si no está
if ! command -v hermes &> /dev/null; then
    echo "Descargando Hermes..."
    curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash
    
    # Agregar al PATH si es necesario
    if [ -d "$HOME/.local/bin" ]; then
        export PATH="$HOME/.local/bin:$PATH"
        echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
    fi
else
    echo "✓ Hermes ya instalado"
fi

# Verificar que hermes funciona
if ! command -v hermes &> /dev/null; then
    echo "❌ Hermes no está en el PATH"
    echo "   Agrega esto a tu ~/.zshrc:"
    echo '   export PATH="$HOME/.local/bin:$PATH"'
    exit 1
fi

echo ""
echo "📦 PASO 2: Importar perfil legal-pro..."

PROFILE_TAR="hermes-legal-pro-profile.tar.gz"
if [ -f "$PROFILE_TAR" ]; then
    tar -xzf "$PROFILE_TAR" -C "$HOME/.hermes/profiles/"
    echo "✓ Perfil importado"
else
    echo "❌ No se encontró $PROFILE_TAR"
    echo "   Asegúrate de ejecutar este script desde el directorio del paquete"
    exit 1
fi

# Activar perfil
hermes profile use "$PROFILE_NAME"
echo "✓ Perfil activado"

echo ""
echo "🔧 PASO 3: Configurar plugins (sin Telegram)..."

# Activar plugins que no requieren config
hermes plugins enable disk-cleanup 2>/dev/null || true
echo "✓ disk-cleanup activado"

# google_meet se activa pero necesita Chrome
if [ -d "/Applications/Google Chrome.app" ]; then
    hermes plugins enable google_meet 2>/dev/null || true
    echo "✓ google_meet activado"
else
    echo "⚠ Google Meet no activado (Chrome no encontrado)"
fi

echo ""
echo "📝 PASO 4: Crear archivo de configuración..."

ENV_FILE="$HOME/.hermes/.env"
if [ ! -f "$ENV_FILE" ]; then
    cat > "$ENV_FILE" << 'EOF'
# Hermes Legal Pro — Variables de Entorno
# CONFIGURA ESTAS VARIABLES ANTES DE USAR

# === OBLIGATORIO: Modelo de IA ===
# Obtén en: https://platform.moonshot.cn
KIMI_API_KEY=

# === OPCIONAL: Fallbacks ===
OPENAI_CODEX_OAUTH=
NVIDIA_API_KEY=

# === OPCIONAL: Google (para Meet y Calendar) ===
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=
GOOGLE_CALENDAR_TOKEN=

# === OPCIONAL: Telegram (configurar al final) ===
# TELEGRAM_BOT_TOKEN=
# TELEGRAM_HOME_CHAT_ID=
EOF
    echo "✓ Template .env creado"
    echo ""
    echo "⚠ IMPORTANTE: Edita ~/.hermes/.env y agrega tu KIMI_API_KEY"
else
    echo "✓ .env ya existe"
fi

echo ""
echo "📁 PASO 5: Crear estructura de carpetas..."

mkdir -p "$HOME/WillowLegal"/{00_Sistema,01_Clientes,02_Administracion,03_Biblioteca_Legal,04_Agentes_Onyx,05_Backups}
mkdir -p "$HOME/WillowLegal/02_Administracion"/{Plantillas,Formatos,Manuales,Reportes}
echo "✓ Carpetas creadas"

echo ""
echo "📦 PASO 6: Instalar dependencias del dashboard..."

pip3 install fastapi uvicorn 2>/dev/null || pip install fastapi uvicorn
echo "✓ FastAPI instalado"

echo ""
echo "=========================================="
echo "  ✅ INSTALACIÓN BASE COMPLETADA"
echo "=========================================="
echo ""
echo "El sistema está instalado pero NO configurado para Telegram."
echo ""
echo "PRÓXIMOS PASOS:"
echo ""
echo "1. Configurar API key de Kimi:"
echo "   nano ~/.hermes/.env"
echo "   Agrega: KIMI_API_KEY=sk-tu-key-aqui"
echo ""
echo "2. Probar que Hermes funciona:"
echo "   hermes chat -q \"Hola\""
echo ""
echo "3. Iniciar el dashboard:"
echo "   cd dashboard/backend && python3 app.py"
echo "   Abre: dashboard/frontend/index.html en Chrome"
echo ""
echo "4. Cuando TODO funcione, configurar Telegram:"
echo "   ./configurar-telegram.sh"
echo ""
echo "=========================================="
echo ""
echo "Si algo falla, ejecuta:"
echo "   ./auditoria-mac.sh"
echo "   (genera reporte de diagnóstico)"
echo ""
