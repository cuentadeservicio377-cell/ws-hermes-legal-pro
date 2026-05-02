# PROMPT FASE 6 — Calendario (Vista semanal/mensual, plazos, reuniones)
## Para OpenCode Go | Hermes Legal Pro v3.0

---

## 🎯 OBJETIVO DE ESTA FASE

Crear la vista de Calendario completa:
- **Vista mensual**: grid tipo calendario con días, navegación mes anterior/siguiente
- **Vista semanal**: lista de eventos de la semana actual
- **Eventos**: plazos (🔴), reuniones (🔵), audiencias (🟡), vencimientos (🟠)
- **Click en día**: ver lista de eventos de ese día
- **Click en evento**: navegar al matter o reunión relacionada
- **Indicadores hoy**: resaltar día actual
- **Resumen sidebar**: próximos 5 eventos, plazos urgentes

---

## 📁 ARCHIVOS A CREAR/MODIFICAR

```
dashboard/frontend/
├── js/
│   ├── app.js          (MODIFICAR — agregar loadCalendario real)
│   └── calendario.js   (CREAR — toda la lógica del calendario)
└── css/
    └── kami.css        (AGREGAR al final — estilos de calendario)
```

---

## 🔧 PASO 1: Crear `js/calendario.js`

```javascript
// js/calendario.js — Calendario: mensual, semanal, eventos, plazos

const Calendario = {
    currentDate: new Date(),
    viewMode: 'month', // 'month' | 'week'
    events: [],
    matters: [],
    reuniones: [],

    // Renderizar vista completa
    async render() {
        const container = document.getElementById('view-calendario');
        
        container.innerHTML = `
            <div class="header">
                <h1>Calendario</h1>
                <div style="display: flex; gap: 8px;">
                    <button class="btn btn-secondary" onclick="Calendario.prev()">←</button>
                    <button class="btn btn-secondary" onclick="Calendario.today()">Hoy</button>
                    <button class="btn btn-secondary" onclick="Calendario.next()">→</button>
                    <button class="btn btn-sm ${this.viewMode === 'month' ? 'btn-primary' : 'btn-secondary'}" 
                            onclick="Calendario.setView('month')">Mensual</button>
                    <button class="btn btn-sm ${this.viewMode === 'week' ? 'btn-primary' : 'btn-secondary'}" 
                            onclick="Calendario.setView('week')">Semanal</button>
                </div>
            </div>
            <div id="calendario-content">
                <div class="text-center" style="padding: 60px;">
                    <div class="spinner"></div>
                    <p style="margin-top: 16px; color: var(--text-secondary);">Cargando calendario...</p>
                </div>
            </div>
        `;

        try {
            const [mattersData, reunionesData] = await Promise.all([
                API.matters(),
                API.reuniones()
            ]);

            this.matters = mattersData || [];
            this.reuniones = reunionesData || [];
            
            // Construir lista de eventos unificada
            this.buildEvents();
            
            if (this.viewMode === 'month') {
                this.renderMonth();
            } else {
                this.renderWeek();
            }

        } catch (err) {
            console.error('Error cargando calendario:', err);
            document.getElementById('calendario-content').innerHTML = `
                <div class="alert alert-red">
                    <strong>Error al cargar calendario:</strong> ${err.message}
                </div>
                <button class="btn btn-primary" onclick="Calendario.render()">Reintentar</button>
            `;
        }
    },

    buildEvents() {
        this.events = [];

        // Plazos desde matters
        this.matters.forEach(m => {
            if (m.plazo && m.plazo.fecha) {
                this.events.push({
                    id: `plazo-${m.id}`,
                    date: new Date(m.plazo.fecha),
                    title: `Plazo: ${m.plazo.tipo || 'General'}`,
                    type: 'plazo',
                    matterId: m.id,
                    priority: m.prioridad,
                    description: m.plazo.descripcion || ''
                });
            }
        });

        // Reuniones
        this.reuniones.forEach(r => {
            if (r.fecha) {
                this.events.push({
                    id: `reunion-${r.id}`,
                    date: new Date(r.fecha),
                    title: r.titulo || `Reunión ${r.id}`,
                    type: 'reunion',
                    matterId: r.matter_id,
                    estado: r.estado,
                    description: r.resumen || ''
                });
            }
        });

        // Ordenar por fecha
        this.events.sort((a, b) => a.date - b.date);
    },

    // ========== VISTA MENSUAL ==========
    renderMonth() {
        const year = this.currentDate.getFullYear();
        const month = this.currentDate.getMonth();
        
        const firstDay = new Date(year, month, 1);
        const lastDay = new Date(year, month + 1, 0);
        const startOffset = firstDay.getDay(); // 0 = domingo
        
        const monthNames = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
                           'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'];
        
        let html = `
            <div style="text-align: center; margin-bottom: 20px;">
                <h2 style="color: var(--ink-blue); margin: 0;">${monthNames[month]} ${year}</h2>
            </div>
            <div class="calendar-grid">
                <div class="calendar-header">Dom</div>
                <div class="calendar-header">Lun</div>
                <div class="calendar-header">Mar</div>
                <div class="calendar-header">Mie</div>
                <div class="calendar-header">Jue</div>
                <div class="calendar-header">Vie</div>
                <div class="calendar-header">Sab</div>
        `;

        // Celdas vacías antes del primer día
        for (let i = 0; i < startOffset; i++) {
            html += '<div class="calendar-day empty"></div>';
        }

        // Días del mes
        const today = new Date();
        for (let day = 1; day <= lastDay.getDate(); day++) {
            const date = new Date(year, month, day);
            const isToday = date.toDateString() === today.toDateString();
            const dayEvents = this.getEventsForDate(date);
            
            html += `
                <div class="calendar-day ${isToday ? 'today' : ''} ${dayEvents.length > 0 ? 'has-events' : ''}" 
                     onclick="Calendario.showDayEvents(${year}, ${month}, ${day})">
                    <div class="day-number">${day}</div>
                    <div class="day-events">
                        ${dayEvents.slice(0, 3).map(e => `
                            <div class="event-dot event-${e.type}"></div>
                        `).join('')}
                        ${dayEvents.length > 3 ? '<div class="event-dot more">+' + (dayEvents.length - 3) + '</div>' : ''}
                    </div>
                </div>
            `;
        }

        html += '</div>';

        // Sidebar con próximos eventos
        html += this.renderSidebar();

        document.getElementById('calendario-content').innerHTML = html;
    },

    // ========== VISTA SEMANAL ==========
    renderWeek() {
        const startOfWeek = new Date(this.currentDate);
        startOfWeek.setDate(startOfWeek.getDate() - startOfWeek.getDay());
        
        const dayNames = ['Domingo', 'Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado'];
        const today = new Date();
        
        let html = `
            <div style="text-align: center; margin-bottom: 20px;">
                <h2 style="color: var(--ink-blue); margin: 0;">
                    Semana del ${startOfWeek.toLocaleDateString('es-MX')}
                </h2>
            </div>
            <div class="week-view">
        `;

        for (let i = 0; i < 7; i++) {
            const date = new Date(startOfWeek);
            date.setDate(date.getDate() + i);
            const isToday = date.toDateString() === today.toDateString();
            const dayEvents = this.getEventsForDate(date);
            
            html += `
                <div class="week-day ${isToday ? 'today' : ''}">
                    <div class="week-day-header">
                        <div class="week-day-name">${dayNames[i]}</div>
                        <div class="week-day-number">${date.getDate()}</div>
                    </div>
                    <div class="week-day-events">
                        ${dayEvents.length === 0 ? 
                            '<div class="no-events">Sin eventos</div>' :
                            dayEvents.map(e => `
                                <div class="week-event event-${e.type}" onclick="Calendario.navigateToEvent('${e.id}')">
                                    <div class="event-time">${e.date.toLocaleTimeString('es-MX', {hour: '2-digit', minute: '2-digit'})}</div>
                                    <div class="event-title">${Utils.escape(e.title)}</div>
                                    ${e.matterId ? `<div class="event-matter">${e.matterId}</div>` : ''}
                                </div>
                            `).join('')
                        }
                    </div>
                </div>
            `;
        }

        html += '</div>';
        html += this.renderSidebar();

        document.getElementById('calendario-content').innerHTML = html;
    },

    // ========== SIDEBAR ==========
    renderSidebar() {
        const upcoming = this.events
            .filter(e => e.date >= new Date())
            .slice(0, 5);

        const urgentPlazos = this.events
            .filter(e => e.type === 'plazo' && e.date >= new Date())
            .sort((a, b) => a.date - b.date)
            .slice(0, 3);

        return `
            <div class="calendar-sidebar">
                <div class="sidebar-section">
                    <h3>📅 Próximos Eventos</h3>
                    ${upcoming.length === 0 ? 
                        '<div class="sidebar-empty">No hay eventos próximos</div>' :
                        upcoming.map(e => `
                            <div class="sidebar-event event-${e.type}" onclick="Calendario.navigateToEvent('${e.id}')">
                                <div class="sidebar-event-date">${e.date.toLocaleDateString('es-MX', {day: 'numeric', month: 'short'})}</div>
                                <div class="sidebar-event-title">${Utils.escape(e.title)}</div>
                                <div class="sidebar-event-matter">${e.matterId || ''}</div>
                            </div>
                        `).join('')
                    }
                </div>
                
                ${urgentPlazos.length > 0 ? `
                    <div class="sidebar-section">
                        <h3>🔴 Plazos Urgentes</h3>
                        ${urgentPlazos.map(e => `
                            <div class="sidebar-event event-plazo urgent" onclick="Calendario.navigateToEvent('${e.id}')">
                                <div class="sidebar-event-date">${e.date.toLocaleDateString('es-MX')}</div>
                                <div class="sidebar-event-title">${Utils.escape(e.title)}</div>
                                <div class="sidebar-event-matter">${e.matterId}</div>
                            </div>
                        `).join('')}
                    </div>
                ` : ''}
                
                <div class="sidebar-section">
                    <h3>🎨 Leyenda</h3>
                    <div class="legend">
                        <div class="legend-item"><div class="event-dot event-plazo"></div> Plazo</div>
                        <div class="legend-item"><div class="event-dot event-reunion"></div> Reunión</div>
                        <div class="legend-item"><div class="event-dot event-audiencia"></div> Audiencia</div>
                        <div class="legend-item"><div class="event-dot event-vencimiento"></div> Vencimiento</div>
                    </div>
                </div>
            </div>
        `;
    },

    // ========== UTILIDADES ==========
    getEventsForDate(date) {
        return this.events.filter(e => 
            e.date.getDate() === date.getDate() &&
            e.date.getMonth() === date.getMonth() &&
            e.date.getFullYear() === date.getFullYear()
        );
    },

    showDayEvents(year, month, day) {
        const date = new Date(year, month, day);
        const events = this.getEventsForDate(date);
        
        if (events.length === 0) return;

        const modal = document.createElement('div');
        modal.className = 'modal-overlay';
        modal.id = 'modal-day-events';
        modal.innerHTML = `
            <div class="modal" style="max-width: 500px;">
                <div class="modal-header">
                    <div class="modal-title">Eventos del ${date.toLocaleDateString('es-MX')}</div>
                    <button class="modal-close" onclick="Calendario.closeModal('modal-day-events')">&times;</button>
                </div>
                <div class="modal-body">
                    ${events.map(e => `
                        <div class="day-event-item event-${e.type}" onclick="Calendario.navigateToEvent('${e.id}'); Calendario.closeModal('modal-day-events');">
                            <div class="day-event-time">${e.date.toLocaleTimeString('es-MX', {hour: '2-digit', minute: '2-digit'})}</div>
                            <div class="day-event-title">${Utils.escape(e.title)}</div>
                            ${e.matterId ? `<div class="day-event-matter">${e.matterId}</div>` : ''}
                            ${e.description ? `<div class="day-event-desc">${Utils.escape(e.description)}</div>` : ''}
                        </div>
                    `).join('')}
                </div>
            </div>
        `;
        document.body.appendChild(modal);
    },

    navigateToEvent(eventId) {
        if (eventId.startsWith('plazo-')) {
            const matterId = eventId.replace('plazo-', '');
            window.location.hash = 'matters';
            // Guardar matter a seleccionar
            localStorage.setItem('scrollToMatter', matterId);
        } else if (eventId.startsWith('reunion-')) {
            window.location.hash = 'reuniones';
        }
    },

    // ========== NAVEGACIÓN ==========
    prev() {
        if (this.viewMode === 'month') {
            this.currentDate.setMonth(this.currentDate.getMonth() - 1);
        } else {
            this.currentDate.setDate(this.currentDate.getDate() - 7);
        }
        this.render();
    },

    next() {
        if (this.viewMode === 'month') {
            this.currentDate.setMonth(this.currentDate.getMonth() + 1);
        } else {
            this.currentDate.setDate(this.currentDate.getDate() + 7);
        }
        this.render();
    },

    today() {
        this.currentDate = new Date();
        this.render();
    },

    setView(mode) {
        this.viewMode = mode;
        this.render();
    },

    closeModal(id) {
        const modal = document.getElementById(id);
        if (modal) modal.remove();
    }
};

window.Calendario = Calendario;
```

**Guardar en:** `~/ws-hermes-legal-pro/dashboard/frontend/js/calendario.js`

---

## 🔧 PASO 2: Modificar `js/app.js`

Buscar `loadCalendario()` placeholder y reemplazar:

**DE:**
```javascript
async loadCalendario() {
    const container = document.getElementById('view-calendario');
    container.innerHTML = `
        <div class="header">...</div>
        <div class="alert alert-yellow">🏗️ Vista en construcción. FASE 6.</div>
    `;
}
```

**A:**
```javascript
async loadCalendario() {
    await Calendario.render();
}
```

---

## 🔧 PASO 3: Agregar CSS al final de `css/kami.css`

```css
/* ===== CALENDARIO SPECIFIC ===== */

.calendar-grid {
    display: grid;
    grid-template-columns: repeat(7, 1fr);
    gap: 4px;
    background: var(--border-light);
    border-radius: var(--radius-lg);
    padding: 4px;
}

.calendar-header {
    text-align: center;
    padding: 8px;
    font-size: 12px;
    font-weight: 600;
    color: var(--text-secondary);
    text-transform: uppercase;
}

.calendar-day {
    background: white;
    min-height: 80px;
    padding: 8px;
    border-radius: var(--radius);
    cursor: pointer;
    transition: all 0.2s;
    position: relative;
}

.calendar-day:hover {
    background: #f8fafc;
    transform: scale(1.02);
}

.calendar-day.empty {
    background: transparent;
    cursor: default;
}

.calendar-day.today {
    background: #eff6ff;
    border: 2px solid var(--corporate-blue);
}

.calendar-day.today .day-number {
    color: var(--corporate-blue);
    font-weight: 700;
}

.day-number {
    font-size: 14px;
    color: var(--ink-blue);
    margin-bottom: 4px;
}

.day-events {
    display: flex;
    flex-wrap: wrap;
    gap: 2px;
}

.event-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
}

.event-dot.event-plazo { background: #dc2626; }
.event-dot.event-reunion { background: #2563eb; }
.event-dot.event-audiencia { background: #f59e0b; }
.event-dot.event-vencimiento { background: #ea580c; }
.event-dot.more {
    width: auto;
    height: auto;
    border-radius: 4px;
    background: var(--text-secondary);
    color: white;
    font-size: 9px;
    padding: 0 3px;
}

/* Week view */
.week-view {
    display: grid;
    grid-template-columns: repeat(7, 1fr);
    gap: 8px;
}

.week-day {
    background: white;
    border-radius: var(--radius-lg);
    padding: 12px;
    min-height: 200px;
}

.week-day.today {
    border: 2px solid var(--corporate-blue);
    background: #eff6ff;
}

.week-day-header {
    text-align: center;
    margin-bottom: 12px;
    padding-bottom: 8px;
    border-bottom: 1px solid var(--border-light);
}

.week-day-name {
    font-size: 12px;
    color: var(--text-secondary);
    text-transform: uppercase;
}

.week-day-number {
    font-size: 20px;
    font-weight: 700;
    color: var(--ink-blue);
}

.week-day-events {
    display: flex;
    flex-direction: column;
    gap: 6px;
}

.no-events {
    text-align: center;
    color: var(--text-secondary);
    font-size: 12px;
    padding: 20px 0;
}

.week-event {
    padding: 8px;
    border-radius: var(--radius);
    cursor: pointer;
    transition: all 0.2s;
    border-left: 3px solid;
}

.week-event:hover {
    transform: translateX(2px);
}

.week-event.event-plazo { background: #fef2f2; border-left-color: #dc2626; }
.week-event.event-reunion { background: #eff6ff; border-left-color: #2563eb; }
.week-event.event-audiencia { background: #fffbeb; border-left-color: #f59e0b; }
.week-event.event-vencimiento { background: #fff7ed; border-left-color: #ea580c; }

.event-time {
    font-size: 11px;
    color: var(--text-secondary);
}

.event-title {
    font-size: 13px;
    font-weight: 600;
    color: var(--ink-blue);
}

.event-matter {
    font-size: 11px;
    color: var(--text-secondary);
}

/* Sidebar */
.calendar-sidebar {
    margin-top: 24px;
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 16px;
}

.sidebar-section {
    background: white;
    border-radius: var(--radius-lg);
    padding: 16px;
    box-shadow: var(--shadow);
}

.sidebar-section h3 {
    font-size: 14px;
    color: var(--ink-blue);
    margin: 0 0 12px 0;
    padding-bottom: 8px;
    border-bottom: 1px solid var(--border-light);
}

.sidebar-event {
    padding: 8px;
    border-radius: var(--radius);
    cursor: pointer;
    margin-bottom: 8px;
    border-left: 3px solid;
    transition: all 0.2s;
}

.sidebar-event:hover {
    background: #f8fafc;
    transform: translateX(2px);
}

.sidebar-event.event-plazo { border-left-color: #dc2626; }
.sidebar-event.event-reunion { border-left-color: #2563eb; }
.sidebar-event.event-audiencia { border-left-color: #f59e0b; }
.sidebar-event.event-vencimiento { border-left-color: #ea580c; }

.sidebar-event.urgent {
    background: #fef2f2;
}

.sidebar-event-date {
    font-size: 11px;
    color: var(--text-secondary);
}

.sidebar-event-title {
    font-size: 13px;
    font-weight: 600;
    color: var(--ink-blue);
}

.sidebar-event-matter {
    font-size: 11px;
    color: var(--text-secondary);
}

.sidebar-empty {
    color: var(--text-secondary);
    font-size: 13px;
    text-align: center;
    padding: 16px;
}

/* Legend */
.legend {
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.legend-item {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 13px;
}

/* Day events modal */
.day-event-item {
    padding: 12px;
    border-radius: var(--radius);
    cursor: pointer;
    margin-bottom: 8px;
    border-left: 3px solid;
    transition: all 0.2s;
}

.day-event-item:hover {
    background: #f8fafc;
}

.day-event-item.event-plazo { border-left-color: #dc2626; background: #fef2f2; }
.day-event-item.event-reunion { border-left-color: #2563eb; background: #eff6ff; }
.day-event-item.event-audiencia { border-left-color: #f59e0b; background: #fffbeb; }
.day-event-item.event-vencimiento { border-left-color: #ea580c; background: #fff7ed; }

.day-event-time {
    font-size: 12px;
    color: var(--text-secondary);
}

.day-event-title {
    font-size: 14px;
    font-weight: 600;
    color: var(--ink-blue);
    margin: 4px 0;
}

.day-event-matter {
    font-size: 12px;
    color: var(--text-secondary);
}

.day-event-desc {
    font-size: 12px;
    color: var(--text-secondary);
    margin-top: 4px;
    font-style: italic;
}
```

**Agregar al final de:** `~/ws-hermes-legal-pro/dashboard/frontend/css/kami.css`

---

## 🔧 PASO 4: Actualizar `index.html`

Agregar script de calendario antes de app.js:

```html
<script src="js/calendario.js"></script>
```

---

## 🧪 TESTS DE ESTA FASE

### Test 1: Calendario mensual carga
```
Abrir http://localhost:8082 → Click en "Calendario"
Esperado: Grid de 7x6, días del mes, headers Lun-Dom
```

### Test 2: Navegación meses
```
Click "←" → Mes anterior
Click "→" → Mes siguiente
Click "Hoy" → Vuelve a mes actual
```

### Test 3: Día actual resaltado
```
Esperado: Día de hoy tiene borde azul y fondo diferente
```

### Test 4: Eventos mostrados
```
Si hay matters con plazos o reuniones → puntos de color en el día
Click en día con puntos → Modal con lista de eventos
```

### Test 5: Vista semanal
```
Click "Semanal" → Muestra 7 columnas (dom-sab)
Cada día muestra eventos con hora, título, matter
```

### Test 6: Sidebar
```
Próximos eventos listados
Plazos urgentes resaltados en rojo
Leyenda visible
```

### Test 7: Click en evento navega
```
Click en plazo → Va a vista Matters
Click en reunión → Va a vista Reuniones
```

### Test 8: Sin errores en consola
```
Cmd+Option+J → Ningún error rojo
```

---

## ✅ CHECKLIST PARA PASAR A FASE 7

- [ ] calendario.js creado y funciona
- [ ] Vista mensual muestra grid correcto
- [ ] Navegación meses funciona
- [ ] Día actual resaltado
- [ ] Eventos aparecen como puntos de color
- [ ] Click en día abre modal de eventos
- [ ] Vista semanal funciona
- [ ] Sidebar con próximos eventos y plazos urgentes
- [ ] Click en evento navega a la vista correcta
- [ ] Sin errores en consola

---

## 📤 ENTREGA

```bash
cd ~/ws-hermes-legal-pro
git add dashboard/frontend/
git commit -m "FASE 6: Calendario - mensual, semanal, eventos, plazos"
git push origin master
```

**Notificar:** "FASE 6 completada. Calendario funcionando al 100%. Listo para FASE 7 (Polish / UX final)."

---

*Prompt FASE 6 — Diseñado para OpenCode Go*
*Hermes Legal Pro v3.0*
