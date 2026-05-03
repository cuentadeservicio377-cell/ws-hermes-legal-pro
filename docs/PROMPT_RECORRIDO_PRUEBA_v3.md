# PROMPT EJECUTABLE — RECORRIDO DE PRUEBA COMPLETO HERMES LEGAL PRO v3

> **Objetivo:** Ejecutar un recorrido end-to-end del sistema Hermes Legal Pro v3, probar cada componente, tomar screenshots, y generar un reporte documentado.
> **Autor:** Hermes Neo
> **Fecha:** 2026-05-02
> **Repo:** cuentadeservicio377-cell/ws-hermes-legal-pro
> **Commit base:** b7d6902 (master)

---

## INSTRUCCIONES GENERALES

1. **NO omitir ninguna fase.** Cada fase tiene checkpoints de verificación.
2. **Tomar screenshot** de cada vista/pantalla significativa.
3. **Si algo falla, documentar el error exacto** (mensaje, stack trace, estado).
4. **Guardar el reporte final** en `docs/REPORTE_PRUEBA_v3.md`.
5. **Usar el perfil `legal-pro`** de Hermes si está disponible.

---

## FASE 0: PREPARACIÓN DEL ENTORNO

### Paso 0.1: Verificar repo actualizado
```bash
cd ~/ws-hermes-legal-pro
git pull origin master
git log --oneline -3
```

**Checkpoint:** Debe mostrar commit `b7d6902` o más reciente.

### Paso 0.2: Verificar estructura de archivos
```bash
cd ~/ws-hermes-legal-pro
ls -la
ls dashboard/backend/
ls motor_kami/
ls hermes_integration/
ls scripts/
```

**Checkpoint:** Deben existir:
- `dashboard/backend/app.py`
- `motor_kami/motor_kami.py`
- `motor_kami/blocks.py`
- `hermes_integration/commands.py`
- `scripts/drive_manager.py`

### Paso 0.3: Verificar dependencias
```bash
python3 -c "import fastapi; print('FastAPI OK')"
python3 -c "import weasyprint; print('WeasyPrint OK')"
python3 -c "import google.auth; print('Google Auth OK')"
```

**Checkpoint:** Todas las importaciones deben funcionar sin error.

### Paso 0.4: Iniciar backend
```bash
cd ~/ws-hermes-legal-pro/dashboard/backend
python3 app.py &
# O si usa uvicorn:
# uvicorn app:app --host 0.0.0.0 --port 8082 --reload
```

**Checkpoint:** `curl http://localhost:8082/api/health` debe retornar JSON con status.

**Screenshot 0:** Terminal mostrando backend iniciado y health check OK.

---

## FASE 1: PRUEBA DEL BACKEND API (Sin frontend)

### Paso 1.1: Health check completo
```bash
curl -s http://localhost:8082/api/health | python3 -m json.tool
```

**Verificar:**
- `status` = "ok"
- `motor_kami` = "ok"
- `templates_count` >= 23

**Screenshot 1:** Terminal con health check mostrando todo OK.

### Paso 1.2: Crear matter de prueba
```bash
curl -s -X POST http://localhost:8082/api/matters \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Cliente Prueba End-to-End",
    "cliente": "Empresa Prueba SA de CV",
    "area": "Corporativo",
    "materia": "corporativo",
    "prioridad": "alta",
    "descripcion": "Matter de prueba para recorrido completo del sistema",
    "deadline": "2026-12-31"
  }' | python3 -m json.tool
```

**Verificar:**
- Response tiene `id` (formato WIL-XXX)
- Response tiene `carpeta` (path válido)
- Status 200

**Guardar:** `MATTER_ID` del response para usar en pasos siguientes.

**Screenshot 2:** Terminal con matter creado y ID guardado.

### Paso 1.3: Listar matters
```bash
curl -s http://localhost:8082/api/matters | python3 -m json.tool | head -50
```

**Verificar:**
- El matter creado aparece en la lista
- Campos completos: id, nombre, cliente, area, estado, prioridad

**Screenshot 3:** Terminal listando matters con el nuevo matter visible.

### Paso 1.4: Obtener detalle del matter
```bash
curl -s http://localhost:8082/api/matters/{MATTER_ID} | python3 -m json.tool
```

**Verificar:**
- Todos los campos del matter están completos
- `carpeta` existe como path

**Screenshot 4:** Terminal con detalle completo del matter.

### Paso 1.5: Actualizar matter
```bash
curl -s -X PUT http://localhost:8082/api/matters/{MATTER_ID} \
  -H "Content-Type: application/json" \
  -d '{
    "estado": "Activo",
    "next_step": "Generar contrato de prestación de servicios"
  }' | python3 -m json.tool
```

**Verificar:**
- Estado cambiado a "Activo"
- Next step actualizado

**Screenshot 5:** Terminal mostrando matter actualizado.

### Paso 1.6: Crear reunión
```bash
curl -s -X POST http://localhost:8082/api/reuniones \
  -H "Content-Type: application/json" \
  -d '{
    "matter_id": "{MATTER_ID}",
    "cliente": "Empresa Prueba SA de CV",
    "fecha": "2026-05-02",
    "meet_url": "https://meet.google.com/test-abc",
    "resumen": "Reunión inicial para definir alcance del proyecto",
    "acuerdos": ["Definir alcance", "Enviar propuesta"],
    "documentos_necesarios": ["Contrato prestación servicios", "NDA"],
    "plazos": [{"descripcion": "Enviar propuesta", "fecha": "2026-05-10"}]
  }' | python3 -m json.tool
```

**Verificar:**
- Reunión creada con ID
- Matter_id correcto

**Guardar:** `REUNION_ID`

**Screenshot 6:** Terminal con reunión creada.

### Paso 1.7: Listar templates
```bash
curl -s http://localhost:8082/api/templates | python3 -m json.tool
```

**Verificar:**
- Lista de 23 templates
- Cada template tiene: key, label, area, materia

**Screenshot 7:** Terminal listando templates (mostrar conteo al final).

### Paso 1.8: Obtener template específico
```bash
curl -s http://localhost:8082/api/templates/prestacion_servicios | python3 -m json.tool
```

**Verificar:**
- Template existe
- Tiene `metadata`, `recommended_blocks`, `document_data_template`

**Screenshot 8:** Terminal mostrando estructura del template.

### Paso 1.9: Generar documento (PDF real)
```bash
curl -s -X POST http://localhost:8082/api/matter/{MATTER_ID}/generar-documento \
  -H "Content-Type: application/json" \
  -d '{
    "template_key": "prestacion_servicios",
    "datos_extra": {
      "prestador": {
        "nombre": "WS Capital Legal Services",
        "rfc": "WSC123456ABC",
        "domicilio": "Calle Principal 123, Ciudad de México"
      },
      "cliente": {
        "nombre": "Empresa Prueba SA de CV",
        "rfc": "EPS987654XYZ",
        "domicilio": "Av. Reforma 456, Ciudad de México"
      },
      "servicios": "Desarrollo de software legal y consultoría",
      "honorarios": "$50,000.00 MXN mensuales",
      "plazo": "12 meses"
    }
  }' | python3 -m json.tool
```

**Verificar:**
- Status 200
- Response tiene `success: true`
- Response tiene `file_path` (path a PDF)
- Response tiene `file_size_kb` > 0

**Guardar:** `PDF_PATH` del response.

**Screenshot 9:** Terminal mostrando documento generado exitosamente.

### Paso 1.10: Verificar PDF generado
```bash
ls -lh {PDF_PATH}
file {PDF_PATH}
```

**Verificar:**
- Archivo existe
- Tamaño > 10KB (PDF real)
- Tipo: PDF document

**Screenshot 10:** Terminal mostrando archivo PDF real.

### Paso 1.11: Validar sustancia del documento
```bash
curl -s -X POST http://localhost:8082/api/kami/validate \
  -H "Content-Type: application/json" \
  -d '{
    "blocks": [
      {"type": "parties_block", "data": {"prestador": {"nombre": "WS Capital"}, "cliente": {"nombre": "Empresa Prueba"}}},
      {"type": "clause_section", "data": {"numero": "1", "titulo": "Objeto", "subclausulas": [{"texto": "Prestación de servicios"}]}},
      {"type": "signature_block", "data": {"prestador": {}, "cliente": {}}}
    ]
  }' | python3 -m json.tool
```

**Verificar:**
- Response tiene `valido: true/false`
- Si `false`, tiene `errores` listando qué falta

**Screenshot 11:** Terminal mostrando validación de sustancia.

### Paso 1.12: Crear plazo
```bash
curl -s -X POST http://localhost:8082/api/plazo \
  -H "Content-Type: application/json" \
  -d '{
    "matter_id": "{MATTER_ID}",
    "titulo": "Entrega de propuesta",
    "descripcion": "Entregar propuesta de servicios al cliente",
    "fecha": "2026-05-10",
    "prioridad": "alta"
  }' | python3 -m json.tool
```

**Verificar:**
- Plazo creado
- Fecha correcta

**Screenshot 12:** Terminal con plazo creado.

### Paso 1.13: Listar plazos
```bash
curl -s http://localhost:8082/api/plazos | python3 -m json.tool
```

**Verificar:**
- Plazo aparece en lista

**Screenshot 13:** Terminal listando plazos.

### Paso 1.14: Verificar alertas
```bash
curl -s http://localhost:8082/api/alertas | python3 -m json.tool
```

**Verificar:**
- Sistema generó alertas automáticamente (matter nuevo, plazo creado)

**Screenshot 14:** Terminal mostrando alertas.

### Paso 1.15: Dashboard KPIs
```bash
curl -s http://localhost:8082/api/dashboard | python3 -m json.tool
```

**Verificar:**
- `matters_activos` >= 1
- `documentos_pendientes` >= 0
- `alertas_urgentes` >= 0
- `balance_mes` (número)

**Screenshot 15:** Terminal mostrando KPIs del dashboard.

---

## FASE 2: PRUEBA DEL FRONTEND (Dashboard SPA)

### Paso 2.1: Abrir dashboard en navegador
Abrir `http://localhost:8082` en navegador (Chrome/Safari).

**Verificar:**
- Página carga sin errores 404
- Sidebar visible con navegación
- Logo/brand visible

**Screenshot 16:** Dashboard cargado en navegador.

### Paso 2.2: Vista Dashboard (KPIs)
Navegar a Dashboard (vista default).

**Verificar:**
- Cards de KPIs visibles
- Matters activos muestra número correcto
- Alertas urgentes visibles
- Gráfico/actividad reciente

**Screenshot 17:** Vista Dashboard completa.

### Paso 2.3: Vista Matters
Click en "Matters" en sidebar.

**Verificar:**
- Tabla de matters visible
- Matter de prueba aparece en lista
- Botones: Ver, Editar, Eliminar, Abrir Drive
- Búsqueda funcional
- Filtros funcionales

**Screenshot 18:** Vista Matters con tabla completa.

### Paso 2.4: Crear matter desde frontend
Click en "Nuevo Matter", llenar formulario:
- Nombre: "Matter Frontend Test"
- Cliente: "Cliente Frontend"
- Área: "Laboral"
- Prioridad: "media"

Guardar.

**Verificar:**
- Matter aparece en tabla sin recargar
- Toast de éxito visible

**Screenshot 19:** Modal de creación + matter nuevo en tabla.

### Paso 2.5: Vista Documentos
Click en "Documentos" en sidebar.

**Verificar:**
- Lista de templates visible
- Template "prestacion_servicios" visible
- Botón "Generar" en cada template
- Documentos generados previamente listados

**Screenshot 20:** Vista Documentos con templates.

### Paso 2.6: Generar documento desde frontend
Click en "Generar" en template "prestacion_servicios".
Seleccionar matter de prueba.
Click "Generar Documento".

**Verificar:**
- Loading spinner visible
- Toast de éxito
- Documento aparece en lista de documentos generados
- Botón "Descargar PDF" funcional

**Screenshot 21:** Documento generado desde frontend.

### Paso 2.7: Descargar PDF
Click en "Descargar PDF" del documento generado.

**Verificar:**
- PDF se descarga
- PDF se abre correctamente
- Contenido legible
- Diseño Kami aplicado (tipografía, colores, estructura)

**Screenshot 22:** PDF abierto mostrando diseño Kami.

### Paso 2.8: Vista Calendario/Plazos
Click en "Calendario" en sidebar.

**Verificar:**
- Calendario mensual visible
- Plazo creado aparece en fecha correcta
- Eventos/dots visibles
- Navegación mes anterior/siguiente funcional

**Screenshot 23:** Vista Calendario con plazos.

### Paso 2.9: Vista Finanzas
Click en "Finanzas" en sidebar.

**Verificar:**
- Formulario para agregar ingreso/egreso
- Lista de transacciones
- Balance calculado correctamente
- Totales por matter

**Screenshot 24:** Vista Finanzas con datos.

### Paso 2.10: Agregar transacción
Llenar formulario:
- Matter: matter de prueba
- Tipo: Ingreso
- Concepto: "Honorarios"
- Monto: 50000
- Fecha: hoy

Guardar.

**Verificar:**
- Transacción aparece en lista
- Balance actualizado

**Screenshot 25:** Transacción agregada + balance actualizado.

### Paso 2.11: Vista Reuniones
Click en "Reuniones" en sidebar.

**Verificar:**
- Reunión creada en API aparece en lista
- Detalles visibles: cliente, fecha, resumen
- Botón "Ver detalle" funcional

**Screenshot 26:** Vista Reuniones.

### Paso 2.12: Vista Alertas
Click en "Alertas" en sidebar.

**Verificar:**
- Alertas del sistema visibles
- Badges de prioridad (urgente, advertencia, info)
- Botones de acción: Verificar plazos, Exportar Sheets, Sync Excel

**Screenshot 27:** Vista Alertas completa.

### Paso 2.13: Verificar plazos desde frontend
Click en "Verificar Plazos Ahora".

**Verificar:**
- Loading state
- Resultado de verificación
- Nuevas alertas si hay plazos vencidos

**Screenshot 28:** Resultado de verificación de plazos.

---

## FASE 3: PRUEBA DE HERMES AGENT (Telegram)

### Paso 3.1: Verificar perfil legal-pro
```bash
hermes config get profile
# O:
cat ~/.hermes/config.yaml | grep profile
```

**Verificar:**
- Profile activo es `legal-pro` o similar

**Screenshot 29:** Terminal mostrando perfil activo.

### Paso 3.2: Ejecutar comando /matter
En Telegram (o simulación):
```
/matter nuevo "Matter Telegram Test"
```

**Verificar:**
- Hermes responde con matter creado
- ID asignado (WIL-XXX)
- Carpeta creada

**Screenshot 30:** Conversación Telegram mostrando comando /matter y respuesta.

### Paso 3.3: Ejecutar comando /status
```
/status
```

**Verificar:**
- Resumen del despacho
- Matters activos
- Próximos plazos
- Alertas pendientes

**Screenshot 31:** Respuesta de /status en Telegram.

### Paso 3.4: Ejecutar comando /contrato
```
/contrato prestacion_servicios WIL-XXX
```

**Verificar:**
- Hermes genera documento
- Responde con confirmación
- Menciona ruta del PDF

**Screenshot 32:** Generación de contrato vía Telegram.

### Paso 3.5: Ejecutar comando /plazo
```
/plazo WIL-XXX "Revisión de documentos" 2026-05-15
```

**Verificar:**
- Plazo creado
- Confirmación en Telegram

**Screenshot 33:** Creación de plazo vía Telegram.

### Paso 3.6: Ejecutar comando /alerta
```
/alerta
```

**Verificar:**
- Lista de alertas
- Alertas del matter de prueba visibles

**Screenshot 34:** Alertas en Telegram.

---

## FASE 4: PRUEBA DE GOOGLE WORKSPACE

### Paso 4.1: Verificar autenticación Google
```bash
ls ~/.config/gcloud/application_default_credentials.json
# O:
python3 -c "from scripts.drive_manager import DriveManager; d = DriveManager(); print('Auth OK')"
```

**Verificar:**
- Token existe o auth funciona

**Screenshot 35:** Verificación de auth Google.

### Paso 4.2: Crear carpeta en Drive para matter
```bash
curl -s http://localhost:8082/api/matter/{MATTER_ID}/drive-folder | python3 -m json.tool
```

**Verificar:**
- Response tiene `folder_link`
- Link es URL válida de Google Drive

**Screenshot 36:** Carpeta creada en Drive.

### Paso 4.3: Abrir carpeta en navegador
Abrir link de Drive en navegador.

**Verificar:**
- Carpeta existe en Google Drive
- Nombre coincide con matter

**Screenshot 37:** Carpeta de matter en Google Drive.

### Paso 4.4: Exportar a Sheets
Desde frontend: Click en "Exportar a Sheets" en vista Alertas o Dashboard.

**Verificar:**
- Sheets creado
- Link funcional
- Datos exportados correctamente

**Screenshot 38:** Google Sheets con datos exportados.

---

## FASE 5: PRUEBA DEL MOTOR KAMI (Standalone)

### Paso 5.1: Generar PDF vía CLI directo
```bash
cd ~/ws-hermes-legal-pro/motor_kami

# Crear archivo de prueba
cat > /tmp/test_input.json << 'EOF'
{
  "blocks": [
    {
      "type": "header_brand",
      "data": {"marca": "WS Capital Legal", "numero_documento": "DOC-001"}
    },
    {
      "type": "parties_block",
      "data": {
        "prestador": {
          "nombre": "WS Capital Legal Services",
          "rfc": "WSC123456ABC",
          "domicilio": "Calle Principal 123, CDMX",
          "representante": "Lic. Pablo García",
          "email": "legal@wscapital.com"
        },
        "cliente": {
          "nombre": "Empresa Prueba SA de CV",
          "rfc": "EPS987654XYZ",
          "domicilio": "Av. Reforma 456, CDMX",
          "representante": "Ing. Juan Pérez",
          "email": "juan@prueba.com"
        }
      }
    },
    {
      "type": "clause_section",
      "data": {
        "numero": "1",
        "titulo": "OBJETO Y ALCANCE",
        "subclausulas": [
          {"numero": "1.1", "texto": "El PRESTADOR se obliga a prestar servicios de consultoría legal."},
          {"numero": "1.2", "texto": "El CLIENTE se obliga a proporcionar información necesaria."}
        ]
      }
    },
    {
      "type": "payment_table",
      "data": {
        "headers": ["Concepto", "Monto", "Fecha"],
        "rows": [
          ["Honorarios mensuales", "$50,000.00 MXN", "Primero de cada mes"],
          ["Pago inicial", "$25,000.00 MXN", "Al firma del contrato"]
        ]
      }
    },
    {
      "type": "signature_block",
      "data": {
        "prestador": {"nombre": "Lic. Pablo García", "puesto": "Director Legal"},
        "cliente": {"nombre": "Ing. Juan Pérez", "puesto": "Director General"},
        "testigo1": {"nombre": "Testigo A", "puesto": "Notario"},
        "testigo2": {"nombre": "Testigo B", "puesto": "Abogado"}
      }
    }
  ],
  "options": {
    "color_primary": "#1a1a18",
    "color_bg": "#faf8f0",
    "titulo": "Contrato de Prestación de Servicios"
  }
}
EOF

python3 motor_kami.py --input /tmp/test_input.json --output /tmp/test_contrato.pdf
```

**Verificar:**
- PDF generado sin errores
- Tamaño > 10KB

**Screenshot 39:** Terminal generando PDF vía CLI.

### Paso 5.2: Verificar diseño del PDF
```bash
ls -lh /tmp/test_contrato.pdf
file /tmp/test_contrato.pdf
```

Abrir `/tmp/test_contrato.pdf` en navegador/visor.

**Verificar:**
- Portada con marca WS Capital
- Bloque de partes con bordes
- Cláusulas numeradas
- Tabla de pagos con estilo
- Bloque de firmas con 2+2 grilla
- Numeración de páginas
- Tipografía serif (Playfair/Newsreader)
- Canvas pergamino (#faf8f0)

**Screenshot 40:** PDF mostrando diseño Kami completo.

### Paso 5.3: Validar sustancia vía CLI
```bash
python3 -c "
import sys
sys.path.insert(0, '.')
from blocks import validar_sustancia

data = {
  'blocks': [
    {'type': 'parties_block', 'data': {'prestador': {'nombre': 'A'}, 'cliente': {'nombre': 'B'}}},
    {'type': 'clause_section', 'data': {'numero': '1', 'titulo': 'Objeto', 'subclausulas': [{'texto': 'x'}]}},
    {'type': 'signature_block', 'data': {'prestador': {}, 'cliente': {}}}
  ]
}
result = validar_sustancia(data)
print(json.dumps(result, indent=2, ensure_ascii=False))
" 2>/dev/null || echo "blocks.py no importable directamente"
```

**Verificar:**
- Validador ejecuta
- Retorna estructura con `valido` y `elementos`

**Screenshot 41:** Validación de sustancia vía CLI.

---

## FASE 6: LIMPIEZA Y VERIFICACIÓN FINAL

### Paso 6.1: Eliminar matters de prueba
```bash
# Listar matters de prueba
curl -s http://localhost:8082/api/matters | python3 -c "import json,sys; d=json.load(sys.stdin); [print(f\"{m['id']}: {m['nombre']}\") for m in d if 'Prueba' in m.get('nombre','') or 'Test' in m.get('nombre','')]"

# Eliminar cada uno
curl -s -X DELETE http://localhost:8082/api/matters/{MATTER_ID_TEST}
```

**Verificar:**
- Matters de prueba eliminados
- Lista limpia

**Screenshot 42:** Terminal mostrando limpieza.

### Paso 6.2: Verificar estado final
```bash
curl -s http://localhost:8082/api/health | python3 -m json.tool
curl -s http://localhost:8082/api/dashboard | python3 -m json.tool
```

**Verificar:**
- Sistema sigue funcionando
- Dashboard muestra datos reales (no de prueba)

**Screenshot 43:** Estado final del sistema.

---

## FASE 7: GENERACIÓN DEL REPORTE

### Paso 7.1: Compilar resultados
Crear archivo `docs/REPORTE_PRUEBA_v3.md` con la siguiente estructura:

```markdown
# Reporte de Prueba End-to-End — Hermes Legal Pro v3

**Fecha:** {fecha_actual}
**Tester:** Hermes Agent (automatizado)
**Commit:** {commit_actual}
**Duración:** {tiempo_total}

## Resumen Ejecutivo

| Métrica | Valor |
|---------|-------|
| Fases completadas | X/7 |
| Pasos exitosos | X/42 |
| Pasos fallidos | X/42 |
| Screenshots tomados | X/43 |
| PDFs generados | X |
| Matters de prueba creados | X |
| Documentos generados | X |

## Estado por Fase

### Fase 0: Preparación
- [ ] Repo actualizado
- [ ] Estructura verificada
- [ ] Dependencias OK
- [ ] Backend iniciado

### Fase 1: Backend API
- [ ] Health check
- [ ] CRUD matters
- [ ] Reuniones
- [ ] Templates
- [ ] Generación PDF
- [ ] Validación sustancia
- [ ] Plazos
- [ ] Alertas
- [ ] Dashboard

### Fase 2: Frontend SPA
- [ ] Dashboard carga
- [ ] Matters CRUD
- [ ] Documentos generación
- [ ] Calendario
- [ ] Finanzas
- [ ] Reuniones
- [ ] Alertas

### Fase 3: Hermes Agent
- [ ] /matter
- [ ] /status
- [ ] /contrato
- [ ] /plazo
- [ ] /alerta

### Fase 4: Google Workspace
- [ ] Auth
- [ ] Drive folder
- [ ] Sheets export

### Fase 5: Motor Kami
- [ ] CLI generación
- [ ] Diseño PDF
- [ ] Validación

### Fase 6: Limpieza
- [ ] Matters eliminados
- [ ] Estado final OK

## Hallazgos

### ✅ Funcionando correctamente
(Listar todo lo que pasó la prueba)

### ⚠️ Advertencias
(Listar comportamientos inesperados pero no bloqueantes)

### ❌ Errores encontrados
(Listar fallos con mensaje exacto y contexto)

## Screenshots

(Insertar referencias a screenshots 0-43)

## Recomendaciones

1. ...
2. ...
3. ...
```

### Paso 7.2: Guardar y commitear reporte
```bash
cd ~/ws-hermes-legal-pro
git add docs/REPORTE_PRUEBA_v3.md
git commit -m "TEST: Reporte de prueba end-to-end v3 — {fecha}"
git push origin master
```

---

## CHECKLIST FINAL DEL RECORRIDO

- [ ] Todas las fases ejecutadas
- [ ] Todos los screenshots tomados
- [ ] Reporte generado y commiteado
- [ ] Matters de prueba limpiados
- [ ] Sistema funcionando en estado limpio

---

## NOTAS PARA EL EJECUTOR

1. **Si algo falla, NO detenerse.** Documentar el error y continuar con la siguiente fase.
2. **Los screenshots son obligatorios.** Si no se puede tomar screenshot, describir lo que se veía.
3. **Usar `python3 -m json.tool` para pretty-print JSON** en todos los curls.
4. **Guardar IDs en variables** para reutilizar entre pasos.
5. **Si el backend no responde en puerto 8082, verificar** si usa otro puerto (8000, 3000, etc.).

---

*Prompt generado por Hermes Neo para recorrido de prueba completo del sistema Hermes Legal Pro v3.*
