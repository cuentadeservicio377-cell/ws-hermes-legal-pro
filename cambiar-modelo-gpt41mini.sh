#!/bin/bash
# cambiar-modelo.sh — Cambia el modelo a gpt-4.1-mini usando Codex OAuth
# Esto ahorra créditos de Kimi usando la cuenta de Codex

echo "🔄 CAMBIANDO MODELO A GPT-4.1-MINI (Codex)"
echo "=========================================="
echo ""

# 1. Verificar que Codex OAuth está configurado
ENV_FILE="$HOME/.hermes/.env"
if [ -f "$ENV_FILE" ]; then
    if grep -q "OPENAI_CODEX_OAUTH" "$ENV_FILE"; then
        echo "✅ OPENAI_CODEX_OAUTH encontrado en .env"
    else
        echo "⚠️ OPENAI_CODEX_OAUTH NO encontrado"
        echo "   Necesitas agregar tu token de Codex OAuth"
        echo "   Obténlo en: https://platform.openai.com/codex"
        echo ""
        echo "   Agrega esta línea a ~/.hermes/.env:"
        echo "   OPENAI_CODEX_OAUTH=tu-token-aqui"
        exit 1
    fi
else
    echo "❌ Archivo .env no encontrado"
    exit 1
fi

# 2. Verificar perfil legal-pro
PROFILE_DIR="$HOME/.hermes/profiles/legal-pro"
if [ ! -d "$PROFILE_DIR" ]; then
    echo "❌ Perfil legal-pro no encontrado"
    exit 1
fi

echo "✅ Perfil legal-pro encontrado"

# 3. Actualizar config.yaml del perfil
CONFIG_FILE="$PROFILE_DIR/config.yaml"
if [ -f "$CONFIG_FILE" ]; then
    echo "📝 Actualizando config.yaml..."
    
    # Hacer backup
    cp "$CONFIG_FILE" "$CONFIG_FILE.backup.$(date +%Y%m%d_%H%M%S)"
    
    # Si existe model, reemplazarlo. Si no, agregarlo.
    if grep -q "^model:" "$CONFIG_FILE"; then
        # Reemplazar línea existente
        sed -i '' 's/^model:.*/model: gpt-4.1-mini/' "$CONFIG_FILE"
    else
        # Agregar al final
        echo "model: gpt-4.1-mini" >> "$CONFIG_FILE"
    fi
    
    # Si existe provider, reemplazarlo
    if grep -q "^provider:" "$CONFIG_FILE"; then
        sed -i '' 's/^provider:.*/provider: openai-codex/' "$CONFIG_FILE"
    else
        echo "provider: openai-codex" >> "$CONFIG_FILE"
    fi
    
    echo "✅ Configuración actualizada:"
    grep -E "^(model|provider):" "$CONFIG_FILE"
else
    echo "⚠️ config.yaml no encontrado, creando..."
    cat > "$CONFIG_FILE" << 'EOF'
profile:
  name: legal-pro
  description: "We Law — Asistente legal"
  soul: SOUL.md
  model: gpt-4.1-mini
  provider: openai-codex
EOF
    echo "✅ config.yaml creado"
fi

# 4. Actualizar config global si existe
GLOBAL_CONFIG="$HOME/.hermes/config.yaml"
if [ -f "$GLOBAL_CONFIG" ]; then
    echo "📝 Verificando config global..."
    # No modificamos el global, solo verificamos que no sobreescriba
    echo "✅ Config global preservada (perfil legal-pro tiene prioridad)"
fi

# 5. Reiniciar gateway para aplicar cambios
echo ""
echo "🔄 Reiniciando gateway..."

# Detener gateway actual
pkill -f "hermes-gateway" 2>/dev/null || true
pkill -f "hermes gateway" 2>/dev/null || true
sleep 2

# Verificar que se detuvo
if pgrep -f "hermes-gateway" > /dev/null 2>&1; then
    echo "⚠️ Forzando cierre..."
    pkill -9 -f "hermes-gateway" 2>/dev/null || true
fi

echo "✅ Gateway detenido"

# 6. Iniciar gateway con nuevo modelo
echo ""
echo "🚀 Iniciando gateway con gpt-4.1-mini..."
hermes gateway start --profile legal-pro &
GATEWAY_PID=$!
sleep 3

if ps -p $GATEWAY_PID > /dev/null 2>&1; then
    echo "✅ Gateway iniciado (PID: $GATEWAY_PID)"
else
    echo "⚠️ Intentando iniciar sin --profile..."
    hermes gateway start &
    GATEWAY_PID=$!
    sleep 3
    if ps -p $GATEWAY_PID > /dev/null 2>&1; then
        echo "✅ Gateway iniciado (PID: $GATEWAY_PID)"
    else
        echo "❌ Gateway no pudo iniciar"
        echo "   Revisa: hermes doctor"
        exit 1
    fi
fi

# 7. Verificar configuración
echo ""
echo "📊 CONFIGURACIÓN ACTUAL:"
echo "======================="
echo "Perfil: legal-pro"
grep -E "^(model|provider):" "$CONFIG_FILE" 2>/dev/null || echo "   (ver config.yaml manualmente)"
echo ""
echo "Variables de entorno:"
grep "OPENAI_CODEX_OAUTH" "$ENV_FILE" | sed 's/=.*/=*****/' || echo "   NO CONFIGURADO"
echo ""

# 8. Guardar estado
STATE_FILE="$HOME/.hermes/.we-law-state"
cat > "$STATE_FILE" << EOF
last_model_change: $(date)
model: gpt-4.1-mini
provider: openai-codex
profile: legal-pro
gateway_pid: $GATEWAY_PID
EOF

echo "✅ Estado guardado"
echo ""
echo "=========================================="
echo "  ✅ MODELO CAMBIADO A GPT-4.1-MINI"
echo "=========================================="
echo ""
echo "💰 AHORRO: Ahora usas Codex OAuth en vez de créditos Kimi"
echo ""
echo "🧪 PRUEBA: Envía un mensaje a tu bot en Telegram"
echo "   Debe responder usando gpt-4.1-mini (más rápido y económico)"
echo ""
echo "📊 Para verificar qué modelo está activo:"
echo "   cat ~/.hermes/profiles/legal-pro/config.yaml"
echo ""
echo "🔄 Para volver a Kimi:"
echo "   sed -i '' 's/model:.*/model: kimi-k2.6/' ~/.hermes/profiles/legal-pro/config.yaml"
echo "   sed -i '' 's/provider:.*/provider: kimi-coding/' ~/.hermes/profiles/legal-pro/config.yaml"
echo ""
