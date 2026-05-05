// js/dashboard.js — Dashboard judicial con KPIs de despacho
// Willow Legal Pro v3.1 — Despacho Lic. Narváez

const Dashboard = {
  data: null,
  
  async render() {
    const container = document.getElementById('dashboard-content');
    
    // Estado de carga
    container.innerHTML = `
      <div class="skeleton" style="height: 160px; margin-bottom: 16px;"></div>
      <div class="skeleton" style="height: 100px; margin-bottom: 16px;"></div>
      <div class="skeleton" style="height: 200px;"></div>
    `;
    
    try {
      // Cargar datos del dashboard
      const dashboard = await API.dashboard();
      
      this.data = { dashboard };
      
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
    const { dashboard } = this.data;
    const kpis = dashboard?.kpis || {};
    const proximosPlazos = dashboard?.proximos_plazos || [];
    const alertasUrgentes = dashboard?.alertas_urgentes || [];
    const expedientesRecientes = dashboard?.expedientes_recientes || [];
    const modelo = dashboard?.modelo || 'legacy';
    
    // Si estamos en modelo judicial (datos migrados de Tato)
    if (modelo === 'judicial') {
      return this.renderDashboardJudicial(kpis, proximosPlazos, alertasUrgentes, expedientesRecientes);
    }
    
    // Fallback al modelo legacy
    return this.renderDashboardLegacy(kpis, proximosPlazos, alertasUrgentes, expedientesRecientes);
  },
  
  renderDashboardJudicial(kpis, plazos, alertas, expedientes) {
    return `
      <!-- KPIs del Despacho -->
      <div class="kpi-grid judicial">
        <div class="kpi-card primary" onclick="App.navigate('expedientes')">
          <div class="kpi-header">
            <div class="icon">⚖️</div>
            <div class="kpi-badge ${kpis.expedientes_activos > 300 ? 'warning' : ''}">${kpis.expedientes_activos || 0}</div>
          </div>
          <div class="kpi-label">Expedientes Activos</div>
          <div class="kpi-sub">${kpis.total_expedientes || 0} total · ${kpis.expedientes_caducidad || 0} caducidad</div>
        </div>
        
        <div class="kpi-card" onclick="App.navigate('clientes')">
          <div class="kpi-header">
            <div class="icon">👥</div>
            <div class="kpi-badge">${kpis.total_clientes || 0}</div>
          </div>
          <div class="kpi-label">Clientes</div>
          <div class="kpi-sub">Personas físicas y morales</div>
        </div>
        
        <div class="kpi-card ${kpis.alertas_pendientes > 0 ? 'alert' : ''}" onclick="App.navigate('alertas')">
          <div class="kpi-header">
            <div class="icon">🔔</div>
            <div class="kpi-badge">${kpis.alertas_pendientes || 0}</div>
          </div>
          <div class="kpi-label">Alertas Pendientes</div>
          <div class="kpi-sub">${kpis.expedientes_con_pendientes || 0} expedientes con acciones</div>
        </div>
        
        <div class="kpi-card ${kpis.plazos_proximos > 0 ? 'urgent' : ''}">
          <div class="kpi-header">
            <div class="icon">⏰</div>
            <div class="kpi-badge">${kpis.plazos_proximos || 0}</div>
          </div>
          <div class="kpi-label">Plazos Próximos</div>
          <div class="kpi-sub">Esta semana</div>
        </div>
      </div>
      
      <!-- Distribución por Tipo de Juicio -->
      ${this.renderDistribucionJuicios()}
      
      <!-- Alertas Urgentes -->
      ${this.renderAlertasUrgentes(alertas)}
      
      <!-- Expedientes Recientes -->
      ${this.renderExpedientesRecientes(expedientes)}
      
      <!-- Plazos Próximos -->
      ${this.renderPlazosProximos(plazos)}
    `;
  },
  
  renderDashboardLegacy(kpis, plazos, alertas, reuniones) {
    // Fallback al dashboard anterior
    return `
      <div class="kpi-grid">
        <div class="kpi-card" onclick="App.navigate('expedientes')">
          <div class="icon">📁</div>
          <div class="number">${kpis.matters_activos || 0}</div>
          <div class="label">Matters activos</div>
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
    `;
  },
  
  renderDistribucionJuicios() {
    // Esta función se llenará con datos reales de la API
    return `
      <section>
        <div class="section-header">
          <div>
            <div class="section-title">Distribución del despacho</div>
            <div class="section-subtitle">Por tipo de juicio</div>
          </div>
        </div>
        <div class="distribucion-grid">
          <div class="dist-item" onclick="App.navigate('expedientes')">
            <div class="dist-icon">⚖️</div>
            <div class="dist-info">
              <div class="dist-title">Mercantil</div>
              <div class="dist-count">122 expedientes</div>
            </div>
            <div class="dist-arrow">›</div>
          </div>
          <div class="dist-item" onclick="App.navigate('expedientes')">
            <div class="dist-icon">👨‍👩‍👧‍👦</div>
            <div class="dist-info">
              <div class="dist-title">Familiar</div>
              <div class="dist-count">82 expedientes</div>
            </div>
            <div class="dist-arrow">›</div>
          </div>
          <div class="dist-item" onclick="App.navigate('expedientes')">
            <div class="dist-icon">🏛️</div>
            <div class="dist-info">
              <div class="dist-title">Civil</div>
              <div class="dist-count">66 expedientes</div>
            </div>
            <div class="dist-arrow">›</div>
          </div>
        </div>
      </section>
    `;
  },
  
  renderAlertasUrgentes(alertas) {
    if (!alertas || alertas.length === 0) {
      return '';
    }
    
    return `
      <section>
        <div class="section-header">
          <div>
            <div class="section-title">Alertas pendientes</div>
            <div class="section-subtitle">${alertas.length} por atender</div>
          </div>
          <button class="btn btn-sm btn-secondary" onclick="App.navigate('alertas')">
            Ver todas
          </button>
        </div>
        <div style="display: flex; flex-direction: column; gap: 12px;">
          ${alertas.slice(0, 3).map(a => `
            <div class="action-card ${a.prioridad === 'alta' ? 'urgent' : ''}" onclick="App.navigate('expediente-detalle', { expedienteId: '${a.expediente_id}' })">
              <div class="action-icon">${a.prioridad === 'alta' ? '🔴' : '🔔'}</div>
              <div class="action-content">
                <div class="action-title">${Utils.escape(a.descripcion || 'Sin descripción')}</div>
                <div class="action-meta">
                  ${a.expediente_id ? `Exp: ${a.expediente_id}` : ''}
                  ${a.numero_expediente ? ` · ${a.numero_expediente}` : ''}
                </div>
              </div>
              <div class="action-arrow">›</div>
            </div>
          `).join('')}
        </div>
      </section>
    `;
  },
  
  renderExpedientesRecientes(expedientes) {
    if (!expedientes || expedientes.length === 0) {
      return '';
    }
    
    return `
      <section>
        <div class="section-header">
          <div>
            <div class="section-title">Expedientes recientes</div>
            <div class="section-subtitle">Últimos actualizados</div>
          </div>
          <button class="btn btn-sm btn-secondary" onclick="App.navigate('expedientes')">
            Ver todos
          </button>
        </div>
        <div style="display: flex; flex-direction: column; gap: 12px;">
          ${expedientes.slice(0, 5).map(e => `
            <div class="expediente-card" onclick="App.navigate('expediente-detalle', { expedienteId: '${e.expediente_id}' })">
              <div class="expediente-header">
                <div class="expediente-numero">${e.numero_expediente || 'S/N'}</div>
                <div class="expediente-estado ${e.estado || 'activo'}">${e.estado || 'activo'}</div>
              </div>
              <div class="expediente-juzgado">${Utils.escape(e.juzgado || 'Sin juzgado')}</div>
              <div class="expediente-partes">
                <span class="actor">${Utils.escape(e.partes?.actor || 'Sin actor')}</span>
                <span class="vs">vs</span>
                <span class="demandado">${Utils.escape(e.partes?.demandado || 'Sin demandado')}</span>
              </div>
              <div class="expediente-meta">
                <span class="tipo">${e.tipo_juicio || 'Sin tipo'}</span>
                ${e.pendientes?.length > 0 ? `<span class="pendientes-badge">${e.pendientes.length} pendientes</span>` : ''}
              </div>
            </div>
          `).join('')}
        </div>
      </section>
    `;
  },
  
  renderPlazosProximos(plazos) {
    if (!plazos || plazos.length === 0) {
      return `
        <section>
          <div class="section-header">
            <div>
              <div class="section-title">Plazos próximos</div>
              <div class="section-subtitle">Esta semana</div>
            </div>
          </div>
          <div class="empty-state" style="padding: 24px;">
            <div class="icon">⏰</div>
            <h3>Sin plazos registrados</h3>
            <p>Captura los plazos de tus expedientes para recibir alertas</p>
          </div>
        </section>
      `;
    }
    
    return `
      <section>
        <div class="section-header">
          <div>
            <div class="section-title">Plazos próximos</div>
            <div class="section-subtitle">${plazos.length} esta semana</div>
          </div>
        </div>
        <div style="display: flex; flex-direction: column; gap: 12px;">
          ${plazos.slice(0, 3).map(p => `
            <div class="action-card ${p.dias_restantes <= 2 ? 'urgent' : ''} ${p.es_fatal ? 'fatal' : ''}">
              <div class="action-icon">${p.es_fatal ? '☠️' : '⏰'}</div>
              <div class="action-content">
                <div class="action-title">${Utils.escape(p.descripcion || 'Plazo')}</div>
                <div class="action-meta">
                  ${p.expediente_id || ''} · ${p.dias_restantes} días restantes
                  ${p.es_fatal ? ' · FATAL' : ''}
                </div>
              </div>
            </div>
          `).join('')}
        </div>
      </section>
    `;
  },
  
  // Vista de alertas completa
  async renderAlertas() {
    const container = document.getElementById('alertas-content');
    
    try {
      const alertas = await API.alertas();
      const pendientes = alertas?.filter(a => a.estado === 'pendiente') || [];
      
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
            <div class="action-card ${a.prioridad === 'alta' ? 'urgent' : ''}" onclick="App.navigate('expediente-detalle', { expedienteId: '${a.expediente_id}' })">
              <div class="action-icon">${a.prioridad === 'alta' ? '🔴' : '🔔'}</div>
              <div class="action-content">
                <div class="action-title">${Utils.escape(a.descripcion || 'Sin descripción')}</div>
                <div class="action-meta">
                  ${a.expediente_id ? `Exp: ${a.expediente_id}` : ''}
                  ${a.numero_expediente ? ` · ${a.numero_expediente}` : ''}
                  ${a.fecha_limite ? ` · Límite: ${Utils.formatDate(a.fecha_limite)}` : ' · Sin fecha límite'}
                </div>
              </div>
              <div class="action-arrow">›</div>
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
