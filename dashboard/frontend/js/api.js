// js/api.js — Cliente HTTP para Hermes Legal Pro API

const API_BASE = 'http://localhost:8082';

class API {
    // GET genérico
    static async get(endpoint) {
        const res = await fetch(`${API_BASE}${endpoint}`);
        if (!res.ok) throw new Error(`Error ${res.status}: ${res.statusText}`);
        return res.json();
    }

    // POST genérico
    static async post(endpoint, data) {
        const res = await fetch(`${API_BASE}${endpoint}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        if (!res.ok) {
            const err = await res.json();
            throw new Error(err.detail || `Error ${res.status}`);
        }
        return res.json();
    }

    // PUT genérico
    static async put(endpoint, data) {
        const res = await fetch(`${API_BASE}${endpoint}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        if (!res.ok) throw new Error(`Error ${res.status}`);
        return res.json();
    }

    // DELETE genérico
    static async delete(endpoint) {
        const res = await fetch(`${API_BASE}${endpoint}`, { method: 'DELETE' });
        if (!res.ok) throw new Error(`Error ${res.status}`);
        return res.ok;
    }

    // Endpoints específicos
    static health() { return this.get('/api/health'); }
    static dashboard() { return this.get('/api/dashboard'); }
    static matters() { return this.get('/api/matters'); }
    static matter(id) { return this.get(`/api/matters/${id}`); }
    static createMatter(data) { return this.post('/api/matters', data); }
    static updateMatter(id, data) { return this.put(`/api/matters/${id}`, data); }
    static deleteMatter(id) { return this.delete(`/api/matters/${id}`); }
    static templates() { return this.get('/api/templates'); }
    static generateDoc(matterId, data) { return this.post(`/api/matter/${matterId}/generar-documento`, data); }
    static reuniones() { return this.get('/api/reuniones'); }
    static createReunion(data) { return this.post('/api/reuniones', data); }
    static documentos() { return this.get('/api/documentos'); }
    static alertas() { return this.get('/api/alertas'); }
    static carpetas(matterId) { return this.get(`/api/carpetas/${matterId}`); }
    static driveFolder(matterId) { return this.get(`/api/matters/${matterId}/drive-folder`); }
    static driveDocuments(matterId) { return this.get(`/api/matters/${matterId}/documents`); }
}

// Google Workspace helpers
async function getDriveFolder(matterId) {
    const response = await fetch(`${API_BASE}/api/matters/${matterId}/drive-folder`);
    return await response.json();
}

async function openInDrive(matterId) {
    const result = await getDriveFolder(matterId);
    if (result.link) {
        window.open(result.link, '_blank');
    }
}

async function openInDocs(docId) {
    window.open(`https://docs.google.com/document/d/${docId}/edit`, '_blank');
}

window.API = API;
