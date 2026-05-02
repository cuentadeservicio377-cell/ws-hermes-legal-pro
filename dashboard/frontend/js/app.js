// js/app.js — Router y estado global

const App = {
    // Estado global
    state: {
        currentView: 'dashboard',
        matters: [],
        templates: [],
        loading: false
    },

    // Inicializar
    async init() {
        console.log('🏛️ Hermes Legal Pro v3.0 iniciando...');
        
        // Verificar API
        try {
            const health = await API.health();
            console.log('✅ API conectada:', health);
        } catch (err) {
            console.error('❌ API no disponible:', err);
            this.showError('No se puede conectar al servidor. ¿Está corriendo el backend?');
            return;
        }

        // Cargar datos base
        await this.loadBaseData();

        // Setup navegación
        this.setupNavigation();

        // Mostrar vista inicial
        this.navigate('dashboard');
    },

    // Cargar datos que necesitan todas las vistas
    async loadBaseData() {
        try {
            const [templates] = await Promise.all([
                API.templates()
            ]);
            this.state.templates = templates.templates || [];
        } catch (err) {
            console.error('Error cargando datos base:', err);
        }
    },

    // Setup clicks en navegación
    setupNavigation() {
        document.querySelectorAll('.nav-item').forEach(item => {
            item.addEventListener('click', (e) => {
                e.preventDefault();
                const view = item.dataset.view;
                if (view) this.navigate(view);
            });
        });
    },

    // Cambiar vista
    navigate(view) {
        console.log('Navegando a:', view);
        
        // Actualizar estado
        this.state.currentView = view;

        // Actualizar navegación activa
        document.querySelectorAll('.nav-item').forEach(item => {
            item.classList.toggle('active', item.dataset.view === view);
        });

        // Ocultar todas las vistas
        document.querySelectorAll('.view').forEach(v => v.classList.add('hidden'));

        // Mostrar vista seleccionada
        const target = document.getElementById(`view-${view}`);
        if (target) {
            target.classList.remove('hidden');
        } else {
            console.error('Vista no encontrada:', view);
            return;
        }

        // Cargar contenido de la vista
        this.loadView(view);
    },

    // Cargar contenido según vista
    async loadView(view) {
        this.setLoading(true);
        
        try {
            switch(view) {
                case 'dashboard':
                    await this.loadDashboard();
                    break;
                case 'matters':
                    await this.loadMatters();
                    break;
                case 'reuniones':
                    await this.loadReuniones();
                    break;
                case 'documentos':
                    await this.loadDocumentos();
                    break;
                case 'calendario':
                    await this.loadCalendario();
                    break;
                default:
                    console.error('Vista desconocida:', view);
            }
        } catch (err) {
            console.error('Error cargando vista:', err);
            this.showError(`Error cargando ${view}: ${err.message}`);
        } finally {
            this.setLoading(false);
        }
    },

    // Placeholders para vistas (se implementan en fases siguientes)
    async loadDashboard() {
        await Dashboard.render();
    },

    async loadMatters() {
        await Matters.render();
    },

    async loadReuniones() {
        await Reuniones.render();
    },

    async loadDocumentos() {
        await Documentos.render();
    },

    async loadCalendario() {
        await Calendario.render();
    },

    // Modal
    showModal(id) {
        const modal = document.getElementById(id);
        if (modal) modal.classList.remove('hidden');
    },

    hideModal(id) {
        const modal = document.getElementById(id);
        if (modal) modal.classList.add('hidden');
    },

    // Loading
    setLoading(loading) {
        this.state.loading = loading;
        document.body.classList.toggle('loading', loading);
    },

    // Error
    showError(message) {
        const container = document.getElementById('main-content') || document.body;
        const alert = document.createElement('div');
        alert.className = 'alert alert-red';
        alert.innerHTML = `<strong>Error:</strong> ${message}`;
        container.insertBefore(alert, container.firstChild);
        
        setTimeout(() => alert.remove(), 5000);
    }
};

// Inicializar cuando carga la página
document.addEventListener('DOMContentLoaded', () => App.init());

window.App = App;
