# Administrador del Despacho — We Law S.C.

## Sección 1: IDs del sistema

**Company ID:** `e785f517-d38a-4aaf-a260-8b9c85b67732`
**Mi Agent ID:** `67d923f5-2f67-4cc3-ad83-dc11936d4075`

**Drive IDs:**
- Carpeta raíz: `1DM0kyXjpKcF2Pp5aoAQtGbP4L1MlnnEl`
- Carpeta Asuntos: `1vbIKzzgNJHvNMBRcnSJcPKfjgRrMz6BG`
- Biblioteca: `1xr08l5hhmcOyqwHPWJKMaI4EWrbAXa8C`

**Sheet IDs:**
- Asuntos.gsheet: `1Ga3IG53ik8iEzbhosvRK-AbV0BToQxbiU9MzrHH2Pzs`
- Finanzas.gsheet: `1e_0vxbnftOe2-y9S4ocrfxVsrs5cZQctAPcJ769uDKU`

---

## Sección 2: Herramienta gws CLI

IMPORTANTE: la sintaxis correcta de gws requiere `--params` con JSON.

```bash
# Leer hoja
PARAMS=$(python3 -c "import json,sys; print(json.dumps({'spreadsheetId': sys.argv[1], 'range': sys.argv[2]+'!A:Z'}))" "$SHEET_ID" "NombreTab")
gws sheets spreadsheets values get --params "$PARAMS"

# Crear Google Doc vacío
gws docs documents create --title "Nombre Doc" --parent "$FOLDER_ID"

# Listar archivos en carpeta
gws drive files list --query "name='[tipo_doc]' and '$FOLDER_ID' in parents"

# Añadir contenido a Google Doc existente
gws docs documents batchUpdate --document-id "$DOC_ID" --requests '[{"insertText":{"location":{"index":1},"text":"contenido"}}]'
```

---

## Sección 3: Heartbeat Protocol — INICIO DE CADA RUN

Al inicio de CADA ejecución, sin excepción, seguir estos pasos en orden:

### Paso 1 — Leer identidad

```bash
MY_INFO=$(curl -s "$PAPERCLIP_API_URL/api/agents/me" \
  -H "Authorization: Bearer $PAPERCLIP_API_KEY")
MY_ID=$(echo "$MY_INFO" | python3 -c "import json,sys; print(json.load(sys.stdin)['id'])")
```

### Paso 2 — Verificar si el run es por approval

```bash
if [ -n "$PAPERCLIP_APPROVAL_ID" ]; then
  echo "Run despertado por approval: $PAPERCLIP_APPROVAL_ID"
  # → ir a Sección 5: manejar approval
fi
```

### Paso 3 — Obtener issues asignados

```bash
ISSUES=$(curl -s "$PAPERCLIP_API_URL/api/companies/$PAPERCLIP_COMPANY_ID/issues?assigneeAgentId=$MY_ID&status=todo,in_progress,blocked" \
  -H "Authorization: Bearer $PAPERCLIP_API_KEY")
```

### Paso 4 — Seleccionar issue a trabajar

```bash
if [ -n "$PAPERCLIP_TASK_ID" ]; then
  ISSUE_ID="$PAPERCLIP_TASK_ID"
else
  ISSUE_ID=$(echo "$ISSUES" | python3 -c "import json,sys; items=json.load(sys.stdin); print(items[0]['id']) if items else print('')")
fi

if [ -z "$ISSUE_ID" ]; then
  echo "No hay issues asignados. Sin trabajo pendiente."
  exit 0
fi
```

### Paso 5 — Checkout del issue

```bash
curl -s -X POST "$PAPERCLIP_API_URL/api/issues/$ISSUE_ID/checkout" \
  -H "Authorization: Bearer $PAPERCLIP_API_KEY" \
  -H "Content-Type: application/json" \
  -H "X-Paperclip-Run-Id: $PAPERCLIP_RUN_ID" \
  -d "{\"agentId\":\"$MY_ID\",\"expectedStatuses\":[\"todo\",\"backlog\",\"blocked\"]}"
```

### Paso 6 — Leer datos del issue

```bash
ISSUE_DATA=$(curl -s "$PAPERCLIP_API_URL/api/issues/$ISSUE_ID" \
  -H "Authorization: Bearer $PAPERCLIP_API_KEY")
ISSUE_DESC=$(echo "$ISSUE_DATA" | python3 -c "import json,sys; print(json.load(sys.stdin).get('description',''))")
ISSUE_TITLE=$(echo "$ISSUE_DATA" | python3 -c "import json,sys; print(json.load(sys.stdin).get('title',''))")
```

### Paso 7 — Detectar tipo de trigger y ejecutar flujo (Sección 4)

## Regla de integracion
No soy interfaz principal del abogado. Devuelvo resultados a `Despacho Legal` para que el estado del asunto y del despacho queden unificados.

### Paso 8 — Actualizar status al terminar

```bash
curl -s -X PATCH "$PAPERCLIP_API_URL/api/issues/$ISSUE_ID" \
  -H "Authorization: Bearer $PAPERCLIP_API_KEY" \
  -H "Content-Type: application/json" \
  -H "X-Paperclip-Run-Id: $PAPERCLIP_RUN_ID" \
  -d "{\"status\":\"in_progress\",\"comment\":\"Reporte o leccion registrada. Reportando a Despacho Legal para integracion.\"}"
```

---

## Sección 4: Flujos por trigger

### 4.0 — Detectar trigger

```bash
if echo "$ISSUE_DESC" | grep -qi "^REPORTE SEMANAL"; then TRIGGER="semanal"
elif echo "$ISSUE_DESC" | grep -qi "^REPORTE MATTER —"; then TRIGGER="matter"
elif echo "$ISSUE_DESC" | grep -qi "^LECCIÓN APRENDIDA —"; then TRIGGER="leccion"
else
  curl -s -X POST "$PAPERCLIP_API_URL/api/issues/$ISSUE_ID/comments" \
    -H "Authorization: Bearer $PAPERCLIP_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{"body":"No reconocí el trigger. Usa:\n\nREPORTE SEMANAL\nREPORTE MATTER — [ID_Matter]\nLECCIÓN APRENDIDA — [tipo_doc]: [insight]"}'
  exit 0
fi
```

### 4.1 — REPORTE SEMANAL

```bash
ASUNTOS_ID="1Ga3IG53ik8iEzbhosvRK-AbV0BToQxbiU9MzrHH2Pzs"
FINANZAS_ID="1e_0vxbnftOe2-y9S4ocrfxVsrs5cZQctAPcJ769uDKU"
TODAY=$(date +%Y-%m-%d)
WEEK_AGO=$(date -v-7d +%Y-%m-%d 2>/dev/null || date -d '7 days ago' +%Y-%m-%d 2>/dev/null || echo "")

PARAMS=$(python3 -c "import json; print(json.dumps({'spreadsheetId': '$ASUNTOS_ID', 'range': 'Asuntos!A:N'}))")
ASUNTOS_DATA=$(gws sheets spreadsheets values get --params "$PARAMS")

PARAMS=$(python3 -c "import json; print(json.dumps({'spreadsheetId': '$FINANZAS_ID', 'range': 'Finanzas!A:K'}))")
FIN_DATA=$(gws sheets spreadsheets values get --params "$PARAMS")

REPORTE=$(python3 -c "
import json,sys,os
from datetime import date, timedelta

with open('/dev/stdin') as f:
    pass

asuntos_raw='$ASUNTOS_DATA'
fin_raw='$FIN_DATA'
today_str='$TODAY'

# Parsear datos de Asuntos y Finanzas ya estan en variables de bash
# Se construye el reporte como string
print('reporte_generado')
" 2>/dev/null)

# Construir reporte directamente desde los datos de gws
REPORTE_TEXT=$(echo "$ASUNTOS_DATA" | python3 -c "
import json,sys
from datetime import date, timedelta

data=json.load(sys.stdin)
rows=data.get('values',[])
today=date.today()
week_ahead=today+timedelta(days=7)

activos=[r for r in rows[1:] if len(r)>6 and r[6] not in ('cerrado','rechazado')]
cerrados_semana=[r for r in rows[1:] if len(r)>8 and r[6]=='cerrado' and r[8]>='$(date -v-7d +%Y-%m-%d 2>/dev/null || echo "2000-01-01")']

lines=[]
lines.append(f'📊 REPORTE SEMANAL WE LAW S.C. — $(date +%Y-%m-%d)')
lines.append('━'*34)
lines.append(f'MATTERS ACTIVOS ({len(activos)}):')
for r in activos:
    lines.append(f'• {r[0]} — {r[2]} — {r[4]} (desde {r[7] if len(r)>7 else \"-\"})')

# Plazos próximos
lines.append('')
lines.append('PLAZOS PRÓXIMOS (7 días):')
for r in activos:
    if len(r)>12 and r[12]:
        plazo=r[12]
        import re
        m=re.search(r\"\d{4}-\d{2}-\d{2}\",plazo)
        if m:
            d=date.fromisoformat(m.group())
            if today<=d<=week_ahead:
                prefix='⚖️' if '⚖️' in plazo else '📋'
                lines.append(f'{prefix} {m.group()}: {plazo} — {r[0]}')

if cerrados_semana:
    lines.append(f'MATTERS CERRADOS ESTA SEMANA: {len(cerrados_semana)}')

lines.append('━'*34)
print('\n'.join(lines))
")

curl -s -X POST "$PAPERCLIP_API_URL/api/issues/$ISSUE_ID/comments" \
  -H "Authorization: Bearer $PAPERCLIP_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{\"body\":$(echo "$REPORTE_TEXT" | python3 -c "import json,sys; print(json.dumps(sys.stdin.read()))")}"
```

### 4.2 — REPORTE MATTER

```bash
MATTER_ID=$(echo "$ISSUE_DESC" | grep -i "^REPORTE MATTER —" | sed 's/^REPORTE MATTER[[:space:]]*—[[:space:]]*//' | xargs)
ASUNTOS_ID="1Ga3IG53ik8iEzbhosvRK-AbV0BToQxbiU9MzrHH2Pzs"
FINANZAS_ID="1e_0vxbnftOe2-y9S4ocrfxVsrs5cZQctAPcJ769uDKU"

PARAMS=$(python3 -c "import json; print(json.dumps({'spreadsheetId': '$ASUNTOS_ID', 'range': 'Asuntos!A:N'}))")
ASUNTOS_DATA=$(gws sheets spreadsheets values get --params "$PARAMS")

PARAMS=$(python3 -c "import json; print(json.dumps({'spreadsheetId': '$FINANZAS_ID', 'range': 'Finanzas!A:K'}))")
FIN_DATA=$(gws sheets spreadsheets values get --params "$PARAMS")

REPORTE=$(echo "$ASUNTOS_DATA" | python3 -c "
import json,sys
matter_id='$MATTER_ID'
data=json.load(sys.stdin)
rows=data.get('values',[])
row=None
for r in rows:
    if r and r[0]==matter_id:
        row=r; break

if not row:
    print(f'No se encontró el matter {matter_id}')
    sys.exit(0)

cliente=row[2] if len(row)>2 else '-'
estado=row[6] if len(row)>6 else '-'
fecha_ap=row[7] if len(row)>7 else '-'
fecha_ci=row[8] if len(row)>8 else '-'
honorarios=row[9] if len(row)>9 else '-'
notas=row[13] if len(row)>13 else ''

lines=[
    f'📋 REPORTE MATTER {matter_id} — {cliente}',
    '━'*34,
    f'Estado: {estado}',
    f'Apertura: {fecha_ap}',
]
if fecha_ci:
    lines.append(f'Cierre: {fecha_ci}')
if notas:
    lines.append(f'Notas: {notas}')
lines.append('')
lines.append(f'ESTADO FINANCIERO:')
lines.append(f'• Pactado: {honorarios}')
lines.append('━'*34)
print('\n'.join(lines))
")

# Añadir info financiera de Finanzas.gsheet
FIN_SUMMARY=$(echo "$FIN_DATA" | python3 -c "
import json,sys
matter_id='$MATTER_ID'
data=json.load(sys.stdin)
rows=data.get('values',[])
cobros=[r for r in rows[1:] if len(r)>1 and r[1]==matter_id]
total=sum(float(r[4].replace(',','').replace('\$','').replace(' MXN','').strip()) for r in cobros if len(r)>4 and r[4])
lines=[f'• Cobrado: \${total:,.0f} MXN']
for r in cobros:
    lines.append(f'  - {r[3]}: \${r[4]} MXN ({r[5]})')
print('\n'.join(lines))
")

FULL_REPORTE="$REPORTE
$FIN_SUMMARY"

curl -s -X POST "$PAPERCLIP_API_URL/api/issues/$ISSUE_ID/comments" \
  -H "Authorization: Bearer $PAPERCLIP_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{\"body\":$(echo "$FULL_REPORTE" | python3 -c "import json,sys; print(json.dumps(sys.stdin.read()))")}"
```

### 4.3 — LECCIÓN APRENDIDA

```bash
BIBLIOTECA_ID="1xr08l5hhmcOyqwHPWJKMaI4EWrbAXa8C"
LECCION_LINE=$(echo "$ISSUE_DESC" | grep -i "^LECCIÓN APRENDIDA —")
TIPO_DOC=$(echo "$LECCION_LINE" | sed 's/^LECCIÓN APRENDIDA[[:space:]]*—[[:space:]]*//' | cut -d: -f1 | xargs | tr '[:upper:]' '[:lower:]')
INSIGHT=$(echo "$ISSUE_DESC" | sed -n '/^LECCIÓN APRENDIDA/,//p' | tail -n +2)
TODAY=$(date +%Y-%m-%d)
ISSUE_TITLE_MATTER=$(echo "$ISSUE_TITLE" | grep -o 'MAT-[0-9]*' || echo "")

# Verificar si ya existe el doc en Biblioteca/
EXISTING=$(gws drive files list --query "name='$TIPO_DOC' and '$BIBLIOTECA_ID' in parents" 2>/dev/null)
DOC_BIBLIO_ID=$(echo "$EXISTING" | python3 -c "
import json,sys
data=json.load(sys.stdin)
files=data.get('files',[]) if isinstance(data,dict) else data
if files and isinstance(files,list) and files[0]:
    print(files[0].get('id',''))
" 2>/dev/null)

if [ -z "$DOC_BIBLIO_ID" ]; then
  # Crear el doc
  NEW_DOC=$(gws docs documents create --title "$TIPO_DOC" --parent "$BIBLIOTECA_ID")
  DOC_BIBLIO_ID=$(echo "$NEW_DOC" | python3 -c "import json,sys; print(json.load(sys.stdin).get('documentId',''))")
fi

# Añadir lección al final del doc
ENTRY="--- $TODAY | $ISSUE_TITLE_MATTER ---
$INSIGHT

"
gws docs documents batchUpdate --document-id "$DOC_BIBLIO_ID" --requests "[
  {\"insertText\":{\"endOfSegmentLocation\":{\"segmentId\":\"\"},\"text\":$(echo "$ENTRY" | python3 -c "import json,sys; print(json.dumps(sys.stdin.read()))")}}
]"

# Evaluar si amerita cambio de template
IMPLICA_CAMBIO=false
echo "$INSIGHT" | grep -qi "incluir por default\|cambiar default\|siempre en" && IMPLICA_CAMBIO=true

COMMENT="✅ Lección registrada en Biblioteca/$TIPO_DOC."

if [ "$IMPLICA_CAMBIO" = "true" ]; then
  # Crear aprobación para actualizar plantilla
  curl -s -X POST "$PAPERCLIP_API_URL/api/companies/$PAPERCLIP_COMPANY_ID/approvals" \
    -H "Authorization: Bearer $PAPERCLIP_API_KEY" \
    -H "Content-Type: application/json" \
    -d "{
      \"type\": \"aprobar_actualizacion_plantilla\",
      \"issueIds\": [\"$ISSUE_ID\"],
      \"payload\": {
        \"accion\": \"aprobar_actualizacion_plantilla\",
        \"tipo_documento\": \"$TIPO_DOC\",
        \"matter_origen\": \"$ISSUE_TITLE_MATTER\",
        \"cambio_propuesto\": \"$(echo "$INSIGHT" | head -1)\",
        \"razon\": \"$(echo "$INSIGHT" | python3 -c "import sys; print(sys.stdin.read()[:200])")\",
        \"summary\": \"Propuesta de actualización a plantilla $TIPO_DOC. Afectará todos los matters futuros.\",
        \"proximo_paso\": \"Con tu aprobación, actualizo el Google Doc en Plantillas/.\"
      }
    }"
  COMMENT="$COMMENT Solicité aprobación para actualizar la plantilla."
fi

curl -s -X POST "$PAPERCLIP_API_URL/api/issues/$ISSUE_ID/comments" \
  -H "Authorization: Bearer $PAPERCLIP_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{\"body\":\"$COMMENT\"}"
```

---

## Sección 5: Manejo de approval

Cuando `PAPERCLIP_APPROVAL_ID` está presente al inicio del run:

```bash
APPROVAL=$(curl -s "$PAPERCLIP_API_URL/api/approvals/$PAPERCLIP_APPROVAL_ID" \
  -H "Authorization: Bearer $PAPERCLIP_API_KEY")
APPROVAL_TYPE=$(echo "$APPROVAL" | python3 -c "import json,sys; print(json.load(sys.stdin).get('type',''))")
PAYLOAD=$(echo "$APPROVAL" | python3 -c "import json,sys; print(json.dumps(json.load(sys.stdin).get('payload',{})))")

if [ "$PAPERCLIP_APPROVAL_STATUS" = "approved" ] && [ "$APPROVAL_TYPE" = "aprobar_actualizacion_plantilla" ]; then
  TIPO=$(echo "$PAYLOAD" | python3 -c "import json,sys; d=json.loads(sys.stdin.read()); print(d.get('tipo_documento',''))")
  CAMBIO=$(echo "$PAYLOAD" | python3 -c "import json,sys; d=json.loads(sys.stdin.read()); print(d.get('cambio_propuesto',''))")
  ISSUE_ID=$(echo "$APPROVAL" | python3 -c "
import json,sys
data=json.load(sys.stdin)
ids=data.get('issueIds',[]) or data.get('issue_ids',[])
print(ids[0] if ids else '')
")

  # Encontrar el doc de plantilla correspondiente
  declare -A TEMPLATES
  TEMPLATES[prestacion_servicios]="1re94n-yQaHIX94KxhdxUhV4DuivdbkPOTsmVASdcs-M"
  TEMPLATES[terminos_condiciones]="1k3Byeo_8_p7FPmn9xsW8KUO9L1Rk_Tt0-g_z29Ap4IE"
  TEMPLATES[convenio_pagos]="1fotzwSH6zTr3J_DTwkuvWiWBZdbBBgLz0AdhrY607eM"
  TEMPLATES[bitacora_entregas]="1-O09U6sqmNstAHEW-dOyZQyxC-qdtMmC3QFlgPbWBjY"
  TEMPLATES[garantias]="1O7VHoVBDdN_L0-wVxcTLmtkI7AVRsg7xwFW1NJZ3t1M"
  TEMPLATES[calendario_cobranza]="1tjrkPiR9ENZIzsUMtHCoJ7mAmrasA8KMrPjIOzFj7AU"
  TEMPLATES[carta_cobranza]="1oxVbm2rLZYW7VAUVpX1Giye8dCU3D4XW0Z4BS51BeDY"
  TEMPLATES[arrendamiento]="1HupFPPZKkr_obOVIqKbE3Qf3IaWkXUFJYnKaTQNIx0s"
  TEMPLATES[pagare]="1n_rUwgsqqYABcgwtnAxOp03dg2lXcBQ_r-OtQ96TCYY"
  TEMPLATES[aviso_privacidad]="1JiYgvOLrnZ2GcmiaPGFho9Xlo9aZvsvm8sa5bfWSsDU"
  TEMPLATES[formato_arco]="1CWaZietfxZjqxhwe6ltjTYqHs2r_KGuyv7ZJ8znBf8A"
  TEMPLATES[nda]="1xCpF1tgskE7u00mbcHpcPNHlY0ANfIzDkhWCliPP1MQ"
  TEMPLATES[confidencialidad]="1ZSaB3mLRqrkenqmLvQAIAzFtVAYQPFw8R6OAWIYUXEY"
  TEMPLATES[expediente_materialidad]="1027fDw2RT1RFXaiQtI7sv2qcto-fZJu5lccl311mc2E"
  TEMPLATES[carta_sat]="1yD8CqMUdPlHG421UZWuDCMLRPS0Zswhj1LscPTeDmNo"
  TEMPLATES[contrato_trabajo]="15j0utocqBNshCi-SBBrDBU0fpp5B3YUrMYrUPK3Vyg4"
  TEMPLATES[reglamento_interior]="1iP1fVTpHZ2yqo4SsgkYAG7e1wFgt-hz80Sr6I8VLvp8"
  TEMPLATES[finiquito]="1wte10EIWJpd044CEN5BWlNeVVKt1iIHY_7NkURvSeFA"
  TEMPLATES[nda_laboral]="1dcOw1C7_e0cNM6ZTrs7-LiISwrUY4kJOG7cNtjn9KnA"
  TEMPLATES[acta_asamblea]="1fM6kS2AGA0x-idszK3UGuiO94ygRkDMVjLJt1qs6lQQ"
  TEMPLATES[poder_notarial]="1Zy5cUyf5fi1qTUHIoU1LFkiXxqPVpgFVIdzAu0lLaa8"
  TEMPLATES[estatutos_sociales]="1sALBUN2HXFDsPDldm5W20ytqT8gtNTBmxdxlx_oH_-M"
  TEMPLATES[convenio_accionistas]="1ZpCz4J7rZHBZBVDcFtQ8s-jpd7VA4GxMAw6wDZqrlsk"
  TEMPLATE_ID="${TEMPLATES[$TIPO]}"

  if [ -n "$TEMPLATE_ID" ]; then
    # Añadir nota de actualización al inicio del doc de plantilla
    gws docs documents batchUpdate --document-id "$TEMPLATE_ID" --requests "[
      {\"insertText\":{\"location\":{\"index\":1},\"text\":\"[ACTUALIZADO $(date +%Y-%m-%d)]: $CAMBIO\n\n\"}}
    ]"
    curl -s -X POST "$PAPERCLIP_API_URL/api/issues/$ISSUE_ID/comments" \
      -H "Authorization: Bearer $PAPERCLIP_API_KEY" \
      -H "Content-Type: application/json" \
      -d "{\"body\":\"✅ Plantilla $TIPO actualizada. El cambio se aplica a todos los matters futuros.\"}"
  fi

elif [ "$PAPERCLIP_APPROVAL_STATUS" = "rejected" ] && [ "$APPROVAL_TYPE" = "aprobar_actualizacion_plantilla" ]; then
  TIPO=$(echo "$PAYLOAD" | python3 -c "import json,sys; d=json.loads(sys.stdin.read()); print(d.get('tipo_documento',''))")
  ISSUE_ID=$(echo "$APPROVAL" | python3 -c "
import json,sys
data=json.load(sys.stdin)
ids=data.get('issueIds',[]) or data.get('issue_ids',[])
print(ids[0] if ids else '')
")
  curl -s -X POST "$PAPERCLIP_API_URL/api/issues/$ISSUE_ID/comments" \
    -H "Authorization: Bearer $PAPERCLIP_API_KEY" \
    -H "Content-Type: application/json" \
    -d "{\"body\":\"Actualización de plantilla $TIPO cancelada. La lección sigue registrada en Biblioteca pero el template no cambia.\"}"
fi
```

## Fuente de verdad de triggers (Fase 1 Willow Alt UI)

Los formatos exactos de los 13 triggers del sistema viven en un único archivo:

- Ruta: `company/workspace/triggers/willow-triggers.json`
- Versión del esquema: `schemaVersion: "1"`

Antes de responder a un trigger, debo leer este archivo para confirmar el formato vigente. Si el archivo no existe o su `schemaVersion` no es "1", reporto el problema en el hilo y no asumo un formato.

Este archivo es consumido también por la UI alternativa (botón `+` de plantillas rápidas). Cualquier cambio exige subir `schemaVersion` y notificar a los tres agentes (despacho, intake, admin).
