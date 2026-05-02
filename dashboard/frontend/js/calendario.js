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
