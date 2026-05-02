# PROMPT FASE 3 — Matters CRUD Completo
## Para OpenCode Go | Hermes Legal Pro v3.0

---

## 🎯 OBJETIVO DE ESTA FASE

Crear la vista de Matters completa:
- **C**rear: Formulario modal para nuevo matter
- **R**ead: Lista con filtros, búsqueda, ordenamiento
- **U**pdate: Editar datos del matter inline
- **D**elete: Eliminar con confirmación
- **Generar documento**: Botón que genera PDF real
- **Abrir carpeta**: Link que abre Finder/Explorer

---

## 📁 ARCHIVOS A CREAR/MODIFICAR

```
dashboard/frontend/
├── js/
│   ├── app.js          (MODIFICAR — agregar loadMatters real)
│   └── matters.js      (CREAR — toda la lógica de matters)
└── css/
    └── kami.css        (AGREGAR al final — estilos de matters)
```

---

## 🔧 PASO 1: Crear `js/matters.js`

```javascript
// js/matters.js — Matters CRUD completo

const Matters = {
    // Estado local
    matters: [],
    templates: [],
    currentFilter: 'todos',
    searchQuery: '',

    // Renderizar vista completa
    async render() {
        const container = document.getElementById('view-matters');
        
        container.innerHTML = `
            <div class="header">
                <h1>Matters</h1>
                <button class="btn btn-primary" onclick="Matters.showCreateModal()">
                    + Nuevo Matter
                </button>
            </div>
            <div id="matters-content">
                <div class="text-center" style="padding: 60px;">
                    <div class="spinner"></div>
                    <p style="margin-top: 16px; color: var(--text-secondary);">
                        Cargando matters...
                    </p>
                </div>
            </div>
        `;

        try {
            // Cargar datos en paralelo
            const [mattersData, templatesData] = await Promise.all([
                API.matters(),
                API.templates()
            ]);

            this.matters = mattersData || [];
            this.templates = (templatesData && templatesData.templates) ? templatesData.templates : [];

            this.renderList();

        } catch (err) {
            console.error('Error cargando matters:', err);
            document.getElementById('matters-content').innerHTML = `
                <div class="alert alert-red">
                    <strong>Error al cargar matters:</strong> ${err.message}
                </div>
                <button class="btn btn-primary" onclick="Matters.render()">Reintentar</button>
            `;
        }
    },

    // Renderizar lista de matters
    renderList() {
        const container = document.getElementById('matters-content');
        
        // Filtrar matters
        let filtered = this.filterMatters();

        // Toolbar
        const toolbar = `
            <div style="display: flex; gap: 12px; margin-bottom: 20px; flex-wrap: wrap;">
                <input type="text" 
                       class="form-input" 
                       placeholder="🔍 Buscar cliente..." 
                       style="flex: 1; min-width: 200px;"
                       oninput="Matters.handleSearch(this.value)">
                
                <select class="form-select" style="width: 150px;" onchange="Matters.handleFilter(this.value)">
                    <option value="todos">Todos</option>
                    <option value="activo">Activos</option>
                    <option value="cerrado">Cerrados</option>
                    <option value="urgente">Urgentes</option>
                </select>
                
                <select class="form-select" style="width: 180px;" onchange="Matters.handleAreaFilter(this.value)">
                    <option value="todos">Todas las áreas</option>
                    <option value="Mercantil">Mercantil</option>
                    <option value="Laboral">Laboral</option>
                    <option value="Civil">Civil</option>
                    <option value="Fiscal">Fiscal</option>
                    <option value="Corporativo">Corporativo</option>
                    <option value="Privacidad">Privacidad</option>
                </select>
            </div>
        `;

        // Lista
        if (filtered.length === 0) {
            container.innerHTML = toolbar + `
                <div class="card" style="text-align: center; padding: 60px;">
                    <div style="font-size: 48px; margin-bottom: 16px;">📁</div>
                    <h3 style="color: var(--ink-blue); margin-bottom: 8px;">No hay matters</h3>
                    <p style="color: var(--text-secondary); margin-bottom: 20px;">
                        ${this.searchQuery ? 'No se encontraron resultados para "' + Utils.escape(this.searchQuery) + '"' : 'Comienza creando tu primer matter'}
                    </p>
                    ${!this.searchQuery ? '<button class="btn btn-primary" onclick="Matters.showCreateModal()">+ Crear Matter</button>' : ''}
                </div>
            `;
            return;
        }

        const list = filtered.map(m => this.renderMatterCard(m)).join('');

        container.innerHTML = toolbar + `
            <div style="display: flex; flex-direction: column; gap: 12px;">
                ${list}
            </div>
            <div style="margin-top: 16px; color: var(--text-secondary); font-size: 12px;">
                Mostrando ${filtered.length} de ${this.matters.length} matters
            </div>
        `;
    },

    // Renderizar tarjeta de un matter
    renderMatterCard(m) {
        const dias = Utils.diasRestantes(m.deadline);
        const urgenciaBadge = Utils.badgeUrgencia(dias);
        const prioridadBadge = Utils.badgePrioridad(m.prioridad);
        const estadoBadge = Utils.badgeEstado(m.estado);
        
        const docsPendientes = (m.documentos || []).filter(d => d.estado === 'borrador').length;
        const totalDocs = (m.documentos || []).length;

        return `
            <div class="matter-card" data-id="${m.id}">
                <div class="matter-header">
                    <div class="matter-title">
                        <strong>${Utils.escape(m.id)}</strong>
                        <span style="margin-left: 8px;">${Utils.escape(m.cliente || 'Sin cliente')}</span>
                        ${prioridadBadge}
                        ${estadoBadge}
                    </div>
                    <div class="matter-actions">
                        <button class="btn btn-sm btn-secondary" onclick="Matters.showEditModal('${m.id}')">✏️ Editar</button>
                        <button class="btn btn-sm btn-primary" onclick="Matters.showGenerateModal('${m.id}')">📄 Generar Doc</button>
                        <button class="btn btn-sm btn-secondary" onclick="Matters.openFolder('${m.id}')">📁 Carpeta</button>
                        <button class="btn btn-sm btn-danger" onclick="Matters.confirmDelete('${m.id}')">🗑️</button>
                    </div>
                </div>
                
                <div class="matter-body">
                    <div class="matter-meta">
                        <span>📂 ${Utils.escape(m.area_practica || 'General')}</span>
                        <span>📅 Deadline: ${Utils.formatDate(m.deadline)} ${urgenciaBadge}</span>
                        <span>📄 ${docsPendientes}/${totalDocs} docs pendientes</span>
                    </div>
                    
                    ${m.descripcion ? `
                        <div class="matter-description">
                            ${Utils.escape(m.descripcion)}
                        </div>
                    ` : ''}
                    
                    ${m.next_step ? `
                        <div class="matter-next-step">
                            <strong>Próximo paso:</strong> ${Utils.escape(m.next_step)}
                        </div>
                    ` : ''}
                </div>
            </div>
        `;
    },

    // Filtrar matters
    filterMatters() {
        let result = [...this.matters];
        
        // Filtro de búsqueda
        if (this.searchQuery) {
            const q = this.searchQuery.toLowerCase();
            result = result.filter(m => 
                (m.cliente && m.cliente.toLowerCase().includes(q)) ||
                (m.id && m.id.toLowerCase().includes(q)) ||
                (m.descripcion && m.descripcion.toLowerCase().includes(q))
            );
        }
        
        // Filtro de estado
        if (this.currentFilter === 'activo') {
            result = result.filter(m => m.estado === 'activo');
        } else if (this.currentFilter === 'cerrado') {
            result = result.filter(m => m.estado === 'cerrado');
        } else if (this.currentFilter === 'urgente') {
            result = result.filter(m => m.prioridad === 'alta' || m.estado === 'urgente');
        }
        
        return result;
    },

    // Handlers de filtro
    handleSearch(value) {
        this.searchQuery = value;
        this.renderList();
    },

    handleFilter(value) {
        this.currentFilter = value;
        this.renderList();
    },

    handleAreaFilter(value) {
        if (value === 'todos') {
            this.currentFilter = 'todos';
        } else {
            this.matters = this.matters.filter(m => m.area_practica === value);
        }
        this.renderList();
    },

    // ========== CREAR ==========
    showCreateModal() {
        const modal = document.createElement('div');
        modal.className = 'modal-overlay';
        modal.id = 'modal-create-matter';
        modal.innerHTML = `
            <div class="modal">
                <div class="modal-header">
                    <div class="modal-title">➕ Nuevo Matter</div>
                    <button class="modal-close" onclick="Matters.closeModal('modal-create-matter')">&times;</button>
                </div>
                
                <div class="modal-body">
                    <div class="form-group">
                        <label class="form-label">Nombre del Cliente *</label>
                        <input type="text" class="form-input" id="new-cliente" placeholder="Ej: Pragma Studio">
                    </div>
                    
                    <div class="form-group">
                        <label class="form-label">Área de Práctica</label>
                        <select class="form-select" id="new-area">
                            <option value="Mercantil">Mercantil</option>
                            <option value="Laboral">Laboral</option>
                            <option value="Civil">Civil</option>
                            <option value="Fiscal">Fiscal</option>
                            <option value="Corporativo">Corporativo</option>
                            <option value="Privacidad">Privacidad</option>
                            <option value="Inmobiliario">Inmobiliario</option>
                        </select>
                    </div>
                    
                    <div class="form-group">
                        <label class="form-label">Descripción</label>
                        <textarea class="form-textarea" id="new-descripcion" placeholder="Breve descripción del caso..."></textarea>
                    </div>
                    
                    <div class="grid-2">
                        <div class="form-group">
                            <label class="form-label">Deadline</label>
                            <input type="date" class="form-input" id="new-deadline">
                        </div>
                        
                        <div class="form-group">
                            <label class="form-label">Prioridad</label>
                            <select class="form-select" id="new-prioridad">
                                <option value="media">Media</option>
                                <option value="alta">Alta</option>
                                <option value="baja">Baja</option>
                            </select>
                        </div>
                    </div>
                </div>
                
                <div class="modal-footer">
                    <button class="btn btn-secondary" onclick="Matters.closeModal('modal-create-matter')">Cancelar</button>
                    <button class="btn btn-primary" onclick="Matters.create()">💾 Crear Matter</button>
                </div>
            </div>
        `;
        document.body.appendChild(modal);
    },

    async create() {
        const data = {
            cliente: document.getElementById('new-cliente').value.trim(),
            area_practica: document.getElementById('new-area').value,
            descripcion: document.getElementById('new-descripcion').value.trim(),
            deadline: document.getElementById('new-deadline').value || null,
            prioridad: document.getElementById('new-prioridad').value
        };

        if (!data.cliente) {
            alert('El nombre del cliente es obligatorio');
            return;
        }

        try {
            this.setLoading(true);
            const newMatter = await API.createMatter(data);
            this.closeModal('modal-create-matter');
            
            // Recargar lista
            await this.render();
            
            // Mostrar éxito
            this.showSuccess(`Matter ${newMatter.id} creado exitosamente`);
            
        } catch (err) {
            alert('Error al crear matter: ' + err.message);
        } finally {
            this.setLoading(false);
        }
    },

    // ========== EDITAR ==========
    showEditModal(id) {
        const m = this.matters.find(x => x.id === id);
        if (!m) return;

        const modal = document.createElement('div');
        modal.className = 'modal-overlay';
        modal.id = 'modal-edit-matter';
        modal.innerHTML = `
            <div class="modal">
                <div class="modal-header">
                    <div class="modal-title">✏️ Editar Matter ${id}</div>
                    <button class="modal-close" onclick="Matters.closeModal('modal-edit-matter')">&times;</button>
                </div>
                
                <div class="modal-body">
                    <div class="form-group">
                        <label class="form-label">Cliente</label>
                        <input type="text" class="form-input" id="edit-cliente" value="${Utils.escape(m.cliente || '')}">
                    </div>
                    
                    <div class="form-group">
                        <label class="form-label">Área</label>
                        <select class="form-select" id="edit-area">
                            <option value="Mercantil" ${m.area_practica === 'Mercantil' ? 'selected' : ''}>Mercantil</option>
                            <option value="Laboral" ${m.area_practica === 'Laboral' ? 'selected' : ''}>Laboral</option>
                            <option value="Civil" ${m.area_practica === 'Civil' ? 'selected' : ''}>Civil</option>
                            <option value="Fiscal" ${m.area_practica === 'Fiscal' ? 'selected' : ''}>Fiscal</option>
                            <option value="Corporativo" ${m.area_practica === 'Corporativo' ? 'selected' : ''}>Corporativo</option>
                            <option value="Privacidad" ${m.area_practica === 'Privacidad' ? 'selected' : ''}>Privacidad</option>
                        </select>
                    </div>
                    
                    <div class="form-group">
                        <label class="form-label">Descripción</label>
                        <textarea class="form-textarea" id="edit-descripcion">${Utils.escape(m.descripcion || '')}</textarea>
                    </div>
                    
                    <div class="grid-2">
                        <div class="form-group">
                            <label class="form-label">Deadline</label>
                            <input type="date" class="form-input" id="edit-deadline" value="${m.deadline || ''}">
                        </div>
                        
                        <div class="form-group">
                            <label class="form-label">Prioridad</label>
                            <select class="form-select" id="edit-prioridad">
                                <option value="alta" ${m.prioridad === 'alta' ? 'selected' : ''}>Alta</option>
                                <option value="media" ${m.prioridad === 'media' ? 'selected' : ''}>Media</option>
                                <option value="baja" ${m.prioridad === 'baja' ? 'selected' : ''}>Baja</option>
                            </select>
                        </div>
                    </div>
                    
                    <div class="form-group">
                        <label class="form-label">Estado</label>
                        <select class="form-select" id="edit-estado">
                            <option value="activo" ${m.estado === 'activo' ? 'selected' : ''}>Activo</option>
                            <option value="cerrado" ${m.estado === 'cerrado' ? 'selected' : ''}>Cerrado</option>
                            <option value="pausado" ${m.estado === 'pausado' ? 'selected' : ''}>Pausado</option>
                        </select>
                    </div>
                </div>
                
                <div class="modal-footer">
                    <button class="btn btn-secondary" onclick="Matters.closeModal('modal-edit-matter')">Cancelar</button>
                    <button class="btn btn-primary" onclick="Matters.update('${id}')">💾 Guardar Cambios</button>
                </div>
            </div>
        `;
        document.body.appendChild(modal);
    },

    async update(id) {
        const data = {
            cliente: document.getElementById('edit-cliente').value.trim(),
            area_practica: document.getElementById('edit-area').value,
            descripcion: document.getElementById('edit-descripcion').value.trim(),
            deadline: document.getElementById('edit-deadline').value || null,
            prioridad: document.getElementById('edit-prioridad').value,
            estado: document.getElementById('edit-estado').value
        };

        try {
            this.setLoading(true);
            await API.updateMatter(id, data);
            this.closeModal('modal-edit-matter');
            await this.render();
            this.showSuccess(`Matter ${id} actualizado`);
        } catch (err) {
            alert('Error al actualizar: ' + err.message);
        } finally {
            this.setLoading(false);
        }
    },

    // ========== ELIMINAR ==========
    confirmDelete(id) {
        const m = this.matters.find(x => x.id === id);
        if (!m) return;

        if (confirm(`¿Estás seguro de eliminar el matter ${id} - ${m.cliente}?\n\nEsta acción no se puede deshacer.`)) {
            this.delete(id);
        }
    },

    async delete(id) {
        try {
            this.setLoading(true);
            await API.deleteMatter(id);
            await this.render();
            this.showSuccess(`Matter ${id} eliminado`);
        } catch (err) {
            alert('Error al eliminar: ' + err.message);
        } finally {
            this.setLoading(false);
        }
    },

    // ========== GENERAR DOCUMENTO ==========
    showGenerateModal(matterId) {
        const m = this.matters.find(x => x.id === matterId);
        if (!m) return;

        const templateOptions = this.templates.map(t => 
            `<option value="${t.key}">${t.label || t.key} (${t.area || 'General'})</option>`
        ).join('');

        const modal = document.createElement('div');
        modal.className = 'modal-overlay';
        modal.id = 'modal-generate-doc';
        modal.innerHTML = `
            <div class="modal">
                <div class="modal-header">
                    <div class="modal-title">📄 Generar Documento</div>
                    <button class="modal-close" onclick="Matters.closeModal('modal-generate-doc')">&times;</button>
                </div>
                
                <div class="modal-body">
                    <div class="form-group">
                        <label class="form-label">Matter</label>
                        <input type="text" class="form-input" value="${Utils.escape(m.id)} - ${Utils.escape(m.cliente)}" disabled>
                    </div>
                    
                    <div class="form-group">
                        <label class="form-label">Tipo de Documento *</label>
                        <select class="form-select" id="gen-template">
                            ${templateOptions}
                        </select>
                    </div>
                    
                    <div class="form-group">
                        <label class="form-label">Nombre del archivo (opcional)</label>
                        <input type="text" class="form-input" id="gen-filename" placeholder="Ej: Contrato_Pragma_2026.pdf">
                    </div>
                    
                    <div id="gen-preview" style="background: var(--bg-warm); padding: 12px; border-radius: var(--radius); margin-top: 12px;">
                        <strong>Vista previa de campos:</strong><br>
                        <small>Cliente: ${Utils.escape(m.cliente)}<br>
                        Área: ${Utils.escape(m.area_practica)}<br>
                        Fecha: ${new Date().toLocaleDateString('es-MX')}</small>
                    </div>
                </div>
                
                <div class="modal-footer">
                    <button class="btn btn-secondary" onclick="Matters.closeModal('modal-generate-doc')">Cancelar</button>
                    <button class="btn btn-primary" id="btn-generate" onclick="Matters.generateDocument('${matterId}')">
                        ⚡ Generar PDF
                    </button>
                </div>
            </div>
        `;
        document.body.appendChild(modal);
    },

    async generateDocument(matterId) {
        const templateKey = document.getElementById('gen-template').value;
        const filename = document.getElementById('gen-filename').value.trim();

        if (!templateKey) {
            alert('Selecciona un tipo de documento');
            return;
        }

        const btn = document.getElementById('btn-generate');
        btn.innerHTML = '<div class="spinner" style="width: 16px; height: 16px; display: inline-block;"></div> Generando...';
        btn.disabled = true;

        try {
            const result = await API.generateDoc(matterId, {
                template_key: templateKey,
                output_filename: filename || undefined,
                datos_extra: {}
            });

            this.closeModal('modal-generate-doc');
            
            // Ofrecer descarga
            if (result.file_path) {
                const downloadUrl = `http://localhost:8082/api/download?path=${encodeURIComponent(result.file_path)}`;
                const a = document.createElement('a');
                a.href = downloadUrl;
                a.download = filename || result.file_path.split('/').pop();
                a.click();
            }

            this.showSuccess(`Documento generado: ${result.file_path}`);
            await this.render();

        } catch (err) {
            alert('Error al generar: ' + err.message);
            btn.innerHTML = '⚡ Generar PDF';
            btn.disabled = false;
        }
    },

    // ========== ABRIR CARPETA ==========
    openFolder(matterId) {
        const m = this.matters.find(x => x.id === matterId);
        if (!m || !m.carpeta) {
            alert('No hay carpeta asociada a este matter');
            return;
        }

        // En macOS, abrir con 'open'
        // En Windows, abrir con 'explorer'
        // Como es web, usamos un endpoint del backend
        fetch(`http://localhost:8082/api/carpetas/${matterId}/abrir`)
            .catch(() => {
                // Fallback: copiar ruta al clipboard
                navigator.clipboard.writeText(m.carpeta);
                alert('Ruta copiada al portapapeles:\n' + m.carpeta);
            });
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
    }
};

window.Matters = Matters;
```

**Guardar en:** `~/ws-hermes-legal-pro/dashboard/frontend/js/matters.js`

---

## 🔧 PASO 2: Modificar `js/app.js`

Buscar la función `loadMatters()` placeholder y reemplazarla:

**DE:**
```javascript
async loadMatters() {
    const container = document.getElementById('view-matters');
    container.innerHTML = `
        <div class="header">...
        <div class="alert alert-yellow">🏗️ Vista en construcción. FASE 3.</div>
    `;
}
```

**A:**
```javascript
async loadMatters() {
    await Matters.render();
}
```

---

## 🔧 PASO 3: Agregar CSS al final de `css/kami.css`

```css
/* ===== MATTERS SPECIFIC ===== */

.matter-card {
    background: white;
    border-radius: var(--radius-lg);
    padding: 20px;
    box-shadow: var(--shadow);
    transition: all 0.2s;
}

.matter-card:hover {
    box-shadow: var(--shadow-hover);
}

.matter-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 12px;
    flex-wrap: wrap;
    gap: 8px;
}

.matter-title {
    display: flex;
    align-items: center;
    gap: 8px;
    flex-wrap: wrap;
}

.matter-title strong {
    font-size: 16px;
    color: var(--ink-blue);
}

.matter-actions {
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
}

.matter-body {
    border-top: 1px solid var(--border-light);
    padding-top: 12px;
}

.matter-meta {
    display: flex;
    gap: 16px;
    flex-wrap: wrap;
    font-size: 13px;
    color: var(--text-secondary);
    margin-bottom: 8px;
}

.matter-description {
    font-size: 13px;
    color: var(--text-secondary);
    margin-bottom: 8px;
    line-height: 1.5;
}

.matter-next-step {
    font-size: 13px;
    background: var(--bg-warm);
    padding: 8px 12px;
    border-radius: var(--radius);
    border-left: 3px solid var(--warning-yellow);
}

/* Modal mejoras */
.modal-body {
    max-height: 60vh;
    overflow-y: auto;
}

.modal-body .form-group:last-child {
    margin-bottom: 0;
}

/* Toast notifications */
.alert {
    animation: slideIn 0.3s ease;
}

@keyframes slideIn {
    from { transform: translateX(100%); opacity: 0; }
    to { transform: translateX(0); opacity: 1; }
}
```

**Agregar al final de:** `~/ws-hermes-legal-pro/dashboard/frontend/css/kami.css`

---

## 🔧 PASO 4: Actualizar `index.html`

Agregar script de matters antes de app.js:

```html
<script src="js/matters.js"></script>
```

---

## 🧪 TESTS DE ESTA FASE

### Preparación
```bash
cd ~/ws-hermes-legal-pro/dashboard/backend
python3 app.py &
```

### Test 1: Lista de matters carga
```
Abrir http://localhost:8082 → Click en "Matters"
Esperado: Lista de matters con tarjetas, filtros, búsqueda
```

### Test 2: Crear matter
```
Click "+ Nuevo Matter" → Llenar formulario → Guardar
Esperado: Matter aparece en lista, carpeta creada en disco
```

### Test 3: Editar matter
```
Click "✏️ Editar" en un matter → Cambiar datos → Guardar
Esperado: Cambios persisten, lista se actualiza
```

### Test 4: Eliminar matter
```
Click "🗑️" → Confirmar → Matter desaparece
Esperado: Matter eliminado, datos persisten
```

### Test 5: Generar documento
```
Click "📄 Generar Doc" → Seleccionar template → Generar
Esperado: PDF generado, descarga automática
```

### Test 6: Filtros funcionan
```
Escribir en búsqueda → Solo muestra coincidencias
Cambiar filtro estado → Solo muestra esos
```

### Test 7: Sin errores en consola
```
Cmd+Option+J → Ningún error rojo
```

---

## ✅ CHECKLIST PARA PASAR A FASE 4

- [ ] matters.js creado y funciona
- [ ] Lista muestra matters reales
- [ ] Filtros y búsqueda funcionan
- [ ] Crear matter con modal
- [ ] Editar matter
- [ ] Eliminar matter con confirmación
- [ ] Generar documento (wizard + descarga)
- [ ] Abrir carpeta
- [ ] Diseño responsive
- [ ] Sin errores en consola

---

## 📤 ENTREGA

```bash
cd ~/ws-hermes-legal-pro
git add dashboard/frontend/
git commit -m "FASE 3: Matters CRUD completo - crear, editar, eliminar, generar doc"
git push origin master
```

**Notificar:** "FASE 3 completada. Matters funcional al 100%. Listo para FASE 4 (Reuniones)."

---

*Prompt FASE 3 — Diseñado para OpenCode Go*
*Hermes Legal Pro v3.0*
