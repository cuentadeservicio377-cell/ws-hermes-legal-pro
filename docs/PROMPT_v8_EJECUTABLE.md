# PROMPT EJECUTABLE v8 — ARQUITECTURA COMPLETA
# Este archivo contiene TODAS las instrucciones para conectar el 100% del backend con el frontend
# NO omitir ninguna sección. NO simplificar. NO asumir que "ya está".

## CONTEXTO DEL SISTEMA (NO MODIFICAR)

Repo: cuentadeservicio377-cell/ws-hermes-legal-pro
Commit actual: 16814db v7

### Backend funcional que YA EXISTE:
- app.py: endpoints REST para matters, documentos, plazos, finanzas, aprobaciones, alertas
- motor_kami/motor_kami.py: genera PDFs con --input/--output
- scripts/drive_manager.py: Google Drive (crear carpetas, subir archivos)
- scripts/calendar_manager.py: Google Calendar (crear eventos)
- scripts/tasks_manager.py: Google Tasks
- scripts/sheets_manager.py: Google Sheets
- scripts/docs_exporter.py: Google Docs
- scripts/sync_excel_json.py: Sincronización Excel
- scripts/check_plazos.py: Verificación de plazos vencidos
- scripts/hermes_bridge.py: 15 comandos Telegram
- hermes_integration/commands.py: comandos de Hermes Agent
- agents/: despacho.md, intake.md, admin.md

### Frontend v7 que YA EXISTE pero está INCOMPLETO:
- index.html: sidebar, 7 secciones, modal, toast
- css/styles.css: responsive, modo oscuro
- js/app.js: navegación SPA, tablas básicas
- js/api.js: llamadas API básicas
- js/finanzas.js: módulo finanzas

### LO QUE FALTA CONECTAR:
1. Botón "Abrir en Drive" para cada matter
2. Botón "Exportar a Docs" en templates
3. Vista calendario para plazos
4. Botón "Calendario" en cada plazo
5. Botón "Verificar plazos ahora" en alertas
6. Botón "Exportar a Sheets" en alertas
7. Botón "Sync Excel" en alertas
8. Badge de alertas urgentes en sidebar
9. Búsqueda en tiempo real en matters
10. Filtros por área funcionales

---

## PASO 0: PREPARACIÓN

```bash
cd ~/ws-hermes-legal-pro
git pull origin master
```

---

## PASO 1: AGREGAR ENDPOINTS BACKEND (app.py)

Abrir `dashboard/backend/app.py` y AGREGAR al final (antes del `if __name__ == '__main__'`):

```python
# === GOOGLE WORKSPACE ENDPOINTS v8 ===

@app.route('/api/drive-link/<matter_id>', methods=['GET'])
def get_drive_link(matter_id):
    """Obtiene el link de Google Drive para un matter"""
    try:
        from scripts.drive_manager import DriveManager
        drive = DriveManager()
        
        matters = load_matters()
        matter = next((m for m in matters if m['id'] == matter_id), None)
        
        if not matter:
            return jsonify({'error': 'Matter no encontrado'}), 404
        
        drive_link = matter.get('drive_folder_link')
        
        if not drive_link:
            # Buscar o crear carpeta
            folder = drive.create_folder(f"{matter_id} - {matter['nombre']}")
            drive_link = folder.get('webViewLink')
            matter['drive_folder_id'] = folder.get('id')
            matter['drive_folder_link'] = drive_link
            save_matters(matters)
        
        return jsonify({
            'matter_id': matter_id,
            'drive_link': drive_link,
            'message': 'Link de Drive obtenido'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/export-sheets', methods=['POST'])
def export_to_sheets():
    """Exporta datos a Google Sheets"""
    try:
        from scripts.sheets_manager import SheetsManager
        sheets = SheetsManager()
        
        data = request.get_json()
        tipo = data.get('tipo', 'resumen')
        
        if tipo == 'resumen':
            matters = load_matters()
            finanzas = load_finanzas()
            
            result = sheets.create_sheet('Willow Legal - Resumen', [
                ['Métrica', 'Valor'],
                ['Casos activos', len(matters)],
                ['Balance', finanzas.get('balance', 0)],
                ['Ingresos', finanzas.get('ingresos', 0)],
                ['Egresos', finanzas.get('egresos', 0)]
            ])
            
            return jsonify({
                'sheets_link': result.get('spreadsheetUrl'),
                'message': 'Datos exportados a Sheets'
            })
        
        return jsonify({'error': 'Tipo no soportado'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/export-docs', methods=['POST'])
def export_to_docs():
    """Exporta documento a Google Docs"""
    try:
        from scripts.docs_exporter import DocsExporter
        docs = DocsExporter()
        
        data = request.get_json()
        template_id = data.get('template_id')
        
        templates = load_templates()
        template = next((t for t in templates if t['id'] == template_id), None)
        
        if not template:
            return jsonify({'error': 'Template no encontrado'}), 404
        
        result = docs.create_document(template['nombre'], template['contenido'])
        
        return jsonify({
            'docs_link': result.get('documentUrl'),
            'message': 'Documento exportado a Google Docs'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/sync-excel', methods=['POST'])
def sync_excel():
    """Sincroniza datos con Excel PM maestro"""
    try:
        from scripts.sync_excel_json import ExcelSync
        sync = ExcelSync()
        
        matters = load_matters()
        finanzas = load_finanzas()
        
        result = sync.sync_data({
            'matters': matters,
            'finanzas': finanzas,
            'fecha_sync': datetime.now().isoformat()
        })
        
        return jsonify({
            'message': 'Sincronización completa',
            'registros_actualizados': result.get('updated', 0),
            'excel_path': result.get('path')
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/tasks', methods=['GET'])
def list_tasks():
    """Lista tareas de Google Tasks"""
    try:
        from scripts.tasks_manager import TasksManager
        tasks_mgr = TasksManager()
        
        tasks = tasks_mgr.list_tasks()
        return jsonify({'tasks': tasks, 'count': len(tasks)})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/task', methods=['POST'])
def create_task():
    """Crea tarea en Google Tasks"""
    try:
        from scripts.tasks_manager import TasksManager
        tasks_mgr = TasksManager()
        
        data = request.get_json()
        
        task = tasks_mgr.create_task(
            title=data.get('titulo', 'Nueva tarea'),
            notes=data.get('notas', ''),
            due=data.get('fecha_vencimiento')
        )
        
        return jsonify({'task': task, 'message': 'Tarea creada'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/calendar-events', methods=['GET'])
def get_calendar_events():
    """Obtiene eventos del calendario"""
    try:
        from scripts.calendar_manager import CalendarManager
        cal = CalendarManager()
        
        now = datetime.now()
        events = cal.list_events(year=now.year, month=now.month)
        
        return jsonify({
            'events': events,
            'count': len(events),
            'month': now.month,
            'year': now.year
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/check-plazos', methods=['POST'])
def check_plazos_endpoint():
    """Ejecuta verificación de plazos vencidos"""
    try:
        from scripts.check_plazos import PlazoChecker
        checker = PlazoChecker()
        
        plazos = load_plazos()
        nuevas_alertas = checker.check_vencimientos(plazos)
        
        if nuevas_alertas:
            alertas = load_alertas()
            alertas.extend(nuevas_alertas)
            save_alertas(alertas)
        
        return jsonify({
            'message': 'Verificación completa',
            'nuevas_alertas': len(nuevas_alertas),
            'alertas': nuevas_alertas
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500
```

---

## PASO 2: ACTUALIZAR api.js

Reemplazar COMPLETAMENTE `dashboard/frontend/js/api.js`:

```javascript
const API = {
  baseUrl: '/api',
  
  async get(endpoint) {
    const res = await fetch(`${this.baseUrl}${endpoint}`);
    if (!res.ok) throw new Error(`Error ${res.status}: ${res.statusText}`);
    return res.json();
  },
  
  async post(endpoint, data) {
    const res = await fetch(`${this.baseUrl}${endpoint}`, {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify(data)
    });
    if (!res.ok) throw new Error(`Error ${res.status}: ${res.statusText}`);
    return res.json();
  },
  
  async put(endpoint, data) {
    const res = await fetch(`${this.baseUrl}${endpoint}`, {
      method: 'PUT',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify(data)
    });
    if (!res.ok) throw new Error(`Error ${res.status}: ${res.statusText}`);
    return res.json();
  },
  
  async delete(endpoint) {
    const res = await fetch(`${this.baseUrl}${endpoint}`, {method: 'DELETE'});
    if (!res.ok) throw new Error(`Error ${res.status}: ${res.statusText}`);
    return res.json();
  },
  
  // Matters
  getMatters() { return this.get('/matters'); },
  createMatter(data) { return this.post('/matter', data); },
  updateMatter(id, data) { return this.put(`/matter/${id}`, data); },
  deleteMatter(id) { return this.delete(`/matter/${id}`); },
  
  // Documentos
  getTemplates() { return this.get('/templates'); },
  generateDocument(templateId, matterId) { 
    return this.post('/documento', {template_id: templateId, matter_id: matterId}); 
  },
  
  // Plazos
  getPlazos() { return this.get('/plazos'); },
  createPlazo(data) { return this.post('/plazo', data); },
  
  // Finanzas
  getFinanzas() { return this.get('/finanzas'); },
  createFinanza(data) { return this.post('/finanza', data); },
  
  // Alertas
  getAlertas() { return this.get('/alertas'); },
  
  // Aprobaciones
  getAprobaciones() { return this.get('/aprobaciones'); },
  approveDocument(id) { return this.post(`/aprobacion/${id}/aprobar`); },
  
  // NUEVO v8 — Google Workspace
  getDriveLink(matterId) { return this.get(`/drive-link/${matterId}`); },
  exportToSheets(data) { return this.post('/export-sheets', data); },
  exportToDocs(data) { return this.post('/export-docs', data); },
  syncExcel() { return this.post('/sync-excel'); },
  getTasks() { return this.get('/tasks'); },
  createTask(data) { return this.post('/task', data); },
  getCalendarEvents() { return this.get('/calendar-events'); },
  checkPlazos() { return this.post('/check-plazos'); }
};

window.API = API;
```

---

## PASO 3: ACTUALIZAR app.js

Reemplazar COMPLETAMENTE `dashboard/frontend/js/app.js` con el código del PLAN ARQUITECTURA v8 sección "2. FRONTEND JS — app.js".

El código completo está en: `docs/PLAN_ARQUITECTURA_COMPLETA_v8.md` sección 2.

Funciones que DEBE tener:
- showSection(), loadSectionData()
- updateDashboard() con badge de alertas
- renderMattersTable() con botón Drive, búsqueda, filtros
- openDriveLink(), openMatterModal(), deleteMatter()
- renderTemplatesList() con botón Exportar a Docs
- generateDocument(), exportToDocs()
- renderPlazosList() con botón Calendario, fila urgente
- renderCalendarView(), generateCalendarGrid()
- openPlazoModal(), openCalendarEvent()
- renderFinanzas() (usa FinanzasUI)
- renderAprobacionesList(), approveDocument(), rejectDocument()
- renderAlertasList() con botones Verificar plazos, Exportar Sheets, Sync Excel
- checkPlazosNow(), exportToSheets(), syncExcel()
- initSearchAndFilters() con debounce
- showModal(), hideModal(), showToast(), setLoading()

---

## PASO 4: ACTUALIZAR CSS

Abrir `dashboard/frontend/css/styles.css` y AGREGAR al final:

```css
/* === ESTILOS v8 === */

/* Templates grid */
.templates-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

.template-card {
  background: white;
  border-radius: var(--radius);
  padding: 24px;
  box-shadow: var(--shadow);
  border-left: 4px solid var(--color-primary);
}

.template-actions {
  display: flex;
  gap: 8px;
  margin-top: 16px;
}

/* Aprobaciones */
.aprobaciones-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.aprobacion-card {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: white;
  padding: 20px;
  border-radius: var(--radius);
  box-shadow: var(--shadow);
}

.aprobacion-actions {
  display: flex;
  gap: 8px;
}

/* Alertas */
.alertas-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 24px;
}

.alerta-card {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px 20px;
  border-radius: var(--radius);
  background: white;
  box-shadow: var(--shadow);
}

.alerta-card.urgente { border-left: 4px solid var(--color-danger); }
.alerta-card.advertencia { border-left: 4px solid var(--color-warning); }
.alerta-card.info { border-left: 4px solid var(--color-primary); }
.alerta-card.exito { border-left: 4px solid var(--color-success); }

.alerta-icon { font-size: 24px; }
.alerta-content { flex: 1; }
.alerta-content h4 { font-size: var(--font-size-lg); margin-bottom: 4px; }
.alerta-fecha { font-size: 12px; color: #64748b; }

.alertas-actions {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

/* Calendario */
.calendar-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.calendar-grid {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 8px;
}

.calendar-day {
  aspect-ratio: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  border: 1px solid #e2e8f0;
  border-radius: var(--radius);
  padding: 8px;
}

.calendar-day.empty { border: none; }
.calendar-day.has-events { background: #dbeafe; border-color: var(--color-primary); }

.day-number { font-weight: 600; margin-bottom: 4px; }
.event-dot {
  width: 8px;
  height: 8px;
  background: var(--color-danger);
  border-radius: 50%;
}

/* Botones pequeños */
.btn-sm {
  padding: 8px 16px;
  font-size: var(--font-size-base);
}

/* Loading spinner */
.loading-spinner {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #e2e8f0;
  border-top-color: var(--color-primary);
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* Urgente row */
.urgent-row { background: #fef2f2 !important; }

/* Badge en sidebar */
#alert-badge {
  display: none;
  background: var(--color-danger);
  color: white;
  font-size: 12px;
  padding: 2px 8px;
  border-radius: 9999px;
  margin-left: auto;
}

/* Empty state */
.empty-state {
  text-align: center;
  padding: 60px 20px;
  color: #64748b;
}

.empty-state p {
  font-size: var(--font-size-lg);
  margin-bottom: 20px;
}
```

---

## PASO 5: ACTUALIZAR index.html

Abrir `dashboard/frontend/index.html` y hacer estos cambios:

### 5.1 En el sidebar, agregar badge a Alertas:
Buscar:
```html
<li><a href="#alertas">🔔 Alertas</a></li>
```

Reemplazar con:
```html
<li>
  <a href="#alertas">
    🔔 Alertas
    <span id="alert-badge">0</span>
  </a>
</li>
```

### 5.2 Verificar que existen todos los IDs que usa app.js:
- `page-title`
- `count-matters`, `count-plazos`, `count-alertas`, `count-balance`
- `matters-table-container`
- `templates-list`
- `plazos-list`, `plazos-calendar`
- `finanzas-resumen`, `finanzas-tabla`
- `aprobaciones-list`
- `alertas-list`
- `modal`, `modal-title`, `modal-body`, `modal-close`, `modal-cancel`, `modal-confirm`
- `toast-container`
- `search-matters`, `filter-area`
- `btn-nuevo-matter`, `btn-nuevo-documento`, `btn-nuevo-plazo`

Si alguno falta, agregarlo.

---

## PASO 6: TESTS DE VERIFICACIÓN

Ejecutar en terminal y reportar output:

```bash
cd ~/ws-hermes-legal-pro

# Test 1: Backend levanta
python3 dashboard/backend/app.py &
sleep 3

# Test 2: Endpoints nuevos
echo "=== DRIVE LINK ==="
curl -s http://localhost:5000/api/drive-link/WIL-001 | python3 -m json.tool

echo "=== CALENDAR EVENTS ==="
curl -s http://localhost:5000/api/calendar-events | python3 -m json.tool

echo "=== TASKS ==="
curl -s http://localhost:5000/api/tasks | python3 -m json.tool

echo "=== CHECK PLAZOS ==="
curl -X POST -s http://localhost:5000/api/check-plazos | python3 -m json.tool

# Test 3: Verificar archivos frontend
ls -la dashboard/frontend/js/api.js
ls -la dashboard/frontend/js/app.js
ls -la dashboard/frontend/css/styles.css

# Test 4: Contar funciones en app.js
grep -c "function " dashboard/frontend/js/app.js
# Debe ser 20+

# Test 5: Verificar IDs en HTML
grep -c "id=" dashboard/frontend/index.html
# Debe ser 20+

# Test 6: Abrir en navegador y verificar visualmente
# - Botón Drive en tabla de casos
# - Botón Exportar a Docs en templates
# - Vista calendario en plazos
# - Botones en alertas (Verificar, Exportar, Sync)
# - Badge de alertas en sidebar
```

---

## PASO 7: GIT

```bash
cd ~/ws-hermes-legal-pro
git add -A
git commit -m "v8: Frontend 100% conectado a Google Workspace backend"
git push origin master
git log --oneline -3
```

---

## REPORTAR RESULTADO

Pegar output de:
1. `git log --oneline -3`
2. Tests de endpoints nuevos (drive-link, calendar-events, tasks, check-plazos)
3. `ls -la` de archivos modificados
4. Descripción visual de cada sección del dashboard
5. Si algo falló, pegar el error EXACTO

## REGLAS IMPORTANTES

- NO omitir ninguna función
- NO simplificar código
- SI un endpoint falla, reportar el error exacto
- SI un archivo no existe, crearlo
- VERIFICAR que cada botón del frontend llame a un endpoint real
- VERIFICAR que cada endpoint del backend sea llamado por el frontend
