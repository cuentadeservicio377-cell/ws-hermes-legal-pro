// js/utils.js — Utilidades compartidas
// Willow Legal Pro v3.0

const Utils = {
  escape(str) {
    if (!str) return '';
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
  },
  
  formatDate(dateStr) {
    if (!dateStr) return 'Sin fecha';
    try {
      const date = new Date(dateStr);
      const hoy = new Date();
      const manana = new Date(hoy);
      manana.setDate(manana.getDate() + 1);
      
      // Comparar solo fechas
      const dateOnly = new Date(date.getFullYear(), date.getMonth(), date.getDate());
      const hoyOnly = new Date(hoy.getFullYear(), hoy.getMonth(), hoy.getDate());
      const mananaOnly = new Date(manana.getFullYear(), manana.getMonth(), manana.getDate());
      
      if (dateOnly.getTime() === hoyOnly.getTime()) {
        return 'Hoy';
      } else if (dateOnly.getTime() === mananaOnly.getTime()) {
        return 'Mañana';
      } else {
        return date.toLocaleDateString('es-MX', { 
          weekday: 'short', 
          day: 'numeric', 
          month: 'short' 
        });
      }
    } catch (e) {
      return dateStr;
    }
  },
  
  formatDateShort(dateStr) {
    if (!dateStr) return '';
    try {
      const date = new Date(dateStr);
      return date.toLocaleDateString('es-MX', { day: 'numeric', month: 'short' });
    } catch (e) {
      return dateStr;
    }
  },
  
  formatDateFull(dateStr) {
    if (!dateStr) return '';
    try {
      const date = new Date(dateStr);
      return date.toLocaleDateString('es-MX', { 
        weekday: 'long', 
        day: 'numeric', 
        month: 'long', 
        year: 'numeric' 
      });
    } catch (e) {
      return dateStr;
    }
  },
  
  diasRestantes(dateStr) {
    if (!dateStr) return null;
    try {
      const fecha = new Date(dateStr);
      const hoy = new Date();
      const diff = Math.ceil((fecha - hoy) / (1000 * 60 * 60 * 24));
      return diff;
    } catch (e) {
      return null;
    }
  },
  
  colorUrgencia(dias) {
    if (dias === null) return 'gray';
    if (dias < 0) return 'red';
    if (dias <= 2) return 'orange';
    if (dias <= 7) return 'yellow';
    return 'green';
  },
  
  formatMoney(amount) {
    if (amount === undefined || amount === null) return '$0.00';
    return new Intl.NumberFormat('es-MX', {
      style: 'currency',
      currency: 'MXN'
    }).format(amount);
  },
  
  debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
      const later = () => {
        clearTimeout(timeout);
        func(...args);
      };
      clearTimeout(timeout);
      timeout = setTimeout(later, wait);
    };
  }
};
