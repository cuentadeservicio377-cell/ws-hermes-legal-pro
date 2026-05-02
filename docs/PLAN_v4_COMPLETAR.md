# PLAN v4: Completar Hermes Legal Pro
# Objetivo: Sustituir completamente al equipo de apoyo legal de una firma boutique
#
# Estado: OpenCode Go completó v3 DUAL pero faltan piezas críticas
# Fecha: 2026-05-01
# Repo: cuentadeservicio377-cell/ws-hermes-legal-pro

---

## 🎯 VISIÓN FINAL

Un abogado en una firma boutique debe poder:

1. **Recibir un cliente nuevo** → Hermes crea matter, carpeta, ficha
2. **Generar cualquier documento** → Motor Kami produce PDF profesional
3. **Trackear plazos y deadlines** → Calendario + alertas automáticas
4. **Editar/eliminar matters** → CRUD completo sin errores 405
5. **Ver estado financiero** → Honorarios, anticipos, facturas
6. **Aprobar documentos** → Flujo de aprobaciones con trazabilidad
7. **Sincronizar con Excel** → Datos compartidos entre sistema y Excel maestro
8. **Operar desde cualquier lado** → Telegram o Dashboard, mismos datos

---

## 📋 FASES PENDIENTES

### FASE A: Fix Backend CRUD (20 min) — CRÍTICO

**Problema:** Frontend tiene botones edit/delete pero backend devuelve 405

**Tareas:**
1. Agregar endpoint PUT `/api/matters/{id}` en dashboard/backend/app.py
2. Agregar endpoint DELETE `/api/matters/{id}` en dashboard/backend/app.py
3. Verificar que frontend puede editar y eliminar matters

**Verificación:**
```bash
curl -X PUT http://localhost:8082/api/matters/WIL-001 -H "Content-Type: application/json" -d '{"nombre":"Nuevo nombre"}'
curl -X DELETE http://localhost:8082/api/matters/WIL-001
```

---

### FASE B: Sincronización Excel ↔ JSON (30 min)

**Problema:** Excel maestro y datos/matters.json están desconectados

**Tareas:**
1. Crear script `scripts/sync_excel_json.py`
2. Leer Excel `excel/Centro_Operativo_Maestro_Willow_v4.xlsx` (hoja "Matters")
3. Sincronizar bidireccional: Excel ↔ datos/matters.json
4. Ejecutar sync automático al crear/editar matter

**Verificación:**
```bash
python3 scripts/sync_excel_json.py --direction excel-to-json
python3 scripts/sync_excel_json.py --direction json-to-excel
```

---

### FASE C: Notificaciones de Plazos (20 min)

**Problema:** No hay alertas cuando se acerca un deadline

**Tareas:**
1. Crear script `scripts/check_plazos.py`
2. Leer alertas.json y comparar fechas con hoy
3. Generar alertas para plazos en 3 días, 1 día, vencidos
4. Integrar con Hermes: enviar mensaje Telegram cuando hay alerta

**Verificación:**
```bash
python3 scripts/check_plazos.py --test
# Debe mostrar alertas de prueba
```

---

### FASE D: Flujo de Aprobaciones (30 min)

**Problema:** Documentos se generan pero no hay flujo de aprobación

**Tareas:**
1. Agregar campo "estado" a documentos: borrador → revisión → aprobado → firmado
2. Crear endpoint `/api/documentos/{id}/aprobar`
3. Agregar trazabilidad: quién aprobó, cuándo, comentarios
4. Integrar en frontend: botones Aprobar, Rechazar, Comentar

**Verificación:**
```bash
curl -X POST http://localhost:8082/api/documentos/DOC-001/aprobar -d '{"aprobado_por":"Pablo","comentario":"OK"}'
```

---

### FASE E: Módulo Financiero (30 min)

**Problema:** No hay tracking de honorarios, anticipos, facturas

**Tareas:**
1. Crear `datos/finanzas.json` con estructura:
   - matter_id, concepto, monto, tipo (anticipo/honorario/factura), estado
2. Agregar endpoints:
   - POST `/api/finanzas` — registrar movimiento
   - GET `/api/finanzas/{matter_id}` — ver movimientos
   - GET `/api/finanzas/resumen` — KPIs financieros
3. Integrar en Dashboard: tab "Finanzas"
4. Comandos Hermes:
   - `/anticipo WIL-001 25000 "Pago inicial"`
   - `/factura WIL-001 50000 "Honorarios mes 1"`

**Verificación:**
```bash
python3 scripts/hermes_bridge.py anticipo WIL-001 25000 "Pago inicial"
python3 scripts/hermes_bridge.py finanzas WIL-001
```

---

### FASE F: Integración Google Drive (Opcional, 40 min)

**Problema:** Carpetas solo locales, no sincronizan con Drive del despacho

**Tareas:**
1. Usar `gws` (Google Workspace CLI) si está disponible
2. Crear script `scripts/sync_drive.py`
3. Sincronizar `~/WillowLegal/01_Clientes/` con carpeta Drive
4. Configurar en `config/.env`: DRIVE_FOLDER_ID

**Verificación:**
```bash
python3 scripts/sync_drive.py --dry-run
```

---

## 🚀 ORDEN DE EJECUCIÓN

OpenCode Go debe ejecutar en este orden:

```
FASE A (20 min) → Fix PUT/DELETE
    ↓
FASE B (30 min) → Sync Excel
    ↓
FASE C (20 min) → Notificaciones plazos
    ↓
FASE D (30 min) → Aprobaciones
    ↓
FASE E (30 min) → Finanzas
    ↓
FASE F (40 min) → Drive sync (opcional)
    ↓
TEST END-TO-END (20 min)
    ↓
COMMIT + PUSH
```

**Tiempo total estimado:** 2.5 - 3 horas

---

## ✅ CRITERIO DE ÉXITO FINAL

Un abogado debe poder hacer ESTO sin ayuda humana:

```
1. Recibe llamada de cliente nuevo
2. Abre Telegram: /matter nuevo "Cliente S.A." area=Corporativo
3. Hermes crea matter, carpeta, ficha
4. Abre Dashboard: ve matter creado, click "Generar contrato"
5. Selecciona template, llena datos, genera PDF
6. PDF aparece en carpeta y en Dashboard
7. Cliente pide cambios: edita matter, regenera documento
8. Documento listo: click "Aprobar", trazabilidad guardada
9. Cliente paga anticipo: /anticipo WIL-001 25000
10. Sistema trackea pago, actualiza Excel maestro
11. Plazo judicial se acerca: alerta automática en Telegram
12. Reporte semanal: /status muestra todo
```

**Si todo esto funciona → Hermes Legal sustituye al equipo de apoyo.**

---

## 📁 ARCHIVOS A CREAR/MODIFICAR

### Nuevos archivos:
- `scripts/sync_excel_json.py`
- `scripts/check_plazos.py`
- `scripts/sync_drive.py` (opcional)
- `datos/finanzas.json`
- `hermes_integration/finanzas.py`

### Archivos a modificar:
- `dashboard/backend/app.py` — PUT/DELETE matters, finanzas, aprobaciones
- `dashboard/frontend/js/matters.js` — Integrar edit/delete
- `scripts/hermes_bridge.py` — Comandos anticipo, factura, finanzas
- `hermes_integration/commands.py` — Métodos financieros

---

## 🎉 RESULTADO ESPERADO

Al finalizar, el producto tendrá:

✅ Modo Hermes (Telegram) completo
✅ Modo Dashboard (Mac) completo  
✅ CRUD Matters sin errores
✅ Sincronización Excel
✅ Alertas de plazos
✅ Flujo de aprobaciones
✅ Tracking financiero
✅ (Opcional) Sync con Drive

**Hermes Legal Pro v4 — Sistema operativo legal completo.**

---

**Creado por:** Hermes Neo
**Fecha:** 2026-05-01
**Estado:** Listo para ejecutar
