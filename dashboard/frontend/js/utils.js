// js/utils.js — Helpers de formateo

const Utils = {
    // Fecha: "2026-05-15" → "15 de mayo de 2026"
    formatDate(dateStr) {
        if (!dateStr) return 'Sin fecha';
        const d = new Date(dateStr + 'T00:00:00');
        return d.toLocaleDateString('es-MX', { day: 'numeric', month: 'long', year: 'numeric' });
    },

    // Fecha corta: "2026-05-15" → "15 may"
    formatDateShort(dateStr) {
        if (!dateStr) return '—';
        const d = new Date(dateStr + 'T00:00:00');
        return d.toLocaleDateString('es-MX', { day: 'numeric', month: 'short' });
    },

    // Días restantes: calcula desde hoy
    diasRestantes(dateStr) {
        if (!dateStr) return null;
        const hoy = new Date();
        hoy.setHours(0,0,0,0);
        const fecha = new Date(dateStr + 'T00:00:00');
        const diff = Math.floor((fecha - hoy) / (1000 * 60 * 60 * 24));
        return diff;
    },

    // Color según días restantes
    colorUrgencia(dias) {
        if (dias === null) return 'gray';
        if (dias < 0) return 'red';      // Vencido
        if (dias <= 3) return 'red';     // Crítico
        if (dias <= 7) return 'yellow';  // Próximo
        return 'green';                  // Tranquilo
    },

    // Badge HTML según urgencia
    badgeUrgencia(dias) {
        const color = this.colorUrgencia(dias);
        const text = dias === null ? 'SIN PLAZO' : 
                     dias < 0 ? `VENCIDO ${Math.abs(dias)} días` :
                     dias === 0 ? 'HOY' :
                     dias === 1 ? '1 día' :
                     `${dias} días`;
        return `<span class="badge badge-${color}">${text}</span>`;
    },

    // Moneda: 150000 → "$150,000 MXN"
    formatMoney(amount) {
        if (!amount && amount !== 0) return 'Por definir';
        return '$' + amount.toLocaleString('es-MX') + ' MXN';
    },

    // Prioridad: "alta" → "ALTA" con color
    badgePrioridad(p) {
        const map = { alta: 'red', media: 'yellow', baja: 'green' };
        const color = map[p] || 'gray';
        return `<span class="badge badge-${color}">${(p || 'MEDIA').toUpperCase()}</span>`;
    },

    // Estado: "activo" → "ACTIVO"
    badgeEstado(e) {
        const map = { activo: 'green', cerrado: 'gray', urgente: 'red' };
        const color = map[e] || 'gray';
        return `<span class="badge badge-${color}">${(e || 'ACTIVO').toUpperCase()}</span>`;
    },

    // Escapar HTML para evitar XSS
    escape(html) {
        const div = document.createElement('div');
        div.textContent = html;
        return div.innerHTML;
    },

    // Spinner de carga
    spinner() {
        return '<div class="spinner"></div>';
    }
};

window.Utils = Utils;
