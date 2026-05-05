// js/documentos.js — Documentos asociados a reuniones
// Willow Legal Pro v3.0 — Mobile-first

const Documentos = {
  documentos: [],
  reuniones: [],
  
  async render() {
    const container = document.getElementById('documentos-content');
    
    container.innerHTML = `
      <div class="empty-state">
        <div class="icon">📄</div>
        <h3>Cargando documentos...</h3>
      </div>
    `;
    
    try {
      const [docsData, reunionesData] = await Promise.all([
        API.documentos(),
        API.reuniones()
      ]);
      
      this.documentos = docsData || [];
      this.reuniones = reunionesData || [];
      
      this.renderList();
    } catch (err) {
      container.innerHTML = `
        <div class="empty-state">
          <div class="icon">⚠️</div>
          <h3>Error de conexión</h3>
          <p>No se pudieron cargar los documentos</p>
          <button class="btn btn-primary mt-md" onclick="Documentos.render()">Reintentar</button>
        </div>
      `;
    }
  },
  
  renderList() {
    const container = document.getElementById('documentos-content');
    
    if (this.documentos.length === 0) {
      container.innerHTML = `
        <div class="empty-state">
          <div class="icon">📄</div>
          <h3>Sin documentos</h3>
          <p>Los documentos aparecerán aquí cuando generes uno desde una reunión</p>
        </div>
      `;
      return;
    }
    
    // Agrupar por reunión
    const porReunion = {};
    this.documentos.forEach(d => {
      const key = d.matter_id || 'sin-matter';
      if (!porReunion[key]) porReunion[key] = [];
      porReunion[key].push(d);
    });
    
    container.innerHTML = `
      <div style="display: flex; flex-direction: column; gap: 24px;">
        ${Object.entries(porReunion).map(([matterId, docs]) => {
          const reunion = this.reuniones.find(r => r.matter_id === matterId);
          const titulo = reunion ? `Reunión con ${reunion.cliente}` : 'Documentos generales';
          
          return `
            <section>
              <div class="section-header">
                <div>
                  <div class="section-title">${Utils.escape(titulo)}</div>
                  <div class="section-subtitle">${docs.length} documentos</div>
                </div>
              </div>
              <div style="display: flex; flex-direction: column; gap: 12px;">
                ${docs.map(d => this.renderCard(d)).join('')}
              </div>
            </section>
          `;
        }).join('')}
      </div>
    `;
  },
  
  renderCard(d) {
    const estadoColors = {
      'borrador': { badge: 'badge-warning', text: 'Borrador' },
      'generado': { badge: 'badge-info', text: 'Generado' },
      'aprobado': { badge: 'badge-success', text: 'Aprobado' },
      'firmado': { badge: 'badge-success', text: 'Firmado' }
    };
    const estado = estadoColors[d.estado] || { badge: 'badge-info', text: d.estado };
    
    return `
      <div class="reunion-card" style="cursor: pointer;" onclick="Documentos.verDetalle('${d.id}')">
        <div class="reunion-header">
          <div class="reunion-cliente">${Utils.escape(d.template_key || 'Documento')}</div>
          <div class="reunion-badges">
            <span class="badge ${estado.badge}">${estado.text}</span>
          </div>
        </div>
        <div class="reunion-meta">
          <span>📅 ${Utils.formatDate(d.fecha_creacion)}</span>
          ${d.ruta_pdf ? '<span>📄 PDF listo</span>' : '<span>⏳ Generando...</span>'}
        </div>
      </div>
    `;
  },
  
  verDetalle(id) {
    const doc = this.documentos.find(d => d.id === id);
    if (!doc) return;
    
    App.showToast(`Documento: ${doc.template_key}`, 'info');
    // Implementar vista detalle
  },
  
  showCreateModal() {
    App.showToast('Generar documento desde una reunión', 'info');
    App.navigate('reuniones');
  }
};