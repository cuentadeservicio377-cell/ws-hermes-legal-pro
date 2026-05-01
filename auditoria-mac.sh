#!/bin/bash
# AUDITORÍA HERMES LEGAL PRO — MacBook Air M2
# Ejecutar esto en la Mac para diagnosticar qué falta

set -e

REPORT_FILE="/tmp/hermes-audit-report.txt"
echo "AUDITORÍA HERMES LEGAL PRO" > "$REPORT_FILE"
echo "Fecha: $(date)" >> "$REPORT_FILE"
echo "Mac: $(sysctl -n hw.model 2>/dev/null || echo 'Desconocido')" >> "$REPORT_FILE"
echo "macOS: $(sw_vers -productVersion 2>/dev/null || echo 'Desconocido')" >> "$REPORT_FILE"
echo "=======================================" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

# 1. VERIFICAR SISTEMA OPERATIVO
echo "🔍 1. SISTEMA OPERATIVO" >> "$REPORT_FILE"
if [[ "$OSTYPE" == "darwin"* ]]; then
    echo "✅ macOS detectado: $OSTYPE" >> "$REPORT_FILE"
    ARCH=$(uname -m)
    echo "✅ Arquitectura: $ARCH" >> "$REPORT_FILE"
    if [[ "$ARCH" == "arm64" ]]; then
        echo "✅ Apple Silicon (M1/M2/M3) detectado" >> "$REPORT_FILE"
    fi
else
    echo "❌ NO es macOS. Este script es solo para macOS." >> "$REPORT_FILE"
    exit 1
fi
echo "" >> "$REPORT_FILE"

# 2. VERIFICAR XCODE COMMAND LINE TOOLS
echo "🔍 2. XCODE COMMAND LINE TOOLS" >> "$REPORT_FILE"
if xcode-select -p &>/dev/null; then
    echo "✅ Xcode CLI tools instalados: $(xcode-select -p)" >> "$REPORT_FILE"
else
    echo "❌ Xcode CLI tools NO instalados" >> "$REPORT_FILE"
    echo "   SOLUCIÓN: Ejecutar 'xcode-select --install'" >> "$REPORT_FILE"
fi
echo "" >> "$REPORT_FILE"

# 3. VERIFICAR HOMEBREW
echo "🔍 3. HOMEBREW" >> "$REPORT_FILE"
if command -v brew &>/dev/null; then
    echo "✅ Homebrew instalado: $(brew --version | head -1)" >> "$REPORT_FILE"
    echo "   Prefix: $(brew --prefix)" >> "$REPORT_FILE"
else
    echo "❌ Homebrew NO instalado" >> "$REPORT_FILE"
    echo "   SOLUCIÓN: /bin/bash -c '$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)'" >> "$REPORT_FILE"
fi
echo "" >> "$REPORT_FILE"

# 4. VERIFICAR PYTHON
echo "🔍 4. PYTHON" >> "$REPORT_FILE"
if command -v python3 &>/dev/null; then
    PY_VER=$(python3 --version 2>&1)
    echo "✅ Python encontrado: $PY_VER" >> "$REPORT_FILE"
    PY_PATH=$(which python3)
    echo "   Ubicación: $PY_PATH" >> "$REPORT_FILE"
    
    # Verificar versión mínima (3.11)
    PY_NUM=$(python3 -c "import sys; print(sys.version_info.major, sys.version_info.minor)")
    if python3 -c "import sys; exit(0 if sys.version_info >= (3, 11) else 1)"; then
        echo "✅ Versión >= 3.11 (correcto)" >> "$REPORT_FILE"
    else
        echo "⚠️ Versión < 3.11. Recomendado actualizar." >> "$REPORT_FILE"
        echo "   SOLUCIÓN: brew install python@3.11" >> "$REPORT_FILE"
    fi
else
    echo "❌ Python 3 NO encontrado" >> "$REPORT_FILE"
    echo "   SOLUCIÓN: brew install python@3.11" >> "$REPORT_FILE"
fi
echo "" >> "$REPORT_FILE"

# 5. VERIFICAR PIP
echo "🔍 5. PIP" >> "$REPORT_FILE"
if command -v pip3 &>/dev/null; then
    echo "✅ pip3 encontrado: $(pip3 --version)" >> "$REPORT_FILE"
else
    echo "❌ pip3 NO encontrado" >> "$REPORT_FILE"
    echo "   SOLUCIÓN: python3 -m ensurepip --upgrade" >> "$REPORT_FILE"
fi
echo "" >> "$REPORT_FILE"

# 6. VERIFICAR NODE.JS
echo "🔍 6. NODE.JS" >> "$REPORT_FILE"
if command -v node &>/dev/null; then
    echo "✅ Node.js encontrado: $(node --version)" >> "$REPORT_FILE"
else
    echo "⚠️ Node.js NO encontrado (opcional, para algunas features)" >> "$REPORT_FILE"
    echo "   SOLUCIÓN: brew install node" >> "$REPORT_FILE"
fi
echo "" >> "$REPORT_FILE"

# 7. VERIFICAR GIT
echo "🔍 7. GIT" >> "$REPORT_FILE"
if command -v git &>/dev/null; then
    echo "✅ Git encontrado: $(git --version)" >> "$REPORT_FILE"
else
    echo "⚠️ Git NO encontrado (opcional)" >> "$REPORT_FILE"
    echo "   SOLUCIÓN: brew install git" >> "$REPORT_FILE"
fi
echo "" >> "$REPORT_FILE"

# 8. VERIFICAR CURL
echo "🔍 8. CURL" >> "$REPORT_FILE"
if command -v curl &>/dev/null; then
    echo "✅ curl encontrado" >> "$REPORT_FILE"
else
    echo "❌ curl NO encontrado (necesario para instalar Hermes)" >> "$REPORT_FILE"
    echo "   SOLUCIÓN: brew install curl" >> "$REPORT_FILE"
fi
echo "" >> "$REPORT_FILE"

# 9. VERIFICAR GOOGLE CHROME
echo "🔍 9. GOOGLE CHROME" >> "$REPORT_FILE"
if [ -d "/Applications/Google Chrome.app" ]; then
    echo "✅ Google Chrome instalado" >> "$REPORT_FILE"
    # Verificar versión
    CHROME_VER=$(/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --version 2>/dev/null || echo "No se pudo verificar versión")
    echo "   Versión: $CHROME_VER" >> "$REPORT_FILE"
else
    echo "⚠️ Google Chrome NO instalado (necesario para Meet)" >> "$REPORT_FILE"
    echo "   SOLUCIÓN: Descargar de https://google.com/chrome" >> "$REPORT_FILE"
fi
echo "" >> "$REPORT_FILE"

# 10. VERIFICAR ESPACIO EN DISCO
echo "🔍 10. ESPACIO EN DISCO" >> "$REPORT_FILE"
DF_OUTPUT=$(df -h / 2>/dev/null | tail -1)
echo "   $DF_OUTPUT" >> "$REPORT_FILE"
AVAILABLE=$(echo "$DF_OUTPUT" | awk '{print $4}')
echo "   Espacio disponible: $AVAILABLE" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

# 11. VERIFICAR HERMES AGENT
echo "🔍 11. HERMES AGENT" >> "$REPORT_FILE"
if command -v hermes &>/dev/null; then
    echo "✅ Hermes instalado: $(hermes --version 2>/dev/null || echo 'versión desconocida')" >> "$REPORT_FILE"
    HERMES_PATH=$(which hermes)
    echo "   Ubicación: $HERMES_PATH" >> "$REPORT_FILE"
    
    # Verificar perfil
    if hermes profile list 2>/dev/null | grep -q "legal-pro"; then
        echo "✅ Perfil 'legal-pro' existe" >> "$REPORT_FILE"
    else
        echo "❌ Perfil 'legal-pro' NO encontrado" >> "$REPORT_FILE"
        echo "   SOLUCIÓN: Ejecutar install-mac.sh para importar perfil" >> "$REPORT_FILE"
    fi
else
    echo "❌ Hermes NO instalado" >> "$REPORT_FILE"
    echo "   SOLUCIÓN: curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash" >> "$REPORT_FILE"
fi
echo "" >> "$REPORT_FILE"

# 12. VERIFICAR API KEYS
echo "🔍 12. API KEYS CONFIGURADAS" >> "$REPORT_FILE"
ENV_FILE="$HOME/.hermes/.env"
if [ -f "$ENV_FILE" ]; then
    echo "✅ Archivo .env existe" >> "$REPORT_FILE"
    # Contar keys configuradas (no vacías)
    CONFIGURED=$(grep -v '^#' "$ENV_FILE" | grep -v '^$' | grep '=' | grep -v '=$' | wc -l)
    TOTAL=$(grep -v '^#' "$ENV_FILE" | grep -v '^$' | grep '=' | wc -l)
    echo "   Keys configuradas: $CONFIGURED / $TOTAL" >> "$REPORT_FILE"
    
    # Verificar keys específicas
    if grep -q "KIMI_API_KEY=" "$ENV_FILE" && ! grep -q "KIMI_API_KEY=$" "$ENV_FILE"; then
        echo "✅ KIMI_API_KEY configurada" >> "$REPORT_FILE"
    else
        echo "❌ KIMI_API_KEY NO configurada" >> "$REPORT_FILE"
    fi
    
    if grep -q "TELEGRAM_BOT_TOKEN=" "$ENV_FILE" && ! grep -q "TELEGRAM_BOT_TOKEN=$" "$ENV_FILE"; then
        echo "✅ TELEGRAM_BOT_TOKEN configurado" >> "$REPORT_FILE"
    else
        echo "❌ TELEGRAM_BOT_TOKEN NO configurado" >> "$REPORT_FILE"
    fi
else
    echo "❌ Archivo .env NO existe" >> "$REPORT_FILE"
    echo "   SOLUCIÓN: Copiar config/.env.template a ~/.hermes/.env y configurar" >> "$REPORT_FILE"
fi
echo "" >> "$REPORT_FILE"

# 13. VERIFICAR PERMISOS
echo "🔍 13. PERMISOS" >> "$REPORT_FILE"
HERMES_HOME="$HOME/.hermes"
if [ -d "$HERMES_HOME" ]; then
    echo "✅ Directorio ~/.hermes existe" >> "$REPORT_FILE"
    ls -la "$HERMES_HOME" >> "$REPORT_FILE" 2>/dev/null || echo "   (no se pudo listar)" >> "$REPORT_FILE"
else
    echo "❌ Directorio ~/.hermes NO existe" >> "$REPORT_FILE"
fi
echo "" >> "$REPORT_FILE"

# 14. VERIFICAR GATEWAY
echo "🔍 14. GATEWAY STATUS" >> "$REPORT_FILE"
if pgrep -f "hermes-gateway" > /dev/null 2>&1; then
    echo "✅ Gateway está corriendo" >> "$REPORT_FILE"
else
    echo "⚠️ Gateway NO está corriendo" >> "$REPORT_FILE"
    echo "   SOLUCIÓN: hermes gateway start" >> "$REPORT_FILE"
fi
echo "" >> "$REPORT_FILE"

# RESUMEN
echo "=======================================" >> "$REPORT_FILE"
echo "RESUMEN DE PROBLEMAS ENCONTRADOS" >> "$REPORT_FILE"
echo "=======================================" >> "$REPORT_FILE"
ERRORS=$(grep -c "❌" "$REPORT_FILE")
WARNINGS=$(grep -c "⚠️" "$REPORT_FILE")
echo "Errores críticos: $ERRORS" >> "$REPORT_FILE"
echo "Advertencias: $WARNINGS" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

if [ "$ERRORS" -eq 0 ] && [ "$WARNINGS" -eq 0 ]; then
    echo "🎉 TODO ESTÁ LISTO. Puedes usar Hermes Legal Pro." >> "$REPORT_FILE"
elif [ "$ERRORS" -eq 0 ]; then
    echo "⚠️ Hay advertencias pero no errores críticos. Puedes usar el sistema." >> "$REPORT_FILE"
else
    echo "❌ Hay errores críticos que debes resolver antes de usar el sistema." >> "$REPORT_FILE"
fi

echo "" >> "$REPORT_FILE"
echo "Reporte guardado en: $REPORT_FILE" >> "$REPORT_FILE"
echo "Envía este archivo a soporte@wscapital.ai si necesitas ayuda." >> "$REPORT_FILE"

# Mostrar resumen en pantalla
cat "$REPORT_FILE"
