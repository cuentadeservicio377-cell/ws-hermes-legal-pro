# PROMPT DE CIERRE v8.1 — CORREGIR CALENDARIO + VERIFICACIÓN COMPLETA
# Este prompt debe ejecutarse al final de la sesión para dejar todo listo

## CONTEXTO ACTUAL DEL REPO (Commit 47c70aa)

### Backend (FastAPI): dashboard/backend/app.py — 1021 líneas, 37996 bytes
- SÍ tiene todos los endpoints v8:
  - GET /api/drive-link/{matter_id}
  - POST /api/export-sheets
  - POST /api/export-docs
  - POST /api/sync-excel
  - GET /api/tasks
  - POST /api/task
  - GET /api/calendar-events
  - POST /api/check-plazos
- Usa funciones genéricas: load_json(), save_json()
- Tiene CORS habilitado
- Sirve archivos estáticos

### Frontend:
- index.html: 158 líneas, 6751 bytes — 6 secciones funcionan
- css/styles.css: 625 líneas, 11639 bytes — todos los estilos v8 presentes
- js/app.js: 806 líneas, 24512 bytes — 42 funciones, incluye renderCalendarView()
- js/api.js: 75 líneas, 2703 bytes — 22 métodos API, rutas correctas
- js/finanzas.js: 121 líneas, 4404 bytes — FinanzasAPI + FinanzasUI

### Scripts Google Workspace (8/8 presentes):
- scripts/drive_manager.py (6818 bytes)
- scripts/calendar_manager.py (2328 bytes)
- scripts/tasks_manager.py (1910 bytes)
- scripts/sheets_manager.py (3731 bytes)
- scripts/docs_exporter.py (2373 bytes)
- scripts/sync_excel_json.py (10290 bytes)
- scripts/check_plazos.py (9476 bytes)
- scripts/hermes_bridge.py (5579 bytes)

### Manuales (3/3 presentes):
- docs/MANUAL_ABOGADO_COMPLETO.md (7020 bytes)
- docs/MANUAL_HERMES_INTEGRATION.md (3443 bytes)
- docs/MANUAL_TECNICO.md (7964 bytes)

### Agentes (3/3 presentes):
- agents/despacho.md (7639 bytes)
- agents/intake.md (3682 bytes)
- agents/admin.md (17105 bytes)

## PROBLEMA A CORREGIR

Falta `<div id="plazos-calendar"></div>` en la sección de plazos de index.html.

La función `renderCalendarView()` en app.js intenta renderizar en `document.getElementById('plazos-calendar')` pero ese elemento NO EXISTE en el HTML.

## TAREAS

### Tarea 1: Corregir HTML

Abrir `dashboard/frontend/index.html` y modificar la sección de plazos.

Buscar:
```html
        <!-- Sección Plazos -->
        <section id="plazos" class="section hidden">
            <h2>Plazos y Vencimientos</h2>
            <div id="plazos-list"></div>
        </section>
```

Reemplazar con:
```html
        <!-- Sección Plazos -->
        <section id="plazos" class="section hidden">
            <h2>Plazos y Vencimientos</h2>
            <div id="plazos-calendar"></div>
            <div id="plazos-list"></div>
        </section>
```

### Tarea 2: Verificar que renderCalendarView() funciona

La función `renderCalendarView()` en app.js debe:
1. Encontrar el elemento `plazos-calendar`
2. Generar un grid de calendario mensual
3. Mostrar días con eventos resaltados
4. Permitir navegación entre meses

Si la función no existe o está incompleta, completarla con:

```javascript
function renderCalendarView() {
  const container = document.getElementById('plazos-calendar')
  if (!container) return
  
  const now = new Date()
  const year = now.getFullYear()
  const month = now.getMonth()
  
  container.innerHTML = `
    <div class="calendar-header">
      <button onclick="changeMonth(-1)" class="btn-icon">←</button>
      <h3>${getMonthName(month)} ${year}</h3>
      <button onclick="changeMonth(1)" class="btn-icon">→</button>
    </div>
    <div class="calendar-grid" id="calendar-grid"></div>
  `
  
  generateCalendarGrid(year, month)
}
```

### Tarea 3: Verificar funciones helper de calendario

Asegurar que existen:
- `generateCalendarGrid(year, month)` — genera los días del mes
- `getMonthName(month)` — retorna nombre del mes en español
- `changeMonth(delta)` — navega entre meses

Si faltan, agregarlas al final de app.js.

### Tarea 4: Verificar que `openPlazoModal()` carga matters en el select

La función debe hacer:
```javascript
// Cargar matters en el select
API.getMatters().then(data => {
  const matters = data.matters || []
  const select = document.getElementById('plazo-matter')
  if (select) {
    select.innerHTML = '<option value="">Ninguno</option>' +
      matters.map(m => `<option value="${m.id}">${m.id} - ${m.nombre}</option>`).join('')
  }
})
```

### Tarea 5: Verificar que `getTasks()` se usa en algún lado

Si `getTasks()` no se usa en app.js, agregar una sección "Tareas" o integrarla en el dashboard.

Opción simple: Agregar en `updateDashboard()`:
```javascript
// Contador de tareas
API.getTasks().then(data => {
  const tasks = data.tasks || []
  const pendingTasks = tasks.filter(t => t.status !== 'completed')
  // Mostrar en sidebar si hay tareas pendientes
}).catch(() => {}) // Silenciar error si Tasks no está configurado
```

### Tarea 6: Tests finales

Ejecutar y reportar:

```bash
cd ~/ws-hermes-legal-pro

# 1. Verificar HTML tiene plazos-calendar
grep -c "plazos-calendar" dashboard/frontend/index.html
# Debe retornar 1

# 2. Verificar app.js tiene renderCalendarView
grep -c "renderCalendarView" dashboard/frontend/js/app.js
# Debe retornar 1+

# 3. Verificar app.js tiene generateCalendarGrid
grep -c "generateCalendarGrid" dashboard/frontend/js/app.js
# Debe retornar 1+

# 4. Verificar app.js tiene getMonthName
grep -c "getMonthName" dashboard/frontend/js/app.js
# Debe retornar 1+

# 5. Verificar backend tiene todos los endpoints v8
grep -c "drive-link" dashboard/backend/app.py
# Debe retornar 1+
grep -c "export-sheets" dashboard/backend/app.py
# Debe retornar 1+
grep -c "calendar-events" dashboard/backend/app.py
# Debe retornar 1+
grep -c "check-plazos" dashboard/backend/app.py
# Debe retornar 1+

# 6. Contar archivos clave
ls -la dashboard/frontend/js/*.js | wc -l
# Debe retornar 3 (api.js, app.js, finanzas.js)

ls -la scripts/*.py | wc -l
# Debe retornar 8+ scripts

ls -la docs/MANUAL_*.md | wc -l
# Debe retornar 3

ls -la agents/*.md | wc -l
# Debe retornar 3

# 7. Git status
git status --short
```

### Tarea 7: Git commit final

```bash
cd ~/ws-hermes-legal-pro
git add -A
git commit -m "v8.1: Fix calendario plazos + verificación completa sistema"
git push origin master
git log --oneline -5
```

## CHECKLIST DE CIERRE

Verificar que todo esté presente:

- [ ] Backend: 8 endpoints v8 funcionan
- [ ] Frontend: 42 funciones en app.js
- [ ] HTML: 7 secciones + plazos-calendar
- [ ] CSS: todos los estilos v8
- [ ] api.js: 22 métodos API
- [ ] Scripts: 8 scripts Google Workspace
- [ ] Manuales: 3 manuales de usuario
- [ ] Agentes: 3 agentes (despacho, intake, admin)
- [ ] Motor Kami: genera PDFs
- [ ] Drive: sube archivos
- [ ] Calendar: crea eventos
- [ ] Tests: todos pasan

## REPORTAR

Pegar output de:
1. `git log --oneline -5`
2. Resultados de todos los grep/tests
3. Confirmación: "Sistema listo para uso" o lista de problemas pendientes
