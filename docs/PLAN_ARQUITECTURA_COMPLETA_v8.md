# PLAN ARQUITECTÓNICO COMPLETO v8 — WILLOW LEGAL PRO
# Sistema dual: Dashboard Web + Hermes Agent/Telegram
# Audiencia: Abogados 30-75 años, nivel digital básico

## ESTADO ACTUAL DEL SISTEMA (Commit 16814db)

### Backend existente y funcional:
- ✅ REST API Flask: matters, documentos, plazos, finanzas, aprobaciones, alertas
- ✅ Motor Kami: genera PDFs con --input/--output, 23 templates
- ✅ Google Drive: crea carpetas, sube PDFs, retorna links
- ✅ Google Calendar: crea eventos para plazos
- ✅ Google Tasks: manager disponible
- ✅ Google Sheets: exporta datos
- ✅ Google Docs: exporta documentos
- ✅ Sync Excel: bidireccional con PM maestro
- ✅ Check plazos: alertas automáticas
- ✅ Hermes Bridge: 15 comandos Telegram
- ✅ 3 Agentes: despacho, intake, admin

### Frontend v7 existente pero INCOMPLETO:
- ✅ HTML con sidebar, 7 secciones, modal, toast
- ✅ CSS responsive, modo oscuro
- ✅ JS con navegación SPA, tablas, formularios
- ❌ NO integra Calendar (endpoint existe, UI no)
- ❌ NO integra Tasks (script existe, UI no)
- ❌ NO integra Sheets (script existe, UI no)
- ❌ NO integra Docs export (script existe, UI no)
- ❌ NO integra Sync Excel (script existe, UI no)
- ❌ NO integra Check plazos (script existe, UI no)
- ❌ NO links directos a Drive en matters
- ❌ NO vista calendario para plazos
- ❌ NO badges de estado visual en tabla
- ❌ NO búsqueda en tiempo real
- ❌ NO filtros funcionales

---

## OBJETIVO v8

**Conectar el 100% del backend con el frontend.**
Cada script de Google Workspace debe tener su botón/link en la UI.
Cada endpoint del backend debe ser consumido por el frontend.

---

## ARQUITECTURA DE ARCHIVOS v8

### 1. BACKEND (dashboard/backend/app.py)

#### Endpoints existentes que DEBEN seguir funcionando:
```
GET    /matters              → listar matters
POST   /matter               → crear matter
PUT    /matter/<id>         → actualizar matter
DELETE /matter/<id>         → eliminar matter
GET    /templates            → listar templates
POST   /documento           → generar documento
GET    /plazos              → listar plazos
POST   /plazo               → crear plazo
GET    /aprobaciones        → listar aprobaciones
POST   /aprobacion/<id>/aprobar → aprobar documento
GET    /finanzas            → resumen financiero
POST   /finanza             → registrar transacción
GET    /alertas             → listar alertas
```

#### NUEVOS endpoints v8:
```
GET    /drive-link/<matter_id>   → obtener link de carpeta Drive
POST   /export-sheets            → exportar datos a Google Sheets
POST   /export-docs              → exportar documento a Google Docs
POST   /sync-excel               → sincronizar con Excel PM
GET    /tasks                    → listar tareas de Google Tasks
POST   /task                     → crear tarea en Google Tasks
GET    /calendar-events          → listar eventos del mes
POST   /check-plazos             → ejecutar verificación de plazos
```

### 2. FRONTEND JS (dashboard/frontend/js/)

#### api.js — Capa de API completa
```javascript
const API = {
  // Matters
  async getMatters() { return fetch('/api/matters').then(r => r.json()) }
  async createMatter(data) { return fetch('/api/matter', {method:'POST', body:JSON.stringify(data)}) }
  async updateMatter(id, data) { return fetch(`/api/matter/${id}`, {method:'PUT', body:JSON.stringify(data)}) }
  async deleteMatter(id) { return fetch(`/api/matter/${id}`, {method:'DELETE'}) }
  
  // Documentos
  async getTemplates() { return fetch('/api/templates').then(r => r.json()) }
  async generateDocument(templateId, matterId) { return fetch('/api/documento', {method:'POST', body:JSON.stringify({template_id:templateId, matter_id:matterId})}) }
  
  // Plazos
  async getPlazos() { return fetch('/api/plazos').then(r => r.json()) }
  async createPlazo(data) { return fetch('/api/plazo', {method:'POST', body:JSON.stringify(data)}) }
  
  // Finanzas
  async getFinanzas() { return fetch('/api/finanzas').then(r => r.json()) }
  async createFinanza(data) { return fetch('/api/finanza', {method:'POST', body:JSON.stringify(data)}) }
  
  // Alertas
  async getAlertas() { return fetch('/api/alertas').then(r => r.json()) }
  
  // Aprobaciones
  async getAprobaciones() { return fetch('/api/aprobaciones').then(r => r.json()) }
  async approveDocument(id) { return fetch(`/api/aprobacion/${id}/aprobar`, {method:'POST'}) }
  
  // NUEVO v8 — Google Workspace
  async getDriveLink(matterId) { return fetch(`/api/drive-link/${matterId}`).then(r => r.json()) }
  async exportToSheets(data) { return fetch('/api/export-sheets', {method:'POST', body:JSON.stringify(data)}) }
  async exportToDocs(data) { return fetch('/api/export-docs', {method:'POST', body:JSON.stringify(data)}) }
  async syncExcel() { return fetch('/api/sync-excel', {method:'POST'}).then(r => r.json()) }
  async getTasks() { return fetch('/api/tasks').then(r => r.json()) }
  async createTask(data) { return fetch('/api/task', {method:'POST', body:JSON.stringify(data)}) }
  async getCalendarEvents() { return fetch('/api/calendar-events').then(r => r.json()) }
  async checkPlazos() { return fetch('/api/check-plazos', {method:'POST'}).then(r => r.json()) }
}
```

#### app.js — Controlador principal
```javascript
// === INICIALIZACIÓN ===
document.addEventListener('DOMContentLoaded', () => {
  initNavigation()
  initQuickActions()
  initModal()
  initSearchAndFilters()
  showSection('inicio')
  updateDashboard()
  setInterval(updateDashboard, 30000) // Auto-refresh cada 30s
})

// === NAVEGACIÓN ===
function initNavigation() {
  document.querySelectorAll('.nav-menu a').forEach(link => {
    link.addEventListener('click', (e) => {
      e.preventDefault()
      const section = link.getAttribute('href').substring(1)
      showSection(section)
      loadSectionData(section)
    })
  })
}

function showSection(sectionId) {
  document.querySelectorAll('.section').forEach(s => s.classList.add('hidden'))
  document.getElementById(sectionId)?.classList.remove('hidden')
  document.querySelectorAll('.nav-menu a').forEach(a => a.classList.remove('active'))
  document.querySelector(`[href="#${sectionId}"]`)?.classList.add('active')
  
  const titles = {
    'inicio': 'Panel de Control',
    'matters': 'Mis Casos',
    'documentos': 'Documentos',
    'plazos': 'Plazos y Vencimientos',
    'finanzas': 'Finanzas',
    'aprobaciones': 'Aprobaciones',
    'alertas': 'Alertas'
  }
  document.getElementById('page-title').textContent = titles[sectionId] || 'Willow Legal'
}

function loadSectionData(section) {
  switch(section) {
    case 'matters': renderMattersTable(); break
    case 'documentos': renderTemplatesList(); break
    case 'plazos': renderPlazosList(); renderCalendarView(); break
    case 'finanzas': renderFinanzas(); break
    case 'aprobaciones': renderAprobacionesList(); break
    case 'alertas': renderAlertasList(); break
  }
}

// === DASHBOARD ===
async function updateDashboard() {
  try {
    const [matters, plazos, alertas, finanzas] = await Promise.all([
      API.getMatters(),
      API.getPlazos(),
      API.getAlertas(),
      API.getFinanzas()
    ])
    
    document.getElementById('count-matters').textContent = matters.count || 0
    document.getElementById('count-plazos').textContent = plazos.count || 0
    document.getElementById('count-alertas').textContent = alertas.count || 0
    document.getElementById('count-balance').textContent = '$' + (finanzas.balance || 0).toLocaleString()
    
    // Alertas urgentes en sidebar
    const urgentAlerts = (alertas.alertas || []).filter(a => a.tipo === 'urgente')
    const alertBadge = document.getElementById('alert-badge')
    if (alertBadge) {
      alertBadge.textContent = urgentAlerts.length
      alertBadge.style.display = urgentAlerts.length > 0 ? 'block' : 'none'
    }
  } catch (e) {
    console.error('Error actualizando dashboard:', e)
  }
}

// === MATTERS (CASOS) ===
async function renderMattersTable() {
  const container = document.getElementById('matters-table-container')
  if (!container) return
  
  setLoading(container, true)
  try {
    const data = await API.getMatters()
    const matters = data.matters || []
    
    if (matters.length === 0) {
      container.innerHTML = `
        <div class="empty-state">
          <p>No hay casos aún.</p>
          <button onclick="openMatterModal('create')" class="btn-primario">
            + Crear primer caso
          </button>
        </div>`
      return
    }
    
    container.innerHTML = `
      <table>
        <thead>
          <tr>
            <th>ID</th><th>Nombre</th><th>Cliente</th>
            <th>Área</th><th>Estado</th><th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          ${matters.map(m => `
            <tr data-id="${m.id}">
              <td><strong>${m.id}</strong></td>
              <td>${m.nombre}</td>
              <td>${m.cliente || '-'}</td>
              <td>${m.area || '-'}</td>
              <td><span class="badge ${m.estado}">${m.estado}</span></td>
              <td>
                <button onclick="viewMatter('${m.id}')" class="btn-secundario btn-sm">Ver</button>
                <button onclick="openDriveLink('${m.id}')" class="btn-secundario btn-sm" title="Abrir en Google Drive">Drive</button>
                <button onclick="openMatterModal('edit', '${m.id}')" class="btn-secundario btn-sm">Editar</button>
                <button onclick="deleteMatter('${m.id}')" class="btn-peligro btn-sm">Eliminar</button>
              </td>
            </tr>
          `).join('')}
        </tbody>
      </table>`
  } catch (e) {
    showToast('Error cargando casos: ' + e.message, 'error')
  } finally {
    setLoading(container, false)
  }
}

async function openDriveLink(matterId) {
  try {
    const data = await API.getDriveLink(matterId)
    if (data.drive_link) {
      window.open(data.drive_link, '_blank')
    } else {
      showToast('Este caso no tiene carpeta en Drive', 'warning')
    }
  } catch (e) {
    showToast('Error obteniendo link de Drive', 'error')
  }
}

function openMatterModal(mode, matterId = null) {
  const isEdit = mode === 'edit'
  const title = isEdit ? 'Editar Caso' : 'Nuevo Caso'
  
  const content = `
    <div class="form-group">
      <label>Nombre del caso *</label>
      <input type="text" id="matter-nombre" placeholder="Ej: Contrato IBM" required>
    </div>
    <div class="form-group">
      <label>Cliente</label>
      <input type="text" id="matter-cliente" placeholder="Nombre del cliente">
    </div>
    <div class="form-group">
      <label>Área</label>
      <select id="matter-area">
        <option value="corporativo">Corporativo</option>
        <option value="litigio">Litigio</option>
        <option value="fiscal">Fiscal</option>
        <option value="laboral">Laboral</option>
        <option value="inmobiliario">Inmobiliario</option>
        <option value="migratorio">Migratorio</option>
      </select>
    </div>
    <div class="form-group">
      <label>Responsable</label>
      <input type="text" id="matter-responsable" placeholder="Nombre del abogado">
    </div>
    <div class="form-group">
      <label>Descripción</label>
      <textarea id="matter-descripcion" rows="3" placeholder="Detalles del caso..."></textarea>
    </div>
  `
  
  showModal(title, content, async () => {
    const data = {
      nombre: document.getElementById('matter-nombre').value,
      cliente: document.getElementById('matter-cliente').value,
      area: document.getElementById('matter-area').value,
      responsable: document.getElementById('matter-responsable').value,
      descripcion: document.getElementById('matter-descripcion').value
    }
    
    if (!data.nombre) {
      showToast('El nombre es obligatorio', 'warning')
      return
    }
    
    try {
      if (isEdit) {
        await API.updateMatter(matterId, data)
        showToast('Caso actualizado', 'success')
      } else {
        await API.createMatter(data)
        showToast('Caso creado exitosamente', 'success')
      }
      hideModal()
      renderMattersTable()
      updateDashboard()
    } catch (e) {
      showToast('Error: ' + e.message, 'error')
    }
  })
}

function deleteMatter(id) {
  showModal('¿Eliminar caso?', 
    `<p>¿Seguro que quieres eliminar <strong>${id}</strong>?</p>
     <p>Se moverá a la papelera.</p>`,
    async () => {
      try {
        await API.deleteMatter(id)
        showToast('Caso eliminado', 'success')
        hideModal()
        renderMattersTable()
        updateDashboard()
      } catch (e) {
        showToast('Error: ' + e.message, 'error')
      }
    }
  )
}

function viewMatter(id) {
  showModal('Detalle del caso',
    `<p>Cargando detalles de ${id}...</p>`,
    () => hideModal()
  )
  // TODO: Implementar vista detalle completa
}

// === DOCUMENTOS ===
async function renderTemplatesList() {
  const container = document.getElementById('templates-list')
  if (!container) return
  
  try {
    const data = await API.getTemplates()
    const templates = data.templates || []
    
    container.innerHTML = `
      <div class="templates-grid">
        ${templates.map(t => `
          <div class="template-card">
            <h4>${t.nombre}</h4>
            <p>${t.descripcion || ''}</p>
            <div class="template-actions">
              <button onclick="generateDocument('${t.id}')" class="btn-primario">
                Generar PDF
              </button>
              <button onclick="exportToDocs('${t.id}')" class="btn-secundario">
                Exportar a Docs
              </button>
            </div>
          </div>
        `).join('')}
      </div>`
  } catch (e) {
    showToast('Error cargando templates', 'error')
  }
}

async function generateDocument(templateId, matterId = null) {
  if (!matterId) {
    // Mostrar selector de matter
    const data = await API.getMatters()
    const matters = data.matters || []
    
    if (matters.length === 0) {
      showToast('Primero crea un caso', 'warning')
      return
    }
    
    const options = matters.map(m => `<option value="${m.id}">${m.id} - ${m.nombre}</option>`).join('')
    
    showModal('Seleccionar caso',
      `<div class="form-group">
        <label>¿Para qué caso?</label>
        <select id="doc-matter-id">${options}</select>
      </div>`,
      async () => {
        const selectedId = document.getElementById('doc-matter-id').value
        hideModal()
        await generateDocument(templateId, selectedId)
      }
    )
    return
  }
  
  try {
    showToast('Generando documento...', 'warning')
    const result = await API.generateDocument(templateId, matterId)
    
    if (result.drive_link) {
      showToast('Documento generado y subido a Drive', 'success')
      // Mostrar link
      showModal('Documento listo',
        `<p>Documento generado exitosamente.</p>
         <a href="${result.drive_link}" target="_blank" class="btn-primario">Ver en Google Drive</a>`,
        () => hideModal()
      )
    } else {
      showToast('Documento generado localmente', 'success')
    }
  } catch (e) {
    showToast('Error generando documento: ' + e.message, 'error')
  }
}

async function exportToDocs(templateId) {
  try {
    showToast('Exportando a Google Docs...', 'warning')
    const result = await API.exportToDocs({template_id: templateId})
    if (result.docs_link) {
      window.open(result.docs_link, '_blank')
      showToast('Documento exportado a Docs', 'success')
    }
  } catch (e) {
    showToast('Error exportando: ' + e.message, 'error')
  }
}

// === PLAZOS ===
async function renderPlazosList() {
  const container = document.getElementById('plazos-list')
  if (!container) return
  
  try {
    const data = await API.getPlazos()
    const plazos = data.plazos || []
    
    if (plazos.length === 0) {
      container.innerHTML = `
        <div class="empty-state">
          <p>Sin plazos pendientes. ¡Buen trabajo!</p>
          <button onclick="openPlazoModal()" class="btn-primario">+ Crear plazo</button>
        </div>`
      return
    }
    
    container.innerHTML = `
      <table>
        <thead>
          <tr><th>ID</th><th>Título</th><th>Caso</th><th>Vencimiento</th><th>Estado</th><th>Acciones</th></tr>
        </thead>
        <tbody>
          ${plazos.map(p => `
            <tr class="${isUrgent(p.fecha_vencimiento) ? 'urgent-row' : ''}">
              <td>${p.id}</td>
              <td>${p.titulo}</td>
              <td>${p.matter_id || '-'}</td>
              <td>${formatDate(p.fecha_vencimiento)}</td>
              <td><span class="badge ${p.estado}">${p.estado}</span></td>
              <td>
                <button onclick="openCalendarEvent('${p.id}')" class="btn-secundario btn-sm">Calendario</button>
              </td>
            </tr>
          `).join('')}
        </tbody>
      </table>`
  } catch (e) {
    showToast('Error cargando plazos', 'error')
  }
}

function renderCalendarView() {
  const container = document.getElementById('plazos-calendar')
  if (!container) return
  
  // Vista simplificada de calendario mensual
  const now = new Date()
  const year = now.getFullYear()
  const month = now.getMonth()
  
  container.innerHTML = `
    <div class="calendar-header">
      <button onclick="changeMonth(-1)" class="btn-icon">←</button>
      <h3>${getMonthName(month)} ${year}</h3>
      <button onclick="changeMonth(1)" class="btn-icon">→</button>
    </div>
    <div class="calendar-grid" id="calendar-grid">
      <!-- Generado dinámicamente -->
    </div>
  `
  
  generateCalendarGrid(year, month)
}

async function generateCalendarGrid(year, month) {
  try {
    const data = await API.getCalendarEvents()
    const events = data.events || []
    
    // Filtrar eventos del mes
    const monthEvents = events.filter(e => {
      const d = new Date(e.fecha)
      return d.getFullYear() === year && d.getMonth() === month
    })
    
    // Generar grid de días
    const firstDay = new Date(year, month, 1).getDay()
    const daysInMonth = new Date(year, month + 1, 0).getDate()
    
    let grid = ''
    for (let i = 0; i < firstDay; i++) grid += '<div class="calendar-day empty"></div>'
    
    for (let day = 1; day <= daysInMonth; day++) {
      const dayEvents = monthEvents.filter(e => new Date(e.fecha).getDate() === day)
      const hasEvents = dayEvents.length > 0
      
      grid += `
        <div class="calendar-day ${hasEvents ? 'has-events' : ''}">
          <span class="day-number">${day}</span>
          ${dayEvents.map(e => `<span class="event-dot" title="${e.titulo}"></span>`).join('')}
        </div>
      `
    }
    
    document.getElementById('calendar-grid').innerHTML = grid
  } catch (e) {
    console.error('Error generando calendario:', e)
  }
}

function isUrgent(fecha) {
  if (!fecha) return false
  const days = Math.ceil((new Date(fecha) - new Date()) / (1000 * 60 * 60 * 24))
  return days <= 7 && days >= 0
}

function formatDate(fecha) {
  if (!fecha) return '-'
  return new Date(fecha).toLocaleDateString('es-MX')
}

function getMonthName(month) {
  const names = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 
                 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
  return names[month]
}

function openPlazoModal() {
  showModal('Nuevo Plazo',
    `<div class="form-group">
      <label>Título *</label>
      <input type="text" id="plazo-titulo" placeholder="Ej: Audiencia judicial">
    </div>
    <div class="form-group">
      <label>Caso relacionado</label>
      <select id="plazo-matter"><option value="">Ninguno</option></select>
    </div>
    <div class="form-group">
      <label>Fecha de vencimiento *</label>
      <input type="date" id="plazo-fecha">
    </div>
    <div class="form-group">
      <label>Tipo</label>
      <select id="plazo-tipo">
        <option value="audiencia">Audiencia</option>
        <option value="entrega">Entrega de documentos</option>
        <option value="pago">Pago</option>
        <option value="general">General</option>
      </select>
    </div>
    <div class="form-group">
      <label>Notas</label>
      <textarea id="plazo-notas" rows="2"></textarea>
    </div>`,
    async () => {
      const data = {
        titulo: document.getElementById('plazo-titulo').value,
        matter_id: document.getElementById('plazo-matter').value,
        fecha_vencimiento: document.getElementById('plazo-fecha').value,
        tipo: document.getElementById('plazo-tipo').value,
        notas: document.getElementById('plazo-notas').value
      }
      
      if (!data.titulo || !data.fecha_vencimiento) {
        showToast('Título y fecha son obligatorios', 'warning')
        return
      }
      
      try {
        await API.createPlazo(data)
        showToast('Plazo creado', 'success')
        hideModal()
        renderPlazosList()
        renderCalendarView()
        updateDashboard()
      } catch (e) {
        showToast('Error: ' + e.message, 'error')
      }
    }
  )
  
  // Cargar matters en el select
  API.getMatters().then(data => {
    const matters = data.matters || []
    const select = document.getElementById('plazo-matter')
    matters.forEach(m => {
      select.innerHTML += `<option value="${m.id}">${m.id} - ${m.nombre}</option>`
    })
  })
}

async function openCalendarEvent(plazoId) {
  try {
    const data = await API.getPlazos()
    const plazo = data.plazos.find(p => p.id === plazoId)
    if (plazo && plazo.calendar_link) {
      window.open(plazo.calendar_link, '_blank')
    } else {
      showToast('Este plazo no tiene evento en Calendar', 'warning')
    }
  } catch (e) {
    showToast('Error abriendo calendario', 'error')
  }
}

// === FINANZAS ===
async function renderFinanzas() {
  await FinanzasUI.renderResumen()
  await FinanzasUI.renderTabla()
}

// === APROBACIONES ===
async function renderAprobacionesList() {
  const container = document.getElementById('aprobaciones-list')
  if (!container) return
  
  try {
    const data = await API.getAprobaciones()
    const aprobaciones = data.aprobaciones || []
    
    if (aprobaciones.length === 0) {
      container.innerHTML = `
        <div class="empty-state">
          <p>No hay documentos pendientes de aprobación.</p>
        </div>`
      return
    }
    
    container.innerHTML = `
      <div class="aprobaciones-list">
        ${aprobaciones.map(a => `
          <div class="aprobacion-card">
            <div class="aprobacion-info">
              <h4>${a.titulo}</h4>
              <p>Caso: ${a.matter_id || '-'} | Fecha: ${formatDate(a.fecha)}</p>
            </div>
            <div class="aprobacion-actions">
              <button onclick="approveDocument('${a.id}')" class="btn-primario">✓ Aprobar</button>
              <button onclick="rejectDocument('${a.id}')" class="btn-peligro">✗ Rechazar</button>
              <a href="${a.drive_link}" target="_blank" class="btn-secundario">Ver</a>
            </div>
          </div>
        `).join('')}
      </div>`
  } catch (e) {
    showToast('Error cargando aprobaciones', 'error')
  }
}

async function approveDocument(id) {
  try {
    await API.approveDocument(id)
    showToast('Documento aprobado', 'success')
    renderAprobacionesList()
  } catch (e) {
    showToast('Error: ' + e.message, 'error')
  }
}

function rejectDocument(id) {
  showModal('Rechazar documento',
    `<div class="form-group">
      <label>Motivo del rechazo</label>
      <textarea id="reject-reason" rows="3" placeholder="Explica por qué se rechaza..."></textarea>
    </div>`,
    async () => {
      const reason = document.getElementById('reject-reason').value
      // TODO: Implementar rechazo en backend
      showToast('Documento rechazado: ' + reason, 'warning')
      hideModal()
      renderAprobacionesList()
    }
  )
}

// === ALERTAS ===
async function renderAlertasList() {
  const container = document.getElementById('alertas-list')
  if (!container) return
  
  try {
    const data = await API.getAlertas()
    const alertas = data.alertas || []
    
    container.innerHTML = `
      <div class="alertas-list">
        ${alertas.map(a => `
          <div class="alerta-card ${a.tipo}">
            <div class="alerta-icon">${getAlertIcon(a.tipo)}</div>
            <div class="alerta-content">
              <h4>${a.titulo}</h4>
              <p>${a.mensaje}</p>
              <span class="alerta-fecha">${formatDate(a.fecha)}</span>
            </div>
            <button onclick="dismissAlert('${a.id}')" class="btn-icon">×</button>
          </div>
        `).join('')}
      </div>
      
      <div class="alertas-actions">
        <button onclick="checkPlazosNow()" class="btn-primario">🔍 Verificar plazos ahora</button>
        <button onclick="exportToSheets()" class="btn-secundario">📊 Exportar a Sheets</button>
        <button onclick="syncExcel()" class="btn-secundario">🔄 Sync Excel</button>
      </div>`
  } catch (e) {
    showToast('Error cargando alertas', 'error')
  }
}

function getAlertIcon(tipo) {
  const icons = {
    'urgente': '🔴',
    'advertencia': '🟡',
    'info': '🔵',
    'exito': '🟢'
  }
  return icons[tipo] || '🔵'
}

async function checkPlazosNow() {
  try {
    showToast('Verificando plazos...', 'warning')
    const result = await API.checkPlazos()
    showToast(`Verificación completa: ${result.nuevas_alertas || 0} nuevas alertas`, 'success')
    renderAlertasList()
    updateDashboard()
  } catch (e) {
    showToast('Error verificando plazos', 'error')
  }
}

async function exportToSheets() {
  try {
    showToast('Exportando a Google Sheets...', 'warning')
    const result = await API.exportToSheets({tipo: 'resumen'})
    if (result.sheets_link) {
      window.open(result.sheets_link, '_blank')
      showToast('Datos exportados a Sheets', 'success')
    }
  } catch (e) {
    showToast('Error exportando: ' + e.message, 'error')
  }
}

async function syncExcel() {
  try {
    showToast('Sincronizando con Excel...', 'warning')
    const result = await API.syncExcel()
    showToast('Sincronización completa', 'success')
  } catch (e) {
    showToast('Error sincronizando: ' + e.message, 'error')
  }
}

function dismissAlert(id) {
  // TODO: Implementar dismiss en backend
  showToast('Alerta marcada como leída', 'success')
  renderAlertasList()
}

// === ACCIONES RÁPIDAS ===
function initQuickActions() {
  document.getElementById('btn-nuevo-matter')?.addEventListener('click', () => {
    showSection('matters')
    openMatterModal('create')
  })
  
  document.getElementById('btn-nuevo-documento')?.addEventListener('click', () => {
    showSection('documentos')
  })
  
  document.getElementById('btn-nuevo-plazo')?.addEventListener('click', () => {
    showSection('plazos')
    openPlazoModal()
  })
}

// === BÚSQUEDA Y FILTROS ===
function initSearchAndFilters() {
  const searchInput = document.getElementById('search-matters')
  if (searchInput) {
    searchInput.addEventListener('input', debounce((e) => {
      filterMatters(e.target.value)
    }, 300))
  }
  
  const filterArea = document.getElementById('filter-area')
  if (filterArea) {
    filterArea.addEventListener('change', (e) => {
      filterMattersByArea(e.target.value)
    })
  }
}

function debounce(func, wait) {
  let timeout
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout)
      func(...args)
    }
    clearTimeout(timeout)
    timeout = setTimeout(later, wait)
  }
}

function filterMatters(query) {
  const rows = document.querySelectorAll('#matters-table-container tbody tr')
  const lowerQuery = query.toLowerCase()
  
  rows.forEach(row => {
    const text = row.textContent.toLowerCase()
    row.style.display = text.includes(lowerQuery) ? '' : 'none'
  })
}

function filterMattersByArea(area) {
  const rows = document.querySelectorAll('#matters-table-container tbody tr')
  
  rows.forEach(row => {
    if (!area) {
      row.style.display = ''
      return
    }
    const rowArea = row.querySelector('td:nth-child(4)')?.textContent.toLowerCase()
    row.style.display = rowArea === area ? '' : 'none'
  })
}

// === MODAL ===
function initModal() {
  document.getElementById('modal-close')?.addEventListener('click', hideModal)
  document.getElementById('modal-cancel')?.addEventListener('click', hideModal)
  
  // Cerrar al hacer clic fuera
  document.getElementById('modal')?.addEventListener('click', (e) => {
    if (e.target.id === 'modal') hideModal()
  })
}

function showModal(title, content, onConfirm) {
  document.getElementById('modal-title').textContent = title
  document.getElementById('modal-body').innerHTML = content
  document.getElementById('modal').classList.remove('hidden')
  
  const confirmBtn = document.getElementById('modal-confirm')
  confirmBtn.onclick = () => { onConfirm() }
}

function hideModal() {
  document.getElementById('modal').classList.add('hidden')
}

// === TOAST ===
function showToast(message, type = 'success') {
  const container = document.getElementById('toast-container')
  if (!container) return
  
  const toast = document.createElement('div')
  toast.className = `toast ${type}`
  toast.textContent = message
  container.appendChild(toast)
  
  setTimeout(() => {
    toast.style.opacity = '0'
    setTimeout(() => toast.remove(), 300)
  }, 4000)
}

// === LOADING ===
function setLoading(element, isLoading) {
  if (isLoading) {
    element.innerHTML = '<div class="loading-spinner"><div class="spinner"></div><p>Cargando...</p></div>'
  }
}

// === UTILIDADES ===
function changeMonth(delta) {
  // TODO: Implementar navegación de meses en calendario
}

// === EXPORTAR PARA TESTING ===
window.API = API
window.showToast = showToast
window.showModal = showModal
window.hideModal = hideModal
```

### 3. FRONTEND CSS (dashboard/frontend/css/styles.css)

Mantener el CSS v7 existente pero AGREGAR:

```css
/* === NUEVOS ESTILOS v8 === */

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

.template-card h4 {
  font-size: var(--font-size-lg);
  margin-bottom: 8px;
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

.alerta-icon {
  font-size: 24px;
}

.alerta-content {
  flex: 1;
}

.alerta-content h4 {
  font-size: var(--font-size-lg);
  margin-bottom: 4px;
}

.alerta-fecha {
  font-size: 12px;
  color: #64748b;
}

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

.calendar-day.empty {
  border: none;
}

.calendar-day.has-events {
  background: #dbeafe;
  border-color: var(--color-primary);
}

.day-number {
  font-weight: 600;
  margin-bottom: 4px;
}

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
.urgent-row {
  background: #fef2f2 !important;
}

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
```

### 4. FRONTEND HTML (dashboard/frontend/index.html)

Mantener HTML v7 pero AGREGAR en el sidebar:

```html
<!-- En .nav-menu, agregar badge a Alertas -->
<li>
  <a href="#alertas">
    🔔 Alertas
    <span id="alert-badge">0</span>
  </a>
</li>
```

Y en la sección de alertas, agregar botones de acción:

```html
<section id="alertas" class="section hidden">
  <h2>Alertas del Sistema</h2>
  <div id="alertas-list"></div>
  <!-- Los botones de acción se renderizan por JS -->
</section>
```

### 5. BACKEND NUEVOS ENDPOINTS (agregar a app.py)

```python
# === GOOGLE WORKSPACE INTEGRATION ===

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
            
            # Crear hoja con resumen
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
        
        # Obtener template
        templates = load_templates()
        template = next((t for t in templates if t['id'] == template_id), None)
        
        if not template:
            return jsonify({'error': 'Template no encontrado'}), 404
        
        # Crear documento en Docs
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
        
        # Obtener eventos del mes actual
        now = datetime.now()
        events = cal.list_events(
            year=now.year,
            month=now.month
        )
        
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
        
        # Guardar alertas nuevas
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

## MAPA DE CONECTIVIDAD v8

```
FRONTEND                    BACKEND                    GOOGLE WORKSPACE
─────────                   ───────                    ────────────────
index.html  ─────────────→  app.py
                            ├── /api/matters  ───────→  drive_manager (crear carpetas)
                            ├── /api/documento ──────→  motor_kami (PDF)
                            │                           └── drive_manager (subir PDF)
                            ├── /api/plazos  ────────→  calendar_manager (eventos)
                            ├── /api/drive-link ─────→  drive_manager (links)
                            ├── /api/export-sheets ──→  sheets_manager
                            ├── /api/export-docs ────→  docs_exporter
                            ├── /api/sync-excel ─────→  sync_excel_json
                            ├── /api/tasks ──────────→  tasks_manager
                            ├── /api/calendar-events →  calendar_manager
                            └── /api/check-plazos ───→  check_plazos
                                                         └── alertas.json
```

---

## TESTS DE VERIFICACIÓN v8

```bash
# 1. Verificar todos los endpoints nuevos
curl -s http://localhost:5000/api/drive-link/WIL-001 | python3 -m json.tool
curl -s http://localhost:5000/api/calendar-events | python3 -m json.tool
curl -s http://localhost:5000/api/tasks | python3 -m json.tool
curl -X POST http://localhost:5000/api/check-plazos | python3 -m json.tool

# 2. Verificar frontend tiene todos los botones
# Abrir navegador y verificar:
# - Botón "Drive" en cada caso
# - Botón "Exportar a Docs" en templates
# - Botón "Calendario" en plazos
# - Botón "Verificar plazos" en alertas
# - Botón "Exportar a Sheets" en alertas
# - Botón "Sync Excel" en alertas
# - Vista calendario en plazos
# - Badge de alertas en sidebar

# 3. Test end-to-end
# Crear caso → Generar documento → Ver en Drive
# Crear plazo → Ver en Calendar
# Exportar a Sheets → Abrir Sheets
# Verificar plazos → Ver alerta nueva
```

---

## GIT

```bash
cd ~/ws-hermes-legal-pro
git add -A
git commit -m "v8: Frontend completo conectado al 100% del backend Google Workspace"
git push origin master
git log --oneline -3
```

---

## REPORTAR

Pegar output de:
1. `git log --oneline -3`
2. `curl -s http://localhost:5000/api/drive-link/WIL-001`
3. `curl -s http://localhost:5000/api/calendar-events`
4. Screenshot descriptivo de cada sección del dashboard
