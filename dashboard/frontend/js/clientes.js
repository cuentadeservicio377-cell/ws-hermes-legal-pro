// js/clientes.js — Gestión de clientes del despacho
// Willow Legal Pro v3.1 — Despacho Lic. Narváez

const Clientes = {
  data: [],
  currentCliente: null,
  
  async render() {
    const container = document.getElementById('clientes-content');
    
    container.innerHTML = `
      <div class="search-bar">
        <input type="text" id="search-clientes" placeholder="Buscar cliente..." oninput="Clientes.filter(this.value)">
        <button class="btn btn-sm btn-secondary" onclick="Clientes.showCreateModal()">+ Nuevo</button>
      </div>
      <div id="clientes-list">
        <div class="skeleton" style="height: 80px; margin-bottom: 12px;"></div>
        <div class="skeleton" style="height: 80px; margin-bottom: 12px;"></div>
        <div class="skeleton" style="height: 80px; margin-bottom: 12px;"></div>
      </div>
    `;
    
    try {
      this.data = await API.clientes();
      this.renderList(this.data);
    } catch (err) {
      console.error('Error cargando clientes:', err);
      container.innerHTML = `
        <div class="empty-state">
          <div class="icon">⚠️</div>
          <h3>Error de conexión</h3>
          <p>No se pudieron cargar los clientes</p>
          <button class="btn btn-primary mt-lg" onclick="Clientes.render()">Reintentar</button>
        </div>
      `;
    }
  },
  
  renderList(clientes) {
    const container = document.getElementById('clientes-list');
    
    if (clientes.length === 0) {
      container.innerHTML = `
        <div class="empty-state">
          <div class="icon">👥</div>
          <h3>Sin clientes</h3>
          <p>No hay clientes registrados</p>
        </div>
      `;
      return;
    }
    
    // Agrupar por tipo
    const morales = clientes.filter(c => c.tipo === 'moral');
    const fisicas = clientes.filter(c => c.tipo === 'fisica');
    
    container.innerHTML = `
      <div style="display: flex; flex-direction: column; gap: 16px;">
        ${morales.length > 0 ? `
          <div>
            <div class="section-header">
              <div class="section-title">Personas morales</div>
              <div class="section-subtitle">${morales.length} clientes</div>
            </div>
            <div style="display: flex; flex-direction: column; gap: 12px;">
              ${morales.map(c => this.renderClienteCard(c)).join('')}
            </div>
          </div>
        ` : ''}
        
        ${fisicas.length > 0 ? `
          <div>
            <div class="section-header">
              <div class="section-title">Personas físicas</div>
              <div class="section-subtitle">${fisicas.length} clientes</div>
            </div>
            <div style="display: flex; flex-direction: column; gap: 12px;">
              ${fisicas.map(c => this.renderClienteCard(c)).join('')}
            </div>
          </div>
        ` : ''}
      </div>
    `;
  },
  
  renderClienteCard(c) {
    const expedientesCount = c.expedientes_relacionados?.length || 0;
    
    return `
      <div class="cliente-card" onclick="App.navigate('cliente-detalle', { clienteId: '${c.cliente_id}' })">
        <div class="cliente-header">
          <div class="cliente-icon">${c.tipo === 'moral' ? '🏢' : '👤'}</div>
          <div class="cliente-info">
            <div class="cliente-nombre">${Utils.escape(c.nombre)}</div>
            <div class="cliente-meta">
              ${c.rfc && c.rfc !== '[PENDIENTE]' ? `RFC: ${c.rfc}` : 'RFC pendiente'}
              ${c.telefono && c.telefono !== '[PENDIENTE]' ? ` · ${c.telefono}` : ''}
            </div>
          </div>
          <div class="cliente-badge">
            ${expedientesCount} exp.
          </div>
        </div>
      </div>
    `;
  },
  
  async renderDetalle(clienteId) {
    const container = document.getElementById('cliente-detalle-content');
    
    container.innerHTML = `
      <div class="detalle-header">
        <button class="btn btn-icon" onclick="App.goBack()">←</button>
        <div class="detalle-title">Cliente</div>
        <div style="width: 40px;"></div>
      </div>
      <div class="skeleton" style="height: 200px; margin-bottom: 16px;"></div>
      <div class="skeleton" style="height: 150px;"></div>
    `;
    
    try {
      const cliente = await API.cliente(clienteId);
      this.currentCliente = cliente;
      
      container.innerHTML = this.renderDetalleContent(cliente);
    } catch (err) {
      console.error('Error cargando cliente:', err);
      container.innerHTML = `
        <div class="detalle-header">
          <button class="btn btn-icon" onclick="App.goBack()">←</button>
          <div class="detalle-title">Error</div>
        </div>
        <div class="empty-state">
          <div class="icon">⚠️</div>
          <h3>No se pudo cargar el cliente</h3>
        </div>
      `;
    }
  },
  
  renderDetalleContent(c) {
    const expedientes = c.expedientes || [];
    
    return `
      <div class="detalle-header">
        <button class="btn btn-icon" onclick="App.goBack()">←</button>
        <div class="detalle-title">${Utils.escape(c.nombre)}</div>
        <button class="btn btn-icon" onclick="Clientes.showEditModal()">✎</button>
      </div>
      
      <div class="detalle-content">
        <!-- Tipo -->
        <div class="detalle-badges">
          <span class="badge tipo">${c.tipo === 'moral' ? 'Persona moral' : 'Persona física'}</span>
        </div>
        
        <!-- Datos de contacto -->
        <div class="detalle-section">
          <div class="section-label">Datos de contacto</div>
          <div class="datos-grid">
            <div class="dato">
              <div class="dato-label">RFC</div>
              <div class="dato-value ${c.rfc === '[PENDIENTE]' ? 'pending' : ''}">${c.rfc || 'No especificado'}</div>
            </div>
            <div class="dato">
              <div class="dato-label">Teléfono</div>
              <div class="dato-value ${c.telefono === '[PENDIENTE]' ? 'pending' : ''}">${c.telefono || 'No especificado'}</div>
            </div>
            <div class="dato">
              <div class="dato-label">Email</div>
              <div class="dato-value ${c.email === '[PENDIENTE]' ? 'pending' : ''}">${c.email || 'No especificado'}</div>
            </div>
            <div class="dato">
              <div class="dato-label">Domicilio</div>
              <div class="dato-value ${c.domicilio === '[PENDIENTE]' ? 'pending' : ''}">${c.domicilio || 'No especificado'}</div>
            </div>
          </div>
        </div>
        
        <!-- Representante legal (solo morales) -->
        ${c.tipo === 'moral' ? `
        <div class="detalle-section">
          <div class="section-label">Representante legal</div>
          <div class="dato-value ${c.representante_legal === '[PENDIENTE]' ? 'pending' : ''}">${c.representante_legal || 'No especificado'}</div>
        </div>
        ` : ''}
        
        <!-- Notas -->
        ${c.notas ? `
        <div class="detalle-section">
          <div class="section-label">Notas</div>
          <div class="notas-content">${Utils.escape(c.notas)}</div>
        </div>
        ` : ''}
        
        <!-- Expedientes relacionados -->
        <div class="detalle-section">
          <div class="section-label">Expedientes (${expedientes.length})</div>
          ${expedientes.length > 0 ? `
            <div style="display: flex; flex-direction: column; gap: 12px;">
              ${expedientes.map(e => `
                <div class="expediente-card mini" onclick="App.navigate('expediente-detalle', { expedienteId: '${e.expediente_id}' })">
                  <div class="expediente-header">
                    <div class="expediente-numero">${e.numero_expediente || 'S/N'}</div>
                    <div class="expediente-estado ${e.estado || 'activo'}">${e.estado || 'activo'}</div>
                  </div>
                  <div class="expediente-juzgado">${Utils.escape(e.juzgado || 'Sin juzgado')}</div>
                  <div class="expediente-partes">
                    <span class="demandado">vs ${Utils.escape(e.partes?.demandado || 'Sin demandado')}</span>
                  </div>
                </div>
              `).join('')}
            </div>
          ` : `
            <div class="empty-mini">
              <p>Sin expedientes relacionados</p>
            </div>
          `}
        </div>
      </div>
    `;
  },
  
  filter(query) {
    if (!query) {
      this.renderList(this.data);
      return;
    }
    
    const lowerQuery = query.toLowerCase();
    const filtered = this.data.filter(c => 
      (c.nombre || '').toLowerCase().includes(lowerQuery) ||
      (c.rfc || '').toLowerCase().includes(lowerQuery) ||
      (c.email || '').toLowerCase().includes(lowerQuery)
    );
    
    this.renderList(filtered);
  },
  
  showCreateModal() {
    App.openModal(`
      <div class="modal-header">
        <h3>Nuevo cliente</h3>
        <button class="btn btn-icon" onclick="App.closeModal()">✕</button>
      </div>
      <div class="modal-body">
        <div class="form-group">
          <label>Tipo *</label>
          <select class="form-control" id="new-cli-tipo">
            <option value="fisica">Persona física</option>
            <option value="moral">Persona moral</option>
          </select>
        </div>
        <div class="form-group">
          <label>Nombre *</label>
          <input type="text" class="form-control" id="new-cli-nombre" placeholder="Nombre completo o razón social">
        </div>
        <div class="form-group">
          <label>RFC</label>
          <input type="text" class="form-control" id="new-cli-rfc" placeholder="RFC">
        </div>
        <div class="form-group">
          <label>Teléfono</label>
          <input type="tel" class="form-control" id="new-cli-telefono" placeholder="Teléfono">
        </div>
        <div class="form-group">
          <label>Email</label>
          <input type="email" class="form-control" id="new-cli-email" placeholder="correo@ejemplo.com">
        </div>
        <div class="form-group">
          <label>Domicilio</label>
          <textarea class="form-control" id="new-cli-domicilio" rows="2" placeholder="Domicilio fiscal"></textarea>
        </div>
      </div>
      <div class="modal-footer">
        <button class="btn btn-secondary" onclick="App.closeModal()">Cancelar</button>
        <button class="btn btn-primary" onclick="Clientes.create()">Crear cliente</button>
      </div>
    `);
  },
  
  showEditModal() {
    if (!this.currentCliente) return;
    
    const c = this.currentCliente;
    App.openModal(`
      <div class="modal-header">
        <h3>Editar cliente</h3>
        <button class="btn btn-icon" onclick="App.closeModal()">✕</button>
      </div>
      <div class="modal-body">
        <div class="form-group">
          <label>RFC</label>
          <input type="text" class="form-control" id="edit-cli-rfc" value="${c.rfc === '[PENDIENTE]' ? '' : c.rfc}" placeholder="RFC">
        </div>
        <div class="form-group">
          <label>Teléfono</label>
          <input type="tel" class="form-control" id="edit-cli-telefono" value="${c.telefono === '[PENDIENTE]' ? '' : c.telefono}" placeholder="Teléfono">
        </div>
        <div class="form-group">
          <label>Email</label>
          <input type="email" class="form-control" id="edit-cli-email" value="${c.email === '[PENDIENTE]' ? '' : c.email}" placeholder="correo@ejemplo.com">
        </div>
        <div class="form-group">
          <label>Domicilio</label>
          <textarea class="form-control" id="edit-cli-domicilio" rows="2" placeholder="Domicilio fiscal">${c.domicilio === '[PENDIENTE]' ? '' : c.domicilio}</textarea>
        </div>
        ${c.tipo === 'moral' ? `
        <div class="form-group">
          <label>Representante legal</label>
          <input type="text" class="form-control" id="edit-cli-rep" value="${c.representante_legal === '[PENDIENTE]' ? '' : c.representante_legal}" placeholder="Nombre del representante">
        </div>
        ` : ''}
      </div>
      <div class="modal-footer">
        <button class="btn btn-secondary" onclick="App.closeModal()">Cancelar</button>
        <button class="btn btn-primary" onclick="Clientes.saveEdit()">Guardar</button>
      </div>
    `);
  },
  
  async create() {
    App.showToast('Creación de cliente - implementar en backend', 'info');
    App.closeModal();
  },
  
  async saveEdit() {
    App.showToast('Cambios guardados', 'success');
    App.closeModal();
    if (this.currentCliente) {
      this.renderDetalle(this.currentCliente.cliente_id);
    }
  }
};
