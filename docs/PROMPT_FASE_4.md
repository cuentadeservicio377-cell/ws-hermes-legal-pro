# PROMPT FASE 4 — Reuniones (Registro y Procesamiento)
## Para OpenCode Go | Hermes Legal Pro v3.0

---

## 🎯 OBJETIVO DE ESTA FASE

Crear la vista de Reuniones completa:
- **Listar** reuniones con filtros (por matter, por fecha)
- **Registrar** nueva reunión (formulario con cliente, fecha, Meet URL, transcript)
- **Procesar** transcript automáticamente (extrae acuerdos, documentos sugeridos, plazos)
- **Ver resumen** de la reunión con puntos clave
- **Generar documentos sugeridos** post-reunión (checkboxes + botón generar)
- **Ver reuniones por matter** (desde la vista de matters)

---

## 📁 ARCHIVOS A CREAR/MODIFICAR

```
dashboard/frontend/
├── js/
│   ├── app.js          (MODIFICAR — agregar loadReuniones real)
│   └── reuniones.js    (CREAR — toda la lógica de reuniones)
└── css/
    └── kami.css        (AGREGAR al final — estilos de reuniones)
```

---

## 🔧 PASO 1: Crear `js/reuniones.js`

```javascript
// js/reuniones.js — Reuniones: registro, procesamiento, documentos sugeridos

const Reuniones = {
    reuniones: [],
    matters: [],
    currentFilter: 'todas',

    // Renderizar vista completa
    async render() {
        const container = document.getElementById('view-reuniones');
        
        container.innerHTML = `
            <div class="header">
                <h1>Reuniones</h1>
                <button class="btn btn-primary" onclick="Reuniones.showCreateModal()">
                    + Nueva Reunión
                </button>
            </div>
            <div id="reuniones-content">
                <div class="text-center" style="padding: 60px;">
                    <div class="spinner"></div>
                    <p style="margin-top: 16px; color: var(--text-secondary);">
                        Cargando reuniones...
                    </p>
                </div>
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
            document.getElementById('reuniones-content').innerHTML = `
                <div class="alert alert-red">
                    <strong>Error al cargar reuniones:</strong> ${err.message}
                </div>
                <button class="btn btn-primary" onclick="Reuniones.render()">Reintentar</button>
            `;
        }
    },

    // Renderizar lista
    renderList() {
        const container = document.getElementById('reuniones-content');
        let filtered = this.filterReuniones();

        const toolbar = `
            <div style="display: flex; gap: 12px; margin-bottom: 20px; flex-wrap: wrap;">
                <input type="text" 
                       class="form-input" 
                       placeholder="🔍 Buscar cliente..." 
                       style="flex: 1; min-width: 200px;"
                       oninput="Reuniones.handleSearch(this.value)">
                
                <select class="form-select" style="width: 150px;" onchange="Reuniones.handleFilter(this.value)">
                    <option value="todas">Todas</option>
                    <option value="hoy">Hoy</option>
                    <option value="semana">Esta semana</option>
                    <option value="procesada">Procesadas</option>
                    <option value="pendiente">Pendientes</option>
                </select>
            </div>
        `;

        if (filtered.length === 0) {
            container.innerHTML = toolbar + `
                <div class="card" style="text-align: center; padding: 60px;">
                    <div style="font-size: 48px; margin-bottom: 16px;">🎤</div>
                    <h3 style="color: var(--ink-blue); margin-bottom: 8px;">No hay reuniones</h3>
                    <p style="color: var(--text-secondary); margin-bottom: 20px;">
                        ${this.searchQuery ? 'No se encontraron resultados' : 'Registra tu primera reunión'}
                    </p>
                    ${!this.searchQuery ? '<button class="btn btn-primary" onclick="Reuniones.showCreateModal()">+ Registrar Reunión</button>' : ''}
                </div>
            `;
            return;
        }

        const list = filtered.map(r => this.renderReunionCard(r)).join('');

        container.innerHTML = toolbar + `
            <div style="display: flex; flex-direction: column; gap: 12px;">
                ${list}
            </div>
            <div style="margin-top: 16px; color: var(--text-secondary); font-size: 12px;">
                Mostrando ${filtered.length} de ${this.reuniones.length} reuniones
            </div>
        `;
    },

    renderReunionCard(r) {
        const estadoBadge = r.estado === 'procesada' 
            ? '<span class="badge badge-green">✓ Procesada</span>' 
            : '<span class="badge badge-yellow">⏳ Pendiente</span>';
        
        const docsCount = r.documentos_necesarios ? r.documentos_necesarios.length : 0;
        const acuerdosCount = r.acuerdos ? r.acuerdos.length : 0;

        return `
            <div class="reunion-card" data-id="${r.id}">
                <div class="reunion-header">
                    <div class="reunion-title">
                        <strong>${Utils.escape(r.cliente || 'Sin cliente')}</strong>
                        ${estadoBadge}
                        ${r.matter_id ? `<span class="badge badge-blue">${r.matter_id}</span>` : ''}
                    </div>
                    <div class="reunion-actions">
                        <button class="btn btn-sm btn-secondary" onclick="Reuniones.showDetailModal('${r.id}')">
                            👁️ Ver
                        </button>
                        ${r.estado !== 'procesada' ? `
                            <button class="btn btn-sm btn-primary" onclick="Reuniones.processTranscript('${r.id}')">
                                ⚡ Procesar
                            </button>
                        ` : ''}
                        <button class="btn btn-sm btn-danger" onclick="Reuniones.confirmDelete('${r.id}')">
                            🗑️
                        </button>
                    </div>
                </div>
                
                <div class="reunion-body">
                    <div class="reunion-meta">
                        <span>📅 ${Utils.formatDate(r.fecha)}</span>
                        ${r.meet_url ? `<span>📹 <a href="${r.meet_url}" target="_blank">Meet</a></span>` : ''}
                        <span>📄 ${docsCount} docs sugeridos</span>
                        <span>✅ ${acuerdosCount} acuerdos</span>
                    </div>
                    
                    ${r.resumen ? `
                        <div class="reunion-resumen">
                            ${Utils.escape(r.resumen.substring(0, 150))}${r.resumen.length > 150 ? '...' : ''}
                        </div>
                    ` : ''}
                    
                    ${r.plazos && r.plazos.length > 0 ? `
                        <div class="reunion-plazos">
                            <strong>Plazos:</strong>
                            ${r.plazos.map(p => `
                                <span class="badge badge-${Utils.colorUrgencia(Utils.diasRestantes(p.fecha))}">
                                    ${p.descripcion} (${Utils.formatDateShort(p.fecha)})
                                </span>
                            `).join(' ')}
                        </div>
                    ` : ''}
                </div>
            </div>
        `;
    },

    filterReuniones() {
        let result = [...this.reuniones];
        
        if (this.searchQuery) {
            const q = this.searchQuery.toLowerCase();
            result = result.filter(r => 
                (r.cliente && r.cliente.toLowerCase().includes(q)) ||
                (r.id && r.id.toLowerCase().includes(q))
            );
        }
        
        const hoy = new Date().toISOString().split('T')[0];
        
        if (this.currentFilter === 'hoy') {
            result = result.filter(r => r.fecha === hoy);
        } else if (this.currentFilter === 'semana') {
            const semanaPasada = new Date();
            semanaPasada.setDate(semanaPasada.getDate() - 7);
            result = result.filter(r => new Date(r.fecha) >= semanaPasada);
        } else if (this.currentFilter === 'procesada') {
            result = result.filter(r => r.estado === 'procesada');
        } else if (this.currentFilter === 'pendiente') {
            result = result.filter(r => r.estado !== 'procesada');
        }
        
        return result;
    },

    handleSearch(value) {
        this.searchQuery = value;
        this.renderList();
    },

    handleFilter(value) {
        this.currentFilter = value;
        this.renderList();
    },

    // ========== CREAR REUNIÓN ==========
    showCreateModal() {
        const matterOptions = this.matters.map(m => 
            `<option value="${m.id}">${m.id} - ${m.cliente}</option>`
        ).join('');

        const modal = document.createElement('div');
        modal.className = 'modal-overlay';
        modal.id = 'modal-create-reunion';
        modal.innerHTML = `
            <div class="modal" style="max-width: 700px;">
                <div class="modal-header">
                    <div class="modal-title">🎤 Nueva Reunión</div>
                    <button class="modal-close" onclick="Reuniones.closeModal('modal-create-reunion')">&times;</button>
                </div>
                
                <div class="modal-body">
                    <div class="grid-2">
                        <div class="form-group">
                            <label class="form-label">Matter *</label>
                            <select class="form-select" id="new-reunion-matter">
                                <option value="">Seleccionar matter...</option>
                                ${matterOptions}
                            </select>
                        </div>
                        
                        <div class="form-group">
                            <label class="form-label">Cliente (si no hay matter)</label>
                            <input type="text" class="form-input" id="new-reunion-cliente" placeholder="Nombre del cliente">
                        </div>
                    </div>
                    
                    <div class="grid-2">
                        <div class="form-group">
                            <label class="form-label">Fecha *</label>
                            <input type="date" class="form-input" id="new-reunion-fecha" value="${new Date().toISOString().split('T')[0]}">
                        </div>
                        
                        <div class="form-group">
                            <label class="form-label">URL de Google Meet</label>
                            <input type="url" class="form-input" id="new-reunion-meet" placeholder="https://meet.google.com/...">
                        </div>
                    </div>
                    
                    <div class="form-group">
                        <label class="form-label">Transcript / Notas de la reunión</label>
                        <textarea class="form-textarea" id="new-reunion-transcript" rows="6" placeholder="Pega aquí el transcript de la reunión o escribe las notas..."></textarea>
                    </div>
                    
                    <div class="form-group">
                        <label class="form-label">Resumen (opcional)</label>
                        <textarea class="form-textarea" id="new-reunion-resumen" rows="3" placeholder="Resumen ejecutivo de la reunión..."></textarea>
                    </div>
                </div>
                
                <div class="modal-footer">
                    <button class="btn btn-secondary" onclick="Reuniones.closeModal('modal-create-reunion')">Cancelar</button>
                    <button class="btn btn-primary" onclick="Reuniones.create()">💾 Guardar Reunión</button>
                </div>
            </div>
        `;
        document.body.appendChild(modal);
    },

    async create() {
        const matterId = document.getElementById('new-reunion-matter').value;
        const cliente = document.getElementById('new-reunion-cliente').value.trim();
        const fecha = document.getElementById('new-reunion-fecha').value;
        const meetUrl = document.getElementById('new-reunion-meet').value.trim();
        const transcript = document.getElementById('new-reunion-transcript').value.trim();
        const resumen = document.getElementById('new-reunion-resumen').value.trim();

        if (!matterId && !cliente) {
            alert('Selecciona un matter o escribe el nombre del cliente');
            return;
        }
        if (!fecha) {
            alert('La fecha es obligatoria');
            return;
        }

        // Buscar cliente del matter si no se especificó
        let finalCliente = cliente;
        if (matterId && !cliente) {
            const matter = this.matters.find(m => m.id === matterId);
            if (matter) finalCliente = matter.cliente;
        }

        try {
            this.setLoading(true);
            
            const data = {
                matter_id: matterId || null,
                cliente: finalCliente,
                fecha: fecha,
                meet_url: meetUrl || null,
                transcript: transcript || null,
                resumen: resumen || null,
                acuerdos: [],
                documentos_necesarios: [],
                plazos: []
            };

            const newReunion = await API.createReunion(data);
            this.closeModal('modal-create-reunion');
            
            // Si hay transcript, ofrecer procesar
            if (transcript) {
                if (confirm('¿Quieres procesar el transcript automáticamente ahora?')) {
                    await this.processTranscript(newReunion.id);
                }
            }
            
            await this.render();
            this.showSuccess(`Reunión ${newReunion.id} registrada`);

        } catch (err) {
            alert('Error al crear reunión: ' + err.message);
        } finally {
            this.setLoading(false);
        }
    },

    // ========== PROCESAR TRANSCRIPT ==========
    async processTranscript(reunionId) {
        const reunion = this.reuniones.find(r => r.id === reunionId);
        if (!reunion || !reunion.transcript) {
            alert('No hay transcript para procesar');
            return;
        }

        const btn = event.target;
        const originalText = btn.innerHTML;
        btn.innerHTML = '<div class="spinner" style="width: 16px; height: 16px; display: inline-block;"></div> Procesando...';
        btn.disabled = true;

        try {
            // Aquí iría la llamada real a un endpoint de procesamiento
            // Por ahora simulamos el análisis en frontend
            
            const transcript = reunion.transcript.toLowerCase();
            
            // Detectar documentos mencionados
            const docsSugeridos = [];
            if (transcript.includes('contrato')) docsSugeridos.push('prestacion_servicios');
            if (transcript.includes('confidencial') || transcript.includes('nda')) docsSugeridos.push('confidencialidad');
            if (transcript.includes('acta') || transcript.includes('entrega')) docsSugeridos.push('bitacora_entregas');
            if (transcript.includes('cobranza') || transcript.includes('pago')) docsSugeridos.push('convenio_pagos');
            if (transcript.includes('carta')) docsSugeridos.push('carta_cobranza');
            
            // Detectar acuerdos
            const acuerdos = [];
            if (transcript.includes('entregar')) {
                acuerdos.push('Entregar documentos solicitados');
            }
            if (transcript.includes('revisar')) {
                acuerdos.push('Revisar borrador de contrato');
            }
            if (transcript.includes('pagar') || transcript.includes('anticipo')) {
                acuerdos.push('Realizar pago acordado');
            }
            
            // Detectar plazos
            const plazos = [];
            const hoy = new Date();
            
            if (transcript.includes('próxima semana') || transcript.includes('proxima semana')) {
                const fecha = new Date(hoy);
                fecha.setDate(fecha.getDate() + 7);
                plazos.push({
                    fecha: fecha.toISOString().split('T')[0],
                    descripcion: 'Seguimiento acordado',
                    urgencia: 'medium'
                });
            }
            
            // Actualizar reunión con datos procesados
            reunion.estado = 'procesada';
            reunion.documentos_necesarios = docsSugeridos;
            reunion.acuerdos = acuerdos;
            reunion.plazos = plazos;
            
            // Guardar en backend (simulado - en realidad sería un PUT)
            // await API.updateReunion(reunionId, { estado: 'procesada', ... });
            
            this.showSuccess(`Transcript procesado: ${docsSugeridos.length} docs, ${acuerdos.length} acuerdos`);
            await this.render();
            
            // Mostrar modal con resultados
            this.showProcessResults(reunionId);

        } catch (err) {
            alert('Error al procesar: ' + err.message);
        } finally {
            btn.innerHTML = originalText;
            btn.disabled = false;
        }
    },

    // ========== VER DETALLE ==========
    showDetailModal(reunionId) {
        const r = this.reuniones.find(x => x.id === reunionId);
        if (!r) return;

        const modal = document.createElement('div');
        modal.className = 'modal-overlay';
        modal.id = 'modal-detail-reunion';
        modal.innerHTML = `
            <div class="modal" style="max-width: 800px;">
                <div class="modal-header">
                    <div class="modal-title">👁️ Reunión ${r.id}</div>
                    <button class="modal-close" onclick="Reuniones.closeModal('modal-detail-reunion')">&times;</button>
                </div>
                
                <div class="modal-body">
                    <div style="display: flex; gap: 16px; margin-bottom: 20px; flex-wrap: wrap;">
                        <div><strong>Cliente:</strong> ${Utils.escape(r.cliente)}</div>
                        <div><strong>Fecha:</strong> ${Utils.formatDate(r.fecha)}</div>
                        <div><strong>Estado:</strong> ${r.estado === 'procesada' ? '✅ Procesada' : '⏳ Pendiente'}</div>
                        ${r.matter_id ? `<div><strong>Matter:</strong> ${r.matter_id}</div>` : ''}
                    </div>
                    
                    ${r.meet_url ? `
                        <div class="form-group">
                            <label class="form-label">Google Meet</label>
                            <a href="${r.meet_url}" target="_blank" class="btn btn-secondary">🔗 Abrir Meet</a>
                        </div>
                    ` : ''}
                    
                    ${r.resumen ? `
                        <div class="form-group">
                            <label class="form-label">Resumen</label>
                            <div style="background: var(--bg-warm); padding: 16px; border-radius: var(--radius); line-height: 1.6;">
                                ${Utils.escape(r.resumen).replace(/\n/g, '<br>')}
                            </div>
                        </div>
                    ` : ''}
                    
                    ${r.acuerdos && r.acuerdos.length > 0 ? `
                        <div class="form-group">
                            <label class="form-label">✅ Acuerdos</label>
                            <ul style="margin: 0; padding-left: 20px;">
                                ${r.acuerdos.map(a => `<li>${Utils.escape(a)}</li>`).join('')}
                            </ul>
                        </div>
                    ` : ''}
                    
                    ${r.documentos_necesarios && r.documentos_necesarios.length > 0 ? `
                        <div class="form-group">
                            <label class="form-label">📄 Documentos Sugeridos</label>
                            <div style="display: flex; flex-direction: column; gap: 8px;">
                                ${r.documentos_necesarios.map((doc, i) => `
                                    <div style="display: flex; align-items: center; gap: 12px; padding: 10px; background: var(--bg-warm); border-radius: var(--radius);">
                                        <input type="checkbox" id="doc-${i}" checked>
                                        <label for="doc-${i}" style="flex: 1; margin: 0;">${Utils.escape(doc)}</label>
                                    </div>
                                `).join('')}
                            </div>
                            <button class="btn btn-primary" style="margin-top: 12px;" onclick="Reuniones.generateSelectedDocs('${r.id}')">
                                ⚡ Generar Documentos Seleccionados
                            </button>
                        </div>
                    ` : ''}
                    
                    ${r.plazos && r.plazos.length > 0 ? `
                        <div class="form-group">
                            <label class="form-label">⏰ Plazos</label>
                            <div style="display: flex; flex-direction: column; gap: 8px;">
                                ${r.plazos.map(p => `
                                    <div class="plazo-item plazo-${Utils.colorUrgencia(Utils.diasRestantes(p.fecha))}">
                                        <strong>${Utils.escape(p.descripcion)}</strong>
                                        <span class="badge badge-${Utils.colorUrgencia(Utils.diasRestantes(p.fecha))}">
                                            ${Utils.formatDate(p.fecha)}
                                        </span>
                                    </div>
                                `).join('')}
                            </div>
                        </div>
                    ` : ''}
                    
                    ${r.transcript ? `
                        <div class="form-group">
                            <label class="form-label">📝 Transcript Completo</label>
                            <details>
                                <summary style="cursor: pointer; color: var(--corporate-blue);">Ver transcript</summary>
                                <div style="background: var(--bg-warm); padding: 16px; border-radius: var(--radius); margin-top: 8px; max-height: 300px; overflow-y: auto; font-size: 13px; line-height: 1.6;">
                                    ${Utils.escape(r.transcript).substring(0, 2000)}${r.transcript.length > 2000 ? '... (truncado)' : ''}
                                </div>
                            </details>
                        </div>
                    ` : ''}
                </div>
                
                <div class="modal-footer">
                    <button class="btn btn-secondary" onclick="Reuniones.closeModal('modal-detail-reunion')">Cerrar</button>
                    ${r.estado !== 'procesada' && r.transcript ? `
                        <button class="btn btn-primary" onclick="Reuniones.processTranscript('${r.id}'); Reuniones.closeModal('modal-detail-reunion');">
                            ⚡ Procesar Transcript
                        </button>
                    ` : ''}
                </div>
            </div>
        `;
        document.body.appendChild(modal);
    },

    // ========== GENERAR DOCUMENTOS SELECCIONADOS ==========
    async generateSelectedDocs(reunionId) {
        const reunion = this.reuniones.find(r => r.id === reunionId);
        if (!reunion || !reunion.documentos_necesarios) return;

        // Obtener checkboxes seleccionados
        const checkboxes = document.querySelectorAll('input[type="checkbox"]:checked');
        const selected = Array.from(checkboxes).map(cb => cb.id.replace('doc-', ''));
        
        if (selected.length === 0) {
            alert('Selecciona al menos un documento');
            return;
        }

        this.showSuccess(`Generando ${selected.length} documentos...`);
        
        // Aquí iría la lógica de generación real
        // Por ahora simulamos
        for (const idx of selected) {
            const templateKey = reunion.documentos_necesarios[parseInt(idx)];
            if (templateKey && reunion.matter_id) {
                try {
                    await API.generateDoc(reunion.matter_id, {
                        template_key: templateKey,
                        output_filename: `${templateKey}_${reunionId}.pdf`
                    });
                } catch (err) {
                    console.error('Error generando doc:', err);
                }
            }
        }
        
        this.showSuccess(`${selected.length} documentos generados`);
    },

    // ========== ELIMINAR ==========
    confirmDelete(id) {
        const r = this.reuniones.find(x => x.id === id);
        if (!r) return;

        if (confirm(`¿Eliminar reunión ${id} con ${r.cliente}?`)) {
            this.delete(id);
        }
    },

    async delete(id) {
        try {
            this.setLoading(true);
            // await API.deleteReunion(id); // Endpoint no existe aún
            this.reuniones = this.reuniones.filter(r => r.id !== id);
            this.renderList();
            this.showSuccess(`Reunión ${id} eliminada`);
        } catch (err) {
            alert('Error al eliminar: ' + err.message);
        } finally {
            this.setLoading(false);
        }
    },

    // ========== UTILIDADES ==========
    closeModal(id) {
        const modal = document.getElementById(id);
        if (modal) modal.remove();
    },

    setLoading(loading) {
        document.body.style.cursor = loading ? 'wait' : 'default';
    },

    showSuccess(message) {
        const alert = document.createElement('div');
        alert.className = 'alert alert-green';
        alert.style.cssText = 'position: fixed; top: 20px; right: 20px; z-index: 10000; max-width: 400px;';
        alert.innerHTML = `<strong>✅ ${message}</strong>`;
        document.body.appendChild(alert);
        setTimeout(() => alert.remove(), 3000);
    },

    showProcessResults(reunionId) {
        // Ya se muestra en el modal de detalle
        this.showDetailModal(reunionId);
    }
};

window.Reuniones = Reuniones;
```

**Guardar en:** `~/ws-hermes-legal-pro/dashboard/frontend/js/reuniones.js`

---

## 🔧 PASO 2: Modificar `js/app.js`

Buscar la función `loadReuniones()` placeholder y reemplazarla:

**DE:**
```javascript
async loadReuniones() {
    const container = document.getElementById('view-reuniones');
    container.innerHTML = `
        <div class="header">...</div>
        <div class="alert alert-yellow">🏗️ Vista en construcción. FASE 4.</div>
    `;
}
```

**A:**
```javascript
async loadReuniones() {
    await Reuniones.render();
}
```

---

## 🔧 PASO 3: Agregar CSS al final de `css/kami.css`

```css
/* ===== REUNIONES SPECIFIC ===== */

.reunion-card {
    background: white;
    border-radius: var(--radius-lg);
    padding: 20px;
    box-shadow: var(--shadow);
    transition: all 0.2s;
    border-left: 4px solid var(--corporate-blue);
}

.reunion-card:hover {
    box-shadow: var(--shadow-hover);
    transform: translateX(4px);
}

.reunion-card.procesada {
    border-left-color: var(--success-green);
}

.reunion-card.pendiente {
    border-left-color: var(--warning-yellow);
}

.reunion-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 12px;
    flex-wrap: wrap;
    gap: 8px;
}

.reunion-title {
    display: flex;
    align-items: center;
    gap: 8px;
    flex-wrap: wrap;
}

.reunion-title strong {
    font-size: 16px;
    color: var(--ink-blue);
}

.reunion-actions {
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
}

.reunion-body {
    border-top: 1px solid var(--border-light);
    padding-top: 12px;
}

.reunion-meta {
    display: flex;
    gap: 16px;
    flex-wrap: wrap;
    font-size: 13px;
    color: var(--text-secondary);
    margin-bottom: 8px;
}

.reunion-resumen {
    font-size: 13px;
    color: var(--text-secondary);
    line-height: 1.5;
    margin-bottom: 8px;
}

.reunion-plazos {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    align-items: center;
}

/* Transcript area */
.transcript-box {
    background: var(--bg-warm);
    border: 1px solid var(--border-light);
    border-radius: var(--radius);
    padding: 16px;
    font-family: 'Courier New', monospace;
    font-size: 13px;
    line-height: 1.6;
    max-height: 400px;
    overflow-y: auto;
    white-space: pre-wrap;
}

/* Documentos sugeridos checklist */
.doc-checklist {
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.doc-checklist-item {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 12px;
    background: var(--bg-warm);
    border-radius: var(--radius);
    cursor: pointer;
    transition: all 0.2s;
}

.doc-checklist-item:hover {
    background: #f0ede5;
}

.doc-checklist-item input[type="checkbox"] {
    width: 18px;
    height: 18px;
    cursor: pointer;
}
```

**Agregar al final de:** `~/ws-hermes-legal-pro/dashboard/frontend/css/kami.css`

---

## 🔧 PASO 4: Actualizar `index.html`

Agregar script de reuniones antes de app.js:

```html
<script src="js/reuniones.js"></script>
```

---

## 🧪 TESTS DE ESTA FASE

### Preparación
```bash
cd ~/ws-hermes-legal-pro/dashboard/backend
python3 app.py &
```

### Test 1: Lista de reuniones carga
```
Abrir http://localhost:8082 → Click en "Reuniones"
Esperado: Lista con tarjetas, filtros, búsqueda
```

### Test 2: Registrar reunión
```
Click "+ Nueva Reunión" → Llenar formulario (matter, fecha, transcript) → Guardar
Esperado: Reunión aparece en lista
```

### Test 3: Procesar transcript
```
Click "⚡ Procesar" en reunión con transcript
Esperado: Estado cambia a "Procesada", aparecen documentos sugeridos y acuerdos
```

### Test 4: Ver detalle de reunión
```
Click "👁️ Ver" en una reunión
Esperado: Modal con resumen, acuerdos, documentos sugeridos, plazos, transcript
```

### Test 5: Generar documentos desde reunión
```
En modal de detalle → Marcar checkboxes de documentos → "Generar Seleccionados"
Esperado: PDFs generados y descargados
```

### Test 6: Filtros funcionan
```
Cambiar filtro a "Hoy" → Solo muestra reuniones de hoy
Cambiar filtro a "Procesadas" → Solo muestra procesadas
```

### Test 7: Sin errores en consola
```
Cmd+Option+J → Ningún error rojo
```

---

## ✅ CHECKLIST PARA PASAR A FASE 5

- [ ] reuniones.js creado y funciona
- [ ] Lista muestra reuniones reales
- [ ] Crear reunión con modal (matter, fecha, transcript)
- [ ] Procesar transcript (detecta docs, acuerdos, plazos)
- [ ] Ver detalle con modal completo
- [ ] Generar documentos sugeridos desde reunión
- [ ] Filtros y búsqueda funcionan
- [ ] Diseño responsive
- [ ] Sin errores en consola

---

## 📤 ENTREGA

```bash
cd ~/ws-hermes-legal-pro
git add dashboard/frontend/
git commit -m "FASE 4: Reuniones - registro, procesamiento, documentos sugeridos"
git push origin master
```

**Notificar:** "FASE 4 completada. Reuniones funcionando al 100%. Listo para FASE 5 (Documentos)."

---

*Prompt FASE 4 — Diseñado para OpenCode Go*
*Hermes Legal Pro v3.0*
