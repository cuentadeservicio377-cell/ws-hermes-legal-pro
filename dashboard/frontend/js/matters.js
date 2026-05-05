// js/matters.js — Matters simplificado (creación automática desde reunión)
// Willow Legal Pro v3.0 — Mobile-first

const Matters = {
  matters: [],
  
  async render() {
    const container = document.getElementById('matters-content');
    
    container.innerHTML = `
      <div class="empty-state">
        <div class="icon">📁</div>
        <h3>Cargando matters...</h3>
      </div>
    `;
    
    try {
      const data = await API.matters();
      this.matters = data || [];
      this.renderList();
    } catch (err) {
      container.innerHTML = `
        <div class="empty-state">
          <div class="icon">⚠️</div>
          <h3>Error de conexión</h3>
          <p>No se pudieron cargar los matters</p>
          <button class="btn btn-primary mt-md" onclick="Matters.render()">Reintentar</button>
        </div>
      `;
    }
  },
  
  renderList() {
    const container = document.getElementById('matters-content');
    
    if (this.matters.length === 0) {
      container.innerHTML = `
        <div class="empty-state">
          <div class="icon">📁</div>
          <h3>Sin matters</h3>
          <p>Los matters se crean automáticamente cuando registras una reunión con un cliente nuevo</p>
          <button class="btn btn-primary mt-lg" onclick="App.navigate('reuniones')">
            Ir a Reuniones
          </button>
        </div>
      `;
      return;
    }
    
    const activos = this.matters.filter(m => m.estado === 'activo');
    const cerrados = this.matters.filter(m => m.estado !== 'activo');
    
    container.innerHTML = `
      <div style="display: flex; flex-direction: column; gap: 24px;">
        ${activos.length > 0 ? `
          <section>
            <div class="section-header">
              <div>
                <div class="section-title">Activos</div>
                <div class="section-subtitle">${activos.length} matters</div>
              </div>
            </div>
            <div style="display: flex; flex-direction: column; gap: 12px;">
              ${activos.map(m => this.renderCard(m)).join('')}
            </div>
          </section>
        ` : ''}
        
        ${cerrados.length > 0 ? `
          <section>
            <div class="section-header">
              <div>
                <div class="section-title">Archivados</div>
                <div class="section-subtitle">${cerrados.length} matters</div>
              </div>
            </div>
            <div style="display: flex; flex-direction: column; gap: 12px;">
              ${cerrados.slice(0, 3).map(m => this.renderCard(m)).join('')}
            </div>
          </section>
        ` : ''}
      </div>
    `;
  },
  
  renderCard(m) {
    const estadoBadge = m.estado === 'activo' 
      ? '<span class="badge badge-success">Activo</span>'
      : '<span class="badge badge-info">Archivado</span>';
    
    const reunionesCount = m.reuniones?.length || 0;
    const documentosCount = m.documentos?.length || 0;
    
    return `
      <div class="reunion-card" onclick="Matters.verDetalle('${m.id}')">
        <div class="reunion-header">
          <div class="reunion-cliente">${Utils.escape(m.cliente || 'Sin nombre')}</div>
          <div class="reunion-badges">
            ${estadoBadge}
            <span class="badge badge-info">${m.id}</span>
          </div>
        </div>
        
        <div class="reunion-meta">
          <span>📅 ${Utils.formatDate(m.fecha_creacion)}</span>
          <span>🏷️ ${m.area_practica || 'General'}</span>
          ${reunionesCount > 0 ? `<span>🎤 ${reunionesCount} reuniones</span>` : ''}
          ${documentosCount > 0 ? `<span>📄 ${documentosCount} docs</span>` : ''}
        </div>
        
        ${m.descripcion ? `
          <div class="reunion-resumen">${Utils.escape(m.descripcion)}</div>
        ` : ''}
      </div>
    `;
  },
  
  verDetalle(id) {
    const matter = this.matters.find(m => m.id === id);
    if (!matter) return;
    
    App.showToast(`Matter: ${matter.cliente}`, 'info');
    // Implementar vista detalle
  },
  
  showCreateModal() {
    App.showToast('Los matters se crean automáticamente desde una reunión', 'info');
    App.navigate('reuniones');
  }
};