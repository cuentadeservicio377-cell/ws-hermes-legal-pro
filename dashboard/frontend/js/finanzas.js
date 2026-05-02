// finanzas.js — Módulo de finanzas para Willow Legal Dashboard

const FinanzasAPI = {
    baseUrl: '/api',
    
    async cargarResumen() {
        const res = await fetch(`${this.baseUrl}/finanzas`);
        return res.json();
    },
    
    async cargarTransacciones(matterId = null) {
        const url = matterId 
            ? `${this.baseUrl}/finanzas?matter_id=${matterId}`
            : `${this.baseUrl}/finanzas`;
        const res = await fetch(url);
        return res.json();
    },
    
    async registrarIngreso(data) {
        const res = await fetch(`${this.baseUrl}/finanzas`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                ...data,
                tipo: 'ingreso'
            })
        });
        return res.json();
    },
    
    async registrarEgreso(data) {
        const res = await fetch(`${this.baseUrl}/finanzas`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                ...data,
                tipo: 'egreso'
            })
        });
        return res.json();
    }
};

const FinanzasUI = {
    async renderResumen() {
        const container = document.getElementById('finanzas-resumen');
        if (!container) return;
        
        try {
            const data = await FinanzasAPI.cargarResumen();
            // Adaptar al formato real del backend: {status, movimientos, resumen}
            const resumen = data.resumen || {};
            const ingresos = resumen.total_cobrado || resumen.total_anticipos || 0;
            const pendientes = resumen.total_pendiente || 0;
            const balance = ingresos - pendientes;
            
            container.innerHTML = `
                <div class="finanzas-cards">
                    <div class="card ingresos">
                        <h4>Ingresos</h4>
                        <p class="monto positivo">$${ingresos.toLocaleString()}</p>
                    </div>
                    <div class="card egresos">
                        <h4>Pendiente</h4>
                        <p class="monto negativo">$${pendientes.toLocaleString()}</p>
                    </div>
                    <div class="card balance">
                        <h4>Balance</h4>
                        <p class="monto ${balance >= 0 ? 'positivo' : 'negativo'}">
                            $${balance.toLocaleString()}
                        </p>
                    </div>
                </div>
            `;
        } catch (e) {
            container.innerHTML = `<p class="error">Error cargando finanzas: ${e.message}</p>`;
        }
    },
    
    async renderTabla(matterId = null) {
        const container = document.getElementById('finanzas-tabla');
        if (!container) return;
        
        try {
            const data = await FinanzasAPI.cargarTransacciones(matterId);
            // Adaptar al formato real del backend: {status, movimientos}
            const transacciones = data.movimientos || data.transacciones || [];
            
            container.innerHTML = `
                <table class="finanzas-table">
                    <thead>
                        <tr>
                            <th>Fecha</th>
                            <th>Concepto</th>
                            <th>Matter</th>
                            <th>Tipo</th>
                            <th>Monto</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${transacciones.map(t => `
                            <tr class="${t.tipo}">
                                <td>${t.fecha || '-'}</td>
                                <td>${t.concepto}</td>
                                <td>${t.matter_id || '-'}</td>
                                <td><span class="badge ${t.tipo}">${t.tipo}</span></td>
                                <td class="monto ${t.tipo}">$${(t.monto || 0).toLocaleString()}</td>
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
            `;
        } catch (e) {
            container.innerHTML = `<p class="error">Error cargando transacciones: ${e.message}</p>`;
        }
    }
};

// Exportar para uso global
window.FinanzasAPI = FinanzasAPI;
window.FinanzasUI = FinanzasUI;
