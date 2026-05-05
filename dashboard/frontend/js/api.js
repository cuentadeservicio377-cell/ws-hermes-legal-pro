// js/api.js — Capa de API para backend
// Willow Legal Pro v3.0

const API = {
  baseUrl: '', // Same origin
  
  async request(endpoint, options = {}) {
    const url = `${this.baseUrl}/api${endpoint}`;
    
    const config = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers
      },
      ...options
    };
    
    if (config.body && typeof config.body === 'object') {
      config.body = JSON.stringify(config.body);
    }
    
    try {
      const response = await fetch(url, config);
      
      if (!response.ok) {
        const error = await response.json().catch(() => ({}));
        throw new Error(error.detail || `HTTP ${response.status}`);
      }
      
      // Handle empty responses
      const text = await response.text();
      return text ? JSON.parse(text) : null;
      
    } catch (err) {
      console.error(`API Error ${endpoint}:`, err);
      throw err;
    }
  },
  
  // Dashboard
  dashboard() {
    return this.request('/dashboard');
  },
  
  // Health check
  health() {
    return this.request('/health');
  },
  
  // Matters
  matters() {
    return this.request('/matters');
  },
  
  matter(id) {
    return this.request(`/matters/${id}`);
  },
  
  crearMatter(data) {
    return this.request('/matters', {
      method: 'POST',
      body: data
    });
  },
  
  // Reuniones
  reuniones() {
    return this.request('/reuniones');
  },
  
  crearReunion(data) {
    return this.request('/reuniones', {
      method: 'POST',
      body: data
    });
  },
  
  eliminarReunion(id) {
    return this.request(`/reuniones/${id}`, {
      method: 'DELETE'
    });
  },
  
  // Documentos
  documentos() {
    return this.request('/documentos');
  },
  
  crearDocumento(data) {
    return this.request('/documentos', {
      method: 'POST',
      body: data
    });
  },
  
  // Templates
  templates() {
    return this.request('/templates');
  },
  
  template(key) {
    return this.request(`/templates/${key}`);
  },
  
  // Finanzas
  finanzas() {
    return this.request('/finanzas');
  },
  
  crearMovimiento(data) {
    return this.request('/finanzas', {
      method: 'POST',
      body: data
    });
  },
  
  // Alertas
  alertas() {
    return this.request('/alertas');
  },
  
  // Plazos
  plazos() {
    return this.request('/plazos');
  },
  
  // Check plazos
  checkPlazos() {
    return this.request('/check-plazos', {
      method: 'POST'
    });
  },
  
  // Drive
  driveLink(matterId) {
    return this.request(`/drive-link/${matterId}`);
  }
};
