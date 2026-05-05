// js/dashboard.js — Dashboard con KPIs visuales, acciones urgentes, timeline
// Willow Legal Pro v3.0 — Mobile-first

const Dashboard = {
  data: null,
  
  async render() {
    const container = document.getElementById('dashboard-content');
    
    // Estado de carga
    container.innerHTML = `
      <div class="skeleton" style="height: 120px; margin-bottom: 16px;"></div>
      <div class="skeleton" style="height: 80px; margin-bottom: 16px;"></div>
      <div class="skeleton" style="height: 200px;"></div>
    `;
    
    try {
      // Cargar datos
      const [dashboard, matters, reuniones, alertas] = await Promise.all([
        API.dashboard(),
        API.matters(),
        API.reuniones(),
        API.alertas()
      ]);
      
      this.data = { dashboard, matters, reuniones, alertas };
      
      // Renderizar dashboard completo
      container.innerHTML = this.renderContent();
      
    } catch (err) {
      console.error('Error cargando dashboard:', err);
      container.innerHTML = `
        <div class="empty-state">
          <div class="icon">⚠️</div>
          <h3>Error de conexión</h3>
          <p>No se pudo cargar el dashboard. Verifica que el servidor esté corriendo.</p>
          <button class="btn btn-primary mt-lg" onclick="Dashboard.render()">Reintentar</button>
        </div>
      `;
    }
  },
  
  renderContent() {
    const { dashboard, matters, reuniones, alertas } = this.data;
    const kpis = dashboard?.kpis || {};
    const proximosPlazos = dashboard?.proximos_plazos || [];
    const reunionesRecientes = dashboard?.reuniones_recientes || [];
    const alertasActivas = alertas?.filter(a => !a.resuelta) || [];
    
    // Reuniones pendientes de procesar
    const reunionesPendientes = reuniones?.filter(r => r.estado !== 'procesada') || [];
    
    return `
      <!-- KPIs -->
      <div class="kpi-grid">
        <div class="kpi-card" onclick="App.navigate('reuniones')">
          <div class="icon">🎤</div>
          <div class="number">${kpis.reuniones_hoy || 0}</div>
          <div class="label">Reuniones hoy</div>
        </div>
        <div class="kpi-card" onclick="App.navigate('documentos')">
          <div class="icon">📄</div>
          <div class="number">${kpis.documentos_pendientes || 0}</div>
          <div class="label">Docs pendientes</div>
        </div>
        <div class="kpi-card" onclick="App.navigate('alertas')">
          <div class="icon">⏰</div>
          <div class="number">${kpis.alertas_activas || 0}</div>
          <div class="label">Alertas</div>
        </div>
      </div>
      
      <!-- Acciones Urgentes -->
      ${this.renderAccionesUrgentes(reunionesPendientes, alertasActivas, proximosPlazos)}
      
      <!-- Timeline de Reuniones -->
      ${this.renderTimeline(reunionesRecientes, reunionesPendientes)}
      
      <!-- Próximos Plazos -->
      ${this.renderPlazos(proximosPlazos)}
    `;
  },
  
  renderAccionesUrgentes(reunionesPendientes, alertas, plazos) {
    const acciones = [];
    
    // Reuniones pendientes de procesar
    reunionesPendientes.slice(0, 2).forEach(r => {
      acciones.push({
        icon: '⚡',
        title: `Procesar reunión con ${r.cliente || 'Cliente'}`,
        meta: `${Utils.formatDate(r.fecha)} · ${r.documentos_necesarios?.length || 0} docs sugeridos`,
        urgent: true,
        action: () => { App.navigate('reuniones'); }
      });
    });
    
    // Plazos urgentes (menos de 3 días)
    plazos.filter(p => p.dias_restantes <= 3).slice(0, 1).forEach(p => {
      acciones.push({
        icon: '⏰',
        title: `Plazo: ${p.descripcion || p.titulo}`,
        meta: `${p.dias_restantes} días restantes · ${p.cliente}`,
        urgent: p.dias_restantes <= 1,
        action: () => { App.navigate('alertas'); }
      });
    });
    
    // Alertas
    alertas.slice(0, 1).forEach(a => {
      acciones.push({
        icon: '🔔',
        title: a.titulo || a.descripcion,
        meta: Utils.formatDate(a.fecha),
        urgent: a.tipo === 'urgente',
        action: () => { App.navigate('alertas'); }
      });
    });
    
    if (acciones.length === 0) {
      return '';
    }
    
    return `
      <section>
        <div class="section-header">
          <div>
            <div class="section-title">Acciones urgentes</div>
            <div class="section-subtitle">${acciones.length} pendientes</div>
          </div>
        </div>
        <div style="display: flex; flex-direction: column; gap: 12px;">
          ${acciones.map(a => `
            <div class="action-card ${a.urgent ? 'urgent' : ''}" onclick="(${a.action.toString()})()">
              <div class="action-icon">${a.icon}</div>
              <div class="action-content">
                <div class="action-title">${Utils.escape(a.title)}</div>
                <div class="action-meta">${Utils.escape(a.meta)}</div>
              </div>
              <div class="action-arrow">›</div>
            </div>
          `).join('')}
        </div>
      </section>
    `;
  },
  
  renderTimeline(reunionesRecientes, reunionesPendientes) {
    // Combinar y ordenar por fecha
    const todas = [
      ...reunionesPendientes.map(r => ({ ...r, tipo: 'pendiente' })),
      ...reunionesRecientes.map(r => ({ ...r, tipo: 'pasada' }))
    ].sort((a, b) => new Date(b.fecha) - new Date(a.fecha));
    
    const proximas = todas.filter(r => r.tipo === 'pendiente').slice(0, 3);
    
    if (proximas.length === 0) {
      return `
        <section>
          <div class="section-header">
            <div class="section-title">Próximas reuniones</div>
          </div>
          <div class="empty-state" style="padding: 32px;">
            <div class="icon">🎤</div>
            <h3>Sin reuniones programadas</h3>
            <p>Registra tu primera reunión para empezar</p>
            <button class="btn btn-primary mt-md" onclick="Reuniones.showCreateModal()">
              + Nueva Reunión
            </button>
          </div>
        </section>
      `;
    }
    
    return `
      <section>
        <div class="section-header">
          <div>
            <div class="section-title">Próximas reuniones</div>
            <div class="section-subtitle">${proximas.length} pendientes</div>
          </div>
          <button class="btn btn-sm btn-secondary" onclick="App.navigate('reuniones')">
            Ver todas
          </button>
        </div>
        <div class="timeline">
          ${proximas.map((r, i) => `
            <div class="timeline-item" onclick="App.navigate('reuniones')">
              <div class="timeline-dot ${r.tipo === 'pasada' ? 'past' : 'upcoming'}"></div>
              <div class="timeline-content">
                <div class="timeline-title">${Utils.escape(r.cliente || 'Sin cliente')}</div>
                <div class="timeline-meta">
                  📅 ${Utils.formatDate(r.fecha)}
                  ${r.meet_url ? '· 📹 Meet' : ''}
                  ${r.estado === 'procesada' ? '· ✅ Procesada' : '· ⏳ Pendiente'}
                </div>
              </div>
            </div>
          `).join('')}
        </div>
      </section>
    `;
  },
  
  renderPlazos(plazos) {
    if (!plazos || plazos.length === 0) return '';
    
    return `
      <section>
        <div class="section-header">
          <div>
            <div class="section-title">Próximos plazos</div>
            <div class="section-subtitle">${plazos.length} esta semana</div>
          </div>
        </div>
        <div style="display: flex; flex-direction: column; gap: 12px;">
          ${plazos.slice(0, 3).map(p => `
            <div class="action-card ${p.dias_restantes <= 2 ? 'urgent' : ''}">
              <div class="action-icon">⏰</div>
              <div class="action-content">
                <div class="action-title">${Utils.escape(p.descripcion || p.titulo || 'Plazo')}</div>
                <div class="action-meta">
                  ${p.cliente || ''} · ${p.dias_restantes} días restantes
                </div>
              </div>
            </div>
          `).join('')}
        </div>
      </section>
    `;
  },
  
  // Vista de alertas
  async renderAlertas() {
    const container = document.getElementById('alertas-content');
    
    try {
      const alertas = await API.alertas();
      const pendientes = alertas?.filter(a => !a.resuelta) || [];
      
      if (pendientes.length === 0) {
        container.innerHTML = `
          <div class="empty-state">
            <div class="icon">✅</div>
            <h3>Todo al día</h3>
            <p>No hay alertas pendientes</p>
          </div>
        `;
        return;
      }
      
      container.innerHTML = `
        <div class="section-header">
          <div>
            <div class="section-title">Alertas pendientes</div>
            <div class="section-subtitle">${pendientes.length} por atender</div>
          </div>
        </div>
        <div style="display: flex; flex-direction: column; gap: 12px;">
          ${pendientes.map(a => `
            <div class="action-card ${a.tipo === 'urgente' ? 'urgent' : ''}">
              <div class="action-icon">${a.tipo === 'urgente' ? '🔴' : '🔔'}</div>
              <div class="action-content">
                <div class="action-title">${Utils.escape(a.titulo || a.descripcion)}</div>
                <div class="action-meta">
                  ${a.matter_id ? `Matter: ${a.matter_id} · ` : ''}
                  ${Utils.formatDate(a.fecha)}
                </div>
              </div>
            </div>
          `).join('')}
        </div>
      `;
    } catch (err) {
      container.innerHTML = `
        <div class="empty-state">
          <div class="icon">⚠️</div>
          <h3>Error</h3>
          <p>No se pudieron cargar las alertas</p>
        </div>
      `;
    }
  },
  
  markAllRead() {
    App.showToast('Marcando alertas como leídas...', 'success');
    // Implementar en backend si es necesario
  }
};
