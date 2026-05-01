#!/bin/bash
# fix-identidad.sh — Arregla la identidad de We Law
# Ejecutar si el bot responde como "Hermes Agent" en vez de "We Law"

echo "🔧 ARREGLANDO IDENTIDAD DE WE LAW"
echo "======================================"
echo ""

# 1. Verificar que existe el perfil legal-pro
if [ ! -d "$HOME/.hermes/profiles/legal-pro" ]; then
    echo "❌ Perfil 'legal-pro' NO existe"
    echo "   Reinstalando perfil..."
    
    # Buscar el tar.gz en el directorio del producto
    PRODUCT_DIR="$HOME/Downloads/hermes-legal-pro/hermes-legal-pro-v1.0.0"
    if [ -f "$PRODUCT_DIR/hermes-legal-pro-profile.tar.gz" ]; then
        tar -xzf "$PRODUCT_DIR/hermes-legal-pro-profile.tar.gz" -C "$HOME/.hermes/profiles/"
        echo "✓ Perfil reinstalado"
    else
        echo "❌ No se encontró hermes-legal-pro-profile.tar.gz"
        echo "   Busca el archivo y ejecuta:"
        echo "   tar -xzf hermes-legal-pro-profile.tar.gz -C ~/.hermes/profiles/"
        exit 1
    fi
fi

# 2. Activar perfil legal-pro
echo "📝 Activando perfil 'legal-pro'..."
hermes profile use legal-pro
if [ $? -eq 0 ]; then
    echo "✓ Perfil 'legal-pro' activado"
else
    echo "❌ Error al activar perfil"
    exit 1
fi

# 3. Verificar que SOUL.md existe
SOUL_FILE="$HOME/.hermes/profiles/legal-pro/SOUL.md"
if [ -f "$SOUL_FILE" ]; then
    echo "✓ SOUL.md encontrado"
    echo "   Primeras líneas:"
    head -3 "$SOUL_FILE"
else
    echo "❌ SOUL.md NO encontrado en $SOUL_FILE"
    echo "   Creando SOUL.md básico..."
    
    mkdir -p "$HOME/.hermes/profiles/legal-pro"
    cat > "$SOUL_FILE" << 'EOF'
---
name: hermes-legal-pro
description: "We Law — Asistente legal inteligente para despachos de abogados"
version: 1.0.0
author: WS Capital
---

# We Law — Identidad

Eres **We Law**, el asistente legal inteligente de un despacho de abogados.
NO eres Hermes Agent. NO eres un chatbot genérico.
Eres el **sistema operativo del despacho**.

## Tu propósito:
- Escuchar reuniones con clientes
- Generar documentos legales profesionales
- Organizar casos y plazos
- Atender consultas de clientes
- Liberar al abogado del trabajo administrativo

## Tono:
- Profesional pero cercano
- Preciso legalmente
- Proactivo
- Discreto

## Reglas:
1. NUNCA dices que eres "Hermes Agent" o "un asistente de IA"
2. SIEMPRE te presentas como "We Law" o "tu asistente legal"
3. NUNCA generas documentos fuera del Motor Kami
4. SIEMPRE organizas por matter
EOF
    echo "✓ SOUL.md creado"
fi

# 4. Verificar config.yaml del perfil
CONFIG_FILE="$HOME/.hermes/profiles/legal-pro/config.yaml"
if [ -f "$CONFIG_FILE" ]; then
    echo "✓ config.yaml encontrado"
    
    # Verificar que tiene SOUL.md referenciado
    if grep -q "soul" "$CONFIG_FILE" || grep -q "SOUL" "$CONFIG_FILE"; then
        echo "✓ SOUL.md está referenciado en config"
    else
        echo "⚠ SOUL.md NO está referenciado en config.yaml"
        echo "   Agregando referencia..."
        echo "soul: SOUL.md" >> "$CONFIG_FILE"
        echo "✓ Referencia agregada"
    fi
else
    echo "⚠ config.yaml NO encontrado, creando..."
    cat > "$CONFIG_FILE" << 'EOF'
profile:
  name: legal-pro
  description: "We Law — Asistente legal"
  soul: SOUL.md
  model: kimi-k2.6
  provider: kimi-coding
EOF
    echo "✓ config.yaml creado"
fi

# 5. Reiniciar gateway si está corriendo
echo ""
echo "🔄 Reiniciando gateway..."

# Detener gateway actual
pkill -f "hermes-gateway" 2>/dev/null || true
pkill -f "hermes gateway" 2>/dev/null || true
sleep 2

# Verificar que se detuvo
if pgrep -f "hermes-gateway" > /dev/null 2>&1; then
    echo "⚠ Gateway sigue corriendo, forzando..."
    pkill -9 -f "hermes-gateway" 2>/dev/null || true
fi

echo "✓ Gateway detenido"

# 6. Iniciar gateway con perfil legal-pro
echo ""
echo "🚀 Iniciando gateway con perfil 'legal-pro'..."
echo "   hermes gateway start --profile legal-pro"
hermes gateway start --profile legal-pro &
GATEWAY_PID=$!

sleep 3

# Verificar que arrancó
if ps -p $GATEWAY_PID > /dev/null 2>&1; then
    echo "✓ Gateway iniciado (PID: $GATEWAY_PID)"
else
    echo "⚠ Gateway no arrancó, intentando sin --profile..."
    hermes gateway start &
    GATEWAY_PID=$!
    sleep 3
    
    if ps -p $GATEWAY_PID > /dev/null 2>&1; then
        echo "✓ Gateway iniciado (PID: $GATEWAY_PID)"
    else
        echo "❌ Gateway no pudo iniciar"
        echo "   Revisa: hermes doctor"
        exit 1
    fi
fi

# 7. Prueba de identidad
echo ""
echo "🧪 PROBANDO IDENTIDAD..."
echo "   Envía un mensaje a tu bot de Telegram: 'Hola, ¿quién eres?'"
echo "   Debe responder: 'Soy We Law, tu asistente legal...'"
echo "   NO debe decir 'Hermes Agent'"
echo ""

# 8. Guardar estado
STATE_FILE="$HOME/.hermes/.we-law-state"
cat > "$STATE_FILE" << EOF
last_fix: $(date)
profile: legal-pro
soul_md: $SOUL_FILE
gateway_pid: $GATEWAY_PID
EOF

echo "✓ Estado guardado en $STATE_FILE"
echo ""
echo "=========================================="
echo "  ✅ IDENTIDAD CONFIGURADA"
echo "=========================================="
echo ""
echo "Si sigue diciendo 'Hermes Agent':"
echo "1. Verifica que enviaste mensaje AL BOT CORRECTO"
echo "2. Revisa que no tengas OTRO bot conectado"
echo "3. Prueba: hermes chat -q 'Quien eres' --profile legal-pro"
echo ""
echo "Para verificar: cat ~/.hermes/profiles/legal-pro/SOUL.md"
echo ""
