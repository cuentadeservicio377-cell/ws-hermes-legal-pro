#!/bin/bash
# actualizar.sh — Actualiza Hermes Legal Pro desde GitHub v2.0
# Uso: ./actualizar.sh
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

echo "🔄 Hermes Legal Pro — Actualizador"
echo "   Repo: github.com/cuentadeservicio377-cell/ws-hermes-legal-pro"
echo ""

# ── Verificar conexión con GitHub ──────────────────────────
echo "🔗 Verificando conexión con GitHub..."
if ! git remote -v | grep -q "origin.*github.com"; then
    echo "❌ No hay remote 'origin' configurado. Ejecuta:"
    echo "   git remote add origin https://github.com/cuentadeservicio377-cell/ws-hermes-legal-pro.git"
    exit 1
fi

# ── Guardar cambios locales (si hay) ──────────────────────
if ! git diff --quiet || ! git diff --cached --quiet; then
    echo "📦 Guardando cambios locales..."
    git stash push -m "auto-stash $(date +%Y%m%d_%H%M%S)"
    STASHED=true
else
    STASHED=false
fi

# ── Pull ──────────────────────────────────────────────────
echo "⬇️  Descargando actualizaciones..."
if git pull origin master; then
    echo "✅ Código actualizado"
else
    echo "❌ Error al descargar. Reintentando con merge..."
    git pull origin master --no-rebase || {
        echo "❌ Error fatal al actualizar"
        [ "$STASHED" = true ] && git stash pop
        exit 1
    }
fi

# ── Restaurar stash si aplica ─────────────────────────────
if [ "$STASHED" = true ]; then
    echo "📦 Restaurando cambios locales..."
    git stash pop 2>/dev/null || echo "⚠️  No se pudieron restaurar cambios locales (posible conflicto)"
fi

# ── Reiniciar Dashboard ───────────────────────────────────
echo ""
echo "🔄 Reiniciando dashboard..."
cd "$SCRIPT_DIR/dashboard"

# Detener dashboard si corre
if pkill -f "python3.*app\.py" 2>/dev/null; then
    echo "   Dashboard detenido"
    sleep 1
fi

# Iniciar de nuevo
nohup python3 backend/app.py > /tmp/hermes-dashboard.log 2>&1 &
DASH_PID=$!
sleep 2

# Verificar que arrancó
if curl -s http://localhost:8082/api/health > /dev/null 2>&1; then
    echo "✅ Dashboard reiniciado (PID: $DASH_PID)"
    echo "   URL: http://localhost:8082"
else
    echo "⚠️  Dashboard iniciado pero sin respuesta aún. Revisa:"
    echo "   cat /tmp/hermes-dashboard.log"
fi

# ── Reiniciar Gateway de Telegram (si está corriendo) ─────
if pgrep -f "hermes.*gateway" > /dev/null 2>&1; then
    echo ""
    echo "🔄 Reiniciando gateway de Telegram..."
    hermes gateway stop 2>/dev/null || true
    sleep 1
    nohup hermes gateway start > /tmp/hermes-gateway.log 2>&1 &
    echo "✅ Gateway reiniciado"
fi

echo ""
echo "=========================================="
echo "  ✅ Hermes Legal Pro actualizado"
echo "  📅 $(date '+%Y-%m-%d %H:%M:%S')"
echo "  🔖 $(git log -1 --format='%h %s')"
echo "=========================================="
