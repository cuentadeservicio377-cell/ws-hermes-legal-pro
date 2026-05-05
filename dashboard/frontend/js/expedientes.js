// js/expedientes.js — Gestión de expedientes judiciales
// Willow Legal Pro v3.1 — Despacho Lic. Narváez

const Expedientes = {
  data: [],
  currentExpediente: null,
  
  async render() {
    const container = document.getElementById('expedientes-content');
    
    container.innerHTML = `
      <div class="search-bar">
        <input type="text" id="search-expedientes" placeholder="Buscar por número, juzgado, actor..." oninput="Expedientes.filter(this.value)">
        <button class="btn btn-sm btn-secondary" onclick="Expedientes.showFilters()">Filtrar</button>
      </div>
      <div id="expedientes-list">
        <div class="skeleton" style="height: 80px; margin-bottom: 12px;"></div>
        <div class="skeleton" style="height: 80px; margin-bottom: 12px;"></div>
        <div class="skeleton" style="height: 80px; margin-bottom: 12px;"></div>
      </div>
    `;
    
    try {
      this.data = await API.expedientes();
      this.renderList(this.data);
    } catch (err) {
      console.error('Error cargando expedientes:', err);
      container.innerHTML = `
        <div class="empty-state">
          <div class="icon">⚠️</div>
          <h3>Error de conexión</h3>
          <p>No se pudieron cargar los expedientes</p>
          <button class="btn btn-primary mt-lg" onclick="Expedientes.render()">Reintentar</button>
        </div>
      `;
    }
  },
  
  renderList(expedientes) {
    const container = document.getElementById('expedientes-list');
    
    if (expedientes.length === 0) {
      container.innerHTML = `
        <div class="empty-state">
          <div class="icon">⚖️</div>
          <h3>Sin expedientes</h3>
          <p>No hay expedientes que coincidan con tu búsqueda</p>
        </div>
      `;
      return;
    }
    
    container.innerHTML = `
      <div style="display: flex; flex-direction: column; gap: 12px;">
        ${expedientes.map(e => this.renderExpedienteCard(e)).join('')}
      </div>
    `;
  },
  
  renderExpedienteCard(e) {
    const estadoClass = e.estado || 'activo';
    const tipoClass = (e.tipo_juicio || '').toLowerCase().replace(/\s+/g, '-');
    
    return `
      <div class="expediente-card" onclick="App.navigate('expediente-detalle', { expedienteId: '${e.expediente_id}' })">
        <div class="expediente-header">
          <div class="expediente-numero">${e.numero_expediente || 'S/N'}</div>
          <div class="expediente-estado ${estadoClass}">${estadoClass}</div>
        </div>
        <div class="expediente-juzgado">${Utils.escape(e.juzgado || 'Sin juzgado')}</div>
        <div class="expediente-partes">
          <span class="actor">${Utils.escape(e.partes?.actor || 'Sin actor')}</span>
          <span class="vs">vs</span>
          <span class="demandado">${Utils.escape(e.partes?.demandado || 'Sin demandado')}</span>
        </div>
        <div class="expediente-meta">
          <span class="tipo ${tipoClass}">${e.tipo_juicio || 'Sin tipo'}</span>
          ${e.pendientes?.length > 0 ? `<span class="pendientes-badge">${e.pendientes.length} pendientes</span>` : ''}
          ${e.es_fatal ? '<span class="fatal-badge">FATAL</span>' : ''}
        </div>
      </div>
    `;
  },
  
  async renderDetalle(expedienteId) {
    const container = document.getElementById('expediente-detalle-content');
    
    container.innerHTML = `
      <div class="detalle-header">
        <button class="btn btn-icon" onclick="App.goBack()">←</button>
        <div class="detalle-title">Expediente</div>
        <div style="width: 40px;"></div>
      </div>
      <div class="skeleton" style="height: 200px; margin-bottom: 16px;"></div>
      <div class="skeleton" style="height: 150px;"></div>
    `;
    
    try {
      const expediente = await API.expediente(expedienteId);
      this.currentExpediente = expediente;
      
      container.innerHTML = this.renderDetalleContent(expediente);
    } catch (err) {
      console.error('Error cargando detalle:', err);
      container.innerHTML = `
        <div class="detalle-header">
          <button class="btn btn-icon" onclick="App.goBack()">←</button>
          <div class="detalle-title">Error</div>
        </div>
        <div class="empty-state">
          <div class="icon">⚠️</div>
          <h3>No se pudo cargar el expediente</h3>
        </div>
      `;
    }
  },
  
  renderDetalleContent(e) {
    const estadoClass = e.estado || 'activo';
    
    return `
      <div class="detalle-header">
        <button class="btn btn-icon" onclick="App.goBack()">←</button>
        <div class="detalle-title">${e.numero_expediente || 'S/N'}</div>
        <button class="btn btn-icon" onclick="Expedientes.showEditModal()">✎</button>
      </div>
      
      <div class="detalle-content">
        <!-- Estado y Tipo -->
        <div class="detalle-badges">
          <span class="badge ${estadoClass}">${estadoClass}</span>
          <span class="badge tipo">${e.tipo_juicio || 'Sin tipo'}</span>
          ${e.es_fatal ? '<span class="badge fatal">FATAL</span>' : ''}
        </div>
        
        <!-- Juzgado -->
        <div class="detalle-section">
          <div class="section-label">Juzgado</div>
          <div class="section-value">${Utils.escape(e.juzgado || 'No especificado')}</div>
          ${e.juzgado_codigo ? `<div class="section-sub">Código: ${e.juzgado_codigo}</div>` : ''}
        </div>
        
        <!-- Partes -->
        <div class="detalle-section">
          <div class="section-label">Partes</div>
          <div class="partes-detalle">
            <div class="parte">
              <div class="parte-label">Actor / Cliente</div>
              <div class="parte-value">${Utils.escape(e.partes?.actor || 'No especificado')}</div>
            </div>
            <div class="parte">
              <div class="parte-label">Demandado</div>
              <div class="parte-value">${Utils.escape(e.partes?.demandado || 'No especificado')}</div>
            </div>
          </div>
        </div>
        
        <!-- Datos del Proceso -->
        <div class="detalle-section">
          <div class="section-label">Datos del proceso</div>
          <div class="datos-grid">
            <div class="dato">
              <div class="dato-label">Etapa procesal</div>
              <div class="dato-value">${e.etapa_procesal || 'No especificada'}</div>
            </div>
            <div class="dato">
              <div class="dato-label">Monto</div>
              <div class="dato-value">${e.monto || 'No especificado'}</div>
            </div>
            <div class="dato">
              <div class="dato-label">Fecha de apertura</div>
              <div class="dato-value">${e.fecha_apertura ? Utils.formatDate(e.fecha_apertura) : 'No especificada'}</div>
            </div>
            <div class="dato">
              <div class="dato-label">Número interno</div>
              <div class="dato-value">${e.numero_interno || 'No especificado'}</div>
            </div>
          </div>
        </div>
        
        <!-- Notas -->
        ${e.notas ? `
        <div class="detalle-section">
          <div class="section-label">Notas</div>
          <div class="notas-content">${Utils.escape(e.notas)}</div>
        </div>
        ` : ''}
        
        <!-- Pendientes -->
        ${e.pendientes?.length > 0 ? `
        <div class="detalle-section">
          <div class="section-label">Pendientes (${e.pendientes.length})</div>
          <div class="pendientes-list">
            ${e.pendientes.map(p => `
              <div class="pendiente-item">
                <div class="pendiente-check">☐</div>
                <div class="pendiente-text">${Utils.escape(p)}</div>
              </div>
            `).join('')}
          </div>
        </div>
        ` : ''}
        
        <!-- Alertas Relacionadas -->
        ${e.alertas_relacionadas?.length > 0 ? `
        <div class="detalle-section">
          <div class="section-label">Alertas (${e.alertas_relacionadas.length})</div>
          <div class="alertas-list">
            ${e.alertas_relacionadas.map(a => `
              <div class="alerta-item ${a.prioridad}">
                <div class="alerta-icon">${a.prioridad === 'alta' ? '🔴' : '🔔'}</div>
                <div class="alerta-content">
                  <div class="alerta-desc">${Utils.escape(a.descripcion)}</div>
                  <div class="alerta-meta">${a.fecha_limite ? 'Límite: ' + Utils.formatDate(a.fecha_limite) : 'Sin fecha límite'}</div>
                </div>
              </div>
            `).join('')}
          </div>
        </div>
        ` : ''}
        
        <!-- Documentos Generados -->
        ${e.documentos_generados?.length > 0 ? `
        <div class="detalle-section">
          <div class="section-label">Documentos generados</div>
          <div class="documentos-list">
            ${e.documentos_generados.map(d => `
              <div class="documento-item">
                <div class="documento-icon">📄</div>
                <div class="documento-name">${d}</div>
              </div>
            `).join('')}
          </div>
        </div>
        ` : `
        <div class="detalle-section">
          <div class="section-label">Documentos</div>
          <div class="empty-mini">
            <p>Sin documentos generados</p>
            <button class="btn btn-sm btn-primary" onclick="Documentos.showCreateModal('${e.expediente_id}')">Generar documento</button>
          </div>
        </div>
        `}
      </div>
    `;
  },
  
  filter(query) {
    if (!query) {
      this.renderList(this.data);
      return;
    }
    
    const lowerQuery = query.toLowerCase();
    const filtered = this.data.filter(e => 
      (e.numero_expediente || '').toLowerCase().includes(lowerQuery) ||
      (e.juzgado || '').toLowerCase().includes(lowerQuery) ||
      (e.partes?.actor || '').toLowerCase().includes(lowerQuery) ||
      (e.partes?.demandado || '').toLowerCase().includes(lowerQuery) ||
      (e.tipo_juicio || '').toLowerCase().includes(lowerQuery)
    );
    
    this.renderList(filtered);
  },
  
  showFilters() {
    App.openModal(`
      <div class="modal-header">
        <h3>Filtrar expedientes</h3>
        <button class="btn btn-icon" onclick="App.closeModal()">✕</button>
      </div>
      <div class="modal-body">
        <div class="form-group">
          <label>Estado</label>
          <select class="form-control" id="filter-estado">
            <option value="">Todos</option>
            <option value="activo">Activo</option>
            <option value="caducidad">Caducidad</option>
            <option value="terminado">Terminado</option>
          </select>
        </div>
        <div class="form-group">
          <label>Tipo de juicio</label>
          <select class="form-control" id="filter-tipo">
            <option value="">Todos</option>
            <option value="MERCANTIL">Mercantil</option>
            <option value="CIVIL">Civil</option>
            <option value="FAMILIAR">Familiar</option>
          </select>
        </div>
        <div class="form-group">
          <label>Juzgado</label>
          <input type="text" class="form-control" id="filter-juzgado" placeholder="Ej: 4M, 1C, 3F">
        </div>
      </div>
      <div class="modal-footer">
        <button class="btn btn-secondary" onclick="App.closeModal()">Cancelar</button>
        <button class="btn btn-primary" onclick="Expedientes.applyFilters()">Aplicar</button>
      </div>
    `);
  },
  
  applyFilters() {
    const estado = document.getElementById('filter-estado').value;
    const tipo = document.getElementById('filter-tipo').value;
    const juzgado = document.getElementById('filter-juzgado').value;
    
    let filtered = this.data;
    
    if (estado) {
      filtered = filtered.filter(e => e.estado === estado);
    }
    if (tipo) {
      filtered = filtered.filter(e => (e.tipo_juicio || '').includes(tipo));
    }
    if (juzgado) {
      filtered = filtered.filter(e => (e.juzgado_codigo || '').toUpperCase() === juzgado.toUpperCase());
    }
    
    this.renderList(filtered);
    App.closeModal();
  },
  
  showCreateModal() {
    App.openModal(`
      <div class="modal-header">
        <h3>Nuevo expediente</h3>
        <button class="btn btn-icon" onclick="App.closeModal()">✕</button>
      </div>
      <div class="modal-body">
        <div class="form-group">
          <label>Número de expediente *</label>
          <input type="text" class="form-control" id="new-exp-numero" placeholder="Ej: 970/2019">
        </div>
        <div class="form-group">
          <label>Juzgado</label>
          <input type="text" class="form-control" id="new-exp-juzgado" placeholder="Ej: Juzgado Cuarto De Lo Mercantil">
        </div>
        <div class="form-group">
          <label>Actor / Cliente</label>
          <input type="text" class="form-control" id="new-exp-actor" placeholder="Nombre del actor">
        </div>
        <div class="form-group">
          <label>Demandado</label>
          <input type="text" class="form-control" id="new-exp-demandado" placeholder="Nombre del demandado">
        </div>
        <div class="form-group">
          <label>Tipo de juicio</label>
          <select class="form-control" id="new-exp-tipo">
            <option value="">Seleccionar...</option>
            <option value="MERCANTIL">Mercantil</option>
            <option value="MERCANTIL EJECUTIVO">Mercantil Ejecutivo</option>
            <option value="CIVIL ORDINARIO">Civil Ordinario</option>
            <option value="FAMILIAR">Familiar</option>
            <option value="SUCESORIO">Sucesorio</option>
          </select>
        </div>
      </div>
      <div class="modal-footer">
        <button class="btn btn-secondary" onclick="App.closeModal()">Cancelar</button>
        <button class="btn btn-primary" onclick="Expedientes.create()">Crear expediente</button>
      </div>
    `);
  },
  
  showEditModal() {
    if (!this.currentExpediente) return;
    
    const e = this.currentExpediente;
    App.openModal(`
      <div class="modal-header">
        <h3>Editar expediente ${e.numero_expediente}</h3>
        <button class="btn btn-icon" onclick="App.closeModal()">✕</button>
      </div>
      <div class="modal-body">
        <div class="form-group">
          <label>Estado</label>
          <select class="form-control" id="edit-exp-estado">
            <option value="activo" ${e.estado === 'activo' ? 'selected' : ''}>Activo</option>
            <option value="caducidad" ${e.estado === 'caducidad' ? 'selected' : ''}>Caducidad</option>
            <option value="terminado" ${e.estado === 'terminado' ? 'selected' : ''}>Terminado</option>
          </select>
        </div>
        <div class="form-group">
          <label>Etapa procesal</label>
          <input type="text" class="form-control" id="edit-exp-etapa" value="${e.etapa_procesal || ''}" placeholder="Ej: Ejecución, Pruebas, Alegatos">
        </div>
        <div class="form-group">
          <label>Próxima actuación</label>
          <input type="text" class="form-control" id="edit-exp-proxima" value="${e.proxima_actuacion || ''}">
        </div>
        <div class="form-group">
          <label>Notas</label>
          <textarea class="form-control" id="edit-exp-notas" rows="3">${e.notas || ''}</textarea>
        </div>
      </div>
      <div class="modal-footer">
        <button class="btn btn-secondary" onclick="App.closeModal()">Cancelar</button>
        <button class="btn btn-primary" onclick="Expedientes.saveEdit()">Guardar</button>
      </div>
    `);
  },
  
  async create() {
    // Implementar creación
    App.showToast('Creación de expediente - implementar en backend', 'info');
    App.closeModal();
  },
  
  async saveEdit() {
    // Implementar edición
    App.showToast('Edición guardada', 'success');
    App.closeModal();
    if (this.currentExpediente) {
      this.renderDetalle(this.currentExpediente.expediente_id);
    }
  }
};
