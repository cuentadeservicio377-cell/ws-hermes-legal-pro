#!/bin/bash
# auditar-sistema-willow.sh — Verifica QUÉ TIENE REALMENTE el bot
# Este script revisa archivos físicos, no descripciones

echo "🔍 AUDITORÍA REAL DEL SISTEMA WILLOW"
echo "======================================"
echo ""

# 1. Perfil legal-pro
PROFILE_DIR="$HOME/.hermes/profiles/legal-pro"
if [ -d "$PROFILE_DIR" ]; then
    echo "✅ Perfil legal-pro existe"
    echo "   Ubicación: $PROFILE_DIR"
    
    # Contar archivos
    FILE_COUNT=$(find "$PROFILE_DIR" -type f | wc -l)
    echo "   Archivos: $FILE_COUNT"
else
    echo "❌ Perfil legal-pro NO existe"
fi
echo ""

# 2. SOUL.md
SOUL_FILE="$PROFILE_DIR/SOUL.md"
if [ -f "$SOUL_FILE" ]; then
    echo "✅ SOUL.md existe"
    # Contar líneas
    LINES=$(wc -l < "$SOUL_FILE")
    echo "   Líneas: $LINES"
    # Verificar si menciona templates
    if grep -q "23" "$SOUL_FILE"; then
        echo "   Menciona 23 templates: SÍ"
    else
        echo "   Menciona 23 templates: NO"
    fi
else
    echo "❌ SOUL.md NO existe"
fi
echo ""

# 3. Skills del perfil
SKILLS_DIR="$PROFILE_DIR/skills"
if [ -d "$SKILLS_DIR" ]; then
    echo "✅ Directorio de skills existe"
    echo "   Skills encontradas:"
    find "$SKILLS_DIR" -name "SKILL.md" -exec dirname {} \; | while read skill_dir; do
        skill_name=$(basename "$skill_dir")
        echo "     - $skill_name"
    done
else
    echo "❌ Directorio de skills NO existe"
fi
echo ""

# 4. Motor Kami
KAMI_DIRS=(
    "$HOME/.hermes/skills/productivity/willow-legal-complete"
    "$PROFILE_DIR/skills/willow-legal-complete"
    "/tmp/hermes-legal-pro-v1.0.0/skills/willow-legal-complete"
)
KAMI_FOUND=false
for dir in "${KAMI_DIRS[@]}"; do
    if [ -d "$dir" ]; then
        echo "✅ Skill willow-legal-complete encontrada en: $dir"
        KAMI_FOUND=true
        # Contar archivos
        KAMI_FILES=$(find "$dir" -type f | wc -l)
        echo "   Archivos: $KAMI_FILES"
        break
    fi
done
if [ "$KAMI_FOUND" = false ]; then
    echo "❌ Skill willow-legal-complete NO encontrada en ningún lado"
fi
echo ""

# 5. Templates JSON
TEMPLATE_DIRS=(
    "$HOME/WillowLegal/00_Sistema/Motor_Kami/templates"
    "/tmp/hermes-legal-pro-v1.0.0/skills/willow-legal-complete/templates"
)
TEMPLATES_FOUND=false
for dir in "${TEMPLATE_DIRS[@]}"; do
    if [ -d "$dir" ]; then
        echo "✅ Directorio de templates encontrado en: $dir"
        TEMPLATE_COUNT=$(find "$dir" -name "*.json" | wc -l)
        echo "   Templates JSON: $TEMPLATE_COUNT"
        TEMPLATES_FOUND=true
        break
    fi
done
if [ "$TEMPLATES_FOUND" = false ]; then
    echo "❌ Directorio de templates NO encontrado"
fi
echo ""

# 6. Carpetas WillowLegal
WILLOW_DIR="$HOME/WillowLegal"
if [ -d "$WILLOW_DIR" ]; then
    echo "✅ Carpeta WillowLegal existe"
    echo "   Subcarpetas:"
    ls -1 "$WILLOW_DIR" 2>/dev/null | head -10
else
    echo "❌ Carpeta WillowLegal NO existe"
fi
echo ""

# 7. Excel Maestro
EXCEL_FILES=(
    "$HOME/WillowLegal/02_Administracion/Centro_Operativo_Maestro_Willow_v4.xlsx"
    "$HOME/Downloads/Centro_Operativo_Maestro_Willow_v4.xlsx"
)
EXCEL_FOUND=false
for file in "${EXCEL_FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ Excel Maestro encontrado en: $file"
        EXCEL_FOUND=true
        break
    fi
done
if [ "$EXCEL_FOUND" = false ]; then
    echo "❌ Excel Maestro NO encontrado"
fi
echo ""

# 8. Bridge API
BRIDGE_FILES=(
    "$HOME/WillowLegal/00_Sistema/willow_bridge.py"
    "/tmp/hermes-legal-pro-v1.0.0/skills/willow-legal-complete/bridge_api.py"
)
BRIDGE_FOUND=false
for file in "${BRIDGE_FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ Bridge API encontrado en: $file"
        BRIDGE_FOUND=true
        break
    fi
done
if [ "$BRIDGE_FOUND" = false ]; then
    echo "❌ Bridge API NO encontrado"
fi
echo ""

# 9. Config.yaml del perfil
CONFIG_FILE="$PROFILE_DIR/config.yaml"
if [ -f "$CONFIG_FILE" ]; then
    echo "✅ config.yaml existe"
    echo "   Contenido:"
    cat "$CONFIG_FILE"
else
    echo "❌ config.yaml NO existe"
fi
echo ""

# 10. Resumen
echo "======================================"
echo "RESUMEN DE LA AUDITORÍA"
echo "======================================"
echo ""

# Contar elementos faltantes
MISSING=0
[ ! -d "$PROFILE_DIR" ] && MISSING=$((MISSING+1))
[ ! -f "$SOUL_FILE" ] && MISSING=$((MISSING+1))
[ "$KAMI_FOUND" = false ] && MISSING=$((MISSING+1))
[ "$TEMPLATES_FOUND" = false ] && MISSING=$((MISSING+1))
[ ! -d "$WILLOW_DIR" ] && MISSING=$((MISSING+1))
[ "$EXCEL_FOUND" = false ] && MISSING=$((MISSING+1))
[ "$BRIDGE_FOUND" = false ] && MISSING=$((MISSING+1))

echo "Elementos faltantes: $MISSING / 7"
echo ""

if [ "$MISSING" -eq 0 ]; then
    echo "🎉 SISTEMA COMPLETO"
elif [ "$MISSING" -le 3 ]; then
    echo "⚠️ SISTEMA PARCIAL — Faltan algunos componentes"
else
    echo "❌ SISTEMA INCOMPLETO — Necesita instalación completa"
fi
echo ""
echo "Para instalar todo: ./instalar-sistema-willow-completo.sh"
echo ""
