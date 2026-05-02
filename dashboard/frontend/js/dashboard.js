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
