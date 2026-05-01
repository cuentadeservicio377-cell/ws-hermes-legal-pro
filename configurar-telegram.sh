#!/bin/bash
# configurar-telegram.sh — Configurar Telegram DESPUÉS de que todo funciona
# Este script se ejecuta cuando ya tienes Hermes funcionando

set -e

echo "=========================================="
echo "  CONFIGURACIÓN DE TELEGRAM"
echo "  (Ejecutar solo cuando Hermes ya funciona)"
echo "=========================================="
echo ""

# Verificar que hermes funciona
if ! command -v hermes &> /dev/null; then
    echo "❌ Hermes no está instalado. Ejecuta install-mac-simple.sh primero."
    exit 1
fi

echo "📱 PASO 1: Crear bot de Telegram"
echo ""
echo "1. Abre Telegram en tu teléfono o computadora"
echo "2. Busca @BotFather"
echo "3. Envía: /newbot"
echo "4. Sigue las instrucciones (nombre + username que termine en 'bot')"
echo "5. Copia el TOKEN que te da (ej: 123456789:ABCdefGHIjklMNOpqrsTUVwxyz)"
echo ""
echo "Presiona ENTER cuando tengas el token..."
read -r

echo ""
echo "📝 PASO 2: Configurar token"
echo ""
echo "Pega el token de tu bot:"
read -r BOT_TOKEN

if [ -z "$BOT_TOKEN" ]; then
    echo "❌ Token vacío. Abortando."
    exit 1
fi

# Validar formato básico
if [[ ! "$BOT_TOKEN" =~ ^[0-9]+:[A-Za-z0-9_-]+$ ]]; then
    echo "⚠ El token no tiene el formato esperado. ¿Estás seguro? (s/n)"
    read -r CONFIRM
    if [[ "$CONFIRM" != "s" && "$CONFIRM" != "S" ]]; then
        exit 1
    fi
fi

ENV_FILE="$HOME/.hermes/.env"

# Actualizar .env
if grep -q "TELEGRAM_BOT_TOKEN=" "$ENV_FILE"; then
    # Reemplazar línea existente
    sed -i '' "s/TELEGRAM_BOT_TOKEN=.*/TELEGRAM_BOT_TOKEN=$BOT_TOKEN/" "$ENV_FILE"
else
    # Agregar al final
    echo "TELEGRAM_BOT_TOKEN=$BOT_TOKEN" >> "$ENV_FILE"
fi

echo "✓ Token guardado en ~/.hermes/.env"

echo ""
echo "🏠 PASO 3: Obtener chat ID"
echo ""
echo "1. Busca tu bot en Telegram (por el username que creaste)"
echo "2. Envía cualquier mensaje (ej: 'hola')"
echo "3. Abre este enlace en navegador:"
echo "   https://api.telegram.org/bot${BOT_TOKEN}/getUpdates"
echo ""
echo "Busca un número largo después de 'chat': {'id': 123456789"
echo "Ese número es tu CHAT_ID"
echo ""
echo "Pega el CHAT_ID:"
read -r CHAT_ID

if [ -z "$CHAT_ID" ]; then
    echo "⚠ Chat ID vacío. Puedes configurarlo después editando ~/.hermes/.env"
else
    if grep -q "TELEGRAM_HOME_CHAT_ID=" "$ENV_FILE"; then
        sed -i '' "s/TELEGRAM_HOME_CHAT_ID=.*/TELEGRAM_HOME_CHAT_ID=$CHAT_ID/" "$ENV_FILE"
    else
        echo "TELEGRAM_HOME_CHAT_ID=$CHAT_ID" >> "$ENV_FILE"
    fi
    echo "✓ Chat ID guardado"
fi

echo ""
echo "🚀 PASO 4: Activar plugin de Telegram"
echo ""

# Intentar activar plugin
hermes plugins enable telegram 2>/dev/null || echo "⚠ Plugin telegram no encontrado, se usará gateway nativo"

echo ""
echo "🔄 PASO 5: Iniciar gateway"
echo ""
echo "Iniciando gateway de Telegram..."
echo "(Presiona Ctrl+C para detener cuando quieras)"
echo ""

# Verificar que las variables están configuradas
if grep -q "TELEGRAM_BOT_TOKEN=$" "$ENV_FILE"; then
    echo "❌ TELEGRAM_BOT_TOKEN está vacío en ~/.hermes/.env"
    echo "   Edita el archivo y agrega el token."
    exit 1
fi

# Iniciar gateway
hermes gateway start &
GATEWAY_PID=$!

echo "Gateway iniciado (PID: $GATEWAY_PID)"
echo ""
echo "=========================================="
echo "  ✅ TELEGRAM CONFIGURADO"
echo "=========================================="
echo ""
echo "Prueba:"
echo "1. Abre Telegram"
echo "2. Busca tu bot"
echo "3. Envía un mensaje"
echo "4. Deberías recibir respuesta de Hermes"
echo ""
echo "Para detener el gateway: kill $GATEWAY_PID"
echo "Para reiniciar: hermes gateway start"
echo ""
echo "Si no funciona, revisa:"
echo "   cat ~/.hermes/logs/gateway.log"
echo ""
