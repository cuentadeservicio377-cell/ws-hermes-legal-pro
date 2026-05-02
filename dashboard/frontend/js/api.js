// js/api.js — Cliente HTTP para Hermes Legal Pro API v8
const API = {
  baseUrl: '/api',
  
  async get(endpoint) {
    const res = await fetch(`http://localhost:8082${this.baseUrl}${endpoint}`);
    if (!res.ok) throw new Error(`Error ${res.status}: ${res.statusText}`);
    return res.json();
  },
  
  async post(endpoint, data) {
    const res = await fetch(`http://localhost:8082${this.baseUrl}${endpoint}`, {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify(data)
    });
    if (!res.ok) throw new Error(`Error ${res.status}: ${res.statusText}`);
    return res.json();
  },
  
  async put(endpoint, data) {
    const res = await fetch(`http://localhost:8082${this.baseUrl}${endpoint}`, {
      method: 'PUT',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify(data)
    });
    if (!res.ok) throw new Error(`Error ${res.status}: ${res.statusText}`);
    return res.json();
  },
  
  async delete(endpoint) {
    const res = await fetch(`http://localhost:8082${this.baseUrl}${endpoint}`, {method: 'DELETE'});
    if (!res.ok) throw new Error(`Error ${res.status}: ${res.statusText}`);
    return res.json();
  },
  
  // Matters
  getMatters() { return this.get('/matters'); },
  createMatter(data) { return this.post('/matters', data); },
  updateMatter(id, data) { return this.put(`/matters/${id}`, data); },
  deleteMatter(id) { return this.delete(`/matters/${id}`); },
  
  // Documentos
  getTemplates() { return this.get('/templates'); },
  generateDocument(templateId, matterId) { 
    return this.post(`/matter/${matterId}/generar-documento`, {template_key: templateId}); 
  },
  
  // Plazos
  getPlazos() { return this.get('/plazos'); },
  createPlazo(data) { return this.post('/plazo', data); },
  
  // Finanzas
  getFinanzas() { return this.get('/finanzas'); },
  createFinanza(data) { return this.post('/finanzas', data); },
  
  // Alertas
  getAlertas() { return this.get('/alertas'); },
  
  // Aprobaciones
  getAprobaciones() { return this.get('/aprobaciones'); },
  approveDocument(id) { return this.post(`/aprobacion/${id}/aprobar`); },
  
  // NUEVO v8 — Google Workspace
  getDriveLink(matterId) { return this.get(`/drive-link/${matterId}`); },
  exportToSheets(data = {}) { return this.post('/export-sheets', data); },
  exportToDocs(data = {}) { return this.post('/export-docs', data); },
  syncExcel() { return this.post('/sync-excel'); },
  getTasks() { return this.get('/tasks'); },
  createTask(data) { return this.post('/task', data); },
  getCalendarEvents() { return this.get('/calendar-events'); },
  checkPlazos() { return this.post('/check-plazos'); }
};

window.API = API;
