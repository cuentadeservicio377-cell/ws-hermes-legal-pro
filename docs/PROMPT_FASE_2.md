# PROMPT FASE 2 — Dashboard Vivo con Datos Reales
## Para OpenCode Go | Hermes Legal Pro v3.0

---

## 🎯 OBJETIVO DE ESTA FASE

Hacer que el Dashboard muestre **datos reales** de la API:
- KPIs con números reales (matters activos, urgentes, reuniones hoy, docs pendientes, alertas)
- Próximos plazos con colores de urgencia
- Reuniones recientes
- Alertas activas
- Todo debe cargar automáticamente al abrir la página

**NO crear vistas completas de Matters/Reuniones/Documentos/Calendario todavía.** Solo el Dashboard.

---

## 📁 ARCHIVOS A MODIFICAR

Trabajas en:
```
~/ws-hermes-legal-pro/dashboard/frontend/
```

Archivos a modificar:
```
dashboard/frontend/
├── js/
│   ├── app.js          (MODIFICAR — reemplazar loadDashboard placeholder)
│   └── dashboard.js     (CREAR — toda la lógica del dashboard)
└── css/
    └── kami.css        (AGREGAR al final — estilos de dashboard)
```

---

## 🔧 PASO 1: Crear `js/dashboard.js`

Este archivo tiene TODA la lógica del dashboard. Carga datos, renderiza KPIs, plazos, reuniones, alertas.

```javascript
// js/dashboard.js — Dashboard con datos reales

const Dashboard = {
    // Cargar y renderizar todo el dashboard
    async render() {
        const container = document.getElementById('view-dashboard');
        
        // Mostrar spinner mientras carga
        container.innerHTML = `
            <div class="header">
                <h1>Dashboard</h1>
                <button class="btn btn-primary" onclick="App.navigate('matters')">+ Nuevo Matter</button>
            </div>
            <div id="dashboard-loading" class="text-center" style="padding: 60px;">
                <div class="spinner"></div>
                <p style="margin-top: 16px; color: var(--text-secondary);">Cargando datos del despacho...</p>
            </div>
        `;

        try {
            // Llamar a la API
            const data = await API.dashboard();
            
            // Ocultar spinner
            const loading = document.getElementById('dashboard-loading');
            if (loading) loading.remove();

            // Renderizar contenido
            container.innerHTML = `
                <div class="header">
                    <h1>Dashboard</h1>
                    <div style="display: flex; gap: 12px;">
                        <button class="btn btn-secondary" onclick="Dashboard.refresh()">🔄 Actualizar</button>
                        <button class="btn btn-primary" onclick="App.navigate('matters')">+ Nuevo Matter</button>
                    </div>
                </div>
                
                ${this.renderKPIs(data.kpis)}
                
                <div class="grid-2" style="margin-top: 24px;">
                    ${this.renderPlazos(data.proximos_plazos)}
                    ${this.renderReuniones(data.reuniones_recientes)}
                </div>
                
                ${this.renderAlertas(data.alertas)}
            `;

        } catch (err) {
            console.error('Error cargando dashboard:', err);
            container.innerHTML = `
                <div class="header">
                    <h1>Dashboard</h1>
                </div>
                <div class="alert alert-red">
                    <strong>Error al cargar datos:</strong> ${err.message}<br>
                    <small>Verifica que el backend esté corriendo en puerto 8082</small>
                </div>
                <button class="btn btn-primary" onclick="Dashboard.render()">Reintentar</button>
            `;
        }
    },

    // Renderizar KPIs
    renderKPIs(kpis) {
        if (!kpis) return '<div class="alert alert-yellow">No hay datos de KPIs disponibles</div>';
        
        return `
            <div class="kpi-grid">
                <div class="kpi-card" onclick="App.navigate('matters')" style="cursor: pointer;">
                    <div class="kpi-value" style="color: var(--ink-blue);">${kpis.matters_activos || 0}</div>
                    <div class="kpi-label">Matters Activos</div>
                </div>
                <div class="kpi-card" onclick="App.navigate('matters')" style="cursor: pointer;">
                    <div class="kpi-value" style="color: var(--alert-red);">${kpis.matters_urgentes || 0}</div>
                    <div class="kpi-label">Urgentes</div>
                </div>
                <div class="kpi-card" onclick="App.navigate('reuniones')" style="cursor: pointer;">
                    <div class="kpi-value" style="color: var(--corporate-blue);">${kpis.reuniones_hoy || 0}</div>
                    <div class="kpi-label">Reuniones Hoy</div>
                </div>
                <div class="kpi-card" onclick="App.navigate('documentos')" style="cursor: pointer;">
                    <div class="kpi-value" style="color: var(--warning-yellow);">${kpis.documentos_pendientes || 0}</div>
                    <div class="kpi-label">Docs Pendientes</div>
                </div>
                <div class="kpi-card" style="cursor: pointer;">
                    <div class="kpi-value" style="color: var(--success-green);">${kpis.alertas_activas || 0}</div>
                    <div class="kpi-label">Alertas Activas</div>
                </div>
            </div>
        `;
    },

    // Renderizar próximos plazos
    renderPlazos(plazos) {
        if (!plazos || plazos.length === 0) {
            return `
                <div class="card">
                    <div class="card-header">
                        <div class="card-title">📅 Próximos Plazos</div>
                    </div>
                    <p style="color: var(--text-secondary); padding: 20px;">
                        No hay plazos próximos (7 días). ¡Buen trabajo!
                    </p>
                </div>
            `;
        }

        const rows = plazos.map(p => {
            const dias = p.dias_restantes;
            const color = dias < 0 ? 'red' : dias <= 3 ? 'red' : dias <= 7 ? 'yellow' : 'green';
            const texto = dias < 0 ? `VENCIDO ${Math.abs(dias)} días` : 
                         dias === 0 ? 'HOY' : 
                         dias === 1 ? '1 día' : 
                         `${dias} días`;
            
            return `
                <div class="plazo-item plazo-${color}" onclick="App.navigate('matters')" style="cursor: pointer;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <strong>${Utils.escape(p.cliente || 'Sin cliente')}</strong>
                            <span class="badge badge-${color}" style="margin-left: 8px;">${texto}</span>
                        </div>
                        <div style="font-size: 12px; color: var(--text-secondary);">
                            ${p.matter_id || ''}
                        </div>
                    </div>
                    <div style="font-size: 13px; color: var(--text-secondary); margin-top: 4px;">
                        ${Utils.escape(p.descripcion || 'Sin descripción')}
                    </div>
                    <div style="font-size: 12px; color: var(--text-secondary); margin-top: 2px;">
                        Deadline: ${Utils.formatDate(p.deadline)}
                    </div>
                </div>
            `;
        }).join('');

        return `
            <div class="card">
                <div class="card-header">
                    <div class="card-title">📅 Próximos Plazos</div>
                    <span class="badge badge-${plazos.some(p => p.dias_restantes < 0) ? 'red' : 'yellow'}">
                        ${plazos.length} plazo${plazos.length !== 1 ? 's' : ''}
                    </span>
                </div>
                <div class="plazos-list">
                    ${rows}
                </div>
            </div>
        `;
    },

    // Renderizar reuniones recientes
    renderReuniones(reuniones) {
        if (!reuniones || reuniones.length === 0) {
            return `
                <div class="card">
                    <div class="card-header">
                        <div class="card-title">🎤 Reuniones Recientes</div>
                    </div>
                    <p style="color: var(--text-secondary); padding: 20px;">
                        No hay reuniones registradas. 
                        <a href="#" onclick="App.navigate('reuniones'); return false;" style="color: var(--corporate-blue);">
                            Registrar primera reunión →
                        </a>
                    </p>
                </div>
            `;
        }

        const rows = reuniones.slice(0, 5).map(r => {
            const docsCount = r.documentos_necesarios ? r.documentos_necesarios.length : 0;
            const estadoBadge = r.estado === 'procesada' 
                ? '<span class="badge badge-green">✓ Procesada</span>' 
                : '<span class="badge badge-yellow">⏳ Pendiente</span>';
            
            return `
                <div class="reunion-item" onclick="App.navigate('reuniones')" style="cursor: pointer;">
                    <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                        <div>
                            <strong>${Utils.escape(r.cliente || 'Sin cliente')}</strong>
                            ${estadoBadge}
                        </div>
                        <div style="font-size: 12px; color: var(--text-secondary);">
                            ${Utils.formatDateShort(r.fecha)}
                        </div>
                    </div>
                    <div style="font-size: 13px; color: var(--text-secondary); margin-top: 4px; line-height: 1.4;">
                        ${r.resumen ? Utils.escape(r.resumen.substring(0, 100)) + '...' : 'Sin resumen'}
                    </div>
                    ${docsCount > 0 ? `
                        <div style="font-size: 12px; color: var(--corporate-blue); margin-top: 6px;">
                            📄 ${docsCount} documento${docsCount !== 1 ? 's' : ''} sugerido${docsCount !== 1 ? 's' : ''}
                        </div>
                    ` : ''}
                </div>
            `;
        }).join('');

        return `
            <div class="card">
                <div class="card-header">
                    <div class="card-title">🎤 Reuniones Recientes</div>
                    <a href="#" onclick="App.navigate('reuniones'); return false;" style="font-size: 13px; color: var(--corporate-blue);">
                        Ver todas →
                    </a>
                </div>
                <div class="reuniones-list">
                    ${rows}
                </div>
            </div>
        `;
    },

    // Renderizar alertas
    renderAlertas(alertas) {
        if (!alertas || alertas.length === 0) {
            return ''; // No mostrar sección si no hay alertas
        }

        const rows = alertas.slice(0, 3).map(a => {
            const tipo = a.tipo || 'general';
            const icono = tipo === 'plazo' ? '⏰' : tipo === 'documento' ? '📄' : '⚠️';
            const color = a.urgencia === 'critical' ? 'red' : a.urgencia === 'high' ? 'yellow' : 'blue';
            
            return `
                <div class="alerta-item alerta-${color}">
                    <div style="display: flex; gap: 12px; align-items: flex-start;">
                        <div style="font-size: 20px;">${icono}</div>
                        <div style="flex: 1;">
                            <div style="font-weight: 600; margin-bottom: 2px;">
                                ${Utils.escape(a.titulo || 'Alerta')}
                            </div>
                            <div style="font-size: 13px; color: var(--text-secondary);">
                                ${Utils.escape(a.mensaje || '')}
                            </div>
                            ${a.matter_id ? `
                                <div style="font-size: 12px; color: var(--corporate-blue); margin-top: 4px;">
                                    Matter: ${a.matter_id}
                                </div>
                            ` : ''}
                        </div>
                    </div>
                </div>
            `;
        }).join('');

        return `
            <div style="margin-top: 24px;">
                <div class="card">
                    <div class="card-header">
                        <div class="card-title">🔔 Alertas Activas</div>
                        <span class="badge badge-red">${alertas.length}</span>
                    </div>
                    ${rows}
                </div>
            </div>
        `;
    },

    // Refrescar dashboard
    async refresh() {
        console.log('Refrescando dashboard...');
        await this.render();
    }
};

window.Dashboard = Dashboard;
```

**Guardar en:** `~/ws-hermes-legal-pro/dashboard/frontend/js/dashboard.js`

---

## 🔧 PASO 2: Modificar `js/app.js`

Reemplazar la función `loadDashboard()` placeholder por la real.

Busca esta sección en `app.js`:
```javascript
async loadDashboard() {
    const container = document.getElementById('view-dashboard');
    container.innerHTML = `
        <div class="header">...` // TODO ESTO ES PLACEHOLDER
```

**Reemplazarla COMPLETAMENTE por:**

```javascript
async loadDashboard() {
    await Dashboard.render();
}
```

Es decir, la función `loadDashboard()` completa debe quedar así:

```javascript
async loadDashboard() {
    await Dashboard.render();
}
```

Nada más. Todo el renderizado ahora vive en `dashboard.js`.

---

## 🔧 PASO 3: Agregar CSS al final de `css/kami.css`

Agregar al final del archivo (después de todo lo existente):

```css
/* ===== DASHBOARD SPECIFIC ===== */

.plazos-list,
.reuniones-list {
    display: flex;
    flex-direction: column;
    gap: 12px;
}

.plazo-item,
.reunion-item {
    padding: 14px;
    border-radius: var(--radius);
    background: var(--bg-warm);
    border-left: 4px solid var(--border-light);
    transition: all 0.2s;
}

.plazo-item:hover,
.reunion-item:hover {
    transform: translateX(4px);
    box-shadow: var(--shadow);
}

.plazo-red { border-left-color: var(--alert-red); background: #fff5f5; }
.plazo-yellow { border-left-color: var(--warning-yellow); background: #fffbeb; }
.plazo-green { border-left-color: var(--success-green); background: #f0fdf4; }

.reunion-item { border-left-color: var(--corporate-blue); }

.alerta-item {
    padding: 14px;
    border-radius: var(--radius);
    margin-bottom: 8px;
    background: var(--bg-warm);
}

.alerta-red { border-left: 4px solid var(--alert-red); background: #fff5f5; }
.alerta-yellow { border-left: 4px solid var(--warning-yellow); background: #fffbeb; }
.alerta-blue { border-left: 4px solid var(--corporate-blue); background: #eff6ff; }

/* Loading states */
.loading .main {
    opacity: 0.6;
    pointer-events: none;
}

/* Animaciones suaves */
.view {
    animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}

/* Responsive */
@media (max-width: 1024px) {
    .grid-2 { grid-template-columns: 1fr; }
    .grid-3 { grid-template-columns: 1fr; }
    .kpi-grid { grid-template-columns: repeat(2, 1fr); }
}

@media (max-width: 768px) {
    .sidebar { width: 200px; }
    .main { margin-left: 200px; width: calc(100% - 200px); padding: 16px; }
    .kpi-grid { grid-template-columns: 1fr; }
}
```

**Agregar al final de:** `~/ws-hermes-legal-pro/dashboard/frontend/css/kami.css`

---

## 🔧 PASO 4: Actualizar `index.html` para cargar dashboard.js

Busca esta línea en `index.html`:
```html
<script src="js/app.js"></script>
```

**Agregar ANTES de esa línea:**
```html
<script src="js/dashboard.js"></script>
```

Es decir, el bloque de scripts debe quedar:
```html
<script src="js/api.js"></script>
<script src="js/utils.js"></script>
<script src="js/dashboard.js"></script>
<script src="js/app.js"></script>
```

---

## 🧪 TESTS DE ESTA FASE

### Preparación
```bash
# Terminal 1: Backend
cd ~/ws-hermes-legal-pro/dashboard/backend
python3 app.py &

# Verificar que hay datos
ls ~/ws-hermes-legal-pro/datos/
cat ~/ws-hermes-legal-pro/datos/matters.json | head -50
```

### Test 1: Dashboard carga con datos reales
```bash
open http://localhost:8082
```
**Esperado:** Ver números reales en KPIs (no "—" ni 0 forzado)

### Test 2: KPIs son clickeables
```
Click en "Matters Activos" → Navega a vista Matters
Click en "Urgentes" → Navega a vista Matters
Click en "Reuniones Hoy" → Navega a vista Reuniones
```

### Test 3: Plazos muestran colores correctos
```
Si hay plazo vencido → Debe verse en rojo con "VENCIDO X días"
Si hay plazo en 3 días → Debe verse en rojo
Si hay plazo en 5 días → Debe verse en amarillo
Si hay plazo en 15 días → Debe verse en verde
```

### Test 4: Reuniones muestran resumen
```
Ver reuniones recientes
Debe mostrar: cliente, fecha, estado (Procesada/Pendiente), resumen corto
Si tiene documentos sugeridos → mostrar "X documentos sugeridos"
```

### Test 5: Alertas se muestran si existen
```
Si hay alertas en datos/alertas.json → Deben aparecer en sección "Alertas Activas"
Si no hay alertas → La sección no debe aparecer (oculta)
```

### Test 6: Botón "Actualizar" funciona
```
Click en "🔄 Actualizar"
Debe recargar datos sin recargar la página
Spinner aparece brevemente
```

### Test 7: Sin errores en consola
```
Cmd+Option+J (Chrome)
No debe haber errores rojos
Solo mensajes informativos
```

---

## ✅ CHECKLIST PARA PASAR A FASE 3

- [ ] `dashboard.js` creado y funciona
- [ ] `app.js` modificado (loadDashboard llama a Dashboard.render)
- [ ] CSS de dashboard agregado al final de kami.css
- [ ] index.html carga dashboard.js
- [ ] Dashboard muestra KPIs con números reales
- [ ] Plazos muestran colores según urgencia
- [ ] Reuniones muestran datos reales
- [ ] Alertas aparecen solo si existen
- [ ] Botón "Actualizar" recarga datos
- [ ] Sin errores en consola
- [ ] Diseño responsive (se ve bien al achicar ventana)

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
git commit -m "FASE 2: Dashboard vivo con datos reales - KPIs, plazos, reuniones, alertas"
git push origin master
```

**Notificar:** "FASE 2 completada. Dashboard muestra datos reales. Listo para FASE 3 (Matters CRUD)."

---

*Prompt FASE 2 — Diseñado para OpenCode Go*
*Hermes Legal Pro v3.0*
