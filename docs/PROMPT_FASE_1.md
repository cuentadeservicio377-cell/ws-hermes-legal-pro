# PROMPT FASE 1 — Fundamentos del Dashboard v3.0
## Para OpenCode Go | Hermes Legal Pro

---

## 🎯 OBJETIVO DE ESTA FASE

Crear la estructura base del frontend que funcione:
1. Cliente HTTP que llama a la API
2. Router que cambia vistas sin recargar
3. Helpers para formatear datos
4. CSS con sistema de diseño Kami v3
5. HTML base con navegación

**NO crear vistas completas todavía.** Solo la infraestructura.

---

## 📁 ESTRUCTURA DEL PROYECTO

Trabajas en:
```
~/ws-hermes-legal-pro/dashboard/frontend/
```

Archivos a crear:
```
dashboard/frontend/
├── index.html          (actualizar)
├── css/
│   └── kami.css        (crear)
└── js/
    ├── api.js          (crear)
    ├── app.js          (crear)
    └── utils.js        (crear)
```

---

## 🔧 PASO 1: Crear `js/api.js`

Este archivo es el cliente HTTP. Todas las llamadas a la API pasan por aquí.

```javascript
// js/api.js — Cliente HTTP para Hermes Legal Pro API

const API_BASE = 'http://localhost:8082';

class API {
    // GET genérico
    static async get(endpoint) {
        const res = await fetch(`${API_BASE}${endpoint}`);
        if (!res.ok) throw new Error(`Error ${res.status}: ${res.statusText}`);
        return res.json();
    }

    // POST genérico
    static async post(endpoint, data) {
        const res = await fetch(`${API_BASE}${endpoint}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        if (!res.ok) {
            const err = await res.json();
            throw new Error(err.detail || `Error ${res.status}`);
        }
        return res.json();
    }

    // PUT genérico
    static async put(endpoint, data) {
        const res = await fetch(`${API_BASE}${endpoint}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        if (!res.ok) throw new Error(`Error ${res.status}`);
        return res.json();
    }

    // DELETE genérico
    static async delete(endpoint) {
        const res = await fetch(`${API_BASE}${endpoint}`, { method: 'DELETE' });
        if (!res.ok) throw new Error(`Error ${res.status}`);
        return res.ok;
    }

    // Endpoints específicos
    static health() { return this.get('/api/health'); }
    static dashboard() { return this.get('/api/dashboard'); }
    static matters() { return this.get('/api/matters'); }
    static matter(id) { return this.get(`/api/matters/${id}`); }
    static createMatter(data) { return this.post('/api/matters', data); }
    static updateMatter(id, data) { return this.put(`/api/matters/${id}`, data); }
    static deleteMatter(id) { return this.delete(`/api/matters/${id}`); }
    static templates() { return this.get('/api/templates'); }
    static generateDoc(matterId, data) { return this.post(`/api/matter/${matterId}/generar-documento`, data); }
    static reuniones() { return this.get('/api/reuniones'); }
    static createReunion(data) { return this.post('/api/reuniones', data); }
    static documentos() { return this.get('/api/documentos'); }
    static alertas() { return this.get('/api/alertas'); }
    static carpetas(matterId) { return this.get(`/api/carpetas/${matterId}`); }
}

window.API = API;
```

**Guardar en:** `~/ws-hermes-legal-pro/dashboard/frontend/js/api.js`

---

## 🔧 PASO 2: Crear `js/utils.js`

Helpers para formatear datos que usa todo el sistema.

```javascript
// js/utils.js — Helpers de formateo

const Utils = {
    // Fecha: "2026-05-15" → "15 de mayo de 2026"
    formatDate(dateStr) {
        if (!dateStr) return 'Sin fecha';
        const d = new Date(dateStr + 'T00:00:00');
        return d.toLocaleDateString('es-MX', { day: 'numeric', month: 'long', year: 'numeric' });
    },

    // Fecha corta: "2026-05-15" → "15 may"
    formatDateShort(dateStr) {
        if (!dateStr) return '—';
        const d = new Date(dateStr + 'T00:00:00');
        return d.toLocaleDateString('es-MX', { day: 'numeric', month: 'short' });
    },

    // Días restantes: calcula desde hoy
    diasRestantes(dateStr) {
        if (!dateStr) return null;
        const hoy = new Date();
        hoy.setHours(0,0,0,0);
        const fecha = new Date(dateStr + 'T00:00:00');
        const diff = Math.floor((fecha - hoy) / (1000 * 60 * 60 * 24));
        return diff;
    },

    // Color según días restantes
    colorUrgencia(dias) {
        if (dias === null) return 'gray';
        if (dias < 0) return 'red';      // Vencido
        if (dias <= 3) return 'red';     // Crítico
        if (dias <= 7) return 'yellow';  // Próximo
        return 'green';                  // Tranquilo
    },

    // Badge HTML según urgencia
    badgeUrgencia(dias) {
        const color = this.colorUrgencia(dias);
        const text = dias === null ? 'SIN PLAZO' : 
                     dias < 0 ? `VENCIDO ${Math.abs(dias)} días` :
                     dias === 0 ? 'HOY' :
                     dias === 1 ? '1 día' :
                     `${dias} días`;
        return `<span class="badge badge-${color}">${text}</span>`;
    },

    // Moneda: 150000 → "$150,000 MXN"
    formatMoney(amount) {
        if (!amount && amount !== 0) return 'Por definir';
        return '$' + amount.toLocaleString('es-MX') + ' MXN';
    },

    // Prioridad: "alta" → "ALTA" con color
    badgePrioridad(p) {
        const map = { alta: 'red', media: 'yellow', baja: 'green' };
        const color = map[p] || 'gray';
        return `<span class="badge badge-${color}">${(p || 'MEDIA').toUpperCase()}</span>`;
    },

    // Estado: "activo" → "ACTIVO"
    badgeEstado(e) {
        const map = { activo: 'green', cerrado: 'gray', urgente: 'red' };
        const color = map[e] || 'gray';
        return `<span class="badge badge-${color}">${(e || 'ACTIVO').toUpperCase()}</span>`;
    },

    // Escapar HTML para evitar XSS
    escape(html) {
        const div = document.createElement('div');
        div.textContent = html;
        return div.innerHTML;
    },

    // Spinner de carga
    spinner() {
        return '<div class="spinner"></div>';
    }
};

window.Utils = Utils;
```

**Guardar en:** `~/ws-hermes-legal-pro/dashboard/frontend/js/utils.js`

---

## 🔧 PASO 3: Crear `css/kami.css`

Sistema de diseño completo. Todos los componentes visuales.

```css
/* css/kami.css — Sistema de Diseño Kami v3 */

:root {
  --ink-blue: #1B365D;
  --corporate-blue: #2F5496;
  --success-green: #548235;
  --warning-yellow: #FFC000;
  --alert-red: #C00000;
  --bg-warm: #faf8f0;
  --bg-white: #ffffff;
  --text-primary: #1a1a18;
  --text-secondary: #5a5a56;
  --border-light: #e0ddd5;
  --shadow: 0 2px 8px rgba(27, 54, 93, 0.12);
  --shadow-hover: 0 4px 16px rgba(27, 54, 93, 0.18);
  --radius: 8px;
  --radius-lg: 12px;
}

* { margin: 0; padding: 0; box-sizing: border-box; }

body {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  background: var(--bg-warm);
  color: var(--text-primary);
  line-height: 1.6;
  font-size: 14px;
}

/* Layout */
.app {
  display: flex;
  min-height: 100vh;
}

/* Sidebar */
.sidebar {
  width: 260px;
  background: var(--ink-blue);
  color: white;
  padding: 24px 16px;
  position: fixed;
  height: 100vh;
  overflow-y: auto;
}

.logo { display: flex; align-items: center; gap: 12px; margin-bottom: 32px; }
.logo-icon {
  width: 40px; height: 40px; background: var(--warning-yellow);
  border-radius: 10px; display: flex; align-items: center; justify-content: center;
  font-size: 20px;
}

.nav-section { margin-bottom: 24px; }
.nav-label {
  font-size: 10px; text-transform: uppercase; letter-spacing: 1.5px;
  opacity: 0.5; margin-bottom: 8px; padding-left: 12px;
}

.nav-item {
  display: flex; align-items: center; gap: 12px;
  padding: 10px 12px; border-radius: var(--radius);
  cursor: pointer; transition: all 0.2s; font-size: 14px;
  margin-bottom: 2px;
}

.nav-item:hover { background: rgba(255,255,255,0.08); }
.nav-item.active { background: var(--corporate-blue); }
.nav-badge {
  margin-left: auto; background: var(--alert-red);
  color: white; font-size: 10px; padding: 2px 6px;
  border-radius: 10px; font-weight: 600;
}

/* Main Content */
.main {
  margin-left: 260px;
  padding: 24px 32px;
  min-height: 100vh;
  width: calc(100% - 260px);
}

.header {
  display: flex; justify-content: space-between; align-items: center;
  margin-bottom: 24px;
}

.header h1 { font-size: 24px; font-weight: 700; color: var(--ink-blue); }

/* Botones */
.btn {
  padding: 10px 20px; border-radius: var(--radius); border: none;
  cursor: pointer; font-size: 14px; font-weight: 600;
  transition: all 0.2s; display: inline-flex; align-items: center; gap: 8px;
}

.btn-primary {
  background: var(--ink-blue); color: white;
}
.btn-primary:hover {
  background: var(--corporate-blue); transform: translateY(-1px);
  box-shadow: var(--shadow-hover);
}

.btn-secondary {
  background: white; color: var(--ink-blue); border: 1px solid var(--border-light);
}
.btn-secondary:hover { background: var(--bg-warm); }

.btn-danger {
  background: var(--alert-red); color: white;
}

.btn-sm { padding: 6px 12px; font-size: 12px; }

/* Cards */
.card {
  background: white; border-radius: var(--radius-lg);
  padding: 20px; box-shadow: var(--shadow);
  margin-bottom: 16px;
}

.card-header {
  display: flex; justify-content: space-between; align-items: center;
  margin-bottom: 16px;
}

.card-title { font-size: 16px; font-weight: 700; color: var(--ink-blue); }

/* KPI Grid */
.kpi-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 16px; margin-bottom: 24px;
}

.kpi-card {
  background: white; border-radius: var(--radius-lg);
  padding: 20px; box-shadow: var(--shadow);
  text-align: center;
}

.kpi-value {
  font-size: 32px; font-weight: 700; color: var(--ink-blue);
}

.kpi-label {
  font-size: 12px; color: var(--text-secondary);
  text-transform: uppercase; letter-spacing: 0.5px;
}

/* Badges */
.badge {
  display: inline-flex; align-items: center; gap: 6px;
  padding: 4px 12px; border-radius: 12px;
  font-size: 11px; font-weight: 600; text-transform: uppercase;
}

.badge-red { background: #fff5f5; color: var(--alert-red); }
.badge-yellow { background: #fffbeb; color: #92400e; }
.badge-green { background: #f0fdf4; color: var(--success-green); }
.badge-gray { background: #f3f4f6; color: var(--text-secondary); }
.badge-blue { background: #eff6ff; color: var(--corporate-blue); }

/* Tablas */
.table-container { overflow-x: auto; }

.data-table {
  width: 100%; border-collapse: collapse;
}

.data-table th {
  background: var(--ink-blue); color: white;
  padding: 12px; text-align: left; font-size: 12px;
  text-transform: uppercase; letter-spacing: 0.5px;
}

.data-table td {
  padding: 12px; border-bottom: 1px solid var(--border-light);
}

.data-table tr:hover { background: var(--bg-warm); }

/* Forms */
.form-group { margin-bottom: 16px; }

.form-label {
  display: block; font-size: 12px; font-weight: 600;
  color: var(--text-secondary); margin-bottom: 6px;
  text-transform: uppercase; letter-spacing: 0.5px;
}

.form-input, .form-select, .form-textarea {
  width: 100%; padding: 10px 12px;
  border: 1px solid var(--border-light); border-radius: var(--radius);
  font-size: 14px; font-family: inherit;
  transition: border-color 0.2s;
}

.form-input:focus, .form-select:focus, .form-textarea:focus {
  outline: none; border-color: var(--corporate-blue);
  box-shadow: 0 0 0 3px rgba(47, 84, 150, 0.1);
}

.form-textarea { min-height: 100px; resize: vertical; }

/* Modal */
.modal-overlay {
  position: fixed; top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(0,0,0,0.5); display: flex;
  align-items: center; justify-content: center; z-index: 1000;
}

.modal {
  background: white; border-radius: var(--radius-lg);
  padding: 24px; width: 90%; max-width: 600px;
  max-height: 90vh; overflow-y: auto;
  box-shadow: 0 20px 60px rgba(0,0,0,0.3);
}

.modal-header {
  display: flex; justify-content: space-between; align-items: center;
  margin-bottom: 20px;
}

.modal-title { font-size: 20px; font-weight: 700; color: var(--ink-blue); }

.modal-close {
  background: none; border: none; font-size: 24px; cursor: pointer;
  color: var(--text-secondary);
}

.modal-close:hover { color: var(--text-primary); }

.modal-footer {
  display: flex; justify-content: flex-end; gap: 12px;
  margin-top: 20px; padding-top: 20px;
  border-top: 1px solid var(--border-light);
}

/* Spinner */
.spinner {
  width: 40px; height: 40px;
  border: 3px solid var(--border-light);
  border-top-color: var(--ink-blue);
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin { to { transform: rotate(360deg); } }

/* Alertas */
.alert {
  padding: 12px 16px; border-radius: var(--radius);
  margin-bottom: 16px; display: flex; align-items: center; gap: 12px;
}

.alert-red { background: #fff5f5; border-left: 4px solid var(--alert-red); }
.alert-yellow { background: #fffbeb; border-left: 4px solid var(--warning-yellow); }
.alert-green { background: #f0fdf4; border-left: 4px solid var(--success-green); }

/* Grid layouts */
.grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
.grid-3 { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 20px; }

/* Utilidades */
.text-right { text-align: right; }
.text-center { text-align: center; }
.mb-0 { margin-bottom: 0; }
.mb-1 { margin-bottom: 8px; }
.mb-2 { margin-bottom: 16px; }
.mb-3 { margin-bottom: 24px; }
.hidden { display: none !important; }
```

**Guardar en:** `~/ws-hermes-legal-pro/dashboard/frontend/css/kami.css`

---

## 🔧 PASO 4: Crear `js/app.js`

Router simple. Cambia vistas sin recargar la página.

```javascript
// js/app.js — Router y estado global

const App = {
    // Estado global
    state: {
        currentView: 'dashboard',
        matters: [],
        templates: [],
        loading: false
    },

    // Inicializar
    async init() {
        console.log('🏛️ Hermes Legal Pro v3.0 iniciando...');
        
        // Verificar API
        try {
            const health = await API.health();
            console.log('✅ API conectada:', health);
        } catch (err) {
            console.error('❌ API no disponible:', err);
            this.showError('No se puede conectar al servidor. ¿Está corriendo el backend?');
            return;
        }

        // Cargar datos base
        await this.loadBaseData();

        // Setup navegación
        this.setupNavigation();

        // Mostrar vista inicial
        this.navigate('dashboard');
    },

    // Cargar datos que necesitan todas las vistas
    async loadBaseData() {
        try {
            const [templates] = await Promise.all([
                API.templates()
            ]);
            this.state.templates = templates.templates || [];
        } catch (err) {
            console.error('Error cargando datos base:', err);
        }
    },

    // Setup clicks en navegación
    setupNavigation() {
        document.querySelectorAll('.nav-item').forEach(item => {
            item.addEventListener('click', (e) => {
                e.preventDefault();
                const view = item.dataset.view;
                if (view) this.navigate(view);
            });
        });
    },

    // Cambiar vista
    navigate(view) {
        console.log('Navegando a:', view);
        
        // Actualizar estado
        this.state.currentView = view;

        // Actualizar navegación activa
        document.querySelectorAll('.nav-item').forEach(item => {
            item.classList.toggle('active', item.dataset.view === view);
        });

        // Ocultar todas las vistas
        document.querySelectorAll('.view').forEach(v => v.classList.add('hidden'));

        // Mostrar vista seleccionada
        const target = document.getElementById(`view-${view}`);
        if (target) {
            target.classList.remove('hidden');
        } else {
            console.error('Vista no encontrada:', view);
            return;
        }

        // Cargar contenido de la vista
        this.loadView(view);
    },

    // Cargar contenido según vista
    async loadView(view) {
        this.setLoading(true);
        
        try {
            switch(view) {
                case 'dashboard':
                    await this.loadDashboard();
                    break;
                case 'matters':
                    await this.loadMatters();
                    break;
                case 'reuniones':
                    await this.loadReuniones();
                    break;
                case 'documentos':
                    await this.loadDocumentos();
                    break;
                case 'calendario':
                    await this.loadCalendario();
                    break;
                default:
                    console.error('Vista desconocida:', view);
            }
        } catch (err) {
            console.error('Error cargando vista:', err);
            this.showError(`Error cargando ${view}: ${err.message}`);
        } finally {
            this.setLoading(false);
        }
    },

    // Placeholders para vistas (se implementan en fases siguientes)
    async loadDashboard() {
        const container = document.getElementById('view-dashboard');
        container.innerHTML = `
            <div class="header">
                <h1>Dashboard</h1>
                <button class="btn btn-primary" onclick="App.navigate('matters')">+ Nuevo Matter</button>
            </div>
            <div id="dashboard-content">
                <div class="spinner"></div>
                <p class="text-center">Cargando dashboard...</p>
            </div>
        `;
        
        // Aquí irá el contenido real en FASE 2
        // Por ahora mostramos que la infraestructura funciona
        setTimeout(() => {
            document.getElementById('dashboard-content').innerHTML = `
                <div class="alert alert-green">
                    ✅ Infraestructura lista. Esperando FASE 2 para datos reales.
                </div>
                <div class="kpi-grid">
                    <div class="kpi-card">
                        <div class="kpi-value">—</div>
                        <div class="kpi-label">Matters Activos</div>
                    </div>
                    <div class="kpi-card">
                        <div class="kpi-value">—</div>
                        <div class="kpi-label">Documentos Pendientes</div>
                    </div>
                </div>
            `;
        }, 500);
    },

    async loadMatters() {
        const container = document.getElementById('view-matters');
        container.innerHTML = `
            <div class="header">
                <h1>Matters</h1>
                <button class="btn btn-primary" onclick="App.showModal('matter-form')">+ Nuevo Matter</button>
            </div>
            <div class="alert alert-yellow">
                🏗️ Vista en construcción. Se implementará en FASE 3.
            </div>
        `;
    },

    async loadReuniones() {
        const container = document.getElementById('view-reuniones');
        container.innerHTML = `
            <div class="header"><h1>Reuniones</h1></div>
            <div class="alert alert-yellow">🏗️ Vista en construcción. FASE 4.</div>
        `;
    },

    async loadDocumentos() {
        const container = document.getElementById('view-documentos');
        container.innerHTML = `
            <div class="header"><h1>Documentos</h1></div>
            <div class="alert alert-yellow">🏗️ Vista en construcción. FASE 5.</div>
        `;
    },

    async loadCalendario() {
        const container = document.getElementById('view-calendario');
        container.innerHTML = `
            <div class="header"><h1>Calendario</h1></div>
            <div class="alert alert-yellow">🏗️ Vista en construcción. FASE 6.</div>
        `;
    },

    // Modal
    showModal(id) {
        const modal = document.getElementById(id);
        if (modal) modal.classList.remove('hidden');
    },

    hideModal(id) {
        const modal = document.getElementById(id);
        if (modal) modal.classList.add('hidden');
    },

    // Loading
    setLoading(loading) {
        this.state.loading = loading;
        document.body.classList.toggle('loading', loading);
    },

    // Error
    showError(message) {
        const container = document.getElementById('main-content') || document.body;
        const alert = document.createElement('div');
        alert.className = 'alert alert-red';
        alert.innerHTML = `<strong>Error:</strong> ${message}`;
        container.insertBefore(alert, container.firstChild);
        
        setTimeout(() => alert.remove(), 5000);
    }
};

// Inicializar cuando carga la página
document.addEventListener('DOMContentLoaded', () => App.init());

window.App = App;
```

**Guardar en:** `~/ws-hermes-legal-pro/dashboard/frontend/js/app.js`

---

## 🔧 PASO 5: Actualizar `index.html`

Estructura base SPA. Carga todos los JS y CSS.

```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hermes Legal Pro v3.0</title>
    <link rel="stylesheet" href="css/kami.css">
</head>
<body>
    <div class="app">
        <!-- Sidebar -->
        <nav class="sidebar">
            <div class="logo">
                <div class="logo-icon">⚖️</div>
                <div class="logo-text">
                    <h1>Hermes Legal</h1>
                    <span>Pro v3.0</span>
                </div>
            </div>

            <div class="nav-section">
                <div class="nav-label">Principal</div>
                <div class="nav-item active" data-view="dashboard">
                    <span>📊</span> Dashboard
                </div>
                <div class="nav-item" data-view="matters">
                    <span>📁</span> Matters
                </div>
                <div class="nav-item" data-view="reuniones">
                    <span>🎤</span> Reuniones
                </div>
                <div class="nav-item" data-view="documentos">
                    <span>📄</span> Documentos
                </div>
                <div class="nav-item" data-view="calendario">
                    <span>📅</span> Calendario
                </div>
            </div>

            <div class="nav-section">
                <div class="nav-label">Sistema</div>
                <div class="nav-item" onclick="location.reload()">
                    <span>🔄</span> Recargar
                </div>
            </div>
        </nav>

        <!-- Main Content -->
        <main class="main" id="main-content">
            <!-- Vistas (inicialmente ocultas excepto dashboard) -->
            <div id="view-dashboard" class="view"></div>
            <div id="view-matters" class="view hidden"></div>
            <div id="view-reuniones" class="view hidden"></div>
            <div id="view-documentos" class="view hidden"></div>
            <div id="view-calendario" class="view hidden"></div>
        </main>
    </div>

    <!-- Scripts -->
    <script src="js/api.js"></script>
    <script src="js/utils.js"></script>
    <script src="js/app.js"></script>
</body>
</html>
```

**Guardar en:** `~/ws-hermes-legal-pro/dashboard/frontend/index.html`

---

## 🧪 TESTS DE ESTA FASE

### Test 1: Archivos creados
```bash
ls -la ~/ws-hermes-legal-pro/dashboard/frontend/js/
ls -la ~/ws-hermes-legal-pro/dashboard/frontend/css/
```
**Esperado:** api.js, utils.js, app.js, kami.css

### Test 2: Backend corriendo
```bash
cd ~/ws-hermes-legal-pro/dashboard/backend
python3 app.py &
```
**Esperado:** Servidor en puerto 8082

### Test 3: Dashboard carga
```bash
open http://localhost:8082
```
**Esperado:** Ver sidebar azul, navegación, "Dashboard" como título

### Test 4: Consola sin errores
```
Cmd+Option+J (Chrome) → Consola
```
**Esperado:** Ningún error rojo. Mensaje: "🏛️ Hermes Legal Pro v3.0 iniciando..."

### Test 5: Navegación funciona
```
Click en "Matters" → Cambia título a "Matters"
Click en "Reuniones" → Cambia título a "Reuniones"
Click en "Dashboard" → Vuelve a "Dashboard"
```

### Test 6: API conectada
```
En consola del navegador:
> await API.health()
```
**Esperado:** `{status: "ok", version: "2.0.0", ...}`

---

## ✅ CHECKLIST PARA PASAR A FASE 2

- [ ] `api.js` creado y funciona
- [ ] `utils.js` creado y funciona
- [ ] `app.js` creado y funciona
- [ ] `kami.css` creado y se ve bien
- [ ] `index.html` actualizado
- [ ] Dashboard carga sin errores
- [ ] Navegación entre vistas funciona
- [ ] API responde desde el navegador
- [ ] Diseño se ve profesional (colores, tipografía)

---

## 📤 ENTREGA

Cuando termines:
1. Corre todos los tests arriba
2. Si pasan todos → haz commit
3. Si falla alguno → corrige antes de continuar

**Commit:**
```bash
cd ~/ws-hermes-legal-pro
git add dashboard/frontend/
git commit -m "FASE 1: Fundamentos - API client, router, CSS, HTML base"
git push origin master
```

**Notificar:** "FASE 1 completada. Todos los tests pasaron. Listo para FASE 2."

---

*Prompt FASE 1 — Diseñado para OpenCode Go*
*Hermes Legal Pro v3.0*
