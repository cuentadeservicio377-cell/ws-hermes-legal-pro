// js/reuniones.js — Reuniones con wizard de 3 pasos
// Willow Legal Pro v3.0 — Mobile-first, flujo centrado en reuniones

const Reuniones = {
  reuniones: [],
  matters: [],
  currentWizardStep: 1,
  wizardData: {},
  
  async render() {
    const container = document.getElementById('reuniones-content');
    
    container.innerHTML = `
      <div class="empty-state">
        <div class="icon">🎤</div>
        <h3>Cargando reuniones...</h3>
      </div>
    `;
    
    try {
      const [reunionesData, mattersData] = await Promise.all([
        API.reuniones(),
        API.matters()
      ]);
      
      this.reuniones = reunionesData || [];
      this.matters = mattersData || [];
      
      this.renderList();
    } catch (err) {
      console.error('Error cargando reuniones:', err);
      container.innerHTML = `
        <div class="empty-state">
          <div class="icon">⚠️</div>
          <h3>Error de conexión</h3>
          <p>No se pudieron cargar las reuniones</p>
          <button class="btn btn-primary mt-md" onclick="Reuniones.render()">Reintentar</button>
        </div>
      `;
    }
  },
  
  renderList() {
    const container = document.getElementById('reuniones-content');
    const pendientes = this.reuniones.filter(r => r.estado !== 'procesada');
    const procesadas = this.reuniones.filter(r => r.estado === 'procesada');
    
    if (this.reuniones.length === 0) {
      container.innerHTML = `
        <div class="empty-state">
          <div class="icon">🎤</div>
          <h3>No hay reuniones</h3>
          <p>Registra tu primera reunión para empezar a trabajar</p>
          <button class="btn btn-primary mt-lg" onclick="Reuniones.showCreateModal()">
            + Nueva Reunión
          </button>
        </div>
      `;
      return;
    }
    
    container.innerHTML = `
      <div style="display: flex; flex-direction: column; gap: 16px;">
        ${pendientes.length > 0 ? `
          <section>
            <div class="section-header">
              <div>
                <div class="section-title">Pendientes de procesar</div>
                <div class="section-subtitle">${pendientes.length} reuniones</div>
              </div>
            </div>
            <div style="display: flex; flex-direction: column; gap: 12px;">
              ${pendientes.map(r => this.renderCard(r)).join('')}
            </div>
          </section>
        ` : ''}
        
        ${procesadas.length > 0 ? `
          <section>
            <div class="section-header">
              <div>
                <div class="section-title">Procesadas</div>
                <div class="section-subtitle">${procesadas.length} reuniones</div>
              </div>
            </div>
            <div style="display: flex; flex-direction: column; gap: 12px;">
              ${procesadas.slice(0, 3).map(r => this.renderCard(r)).join('')}
            </div>
          </section>
        ` : ''}
      </div>
    `;
  },
  
  renderCard(r) {
    const docsCount = r.documentos_necesarios?.length || 0;
    const acuerdosCount = r.acuerdos?.length || 0;
    const plazosCount = r.plazos?.length || 0;
    
    return `
      <div class="reunion-card ${r.estado || 'pendiente'}" onclick="Reuniones.showDetailModal('${r.id}')">
        <div class="reunion-header">
          <div class="reunion-cliente">${Utils.escape(r.cliente || 'Sin cliente')}</div>
          <div class="reunion-badges">
            ${r.estado === 'procesada' 
              ? '<span class="badge badge-success">✓ Procesada</span>'
              : '<span class="badge badge-warning">⏳ Pendiente</span>'
            }
            ${r.matter_id ? `<span class="badge badge-info">${r.matter_id}</span>` : ''}
          </div>
        </div>
        
        <div class="reunion-meta">
          <span>📅 ${Utils.formatDate(r.fecha)}</span>
          ${r.meet_url ? '<span>📹 Meet</span>' : ''}
          ${docsCount > 0 ? `<span>📄 ${docsCount} docs</span>` : ''}
          ${acuerdosCount > 0 ? `<span>✅ ${acuerdosCount} acuerdos</span>` : ''}
          ${plazosCount > 0 ? `<span>⏰ ${plazosCount} plazos</span>` : ''}
        </div>
        
        ${r.resumen ? `
          <div class="reunion-resumen">${Utils.escape(r.resumen)}</div>
        ` : ''}
      </div>
    `;
  },
  
  // ========== WIZARD: PASO 1 — Datos básicos ==========
  showCreateModal() {
    this.currentWizardStep = 1;
    this.wizardData = {};
    
    const matterOptions = this.matters.map(m => 
      `<option value="${m.id}">${m.id} — ${m.cliente}</option>`
    ).join('');
    
    const modalContent = `
      <div class="modal-header">
        <div class="modal-title">🎤 Nueva Reunión</div>
        <button class="modal-close" onclick="App.closeModal()">&times;</button>
      </div>
      
      ${this.renderWizardHeader(1)}
      
      <div class="form-group">
        <label class="form-label">Matter existente</label>
        <select class="form-select" id="wizard-matter" onchange="Reuniones.handleMatterSelect()">
          <option value="">Seleccionar matter...</option>
          ${matterOptions}
        </select>
      </div>
      
      <div class="form-group" id="nuevo-cliente-group">
        <label class="form-label">O cliente nuevo</label>
        <input type="text" class="form-input" id="wizard-cliente" placeholder="Nombre del cliente">
      </div>
      
      <div class="form-group">
        <label class="form-label">Fecha</label>
        <input type="date" class="form-input" id="wizard-fecha" value="${new Date().toISOString().split('T')[0]}">
      </div>
      
      <div class="form-group">
        <label class="form-label">URL de Google Meet</label>
        <input type="url" class="form-input" id="wizard-meet" placeholder="https://meet.google.com/...">
      </div>
      
      <div class="modal-footer">
        <button class="btn btn-secondary" onclick="App.closeModal()">Cancelar</button>
        <button class="btn btn-primary" onclick="Reuniones.goToStep(2)">Continuar →</button>
      </div>
    `;
    
    App.openModal(modalContent);
  },
  
  renderWizardHeader(step) {
    return `
      <div class="wizard-header">
        <div class="wizard-step ${step === 1 ? 'active' : step > 1 ? 'completed' : ''}">
          <div class="wizard-step-number">${step > 1 ? '✓' : '1'}</div>
          <span>Datos</span>
        </div>
        <div class="wizard-step-divider"></div>
        <div class="wizard-step ${step === 2 ? 'active' : step > 2 ? 'completed' : ''}">
          <div class="wizard-step-number">${step > 2 ? '✓' : '2'}</div>
          <span>Notas</span>
        </div>
        <div class="wizard-step-divider"></div>
        <div class="wizard-step ${step === 3 ? 'active' : ''}">
          <div class="wizard-step-number">3</div>
          <span>Resultados</span>
        </div>
      </div>
    `;
  },
  
  handleMatterSelect() {
    const matterId = document.getElementById('wizard-matter').value;
    const clienteInput = document.getElementById('wizard-cliente');
    
    if (matterId) {
      const matter = this.matters.find(m => m.id === matterId);
      if (matter) {
        clienteInput.value = matter.cliente || '';
        clienteInput.disabled = true;
      }
    } else {
      clienteInput.value = '';
      clienteInput.disabled = false;
    }
  },
  
  // ========== WIZARD: PASO 2 — Transcript ==========
  goToStep(step) {
    if (step === 2) {
      // Validar paso 1
      const matterId = document.getElementById('wizard-matter').value;
      const cliente = document.getElementById('wizard-cliente').value.trim();
      const fecha = document.getElementById('wizard-fecha').value;
      
      if (!matterId && !cliente) {
        App.showToast('Selecciona un matter o escribe el nombre del cliente', 'error');
        return;
      }
      if (!fecha) {
        App.showToast('La fecha es obligatoria', 'error');
        return;
      }
      
      this.wizardData = {
        matter_id: matterId || null,
        cliente: cliente,
        fecha: fecha,
        meet_url: document.getElementById('wizard-meet').value.trim()
      };
    }
    
    if (step === 3) {
      this.wizardData.transcript = document.getElementById('wizard-transcript').value.trim();
      this.wizardData.resumen = document.getElementById('wizard-resumen').value.trim();
    }
    
    this.currentWizardStep = step;
    
    if (step === 2) {
      this.renderStep2();
    } else if (step === 3) {
      this.renderStep3();
    }
  },
  
  renderStep2() {
    const modalContent = `
      <div class="modal-header">
        <div class="modal-title">🎤 ${Utils.escape(this.wizardData.cliente)}</div>
        <button class="modal-close" onclick="App.closeModal()">&times;</button>
      </div>
      
      ${this.renderWizardHeader(2)}
      
      <div class="form-group">
        <label class="form-label">Transcript / Notas de la reunión</label>
        <textarea class="form-textarea" id="wizard-transcript" rows="8" 
          placeholder="Pega aquí el transcript de Google Meet o escribe las notas de la reunión..."></textarea>
      </div>
      
      <div class="form-group">
        <label class="form-label">Resumen ejecutivo (opcional)</label>
        <textarea class="form-textarea" id="wizard-resumen" rows="3" 
          placeholder="Resumen breve de los puntos clave..."></textarea>
      </div>
      
      <div style="background: var(--surface-hover); border-radius: var(--radius-md); padding: 16px; margin-bottom: 16px;">
        <div style="font-size: 0.875rem; font-weight: 600; color: var(--legal-blue); margin-bottom: 8px;">
          💡 Tip
        </div>
        <div style="font-size: 0.875rem; color: var(--ink-muted);">
          Puedes pegar el transcript completo y el sistema extraerá automáticamente acuerdos, documentos sugeridos y plazos.
        </div>
      </div>
      
      <div class="modal-footer">
        <button class="btn btn-secondary" onclick="Reuniones.goToStep(1)">← Atrás</button>
        <button class="btn btn-primary" onclick="Reuniones.processAndGoToStep3()">⚡ Procesar con IA</button>
        <button class="btn btn-secondary" onclick="Reuniones.goToStep(3)">Saltar →</button>
      </div>
    `;
    
    App.openModal(modalContent);
  },
  
  async processAndGoToStep3() {
    const transcript = document.getElementById('wizard-transcript').value.trim();
    
    if (!transcript) {
      App.showToast('Escribe o pega el transcript primero', 'error');
      return;
    }
    
    App.showToast('Procesando con IA...', 'info');
    
    // Simular procesamiento (en producción, llamar al backend)
    // Por ahora, extraer palabras clave simples
    const palabrasClave = this.extractKeywords(transcript);
    
    this.wizardData.transcript = transcript;
    this.wizardData.resumen = document.getElementById('wizard-resumen').value.trim();
    this.wizardData.acuerdos = palabrasClave.acuerdos;
    this.wizardData.documentos_necesarios = palabrasClave.documentos;
    this.wizardData.plazos = palabrasClave.plazos;
    
    this.goToStep(3);
  },
  
  extractKeywords(text) {
    // Procesamiento simple local (en producción: llamada al backend)
    const acuerdos = [];
    const documentos = [];
    const plazos = [];
    
    // Detectar acuerdos
    if (text.match(/pagar|anticipo|honorarios|costos/i)) {
      acuerdos.push('Pagar anticipo/honorarios');
    }
    if (text.match(/contrato|acuerdo|pactar/i)) {
      acuerdos.push('Enviar contrato');
      documentos.push('prestacion_servicios');
    }
    if (text.match(/confidencial|secreto|no divulgar/i)) {
      acuerdos.push('Firmar confidencialidad');
      documentos.push('nda');
    }
    if (text.match(/carta|oficio|notificar/i)) {
      acuerdos.push('Enviar carta/oficio');
    }
    
    // Detectar plazos
    const fechaRegex = /(\d{1,2})\s+de\s+(\w+)|(\d{1,2})\/(\d{1,2})\/(\d{4})/gi;
    const fechas = text.match(fechaRegex);
    if (fechas) {
      fechas.slice(0, 2).forEach((f, i) => {
        plazos.push({
          descripcion: `Acción ${i + 1}`,
          fecha: f
        });
      });
    }
    
    return { acuerdos, documentos, plazos };
  },
  
  // ========== WIZARD: PASO 3 — Resultados ==========
  renderStep3() {
    const { acuerdos, documentos_necesarios, plazos } = this.wizardData;
    
    const modalContent = `
      <div class="modal-header">
        <div class="modal-title">✅ Resultados</div>
        <button class="modal-close" onclick="App.closeModal()">&times;</button>
      </div>
      
      ${this.renderWizardHeader(3)}
      
      ${acuerdos?.length > 0 ? `
        <div style="margin-bottom: 24px;">
          <div style="font-size: 0.875rem; font-weight: 600; color: var(--ink-muted); margin-bottom: 12px; text-transform: uppercase; letter-spacing: 0.08em;">
            Acuerdos detectados
          </div>
          <div style="display: flex; flex-direction: column; gap: 8px;">
            ${acuerdos.map(a => `
              <div style="display: flex; align-items: center; gap: 12px; padding: 12px; background: var(--surface-hover); border-radius: var(--radius-md);">
                <input type="checkbox" checked style="width: 20px; height: 20px; accent-color: var(--legal-blue);">
                <span>${Utils.escape(a)}</span>
              </div>
            `).join('')}
          </div>
        </div>
      ` : ''}
      
      ${documentos_necesarios?.length > 0 ? `
        <div style="margin-bottom: 24px;">
          <div style="font-size: 0.875rem; font-weight: 600; color: var(--ink-muted); margin-bottom: 12px; text-transform: uppercase; letter-spacing: 0.08em;">
            Documentos sugeridos
          </div>
          <div style="display: flex; flex-direction: column; gap: 8px;">
            ${documentos_necesarios.map(d => `
              <div class="action-card" onclick="Reuniones.generarDocumento('${d}')">
                <div class="action-icon" style="background: var(--legal-blue-muted);">📄</div>
                <div class="action-content">
                  <div class="action-title">${Utils.escape(d.replace('_', ' ').toUpperCase())}</div>
                  <div class="action-meta">Click para generar</div>
                </div>
                <div class="action-arrow">›</div>
              </div>
            `).join('')}
          </div>
        </div>
      ` : ''}
      
      ${plazos?.length > 0 ? `
        <div style="margin-bottom: 24px;">
          <div style="font-size: 0.875rem; font-weight: 600; color: var(--ink-muted); margin-bottom: 12px; text-transform: uppercase; letter-spacing: 0.08em;">
            Plazos detectados
          </div>
          <div style="display: flex; flex-direction: column; gap: 8px;">
            ${plazos.map(p => `
              <div class="action-card">
                <div class="action-icon" style="background: var(--warning);">⏰</div>
                <div class="action-content">
                  <div class="action-title">${Utils.escape(p.descripcion)}</div>
                  <div class="action-meta">${Utils.escape(p.fecha)}</div>
                </div>
              </div>
            `).join('')}
          </div>
        </div>
      ` : ''}
      
      <div class="modal-footer">
        <button class="btn btn-secondary" onclick="Reuniones.goToStep(2)">← Atrás</button>
        <button class="btn btn-primary" onclick="Reuniones.finalizarWizard()">💾 Guardar Reunión</button>
      </div>
    `;
    
    App.openModal(modalContent);
  },
  
  async finalizarWizard() {
    try {
      App.showToast('Guardando reunión...', 'info');
      
      const result = await API.crearReunion({
        matter_id: this.wizardData.matter_id,
        cliente: this.wizardData.cliente,
        fecha: this.wizardData.fecha,
        meet_url: this.wizardData.meet_url,
        transcript: this.wizardData.transcript,
        resumen: this.wizardData.resumen,
        acuerdos: this.wizardData.acuerdos,
        documentos_necesarios: this.wizardData.documentos_necesarios,
        plazos: this.wizardData.plazos
      });
      
      App.closeModal();
      App.showToast('✅ Reunión guardada exitosamente', 'success');
      
      // Recargar lista
      await this.render();
      
      // Actualizar dashboard
      Dashboard.render();
      
    } catch (err) {
      console.error('Error guardando reunión:', err);
      App.showToast('Error al guardar: ' + err.message, 'error');
    }
  },
  
  generarDocumento(templateKey) {
    App.showToast(`Generando documento: ${templateKey}...`, 'info');
    // Implementar generación
  },
  
  // ========== DETALLE ==========
  showDetailModal(id) {
    const reunion = this.reuniones.find(r => r.id === id);
    if (!reunion) return;
    
    const modalContent = `
      <div class="modal-header">
        <div class="modal-title">🎤 ${Utils.escape(reunion.cliente)}</div>
        <button class="modal-close" onclick="App.closeModal()">&times;</button>
      </div>
      
      <div style="display: flex; flex-direction: column; gap: 16px;">
        <div class="reunion-badges">
          ${reunion.estado === 'procesada' 
            ? '<span class="badge badge-success">✓ Procesada</span>'
            : '<span class="badge badge-warning">⏳ Pendiente</span>'
          }
          ${reunion.matter_id ? `<span class="badge badge-info">${reunion.matter_id}</span>` : ''}
        </div>
        
        <div class="reunion-meta">
          <span>📅 ${Utils.formatDate(reunion.fecha)}</span>
          ${reunion.meet_url ? `<span>📹 <a href="${reunion.meet_url}" target="_blank">Meet</a></span>` : ''}
        </div>
        
        ${reunion.resumen ? `
          <div>
            <div style="font-size: 0.875rem; font-weight: 600; color: var(--ink-muted); margin-bottom: 8px;">Resumen</div>
            <div style="padding: 16px; background: var(--surface-hover); border-radius: var(--radius-md); font-size: 0.9375rem; line-height: 1.5;">
              ${Utils.escape(reunion.resumen)}
            </div>
          </div>
        ` : ''}
        
        ${reunion.acuerdos?.length > 0 ? `
          <div>
            <div style="font-size: 0.875rem; font-weight: 600; color: var(--ink-muted); margin-bottom: 8px;">Acuerdos</div>
            <div style="display: flex; flex-direction: column; gap: 8px;">
              ${reunion.acuerdos.map(a => `
                <div style="padding: 12px; background: var(--surface-hover); border-radius: var(--radius-md);">
                  ✅ ${Utils.escape(a)}
                </div>
              `).join('')}
            </div>
          </div>
        ` : ''}
        
        ${reunion.documentos_necesarios?.length > 0 ? `
          <div>
            <div style="font-size: 0.875rem; font-weight: 600; color: var(--ink-muted); margin-bottom: 8px;">Documentos sugeridos</div>
            <div style="display: flex; flex-direction: column; gap: 8px;">
              ${reunion.documentos_necesarios.map(d => `
                <div class="action-card" style="padding: 12px;">
                  <div class="action-icon" style="width: 36px; height: 36px; font-size: 1.25rem;">📄</div>
                  <div class="action-content">
                    <div class="action-title" style="font-size: 0.9375rem;">${Utils.escape(d)}</div>
                  </div>
                </div>
              `).join('')}
            </div>
          </div>
        ` : ''}
      </div>
      
      <div class="modal-footer">
        ${reunion.estado !== 'procesada' ? `
          <button class="btn btn-primary" onclick="Reuniones.procesar('${reunion.id}')">⚡ Procesar</button>
        ` : ''}
        <button class="btn btn-danger" onclick="Reuniones.eliminar('${reunion.id}')">🗑️ Eliminar</button>
      </div>
    `;
    
    App.openModal(modalContent);
  },
  
  async procesar(id) {
    App.showToast('Procesando reunión...', 'info');
    // Implementar
  },
  
  async eliminar(id) {
    if (!confirm('¿Eliminar esta reunión?')) return;
    
    try {
      await API.eliminarReunion(id);
      App.closeModal();
      App.showToast('Reunión eliminada', 'success');
      await this.render();
    } catch (err) {
      App.showToast('Error al eliminar', 'error');
    }
  }
};
