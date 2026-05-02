// === NAVEGACIÓN ===
function showSection(sectionId) {
  document.querySelectorAll('.section').forEach(s => s.classList.add('hidden'));
  document.getElementById(sectionId).classList.remove('hidden');
  document.querySelectorAll('.nav-menu a').forEach(a => a.classList.remove('active'));
  document.querySelector(`[href="#${sectionId}"]`).classList.add('active');
  document.getElementById('page-title').textContent = {
    'inicio': 'Panel de Control',
    'matters': 'Mis Casos',
    'documentos': 'Documentos',
    'plazos': 'Plazos y Vencimientos',
    'finanzas': 'Finanzas',
    'aprobaciones': 'Aprobaciones Pendientes',
    'alertas': 'Alertas del Sistema'
  }[sectionId];
}

// === MATTERS ===
async function renderMattersTable() {
  const container = document.getElementById('matters-table-container');
  setLoading(container, true);
  
  try {
    const matters = await API.getMatters(); // returns array
    const mattersList = Array.isArray(matters) ? matters : (matters.matters || []);
    
    if (mattersList.length === 0) {
      container.innerHTML = `
        <div class="empty-state">
          <p>No hay casos aún.</p>
          <button onclick="openMatterModal('create')" class="btn-primario">
            + Crear primer caso
          </button>
        </div>`;
      return;
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
          ${mattersList.map(m => `
            <tr>
              <td><strong>${m.id}</strong></td>
              <td>${m.nombre || m.id}</td>
              <td>${m.cliente || '-'}</td>
              <td>${m.area_practica || m.area || '-'}</td>
              <td><span class="badge ${m.estado}">${m.estado || 'N/A'}</span></td>
              <td>
                <button onclick="viewMatter('${m.id}')" class="btn-secundario">Ver</button>
                <button onclick="openMatterModal('edit', '${m.id}')" class="btn-secundario">Editar</button>
                <button onclick="deleteMatter('${m.id}')" class="btn-peligro">Eliminar</button>
              </td>
            </tr>
          `).join('')}
        </tbody>
      </table>`;
  } catch (e) {
    showToast('Error cargando casos: ' + e.message, 'error');
  } finally {
    setLoading(container, false);
  }
}

function openMatterModal(mode, matterId = null) {
  const isEdit = mode === 'edit';
  const title = isEdit ? 'Editar Caso' : 'Nuevo Caso';
  
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
  `;
  
  showModal(title, content, async () => {
    const data = {
      nombre: document.getElementById('matter-nombre').value,
      cliente: document.getElementById('matter-cliente').value,
      area: document.getElementById('matter-area').value,
      responsable: document.getElementById('matter-responsable').value,
      descripcion: document.getElementById('matter-descripcion').value
    };
    
    if (!data.nombre) {
      showToast('El nombre es obligatorio', 'warning');
      return;
    }
    
    try {
      if (isEdit) {
        await API.updateMatter(matterId, data);
        showToast('Caso actualizado', 'success');
      } else {
        await API.createMatter(data);
        showToast('Caso creado exitosamente', 'success');
      }
      hideModal();
      renderMattersTable();
      updateDashboard();
    } catch (e) {
      showToast('Error: ' + e.message, 'error');
    }
  });
}

function deleteMatter(id) {
  showModal('¿Eliminar caso?', 
    `<p>¿Seguro que quieres eliminar el caso <strong>${id}</strong>?</p>
     <p>Se moverá a la papelera y podrás recuperarlo.</p>`,
    async () => {
      try {
        await API.deleteMatter(id);
        showToast('Caso eliminado', 'success');
        hideModal();
        renderMattersTable();
        updateDashboard();
      } catch (e) {
        showToast('Error: ' + e.message, 'error');
      }
    }
  );
}

// === DOCUMENTOS ===
async function renderTemplatesList() {
  const container = document.getElementById('templates-list');
  try {
    const data = await API.getTemplates();
    const templates = data.templates || [];
    
    container.innerHTML = templates.map(t => `
      <div class="template-card">
        <h4>${t.nombre}</h4>
        <p>${t.descripcion || ''}</p>
        <button onclick="generateDocument('${t.id}')" class="btn-primario">
          Generar documento
        </button>
      </div>
    `).join('');
  } catch (e) {
    showToast('Error cargando templates', 'error');
  }
}

// === PLAZOS ===
async function renderPlazosList() {
  const container = document.getElementById('plazos-list');
  try {
    const data = await API.getPlazos();
    const plazos = data.plazos || [];
    
    if (plazos.length === 0) {
      container.innerHTML = `
        <div class="empty-state">
          <p>Sin plazos pendientes. ¡Buen trabajo!</p>
          <button onclick="openPlazoModal()" class="btn-primario">+ Crear plazo</button>
        </div>`;
      return;
    }
    
    container.innerHTML = `
      <table>
        <thead>
          <tr><th>ID</th><th>Título</th><th>Matter</th><th>Vencimiento</th><th>Estado</th></tr>
        </thead>
        <tbody>
          ${plazos.map(p => `
            <tr>
              <td>${p.id}</td>
              <td>${p.titulo}</td>
              <td>${p.matter_id || '-'}</td>
              <td>${p.fecha_vencimiento || '-'}</td>
              <td><span class="badge ${p.estado}">${p.estado}</span></td>
            </tr>
          `).join('')}
        </tbody>
      </table>`;
  } catch (e) {
    showToast('Error cargando plazos', 'error');
  }
}

// === FINANZAS ===
async function renderFinanzas() {
  await FinanzasUI.renderResumen();
  await FinanzasUI.renderTabla();
}

// === DASHBOARD ===
async function updateDashboard() {
  try {
    const matters = await API.getMatters();
    const mattersArr = Array.isArray(matters) ? matters : (matters.matters || []);
    document.getElementById('count-matters').textContent = mattersArr.length;
    
    const plazos = await API.getPlazos();
    document.getElementById('count-plazos').textContent = plazos.count || plazos.plazos?.length || 0;
    
    const alertas = await API.getAlertas();
    const alertasArr = Array.isArray(alertas) ? alertas : (alertas.alertas || []);
    document.getElementById('count-alertas').textContent = alertasArr.length;
    
    const finanzas = await FinanzasAPI.cargarResumen();
    const balance = finanzas.balance || (finanzas.resumen?.total_anticipos || 0) - (finanzas.resumen?.total_pendiente || 0);
    document.getElementById('count-balance').textContent = 
      '$' + (balance || 0).toLocaleString();
  } catch (e) {
    console.error('Error actualizando dashboard:', e);
  }
}

// === HELPERS ADICIONALES ===
function generateDocQuick(template) {
  showModal('Generar Documento', `
    <div class="form-group">
      <label>Matter ID</label>
      <input type="text" id="gen-matter-id" placeholder="Ej: LEG-001">
    </div>
    <p>Template: ${template}</p>
  `, async () => {
    const matterId = document.getElementById('gen-matter-id').value.trim();
    if (!matterId) { showToast('Ingresa un Matter ID', 'warning'); return; }
    try {
      const result = await API.generateDoc(matterId, { template_key: template });
      showToast('Documento generado: ' + (result.file_path || 'OK'), 'success');
      hideModal();
    } catch (e) {
      showToast('Error: ' + e.message, 'error');
    }
  });
}

function openPlazoModal() {
  showModal('Nuevo Plazo', `
    <div class="form-group">
      <label>Matter ID *</label>
      <input type="text" id="plazo-matter" placeholder="Ej: WIL-001">
    </div>
    <div class="form-group">
      <label>Título *</label>
      <input type="text" id="plazo-titulo" placeholder="Ej: Vencimiento contrato">
    </div>
    <div class="form-group">
      <label>Fecha de vencimiento *</label>
      <input type="date" id="plazo-fecha">
    </div>
    <div class="form-group">
      <label>Tipo</label>
      <select id="plazo-tipo">
        <option value="general">General</option>
        <option value="judicial">Judicial</option>
        <option value="contractual">Contractual</option>
        <option value="fiscal">Fiscal</option>
      </select>
    </div>
  `, async () => {
    const data = {
      matter_id: document.getElementById('plazo-matter').value.trim(),
      titulo: document.getElementById('plazo-titulo').value.trim(),
      fecha_vencimiento: document.getElementById('plazo-fecha').value,
      tipo: document.getElementById('plazo-tipo').value
    };
    if (!data.matter_id || !data.titulo || !data.fecha_vencimiento) {
      showToast('Completa todos los campos', 'warning');
      return;
    }
    try {
      await API.createPlazo(data);
      showToast('Plazo creado', 'success');
      hideModal();
      renderPlazosList();
    } catch (e) {
      showToast('Error: ' + e.message, 'error');
    }
  });
}

function viewMatter(id) {
  window.open(`http://localhost:8082/api/matters/${id}`, '_blank');
}

function generateDocument(templateId) {
  generateDocQuick(templateId);
}

// === UI HELPERS ===
function showModal(title, content, onConfirm) {
  document.getElementById('modal-title').textContent = title;
  document.getElementById('modal-body').innerHTML = content;
  document.getElementById('modal').classList.remove('hidden');
  
  const confirmBtn = document.getElementById('modal-confirm');
  confirmBtn.onclick = () => { onConfirm(); };
}

function hideModal() {
  document.getElementById('modal').classList.add('hidden');
}

function showToast(message, type = 'success') {
  const container = document.getElementById('toast-container');
  const toast = document.createElement('div');
  toast.className = `toast ${type}`;
  toast.textContent = message;
  container.appendChild(toast);
  
  setTimeout(() => {
    toast.remove();
  }, 4000);
}

function setLoading(element, isLoading) {
  if (isLoading) {
    element.innerHTML = '<p class="loading">Cargando...</p>';
  }
}

// === EVENT LISTENERS ===
document.addEventListener('DOMContentLoaded', () => {
  // Navegación
  document.querySelectorAll('.nav-menu a').forEach(link => {
    link.addEventListener('click', (e) => {
      e.preventDefault();
      const section = link.getAttribute('href').substring(1);
      showSection(section);
      
      if (section === 'matters') renderMattersTable();
      if (section === 'documentos') renderTemplatesList();
      if (section === 'plazos') renderPlazosList();
      if (section === 'finanzas') renderFinanzas();
    });
  });
  
  // Botones de acción rápida
  document.getElementById('btn-nuevo-matter').onclick = () => {
    showSection('matters');
    openMatterModal('create');
  };
  
  document.getElementById('btn-nuevo-documento').onclick = () => {
    showSection('documentos');
  };
  
  document.getElementById('btn-nuevo-plazo').onclick = () => {
    showSection('plazos');
    openPlazoModal();
  };
  
  // Modal close
  document.getElementById('modal-close').onclick = hideModal;
  document.getElementById('modal-cancel').onclick = hideModal;
  
  // Inicializar
  showSection('inicio');
  updateDashboard();
  
  // Auto-refresh cada 30 segundos
  setInterval(updateDashboard, 30000);
});
