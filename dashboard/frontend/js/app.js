// js/app.js — Router, navegación táctil, y coordinación de vistas
// Willow Legal Pro v3.1 — Despacho Judicial Mexicano (Lic. Narváez)

const App = {
  currentView: 'dashboard',
  modalOpen: false,
  previousView: null,
  
  // Inicialización
  init() {
    // Cargar vista inicial
    this.navigate('dashboard', false);
    
    // Setup eventos táctiles
    this.setupTouchEvents();
    
    // Actualizar badge de alertas periódicamente
    this.updateAlertBadge();
    setInterval(() => this.updateAlertBadge(), 30000);
    
    console.log('✅ Willow Legal Pro v3.1 — Despacho Lic. Narváez iniciado');
  },
  
  // Navegación entre vistas
  navigate(view, pushState = true, data = null) {
    if (this.modalOpen) {
      this.closeModal();
    }
    
    // Guardar vista anterior para volver
    if (view !== this.currentView && !view.startsWith('expediente-') && !view.startsWith('cliente-')) {
      this.previousView = this.currentView;
    }
    
    // Ocultar todas las vistas
    document.querySelectorAll('.view').forEach(v => {
      v.classList.remove('active');
    });
    
    // Mostrar vista objetivo
    const targetView = document.getElementById(`view-${view}`);
    if (targetView) {
      targetView.classList.add('active');
      this.currentView = view;
    }
    
    // Actualizar navegación inferior (solo para vistas principales)
    if (!view.startsWith('expediente-') && !view.startsWith('cliente-')) {
      document.querySelectorAll('.nav-item').forEach(item => {
        item.classList.toggle('active', item.dataset.view === view);
      });
    }
    
    // Actualizar FAB según vista
    this.updateFab();
    
    // Renderizar contenido específico
    this.renderView(view, data);
    
    // Scroll al top
    window.scrollTo({ top: 0, behavior: 'smooth' });
    
    // Push state para navegación del browser
    if (pushState && window.history) {
      window.history.pushState({ view, data }, '', `#${view}`);
    }
  },
  
  // Renderizar contenido de cada vista
  async renderView(view, data = null) {
    switch(view) {
      case 'dashboard':
        await Dashboard.render();
        break;
      case 'expedientes':
        await Expedientes.render();
        break;
      case 'clientes':
        await Clientes.render();
        break;
      case 'documentos':
        await Documentos.render();
        break;
      case 'alertas':
        await Dashboard.renderAlertas();
        break;
      case 'expediente-detalle':
        if (data && data.expedienteId) {
          await Expedientes.renderDetalle(data.expedienteId);
        }
        break;
      case 'cliente-detalle':
        if (data && data.clienteId) {
          await Clientes.renderDetalle(data.clienteId);
        }
        break;
    }
  },
  
  // Volver a la vista anterior
  goBack() {
    if (this.previousView) {
      this.navigate(this.previousView);
    } else {
      this.navigate('dashboard');
    }
  },
  
  // Actualizar FAB según vista actual
  updateFab() {
    const fab = document.getElementById('fab-action');
    const views = {
      'dashboard': { icon: '+', action: () => this.showNewExpedienteModal() },
      'expedientes': { icon: '+', action: () => Expedientes.showCreateModal() },
      'clientes': { icon: '+', action: () => Clientes.showCreateModal() },
      'documentos': { icon: '+', action: () => Documentos.showCreateModal() },
      'alertas': { icon: '✓', action: () => Dashboard.markAllRead() },
      'expediente-detalle': { icon: '✎', action: () => Expedientes.showEditModal() },
      'cliente-detalle': { icon: '✎', action: () => Clientes.showEditModal() }
    };
    
    const config = views[this.currentView] || views['dashboard'];
    fab.textContent = config.icon;
    fab.onclick = config.action;
  },
  
  handleFab() {
    // Delegado a updateFab
  },
  
  // Modal system
  openModal(content) {
    const overlay = document.getElementById('modal-overlay');
    const modalContent = document.getElementById('modal-content');
    
    modalContent.innerHTML = content;
    overlay.classList.add('active');
    this.modalOpen = true;
    
    // Prevenir scroll del body
    document.body.style.overflow = 'hidden';
  },
  
  closeModal(event) {
    if (event && event.target !== event.currentTarget && event.target.closest('.modal')) {
      return;
    }
    
    const overlay = document.getElementById('modal-overlay');
    overlay.classList.remove('active');
    this.modalOpen = false;
    
    // Restaurar scroll
    document.body.style.overflow = '';
    
    // Limpiar contenido después de la animación
    setTimeout(() => {
      if (!this.modalOpen) {
        document.getElementById('modal-content').innerHTML = '';
      }
    }, 300);
  },
  
  // Toast notifications
  showToast(message, type = 'info') {
    const toast = document.getElementById('toast');
    toast.textContent = message;
    toast.className = `toast ${type}`;
    
    requestAnimationFrame(() => {
      toast.classList.add('show');
    });
    
    setTimeout(() => {
      toast.classList.remove('show');
    }, 3000);
  },
  
  // Actualizar badge de alertas
  async updateAlertBadge() {
    try {
      const alertas = await API.alertas();
      const count = alertas ? alertas.filter(a => a.estado === 'pendiente').length : 0;
      const badge = document.getElementById('alert-badge');
      badge.textContent = count;
      badge.style.display = count > 0 ? 'flex' : 'none';
    } catch (e) {
      // Silencioso
    }
  },
  
  // Eventos táctiles
  setupTouchEvents() {
    let touchStartX = 0;
    let touchEndX = 0;
    
    document.addEventListener('touchstart', (e) => {
      touchStartX = e.changedTouches[0].screenX;
    }, { passive: true });
    
    document.addEventListener('touchend', (e) => {
      touchEndX = e.changedTouches[0].screenX;
      this.handleSwipe();
    }, { passive: true });
    
    // Back button del browser
    window.addEventListener('popstate', (e) => {
      if (e.state && e.state.view) {
        this.navigate(e.state.view, false, e.state.data);
      }
    });
  },
  
  handleSwipe() {
    const swipeThreshold = 100;
    const diff = touchStartX - touchEndX;
    
    if (Math.abs(diff) > swipeThreshold) {
      const views = ['dashboard', 'expedientes', 'clientes', 'documentos'];
      const currentIndex = views.indexOf(this.currentView);
      
      if (diff > 0 && currentIndex < views.length - 1) {
        // Swipe left → siguiente
        this.navigate(views[currentIndex + 1]);
      } else if (diff < 0 && currentIndex > 0) {
        // Swipe right → anterior
        this.navigate(views[currentIndex - 1]);
      }
    }
  },
  
  // Nuevo expediente desde dashboard
  showNewExpedienteModal() {
    Expedientes.showCreateModal();
  }
};

// Inicializar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', () => {
  App.init();
});
