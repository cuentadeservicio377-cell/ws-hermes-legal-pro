// js/documentos.js — Documentos: generar, previsualizar, descargar, gestionar

const Documentos = {
    documentos: [],
    matters: [],
    templates: [],
    currentFilter: 'todos',

    // Renderizar vista completa
    async render() {
        const container = document.getElementById('view-documentos');
        
        container.innerHTML = `
            <div class="header">
                <h1>Documentos</h1>
                <button class="btn btn-primary" onclick="Documentos.showGenerateModal()">
                    + Generar Documento
                </button>
            </div>
            <div id="documentos-content">
                <div class="text-center" style="padding: 60px;">
                    <div class="spinner"></div>
                    <p style="margin-top: 16px; color: var(--text-secondary);">
                        Cargando documentos...
                    </p>
                </div>
            </div>
        `;

        try {
            const [docsData, mattersData, templatesData] = await Promise.all([
                API.documentos(),
                API.matters(),
                API.templates()
            ]);

            this.documentos = docsData || [];
            this.matters = mattersData || [];
            this.templates = (templatesData && templatesData.templates) ? templatesData.templates : [];

            this.renderList();

        } catch (err) {
            console.error('Error cargando documentos:', err);
            document.getElementById('documentos-content').innerHTML = `
                <div class="alert alert-red">
                    <strong>Error al cargar documentos:</strong> ${err.message}
                </div>
                <button class="btn btn-primary" onclick="Documentos.render()">Reintentar</button>
            `;
        }
    },

    // Renderizar lista
    renderList() {
        const container = document.getElementById('documentos-content');
        let filtered = this.filterDocumentos();

        const toolbar = `
            <div style="display: flex; gap: 12px; margin-bottom: 20px; flex-wrap: wrap;">
                <input type="text" 
                       class="form-input" 
                       placeholder="🔍 Buscar documento..." 
                       style="flex: 1; min-width: 200px;"
                       oninput="Documentos.handleSearch(this.value)">
                
                <select class="form-select" style="width: 150px;" onchange="Documentos.handleFilter(this.value)">
                    <option value="todos">Todos</option>
                    <option value="borrador">Borradores</option>
                    <option value="generado">Generados</option>
                    <option value="firmado">Firmados</option>
                </select>
            </div>
        `;

        if (filtered.length === 0) {
            container.innerHTML = toolbar + `
                <div class="card" style="text-align: center; padding: 60px;">
                    <div style="font-size: 48px; margin-bottom: 16px;">📄</div>
                    <h3 style="color: var(--ink-blue); margin-bottom: 8px;">No hay documentos</h3>
                    <p style="color: var(--text-secondary); margin-bottom: 20px;">
                        ${this.searchQuery ? 'No se encontraron resultados' : 'Genera tu primer documento legal'}
                    </p>
                    ${!this.searchQuery ? '<button class="btn btn-primary" onclick="Documentos.showGenerateModal()">+ Generar Documento</button>' : ''}
                </div>
            `;
            return;
        }

        const list = filtered.map(d => this.renderDocumentoCard(d)).join('');

        container.innerHTML = toolbar + `
            <div style="display: flex; flex-direction: column; gap: 12px;">
                ${list}
            </div>
            <div style="margin-top: 16px; color: var(--text-secondary); font-size: 12px;">
                Mostrando ${filtered.length} de ${this.documentos.length} documentos
            </div>
        `;
    },

    renderDocumentoCard(d) {
        const matter = this.matters.find(m => m.id === d.matter_id);
        const template = this.templates.find(t => t.key === d.template_key);
        
        const estadoColors = {
            borrador: 'yellow',
            generado: 'blue',
            firmado: 'green',
            archivado: 'gray'
        };
        const estadoBadge = `<span class="badge badge-${estadoColors[d.estado] || 'gray'}">${(d.estado || 'BORRADOR').toUpperCase()}</span>`;

        const icono = d.ruta_pdf ? '📄' : '📝';
        const nombre = d.ruta_pdf ? d.ruta_pdf.split('/').pop() : `${d.template_key || 'documento'}_${d.matter_id}.pdf`;

        return `
            <div class="documento-card" data-id="${d.id}">
                <div class="documento-header">
                    <div class="documento-title">
                        <span style="font-size: 24px;">${icono}</span>
                        <div>
                            <strong>${Utils.escape(nombre)}</strong>
                            ${estadoBadge}
                            ${matter ? `<span class="badge badge-blue">${matter.id}</span>` : ''}
                        </div>
                    </div>
                    <div class="documento-actions">
                        ${d.ruta_pdf ? `
                            <button class="btn btn-sm btn-secondary" onclick="Documentos.preview('${d.id}')">
                                👁️ Ver
                            </button>
                            <button class="btn btn-sm btn-primary" onclick="Documentos.download('${d.id}')">
                                ⬇️ Descargar
                            </button>
                        ` : `
                            <button class="btn btn-sm btn-primary" onclick="Documentos.regenerate('${d.id}')">
                                ⚡ Generar
                            </button>
                        `}
                        <select class="form-select btn-sm" style="width: 120px;" onchange="Documentos.changeEstado('${d.id}', this.value)"
                            ${d.estado === 'firmado' ? 'disabled' : ''}>
                            <option value="borrador" ${d.estado === 'borrador' ? 'selected' : ''}>Borrador</option>
                            <option value="generado" ${d.estado === 'generado' ? 'selected' : ''}>Generado</option>
                            <option value="firmado" ${d.estado === 'firmado' ? 'selected' : ''}>Firmado</option>
                            <option value="archivado" ${d.estado === 'archivado' ? 'selected' : ''}>Archivado</option>
                        </select>
                        <button class="btn btn-sm btn-danger" onclick="Documentos.confirmDelete('${d.id}')">
                            🗑️
                        </button>
                    </div>
                </div>
                
                <div class="documento-body">
                    <div class="documento-meta">
                        <span>📁 ${template ? template.label : d.template_key || 'Desconocido'}</span>
                        ${matter ? `<span>👤 ${Utils.escape(matter.cliente)}</span>` : ''}
                        <span>📅 ${Utils.formatDateShort(d.fecha_creacion)}</span>
                        ${d.file_size_kb ? `<span>💾 ${d.file_size_kb} KB</span>` : ''}
                    </div>
                </div>
            </div>
        `;
    },

    filterDocumentos() {
        let result = [...this.documentos];
        
        if (this.searchQuery) {
            const q = this.searchQuery.toLowerCase();
            result = result.filter(d => 
                (d.id && d.id.toLowerCase().includes(q)) ||
                (d.template_key && d.template_key.toLowerCase().includes(q)) ||
                (d.matter_id && d.matter_id.toLowerCase().includes(q))
            );
        }
        
        if (this.currentFilter !== 'todos') {
            result = result.filter(d => d.estado === this.currentFilter);
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

    // ========== GENERAR NUEVO DOCUMENTO (WIZARD) ==========
    showGenerateModal() {
        const matterOptions = this.matters.map(m => 
            `<option value="${m.id}">${m.id} - ${m.cliente}</option>`
        ).join('');

        const modal = document.createElement('div');
        modal.className = 'modal-overlay';
        modal.id = 'modal-generate-doc';
        modal.innerHTML = `
            <div class="modal" style="max-width: 700px;">
                <div class="modal-header">
                    <div class="modal-title">📄 Generar Documento</div>
                    <button class="modal-close" onclick="Documentos.closeModal('modal-generate-doc')">&times;</button>
                </div>
                
                <div class="modal-body">
                    <!-- Paso 1: Seleccionar Matter -->
                    <div id="wizard-step-1">
                        <div class="form-group">
                            <label class="form-label">Paso 1: Seleccionar Matter *</label>
                            <select class="form-select" id="gen-matter" onchange="Documentos.onMatterSelect()">
                                <option value="">Seleccionar matter...</option>
                                ${matterOptions}
                            </select>
                        </div>
                        <div id="matter-preview" style="background: var(--bg-warm); padding: 12px; border-radius: var(--radius); margin-top: 12px; display: none;">
                            <!-- Se llena dinámicamente -->
                        </div>
                    </div>
                    
                    <!-- Paso 2: Seleccionar Template -->
                    <div id="wizard-step-2" style="display: none;">
                        <div class="form-group">
                            <label class="form-label">Paso 2: Tipo de Documento *</label>
                            <div id="template-grid" style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px;">
                                ${this.templates.map(t => `
                                    <div class="template-option" onclick="Documentos.selectTemplate('${t.key}')" data-template="${t.key}">
                                        <strong>${t.label || t.key}</strong>
                                        <small style="color: var(--text-secondary);">${t.area || 'General'}</small>
                                    </div>
                                `).join('')}
                            </div>
                        </div>
                    </div>
                    
                    <!-- Paso 3: Revisar y Generar -->
                    <div id="wizard-step-3" style="display: none;">
                        <div class="form-group">
                            <label class="form-label">Paso 3: Revisar Datos</label>
                            <div id="review-data" style="background: var(--bg-warm); padding: 16px; border-radius: var(--radius);">
                                <!-- Se llena dinámicamente -->
                            </div>
                        </div>
                        <div class="form-group">
                            <label class="form-label">Nombre del archivo (opcional)</label>
                            <input type="text" class="form-input" id="gen-filename" placeholder="Ej: Contrato_Pragma_2026.pdf">
                        </div>
                    </div>
                </div>
                
                <div class="modal-footer">
                    <button class="btn btn-secondary" onclick="Documentos.closeModal('modal-generate-doc')">Cancelar</button>
                    <button class="btn btn-secondary" id="btn-prev" onclick="Documentos.prevStep()" style="display: none;">← Anterior</button>
                    <button class="btn btn-primary" id="btn-next" onclick="Documentos.nextStep()">Siguiente →</button>
                    <button class="btn btn-primary" id="btn-generate" onclick="Documentos.generate()" style="display: none;">
                        ⚡ Generar PDF
                    </button>
                </div>
            </div>
        `;
        document.body.appendChild(modal);
        
        this.wizardStep = 1;
        this.selectedMatter = null;
        this.selectedTemplate = null;
    },

    onMatterSelect() {
        const matterId = document.getElementById('gen-matter').value;
        const matter = this.matters.find(m => m.id === matterId);
        
        if (matter) {
            this.selectedMatter = matter;
            const preview = document.getElementById('matter-preview');
            preview.style.display = 'block';
            preview.innerHTML = `
                <strong>${matter.id}</strong> - ${Utils.escape(matter.cliente)}<br>
                <small>Área: ${matter.area_practica} | Prioridad: ${matter.prioridad}</small>
            `;
        }
    },

    selectTemplate(templateKey) {
        this.selectedTemplate = templateKey;
        document.querySelectorAll('.template-option').forEach(el => {
            el.classList.toggle('selected', el.dataset.template === templateKey);
        });
    },

    nextStep() {
        if (this.wizardStep === 1) {
            if (!this.selectedMatter) {
                alert('Selecciona un matter');
                return;
            }
            document.getElementById('wizard-step-1').style.display = 'none';
            document.getElementById('wizard-step-2').style.display = 'block';
            document.getElementById('btn-prev').style.display = 'inline-flex';
            this.wizardStep = 2;
        } else if (this.wizardStep === 2) {
            if (!this.selectedTemplate) {
                alert('Selecciona un tipo de documento');
                return;
            }
            document.getElementById('wizard-step-2').style.display = 'none';
            document.getElementById('wizard-step-3').style.display = 'block';
            
            // Llenar datos de revisión
            const template = this.templates.find(t => t.key === this.selectedTemplate);
            document.getElementById('review-data').innerHTML = `
                <div><strong>Matter:</strong> ${this.selectedMatter.id} - ${Utils.escape(this.selectedMatter.cliente)}</div>
                <div><strong>Documento:</strong> ${template ? template.label : this.selectedTemplate}</div>
                <div><strong>Fecha:</strong> ${new Date().toLocaleDateString('es-MX')}</div>
            `;
            
            document.getElementById('btn-next').style.display = 'none';
            document.getElementById('btn-generate').style.display = 'inline-flex';
            this.wizardStep = 3;
        }
    },

    prevStep() {
        if (this.wizardStep === 2) {
            document.getElementById('wizard-step-2').style.display = 'none';
            document.getElementById('wizard-step-1').style.display = 'block';
            document.getElementById('btn-prev').style.display = 'none';
            this.wizardStep = 1;
        } else if (this.wizardStep === 3) {
            document.getElementById('wizard-step-3').style.display = 'none';
            document.getElementById('wizard-step-2').style.display = 'block';
            document.getElementById('btn-next').style.display = 'inline-flex';
            document.getElementById('btn-generate').style.display = 'none';
            this.wizardStep = 2;
        }
    },

    async generate() {
        if (!this.selectedMatter || !this.selectedTemplate) return;

        const btn = document.getElementById('btn-generate');
        btn.innerHTML = '<div class="spinner" style="width: 16px; height: 16px; display: inline-block;"></div> Generando...';
        btn.disabled = true;

        try {
            const filename = document.getElementById('gen-filename').value.trim();
            
            const result = await API.generateDoc(this.selectedMatter.id, {
                template_key: this.selectedTemplate,
                output_filename: filename || undefined,
                datos_extra: {
                    cliente: this.selectedMatter.cliente,
                    area: this.selectedMatter.area_practica
                }
            });

            this.closeModal('modal-generate-doc');
            
            // Descargar automáticamente
            if (result.file_path) {
                const a = document.createElement('a');
                a.href = `http://localhost:8082${result.file_path}`;
                a.download = filename || result.file_path.split('/').pop();
                a.click();
            }

            this.showSuccess(`Documento generado: ${result.documento_id || 'nuevo'}`);
            await this.render();

        } catch (err) {
            alert('Error al generar: ' + err.message);
            btn.innerHTML = '⚡ Generar PDF';
            btn.disabled = false;
        }
    },

    // ========== PREVISUALIZAR ==========
    preview(docId) {
        const d = this.documentos.find(x => x.id === docId);
        if (!d || !d.ruta_pdf) {
            alert('No hay PDF para previsualizar');
            return;
        }

        // Abrir en nueva pestaña
        window.open(`http://localhost:8082${d.ruta_pdf}`, '_blank');
    },

    // ========== DESCARGAR ==========
    download(docId) {
        const d = this.documentos.find(x => x.id === docId);
        if (!d || !d.ruta_pdf) {
            alert('No hay archivo para descargar');
            return;
        }

        const a = document.createElement('a');
        a.href = `http://localhost:8082${d.ruta_pdf}`;
        a.download = d.ruta_pdf.split('/').pop();
        document.body.appendChild(a);
        a.click();
        a.remove();
    },

    // ========== REGENERAR ==========
    async regenerate(docId) {
        const d = this.documentos.find(x => x.id === docId);
        if (!d) return;

        if (confirm(`¿Regenerar documento ${d.id}?`)) {
            try {
                await API.generateDoc(d.matter_id, {
                    template_key: d.template_key,
                    output_filename: d.ruta_pdf ? d.ruta_pdf.split('/').pop() : undefined
                });
                this.showSuccess('Documento regenerado');
                await this.render();
            } catch (err) {
                alert('Error: ' + err.message);
            }
        }
    },

    // ========== CAMBIAR ESTADO ==========
    async changeEstado(docId, nuevoEstado) {
        const d = this.documentos.find(x => x.id === docId);
        if (!d) return;

        try {
            // Actualizar en backend (simulado - necesitaría endpoint PUT)
            d.estado = nuevoEstado;
            
            // Si se marca como firmado, mover a carpeta de firmados
            if (nuevoEstado === 'firmado' && d.ruta_pdf) {
                this.showSuccess('Documento marcado como firmado');
            }
            
            this.renderList();
        } catch (err) {
            alert('Error: ' + err.message);
        }
    },

    // ========== ELIMINAR ==========
    confirmDelete(id) {
        const d = this.documentos.find(x => x.id === id);
        if (!d) return;

        if (confirm(`¿Eliminar documento ${d.id}?\n\nEsta acción no se puede deshacer.`)) {
            this.delete(id);
        }
    },

    async delete(id) {
        try {
            this.documentos = this.documentos.filter(d => d.id !== id);
            this.renderList();
            this.showSuccess(`Documento ${id} eliminado`);
        } catch (err) {
            alert('Error al eliminar: ' + err.message);
        }
    },

    // ========== UTILIDADES ==========
    closeModal(id) {
        const modal = document.getElementById(id);
        if (modal) modal.remove();
    },

    showSuccess(message) {
        const alert = document.createElement('div');
        alert.className = 'alert alert-green';
        alert.style.cssText = 'position: fixed; top: 20px; right: 20px; z-index: 10000; max-width: 400px;';
        alert.innerHTML = `<strong>✅ ${message}</strong>`;
        document.body.appendChild(alert);
        setTimeout(() => alert.remove(), 3000);
    }
};

window.Documentos = Documentos;
