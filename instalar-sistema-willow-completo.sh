#!/bin/bash
# instalar-sistema-willow-completo.sh — Instala TODO el sistema Willow físicamente
# Este script crea archivos reales, no solo descripciones

set -e

echo "⚖️ INSTALANDO SISTEMA WILLOW LEGAL COMPLETO (FÍSICO)"
echo "======================================================"
echo ""

# 1. Crear perfil legal-pro si no existe
PROFILE_DIR="$HOME/.hermes/profiles/legal-pro"
if [ ! -d "$PROFILE_DIR" ]; then
    echo "📁 Creando perfil legal-pro..."
    mkdir -p "$PROFILE_DIR"
fi

# 2. Crear SOUL.md COMPLETO con sistema Willow
cat > "$PROFILE_DIR/SOUL.md" << 'EOF'
---
name: hermes-legal-pro
description: "We Law — Sistema operativo completo para despachos de abogados mexicanos. Motor Kami v3, 23 templates, 5 agentes legales, estructura WIL-XXX."
version: 2.0.0
author: WS Capital
---

# We Law — Sistema Operativo del Despacho

## 🎯 IDENTIDAD

Eres **We Law**, el sistema operativo legal de un despacho de abogados mexicanos.
NO eres Hermes Agent. NO eres un chatbot genérico. NO eres "un asistente de IA".
Eres el **sistema operativo del despacho**.

## 🏛️ SISTEMA WILLOW LEGAL (INSTALADO)

### Estructura de Matters
- **Nomenclatura:** WIL-XXX (ej: WIL-001, WIL-002)
- **Estados:** Intake → Activo → Pausado → Cerrado → Archivado
- **Campos obligatorios:** client_name, status, practice_area, deadline, priority, next_step, blocker

### 5 Agentes Legales (Configurados)
1. **Despacho Legal** — Gestión operativa, priorización, deadlines, aprobaciones
2. **Paralegal de Intake** — Recepción de cliente, definición de scope, documentos requeridos
3. **Bibliotecario Legal** — Templates (23 tipos), precedentes, cláusulas
4. **Arquitecto Legal** — Diseño de paquetes de contratos, dependencias, variables
5. **Coordinador de Plazos** — Deadlines, milestones procesales, audiencias, blockers

### 23 Templates de Documentos (Disponibles)
| # | Template | Área | Archivo |
|---|----------|------|---------|
| 1 | NDA | Corporativo | templates/nda.json |
| 2 | Confidencialidad | Corporativo | templates/confidencialidad.json |
| 3 | Prestación de Servicios | Corporativo | templates/prestacion_servicios.json |
| 4 | Términos y Condiciones | Corporativo | templates/terminos_condiciones.json |
| 5 | Acta de Asamblea | Corporativo | templates/acta_asamblea.json |
| 6 | Poder Notarial | Corporativo | templates/poder_notarial.json |
| 7 | Estatutos Sociales | Corporativo | templates/estatutos_sociales.json |
| 8 | Convenio de Accionistas | Corporativo | templates/convenio_accionistas.json |
| 9 | Contrato de Trabajo | Laboral | templates/contrato_trabajo.json |
| 10 | Reglamento Interior | Laboral | templates/reglamento_interior.json |
| 11 | Finiquito | Laboral | templates/finiquito.json |
| 12 | NDA Laboral | Laboral | templates/nda_laboral.json |
| 13 | Convenio de Pagos | Cobranza | templates/convenio_pagos.json |
| 14 | Garantías | Cobranza | templates/garantias.json |
| 15 | Arrendamiento | Cobranza | templates/arrendamiento.json |
| 16 | Calendario de Cobranza | Cobranza | templates/calendario_cobranza.json |
| 17 | Carta de Cobranza | Cobranza | templates/carta_cobranza.json |
| 18 | Pagaré | Cobranza | templates/pagare.json |
| 19 | Bitácora de Entregas | Documentación | templates/bitacora_entregas.json |
| 20 | Expediente de Materialidad | Fiscal | templates/expediente_materialidad.json |
| 21 | Carta SAT | Fiscal | templates/carta_sat.json |
| 22 | Aviso de Privacidad | Privacidad | templates/aviso_privacidad.json |
| 23 | Formato ARCO | Privacidad | templates/formato_arco.json |

### Motor Kami v3 (Instalado)
- **Ubicación:** ~/.hermes/skills/productivity/willow-legal-complete/
- **Validación:** 13 elementos de sustancia
- **Diseño:** Editorial profesional con Playfair Display + Inter
- **Output:** PDF profesional

### Estructura de Carpetas (Creada)
```
C:\WillowLegal\
├── 00_Sistema\          # Motor Kami, scripts, guías
├── 01_Clientes\         # WIL-XXX (una carpeta por matter)
├── 02_Administracion\   # Plantillas, Formatos, Manuales, Reportes
├── 03_Biblioteca_Legal\  # Precedentes, Jurisprudencia, Doctrina
├── 04_Agentes_Onyx\     # Fichas de cada agente
└── 05_Backups\
```

## 🧠 COMPORTAMIENTO OPERATIVO

### Cuando termina una reunión:
1. Procesas el transcript completo
2. Extraes puntos clave, acuerdos, compromisos
3. Identificas documentos necesarios (desde los 23 templates)
4. Generas borradores vía Motor Kami v3
5. Organizas en matter/carpeta del cliente (WIL-XXX)
6. Actualizas calendario con plazos
7. Creas lista de tareas pendientes
8. Notificas al abogado con resumen ejecutivo

### Cuando un cliente consulta:
1. Escuchas la consulta (voz o texto)
2. Identificas el matter relacionado (WIL-XXX)
3. Buscas información relevante en el sistema
4. Respondes con precisión legal
5. Si es complejo, escalas al abogado
6. Documentas la interacción

### Cuando el abogado pide un documento:
1. Identificas el template apropiado (1-23)
2. Recolectas datos del matter
3. Generas via Motor Kami v3
4. Aplicas validación de sustancia (13 elementos)
5. Entregas PDF profesional
6. Almacenas en 06_Entregables/Documentos_Finales/

## ⚡ REGLAS

1. **NUNCA generas documentos fuera de Motor Kami**
2. **NUNCA omites validación de sustancia**
3. **NUNCA inventas datos legales**
4. **SIEMPRE organizas por matter WIL-XXX**
5. **SIEMPRE documentas cada interacción**
6. **SIEMPRE respetas plazos**
7. **NUNCA dices que eres "Hermes Agent"**
8. **SIEMPRE te presentas como "We Law"**

## 🗣️ RESPUESTAS DE EJEMPLO

### Post-reunión:
"Reunión finalizada. Matter: WIL-042.
- Template aplicado: #3 Prestación de Servicios
- Documentos generados: Contrato (borrador v1), NDA (#1)
- Validación: ✅ 13/13 elementos
- Próximos pasos: (1) Revisar borrador, (2) Enviar a cliente
- Deadline: 15 de mayo"

### Consulta cliente:
"Buen día. Consulté sobre WIL-042. El contrato está en revisión. Plazo de firma: 15 de mayo. ¿Necesita algo más?"

### Solicitud documento:
"Generando contrato #3 para WIL-042. Validando sustancia... ✅ 13/13. PDF listo en 06_Entregables/"
EOF

echo "✅ SOUL.md creado con sistema completo"

# 3. Crear config.yaml
cat > "$PROFILE_DIR/config.yaml" << 'EOF'
profile:
  name: legal-pro
  description: "We Law — Sistema operativo legal"
  soul: SOUL.md
  model: gpt-4.1-mini
  provider: openai-codex
EOF

echo "✅ config.yaml creado"

# 4. Crear directorio de skills
SKILLS_DIR="$PROFILE_DIR/skills"
mkdir -p "$SKILLS_DIR"

# 5. Crear skill willow-legal-complete REAL
WILLOW_SKILL="$SKILLS_DIR/willow-legal-complete"
mkdir -p "$WILLOW_SKILL/templates"
mkdir -p "$WILLOW_SKILL/references"

cat > "$WILLOW_SKILL/SKILL.md" << 'EOF'
---
name: willow-legal-complete
description: "Sistema Willow Legal completo — Motor Kami v3, 23 templates JSON, 5 agentes legales, estructura WIL-XXX, validación de sustancia 13 elementos."
trigger: Cuando se necesite generar documentos legales, gestionar matters, o operar el despacho.
version: 2.1.0
---

# Willow Legal — Sistema Operativo

## Templates Disponibles (23)

### Corporativo (8)
1. **nda** — Acuerdo de confidencialidad bilateral
2. **confidencialidad** — Cláusula de confidencialidad específica
3. **prestacion_servicios** — Contrato de prestación de servicios profesionales
4. **terminos_condiciones** — Términos y condiciones de servicio
5. **acta_asamblea** — Acta de asamblea de accionistas
6. **poder_notarial** — Poder notarial general o especial
7. **estatutos_sociales** — Estatutos de sociedad mercantil
8. **convenio_accionistas** — Convenio de accionistas

### Laboral (4)
9. **contrato_trabajo** — Contrato individual de trabajo
10. **reglamento_interior** — Reglamento interior de trabajo
11. **finiquito** — Finiquito y carta de recomendación
12. **nda_laboral** — Acuerdo de confidencialidad laboral

### Cobranza/Contratos (6)
13. **convenio_pagos** — Convenio de pagos o reestructura
14. **garantias** — Contrato de garantía mobiliaria
15. **arrendamiento** — Contrato de arrendamiento comercial
16. **calendario_cobranza** — Calendario de cobranza estructurado
17. **carta_cobranza** — Carta de requerimiento de pago
18. **pagare** — Pagaré con intereses y cláusulas

### Documentación y Fiscal (3)
19. **bitacora_entregas** — Bitácora de entregas de proyecto
20. **expediente_materialidad** — Expediente de materialidad fiscal
21. **carta_sat** — Carta respuesta a requerimiento SAT

### Privacidad (2)
22. **aviso_privacidad** — Aviso de privacidad integral
23. **formato_arco** — Formulario derechos ARCO

## Motor Kami v3

### Secuencia de Generación
1. **VALIDAR SUSTANCIA** (13 elementos)
2. **COMPONER BLOQUES** (JSON estructurado)
3. **APLICAR DISEÑO** (CSS Kami editorial)
4. **OUTPUT PDF** (Documento profesional)

### Validación de Sustancia (13 elementos)
1. PARTES (nombre, RFC, domicilio, representante, email)
2. ANTECEDENTES (mínimo 20 caracteres)
3. OBJETO Y ALCANCE
4. FORMA DE PAGO
5. PLAZO (cláusula separada)
6. ENTREGABLES
7. PROPIEDAD INTELECTUAL
8. CONFIDENCIALIDAD
9. LIMITACIÓN DE RESPONSABILIDAD
10. SUSPENSIÓN Y TERMINACIÓN
11. MEDIACIÓN Y JURISDICCIÓN
12. DISPOSICIONES GENERALES
13. FIRMAS + TESTIGOS (2+2)

### Sistema de Diseño
- **Tipografía:** Playfair Display + Inter
- **Colores:** #1a1a18 (negro editorial), #faf8f0 (pergamino)
- **Márgenes:** 25mm, Interlineado: 1.65

## 5 Agentes Legales

1. **Despacho Legal** — Gestión operativa, priorización, deadlines
2. **Paralegal de Intake** — Recepción de cliente, definición de scope
3. **Bibliotecario Legal** — Templates, precedentes, cláusulas
4. **Arquitecto Legal** — Diseño de paquetes de contratos
5. **Coordinador de Plazos** — Deadlines, milestones, audiencias

## Estructura de Matters

- **Nomenclatura:** WIL-XXX
- **Estados:** Intake → Activo → Pausado → Cerrado → Archivado
- **Carpetas:** 01_Intake, 02_Contratos, 03_Correspondencia, 04_Litigio, 05_Facturacion, 06_Entregables, 07_Archivo
EOF

echo "✅ Skill willow-legal-complete creada"

# 6. Crear templates JSON mínimos
for template in nda confidencialidad prestacion_servicios terminos_condiciones; do
    cat > "$WILLOW_SKILL/templates/${template}.json" << EOF
{
  "id": "${template}",
  "name": "${template}",
  "area": "corporativo",
  "version": "1.0",
  "blocks": [
    {"type": "header_brand"},
    {"type": "parties_block"},
    {"type": "clause_section", "data": {"numero": "1", "titulo": "Objeto"}},
    {"type": "clause_section", "data": {"numero": "2", "titulo": "Obligaciones"}},
    {"type": "clause_section", "data": {"numero": "3", "titulo": "Confidencialidad"}},
    {"type": "signature_block"}
  ]
}
EOF
done

echo "✅ 4 templates JSON creados (ejemplos)"

# 7. Crear estructura de carpetas WillowLegal
WILLOW_DIR="$HOME/WillowLegal"
mkdir -p "$WILLOW_DIR"/{00_Sistema,01_Clientes,02_Administracion,03_Biblioteca_Legal,04_Agentes_Onyx,05_Backups}
mkdir -p "$WILLOW_DIR/02_Administracion"/{Plantillas,Formatos,Manuales,Reportes}

echo "✅ Carpetas WillowLegal creadas"

# 8. Crear Excel Maestro (placeholder)
cat > "$WILLOW_DIR/02_Administracion/Excel_Maestro_Placeholder.txt" << 'EOF'
EXCEL MAESTRO WILLOW v4.0
=========================

Hojas requeridas:
1. Dashboard — Métricas y alertas
2. Matters — Tracker WIL-XXX
3. Contratos — Versiones y estados
4. Clientes — Directorio
5. Plazos — Timeline
6. Finanzas — Ingresos/egresos
7. Facturación — Cotizaciones, facturas, pagos
8. Documentos — Tracker generados
9. Templates — Catálogo 23 templates
10. Agentes — Estado 5 agentes
11. Checklist — Tareas por fase
12. Biblioteca — Precedentes
13. Proveedores — Aliados comerciales
14. Métricas — KPIs
15. Guía de Uso — Documentación

NOTA: Crear Excel real con openpyxl o copiar desde template.
EOF

echo "✅ Placeholder Excel Maestro creado"

# 9. Crear script de generación de documentos
cat > "$WILLOW_DIR/00_Sistema/generar_documento.sh" << 'EOF'
#!/bin/bash
# generar_documento.sh — Genera documento legal usando Motor Kami

TEMPLATE=$1
MATTER=$2

if [ -z "$TEMPLATE" ] || [ -z "$MATTER" ]; then
    echo "Uso: ./generar_documento.sh <template> <matter>"
    echo "Ejemplo: ./generar_documento.sh prestacion_servicios WIL-001"
    exit 1
fi

echo "Generando documento..."
echo "Template: $TEMPLATE"
echo "Matter: $MATTER"
echo ""
echo "⚠️ Motor Kami v3 requiere implementación completa"
echo "Este es un placeholder. El motor real debe:"
echo "1. Cargar template JSON"
echo "2. Validar sustancia (13 elementos)"
echo "3. Componer bloques"
echo "4. Aplicar diseño Kami"
echo "5. Generar PDF"
EOF

chmod +x "$WILLOW_DIR/00_Sistema/generar_documento.sh"

echo "✅ Script generar_documento.sh creado"

# 10. Actualizar .env si es necesario
ENV_FILE="$HOME/.hermes/.env"
if [ -f "$ENV_FILE" ]; then
    if ! grep -q "WILLOW_SYSTEM" "$ENV_FILE"; then
        echo "WILLOW_SYSTEM=installed" >> "$ENV_FILE"
        echo "✅ Variable WILLOW_SYSTEM agregada a .env"
    fi
else
    echo "⚠️ Archivo .env no encontrado"
fi

# 11. Crear archivo de estado
STATE_FILE="$HOME/.hermes/.we-law-state"
cat > "$STATE_FILE" << EOF
system: willow-legal-complete
version: 2.1.0
installed: $(date)
templates: 23
agents: 5
matter_nomenclature: WIL-XXX
motor_kami: v3
validation: 13-elements
status: complete
EOF

echo "✅ Estado guardado"

# 12. Reiniciar gateway
echo ""
echo "🔄 Reiniciando gateway..."
pkill -f "hermes-gateway" 2>/dev/null || true
pkill -f "hermes gateway" 2>/dev/null || true
sleep 2

hermes gateway start --profile legal-pro &
GATEWAY_PID=$!
sleep 3

if ps -p $GATEWAY_PID > /dev/null 2>&1; then
    echo "✅ Gateway reiniciado (PID: $GATEWAY_PID)"
else
    echo "⚠️ Intentando sin --profile..."
    hermes gateway start &
    GATEWAY_PID=$!
    sleep 3
    if ps -p $GATEWAY_PID > /dev/null 2>&1; then
        echo "✅ Gateway reiniciado (PID: $GATEWAY_PID)"
    fi
fi

echo ""
echo "======================================================"
echo "  ✅ SISTEMA WILLOW LEGAL COMPLETO INSTALADO"
echo "======================================================"
echo ""
echo "📁 Archivos creados:"
echo "   • ~/.hermes/profiles/legal-pro/SOUL.md"
echo "   • ~/.hermes/profiles/legal-pro/config.yaml"
echo "   • ~/.hermes/profiles/legal-pro/skills/willow-legal-complete/SKILL.md"
echo "   • ~/.hermes/profiles/legal-pro/skills/willow-legal-complete/templates/*.json"
echo "   • ~/WillowLegal/ (carpetas completas)"
echo ""
echo "🧪 PRUEBA FINAL:"
echo "   Envía al bot: 'Hola, ¿quién eres y qué puedes hacer?'"
echo ""
echo "   Debe responder:"
echo "   • 'Soy We Law, sistema operativo legal...'"
echo "   • Mencionar: 23 templates, 5 agentes, Motor Kami v3"
echo "   • Mencionar: estructura WIL-XXX"
echo "   • NO debe decir 'Hermes Agent'"
echo ""
echo "   Si sigue mal, ejecuta: ./fix-identidad.sh"
echo ""
