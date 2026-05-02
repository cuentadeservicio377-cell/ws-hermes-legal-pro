# PROMPT EJECUTABLE v7 — POLISH + DOCUMENTACIÓN PARA ABOGADOS NO-DIGITAL

## Contexto
Hermes Legal Pro v6 tiene backend completo. Falta frontend usable y documentación para abogados de 30-75 años con poca experiencia digital.

## Principios
- Cero suposiciones técnicas
- Botones grandes, texto grande, contraste alto
- Un solo botón por acción
- Siempre explicar qué pasó y qué hacer si falla

---

## TAREA 1: Crear styles.css completo

**Archivo nuevo**: `dashboard/frontend/css/styles.css`

Crear CSS con estas secciones exactas:

```css
/* === RESET Y BASE === */
* { margin: 0; padding: 0; box-sizing: border-box; }

:root {
  --font-main: 'Segoe UI', system-ui, -apple-system, sans-serif;
  --color-bg: #ffffff;
  --color-text: #1a1a1a;
  --color-primary: #2563eb;
  --color-primary-hover: #1d4ed8;
  --color-success: #16a34a;
  --color-warning: #ca8a04;
  --color-danger: #dc2626;
  --color-sidebar: #1e293b;
  --color-card: #f8fafc;
  --shadow: 0 2px 8px rgba(0,0,0,0.1);
  --radius: 8px;
  --spacing: 16px;
  --font-size-base: 16px;
  --font-size-lg: 18px;
  --font-size-xl: 24px;
  --font-size-xxl: 32px;
}

body {
  font-family: var(--font-main);
  font-size: var(--font-size-base);
  color: var(--color-text);
  background: var(--color-bg);
  line-height: 1.6;
}

/* === LAYOUT: SIDEBAR + MAIN === */
.sidebar {
  width: 260px;
  height: 100vh;
  background: var(--color-sidebar);
  color: white;
  position: fixed;
  left: 0;
  top: 0;
  display: flex;
  flex-direction: column;
  padding: var(--spacing);
}

.logo {
  display: flex;
  align-items: center;
  gap: 12px;
  padding-bottom: 24px;
  border-bottom: 1px solid rgba(255,255,255,0.1);
  margin-bottom: 24px;
}

.logo img { width: 40px; height: 40px; }
.logo span { font-size: var(--font-size-lg); font-weight: 700; }

.nav-menu {
  list-style: none;
  flex: 1;
}

.nav-menu li { margin-bottom: 4px; }

.nav-menu a {
  display: block;
  padding: 12px 16px;
  color: rgba(255,255,255,0.8);
  text-decoration: none;
  border-radius: var(--radius);
  font-size: var(--font-size-lg);
  transition: all 0.2s;
}

.nav-menu a:hover,
.nav-menu a.active {
  background: rgba(255,255,255,0.1);
  color: white;
}

.user-info {
  padding-top: 16px;
  border-top: 1px solid rgba(255,255,255,0.1);
}

.user-info span {
  display: block;
  margin-bottom: 12px;
  font-size: 14px;
  color: rgba(255,255,255,0.6);
}

.main-content {
  margin-left: 260px;
  min-height: 100vh;
  padding: var(--spacing);
}

/* === HEADER === */
.main-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  padding-bottom: 16px;
  border-bottom: 2px solid #e2e8f0;
}

.main-header h1 {
  font-size: var(--font-size-xxl);
  font-weight: 700;
}

.quick-actions {
  display: flex;
  gap: 12px;
}

/* === BOTONES === */
.btn-primario,
.btn-secundario,
.btn-peligro,
.btn-icon {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 14px 28px;
  border: none;
  border-radius: var(--radius);
  font-size: var(--font-size-lg);
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-primario {
  background: var(--color-primary);
  color: white;
}

.btn-primario:hover {
  background: var(--color-primary-hover);
  transform: translateY(-1px);
}

.btn-secundario {
  background: white;
  color: var(--color-primary);
  border: 2px solid var(--color-primary);
}

.btn-peligro {
  background: var(--color-danger);
  color: white;
}

.btn-icon {
  padding: 8px 12px;
  background: transparent;
  font-size: 24px;
}

/* === TARJETAS === */
.cards-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 20px;
  margin-bottom: 32px;
}

.card {
  background: var(--color-card);
  border-radius: var(--radius);
  padding: 24px;
  box-shadow: var(--shadow);
  border-left: 4px solid var(--color-primary);
}

.card h3 {
  font-size: 14px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  color: #64748b;
  margin-bottom: 8px;
}

.big-number {
  font-size: var(--font-size-xxl);
  font-weight: 700;
  color: var(--color-text);
  margin-bottom: 8px;
}

.card a {
  color: var(--color-primary);
  text-decoration: none;
  font-weight: 600;
}

.card-matters { border-left-color: var(--color-primary); }
.card-plazos { border-left-color: var(--color-warning); }
.card-alertas { border-left-color: var(--color-danger); }
.card-balance { border-left-color: var(--color-success); }

/* === SECCIONES === */
.section {
  display: none;
}

.section:not(.hidden) {
  display: block;
}

.section h2 {
  font-size: var(--font-size-xl);
  margin-bottom: 20px;
}

/* === TABLAS === */
table {
  width: 100%;
  border-collapse: collapse;
  background: white;
  border-radius: var(--radius);
  overflow: hidden;
  box-shadow: var(--shadow);
}

th, td {
  padding: 14px 16px;
  text-align: left;
  border-bottom: 1px solid #e2e8f0;
}

th {
  background: var(--color-card);
  font-weight: 600;
  font-size: 14px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  color: #64748b;
}

tr:hover {
  background: #f8fafc;
}

/* === BADGES === */
.badge {
  display: inline-block;
  padding: 4px 12px;
  border-radius: 9999px;
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
}

.badge.activo { background: #dcfce7; color: #166534; }
.badge.pendiente { background: #fef9c3; color: #854d0e; }
.badge.urgente { background: #fee2e2; color: #991b1b; }
.badge.aprobado { background: #dcfce7; color: #166534; }
.badge.rechazado { background: #fee2e2; color: #991b1b; }
.badge.ingreso { background: #dcfce7; color: #166534; }
.badge.egreso { background: #fee2e2; color: #991b1b; }

/* === FORMULARIOS === */
.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 600;
  font-size: var(--font-size-lg);
}

.form-group input,
.form-group select,
.form-group textarea {
  width: 100%;
  padding: 12px 16px;
  border: 2px solid #e2e8f0;
  border-radius: var(--radius);
  font-size: var(--font-size-lg);
  transition: border-color 0.2s;
}

.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
  outline: none;
  border-color: var(--color-primary);
}

/* === MODAL === */
.modal {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal.hidden { display: none; }

.modal-content {
  background: white;
  border-radius: var(--radius);
  width: 90%;
  max-width: 600px;
  max-height: 90vh;
  overflow-y: auto;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 24px;
  border-bottom: 1px solid #e2e8f0;
}

.modal-header h3 {
  font-size: var(--font-size-xl);
}

.modal-body {
  padding: 24px;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  padding: 20px 24px;
  border-top: 1px solid #e2e8f0;
}

/* === TOAST === */
#toast-container {
  position: fixed;
  top: 20px;
  right: 20px;
  z-index: 1001;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.toast {
  padding: 16px 24px;
  border-radius: var(--radius);
  color: white;
  font-weight: 600;
  box-shadow: var(--shadow);
  animation: slideIn 0.3s ease;
}

.toast.success { background: var(--color-success); }
.toast.error { background: var(--color-danger); }
.toast.warning { background: var(--color-warning); }

@keyframes slideIn {
  from { transform: translateX(100%); opacity: 0; }
  to { transform: translateX(0); opacity: 1; }
}

/* === FINANZAS === */
.finanzas-cards {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
  margin-bottom: 24px;
}

.finanzas-cards .card {
  text-align: center;
}

.finanzas-cards .monto {
  font-size: var(--font-size-xl);
  font-weight: 700;
}

.finanzas-cards .monto.positivo { color: var(--color-success); }
.finanzas-cards .monto.negativo { color: var(--color-danger); }

.finanzas-table .monto.ingreso { color: var(--color-success); }
.finanzas-table .monto.egreso { color: var(--color-danger); }

/* === TOOLBAR === */
.toolbar {
  display: flex;
  gap: 12px;
  margin-bottom: 20px;
  flex-wrap: wrap;
}

.toolbar input,
.toolbar select {
  padding: 10px 16px;
  border: 2px solid #e2e8f0;
  border-radius: var(--radius);
  font-size: var(--font-size-base);
}

/* === RESPONSIVE === */
@media (max-width: 768px) {
  .sidebar {
    width: 100%;
    height: auto;
    position: relative;
  }
  
  .main-content {
    margin-left: 0;
  }
  
  .cards-grid {
    grid-template-columns: 1fr;
  }
  
  .finanzas-cards {
    grid-template-columns: 1fr;
  }
  
  .main-header {
    flex-direction: column;
    gap: 16px;
    align-items: flex-start;
  }
}

/* === MODO OSCURO === */
@media (prefers-color-scheme: dark) {
  :root {
    --color-bg: #0f172a;
    --color-text: #f1f5f9;
    --color-card: #1e293b;
  }
  
  table {
    background: #1e293b;
  }
  
  th {
    background: #334155;
  }
  
  tr:hover {
    background: #334155;
  }
}
```

---

## TAREA 2: Crear index.html reestructurado

**Archivo**: `dashboard/frontend/index.html`

Reemplazar completamente con el HTML del PLAN MAESTRO v7 (sección 1.2).

Elementos clave que DEBE tener:
- Sidebar con navegación por iconos + texto
- Header con título y botones de acción rápida
- 4 tarjetas de resumen (matters, plazos, alertas, balance)
- Secciones: inicio, matters, documentos, plazos, finanzas, aprobaciones, alertas
- Modal genérico
- Toast container
- Scripts: api.js, finanzas.js, app.js

---

## TAREA 3: Actualizar app.js completo

**Archivo**: `dashboard/frontend/js/app.js`

Reemplazar con funciones:

```javascript
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
    const data = await API.getMatters();
    const matters = data.matters || [];
    
    if (matters.length === 0) {
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
          ${matters.map(m => `
            <tr>
              <td><strong>${m.id}</strong></td>
              <td>${m.nombre}</td>
              <td>${m.cliente || '-'}</td>
              <td>${m.area || '-'}</td>
              <td><span class="badge ${m.estado}">${m.estado}</span></td>
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
    document.getElementById('count-matters').textContent = matters.count || 0;
    
    const plazos = await API.getPlazos();
    document.getElementById('count-plazos').textContent = plazos.count || 0;
    
    const alertas = await API.getAlertas();
    document.getElementById('count-alertas').textContent = alertas.count || 0;
    
    const finanzas = await FinanzasAPI.cargarResumen();
    document.getElementById('count-balance').textContent = 
      '$' + (finanzas.balance || 0).toLocaleString();
  } catch (e) {
    console.error('Error actualizando dashboard:', e);
  }
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
```

---

## TAREA 4: Crear manuales de usuario

### 4.1 MANUAL_ABOGADO_COMPLETO.md

**Archivo**: `docs/MANUAL_ABOGADO_COMPLETO.md`

Contenido mínimo (3000+ palabras):
- Introducción en lenguaje humano
- "Tu primera vez en Willow" — paso a paso con emojis
- Crear caso: 5 pasos numerados
- Generar documento: 3 pasos
- Plazos: qué son, cómo crearlos, qué pasa cuando vencen
- Finanzas: registrar cobro, ver balance
- Aprobaciones: por qué existen, cómo aprobar
- Alertas: qué significan los colores
- "Cuando algo sale mal" — 10 problemas comunes con solución
- Glosario: Matter, Template, Plazo, etc.
- "¿Necesitas ayuda?" — contacto WS Capital

### 4.2 MANUAL_HERMES_INTEGRATION.md

**Archivo**: `docs/MANUAL_HERMES_INTEGRATION.md`

Contenido:
- "Tu asistente en Telegram"
- Lista de comandos con ejemplos reales
- 5 conversaciones de ejemplo (Pablo hablando con Hermes)
- Cómo recibir PDFs
- Cómo configurar alertas automáticas

### 4.3 MANUAL_TECNICO.md

**Archivo**: `docs/MANUAL_TECNICO.md`

Contenido:
- Requisitos: Python 3.9+, Google account
- Instalación paso a paso
- Configuración de credenciales
- Estructura de archivos
- Backup: qué copiar, dónde guardar
- Troubleshooting: 15 problemas técnicos con solución

---

## TAREA 5: Assets

### 5.1 Logo placeholder

Crear `assets/logo-willow.png` — si no hay diseñador, crear SVG inline en HTML:
```html
<div class="logo">
  <svg width="40" height="40" viewBox="0 0 40 40">
    <circle cx="20" cy="20" r="18" fill="#2563eb"/>
    <text x="20" y="26" text-anchor="middle" fill="white" font-size="20" font-weight="bold">W</text>
  </svg>
  <span>Willow Legal</span>
</div>
```

### 5.2 Favicon

Crear `assets/favicon.ico` — usar el mismo SVG convertido.

---

## TAREA 6: Tests de verificación

Ejecutar en terminal:

```bash
cd ~/ws-hermes-legal-pro

# Test 1: CSS existe y tiene tamaño
ls -la dashboard/frontend/css/styles.css

# Test 2: HTML tiene todas las secciones
grep -c "section id=" dashboard/frontend/index.html
# Debe retornar 7

# Test 3: Manuales existen
ls -la docs/MANUAL_ABOGADO_COMPLETO.md
ls -la docs/MANUAL_HERMES_INTEGRATION.md
ls -la docs/MANUAL_TECNICO.md

# Test 4: Abrir en navegador y verificar visualmente:
# - Sidebar con 7 links
# - 4 tarjetas grandes en inicio
# - Botones "Nuevo Caso", "Nuevo Documento"
# - Tabla de casos se renderiza
# - Modal se abre al hacer clic en botón
# - Toast aparece al crear algo

# Test 5: Responsive
# Redimensionar navegador a 768px, verificar que no se rompe
```

---

## GIT

```bash
cd ~/ws-hermes-legal-pro
git add -A
git commit -m "v7: Polish completo + documentación para abogados no-digital"
git push origin master
git log --oneline -3
```

---

## REPORTAR

Pegar output de:
1. `git log --oneline -3`
2. `ls -la dashboard/frontend/css/styles.css`
3. `ls -la docs/MANUAL_*.md`
4. Screenshot descriptivo de cómo se ve el dashboard
