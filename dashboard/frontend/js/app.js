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
    
    // Tareas pendientes (Google Tasks)
    API.getTasks().then(data => {
      const tasks = data.tasks || []
      const pendingTasks = tasks.filter(t => t.status !== 'completed')
      // Opcional: mostrar en consola o dashboard
      console.log(`📋 Tareas pendientes: ${pendingTasks.length}`)
    }).catch(() => {}) // Silenciar si no está configurado
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
