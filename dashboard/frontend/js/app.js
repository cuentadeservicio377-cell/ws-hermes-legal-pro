// js/app.js — Router, navegación táctil, y coordinación de vistas
// Willow Legal Pro v3.0 — Mobile-first SPA

const App = {
  currentView: 'dashboard',
  modalOpen: false,
  
  // Inicialización
  init() {
    // Cargar vista inicial
    this.navigate('dashboard', false);
    
    // Setup eventos táctiles
    this.setupTouchEvents();
    
    // Actualizar badge de alertas periódicamente
    this.updateAlertBadge();
    setInterval(() => this.updateAlertBadge(), 30000);
    
    console.log('✅ Willow Legal Pro v3.0 iniciado');
  },
  
  // Navegación entre vistas
  navigate(view, pushState = true) {
    if (this.modalOpen) {
      this.closeModal();
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
    
    // Actualizar navegación inferior
    document.querySelectorAll('.nav-item').forEach(item => {
      item.classList.toggle('active', item.dataset.view === view);
    });
    
    // Actualizar FAB según vista
    this.updateFab();
    
    // Renderizar contenido específico
    this.renderView(view);
    
    // Scroll al top
    window.scrollTo({ top: 0, behavior: 'smooth' });
    
    // Push state para navegación del browser
    if (pushState && window.history) {
      window.history.pushState({ view }, '', `#${view}`);
    }
  },
  
  // Renderizar contenido de cada vista
  async renderView(view) {
    switch(view) {
      case 'dashboard':
        await Dashboard.render();
        break;
      case 'reuniones':
        await Reuniones.render();
        break;
      case 'documentos':
        await Documentos.render();
        break;
      case 'matters':
        await Matters.render();
        break;
      case 'alertas':
        await Dashboard.renderAlertas();
        break;
    }
  },
  
  // Actualizar FAB según vista actual
  updateFab() {
    const fab = document.getElementById('fab-action');
    const views = {
      'dashboard': { icon: '+', action: () => this.showNewReunionModal() },
      'reuniones': { icon: '+', action: () => Reuniones.showCreateModal() },
      'documentos': { icon: '+', action: () => Documentos.showCreateModal() },
      'matters': { icon: '+', action: () => Matters.showCreateModal() },
      'alertas': { icon: '✓', action: () => Dashboard.markAllRead() }
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
      const count = alertas ? alertas.filter(a => !a.resuelta).length : 0;
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
        this.navigate(e.state.view, false);
      }
    });
  },
  
  handleSwipe() {
    const swipeThreshold = 100;
    const diff = touchStartX - touchEndX;
    
    if (Math.abs(diff) > swipeThreshold) {
      const views = ['dashboard', 'reuniones', 'documentos', 'matters'];
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
  
  // Nueva reunión desde dashboard
  showNewReunionModal() {
    Reuniones.showCreateModal();
  }
};

// Inicializar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', () => {
  App.init();
});
