# PLAN MAESTRO v7 — POLISH + DOCUMENTACIÓN PARA ABOGADOS NO-DIGITAL

## Audiencia
Abogados de 30 a 75 años. Nivel digital: básico a intermedio. Nunca usaron un "dashboard". Usan WhatsApp, Excel básico, y Google Drive porque alguien les enseñó.

## Principios de diseño
1. **Cero suposiciones técnicas** — explicar cada clic
2. **Lenguaje legal, no técnico** — "Matter" no "entidad", "Carpeta" no "directorio"
3. **Visual + paso a paso** — screenshots descriptivos, numeración
4. **Fallback siempre** — si algo falla, qué hacer
5. **Un solo botón para cada acción** — no menús anidados

---

## FASE 1: FRONTEND ULTRA-SIMPLE (CSS + HTML)

### 1.1 Crear styles.css completo

**Archivo**: `dashboard/frontend/css/styles.css`

Requisitos:
- Tipografía grande (16px mínimo, 18px para botones)
- Contraste alto (fondo blanco, texto #1a1a1a, acentos azul #2563eb)
- Botones enormes (padding 16px 32px, border-radius 8px)
- Tarjetas con sombra suave (box-shadow: 0 2px 8px rgba(0,0,0,0.1))
- Estados visuales claros: verde éxito, rojo error, amarillo alerta
- Responsive: debe verse bien en laptop y tablet (iPad común en despachos)
- Modo oscuro opcional (toggle simple)

Secciones CSS:
```css
/* Base */
/* Layout: sidebar + main */
/* Header con logo Willow */
/* Tarjetas de resumen (matters, plazos, alertas) */
/* Tablas con hover y zebra striping */
/* Formularios con labels grandes */
/* Botones primario/secundario/peligro */
/* Badges de estado (activo, pendiente, urgente) */
/* Finanzas: cards de ingreso/egreso/balance */
/* Aprobaciones: lista con checkboxes */
/* Toast notifications */
/* Modal overlay */
/* Loading spinner */
/* Responsive */
/* Modo oscuro */
```

### 1.2 Rediseñar index.html

**Archivo**: `dashboard/frontend/index.html`

Estructura:
```html
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Willow Legal — Sistema de Gestión</title>
  <link rel="stylesheet" href="css/styles.css">
</head>
<body>
  <!-- Sidebar: logo + navegación -->
  <nav class="sidebar">
    <div class="logo">
      <img src="assets/logo-willow.png" alt="Willow Legal">
      <span>Willow Legal</span>
    </div>
    <ul class="nav-menu">
      <li><a href="#inicio" class="active">🏠 Inicio</a></li>
      <li><a href="#matters">📁 Casos (Matters)</a></li>
      <li><a href="#documentos">📄 Documentos</a></li>
      <li><a href="#plazos">⏰ Plazos</a></li>
      <li><a href="#finanzas">💰 Finanzas</a></li>
      <li><a href="#aprobaciones">✅ Aprobaciones</a></li>
      <li><a href="#alertas">🔔 Alertas</a></li>
    </ul>
    <div class="user-info">
      <span id="user-name">Abogado</span>
      <button id="btn-ayuda" class="btn-secundario">❓ Ayuda</button>
    </div>
  </nav>

  <!-- Main content -->
  <main class="main-content">
    <!-- Header con título y acciones rápidas -->
    <header class="main-header">
      <h1 id="page-title">Panel de Control</h1>
      <div class="quick-actions">
        <button id="btn-nuevo-matter" class="btn-primario">+ Nuevo Caso</button>
        <button id="btn-nuevo-documento" class="btn-primario">+ Nuevo Documento</button>
        <button id="btn-nuevo-plazo" class="btn-secundario">+ Nuevo Plazo</button>
      </div>
    </header>

    <!-- Dashboard resumen -->
    <section id="inicio" class="dashboard">
      <div class="cards-grid">
        <div class="card card-matters">
          <h3>Casos Activos</h3>
          <p class="big-number" id="count-matters">0</p>
          <a href="#matters">Ver todos →</a>
        </div>
        <div class="card card-plazos">
          <h3>Plazos esta semana</h3>
          <p class="big-number" id="count-plazos">0</p>
          <a href="#plazos">Ver plazos →</a>
        </div>
        <div class="card card-alertas">
          <h3>Alertas</h3>
          <p class="big-number" id="count-alertas">0</p>
          <a href="#alertas">Ver alertas →</a>
        </div>
        <div class="card card-balance">
          <h3>Balance Mes</h3>
          <p class="big-number" id="count-balance">$0</p>
          <a href="#finanzas">Ver finanzas →</a>
        </div>
      </div>
    </section>

    <!-- Sección Matters -->
    <section id="matters" class="section hidden">
      <h2>Mis Casos</h2>
      <div class="toolbar">
        <input type="search" id="search-matters" placeholder="Buscar caso...">
        <select id="filter-area">
          <option value="">Todas las áreas</option>
          <option value="corporativo">Corporativo</option>
          <option value="litigio">Litigio</option>
          <option value="fiscal">Fiscal</option>
          <option value="laboral">Laboral</option>
        </select>
      </div>
      <div id="matters-table-container">
        <!-- Tabla generada por JS -->
      </div>
    </section>

    <!-- Sección Documentos -->
    <section id="documentos" class="section hidden">
      <h2>Documentos</h2>
      <div class="toolbar">
        <button id="btn-generar-nda" class="btn-primario">Generar NDA</button>
        <button id="btn-generar-contrato" class="btn-primario">Generar Contrato</button>
        <button id="btn-generar-carta" class="btn-secundario">Generar Carta</button>
      </div>
      <div id="templates-list">
        <!-- Lista de templates -->
      </div>
    </section>

    <!-- Sección Plazos -->
    <section id="plazos" class="section hidden">
      <h2>Plazos y Vencimientos</h2>
      <div id="plazos-calendar">
        <!-- Vista de calendario simplificada -->
      </div>
      <div id="plazos-list">
        <!-- Lista de plazos -->
      </div>
    </section>

    <!-- Sección Finanzas -->
    <section id="finanzas" class="section hidden">
      <h2>Finanzas</h2>
      <div id="finanzas-resumen"></div>
      <div id="finanzas-tabla"></div>
      <div class="toolbar">
        <button id="btn-ingreso" class="btn-primario">+ Registrar Ingreso</button>
        <button id="btn-egreso" class="btn-peligro">+ Registrar Egreso</button>
      </div>
    </section>

    <!-- Sección Aprobaciones -->
    <section id="aprobaciones" class="section hidden">
      <h2>Aprobaciones Pendientes</h2>
      <div id="aprobaciones-list">
        <!-- Lista de documentos por aprobar -->
      </div>
    </section>

    <!-- Sección Alertas -->
    <section id="alertas" class="section hidden">
      <h2>Alertas del Sistema</h2>
      <div id="alertas-list"></div>
    </section>
  </main>

  <!-- Modal genérico -->
  <div id="modal" class="modal hidden">
    <div class="modal-content">
      <header class="modal-header">
        <h3 id="modal-title">Título</h3>
        <button id="modal-close" class="btn-icon">×</button>
      </header>
      <div id="modal-body"></div>
      <footer class="modal-footer">
        <button id="modal-cancel" class="btn-secundario">Cancelar</button>
        <button id="modal-confirm" class="btn-primario">Confirmar</button>
      </footer>
    </div>
  </div>

  <!-- Toast notifications -->
  <div id="toast-container"></div>

  <!-- Scripts -->
  <script src="js/api.js"></script>
  <script src="js/finanzas.js"></script>
  <script src="js/app.js"></script>
</body>
</html>
```

### 1.3 Actualizar app.js

**Archivo**: `dashboard/frontend/js/app.js`

Requisitos:
- Navegación por secciones (mostrar/ocultar)
- Render de tablas con botones de acción (Ver, Editar, Eliminar)
- Formularios modales para crear/editar
- Toast notifications (éxito, error, info)
- Loading states
- Confirmación antes de eliminar
- Búsqueda en tiempo real
- Filtros por área/estado
- Auto-refresh cada 30 segundos

Funciones clave:
```javascript
// Navegación
function showSection(sectionId)

// Matters
function renderMattersTable()
function openMatterModal(mode, matterId)
function deleteMatter(id)

// Documentos
function renderTemplatesList()
function generateDocument(templateId, matterId)

// Plazos
function renderPlazosList()
function openPlazoModal()

// Finanzas (usa FinanzasUI)
function renderFinanzas()

// Aprobaciones
function renderAprobacionesList()
function approveDocument(id)

// Alertas
function renderAlertas()

// UI helpers
function showToast(message, type)
function showModal(title, content, onConfirm)
function hideModal()
function setLoading(element, isLoading)
```

---

## FASE 2: MANUALES DE USUARIO

### 2.1 MANUAL_ABOGADO_COMPLETO.md

**Audiencia**: Abogado de 50 años, nunca usó un sistema de gestión.

Estructura:
```
# Manual de Usuario — Willow Legal

## 1. ¿Qué es Willow Legal?
(1 párrafo, lenguaje humano)

## 2. Primeros pasos
### 2.1 Abrir el sistema
(paso a paso con screenshot descriptivo)
### 2.2 Tu pantalla principal
(explicar cada zona: sidebar, tarjetas, botones)
### 2.3 Crear tu primer Caso
(paso 1, paso 2, paso 3...)

## 3. Casos (Matters)
### 3.1 Ver mis casos
### 3.2 Crear un caso nuevo
### 3.3 Editar un caso
### 3.4 Buscar un caso
### 3.5 Cerrar o eliminar un caso

## 4. Documentos
### 4.1 Generar un documento
### 4.2 Ver documentos en Google Drive
### 4.3 Editar un documento

## 5. Plazos
### 5.1 Crear un plazo
### 5.2 Ver plazos en calendario
### 5.3 Recibir alertas de plazos

## 6. Finanzas
### 6.1 Registrar un cobro
### 6.2 Registrar un gasto
### 6.3 Ver balance

## 7. Aprobaciones
### 7.1 Aprobar un documento
### 7.2 Ver historial

## 8. Alertas
### 8.1 Entender las alertas
### 8.2 Configurar alertas

## 9. Problemas comunes
### 9.1 "No puedo entrar"
### 9.2 "No veo mi caso"
### 9.3 "El documento no se generó"
### 9.4 "No me llegan alertas"
### 9.5 "Todo está muy lento"

## 10. Glosario
(Matter = Caso, Template = Modelo, etc.)

## 11. Soporte
(Cómo contactar a WS Capital)
```

### 2.2 MANUAL_HERMES_INTEGRATION.md

**Audiencia**: Abogado que quiere usar Willow por Telegram.

Estructura:
```
# Manual — Willow Legal por Telegram

## 1. ¿Qué es Hermes?
(Tu asistente virtual en Telegram)

## 2. Comandos disponibles
### /matter nuevo "Nombre" area=Corporativo
### /matter list
### /contrato nda WIL-001
### /plazo nuevo WIL-001 "Audiencia" 2026-06-15
### /status
### /alerta

## 3. Ejemplos de conversaciones
(5 ejemplos reales de chat)

## 4. Cómo recibir documentos
(PDFs en Telegram + link a Drive)

## 5. Alertas automáticas
(Cómo configurar)
```

### 2.3 MANUAL_TECNICO.md

**Audiencia**: Persona técnica que instala o da soporte.

Estructura:
```
# Manual Técnico

## 1. Arquitectura
## 2. Requisitos técnicos
## 3. Instalación paso a paso
## 4. Configuración de Google Workspace
## 5. Backup y restauración
## 6. Troubleshooting técnico
## 7. API Reference
```

---

## FASE 3: MEJORAS UX

### 3.1 Onboarding wizard

Primer inicio: modal de bienvenida con 3 pasos:
1. "Bienvenido a Willow Legal" — qué es
2. "Conecta tu Google" — botón de auth
3. "Crea tu primer caso" — formulario simplificado

### 3.2 Tooltips y ayuda en contexto

- Cada botón tiene tooltip explicativo
- Icono ❓ en cada sección abre mini-guía
- "¿Necesitas ayuda?" flotante en esquina

### 3.3 Empty states amigables

- Tabla vacía: "No hay casos aún. Crea tu primer caso →"
- Sin plazos: "Sin plazos pendientes. ¡Buen trabajo!"
- Sin alertas: "Todo en orden. No hay alertas."

### 3.4 Confirmaciones y undo

- Eliminar: "¿Seguro? Este caso se moverá a papelera"
- Undo: "Caso eliminado. Deshacer (5s)"

### 3.5 Notificaciones visuales

- Toast en esquina superior derecha
- Badge rojo en sidebar cuando hay alertas nuevas
- Sonido opcional para alertas urgentes

---

## FASE 4: ASSETS VISUALES

### 4.1 Logo y branding

- Logo "Willow Legal" (texto + icono árbol/sauz)
- Favicon
- Colores oficiales documentados

### 4.2 Iconografía

- Usar emojis nativos (no dependencias externas)
- O librería ligera: Phosphor Icons o Heroicons

### 4.3 Screenshots de referencia

Crear descripciones de screenshots para el manual:
- "Pantalla principal con 4 tarjetas grandes"
- "Modal de nuevo caso con formulario"
- "Lista de documentos con botones de acción"

---

## FASE 5: TESTS DE USABILIDAD

### 5.1 Checklist de accesibilidad

- [ ] Texto legible sin zoom
- [ ] Contraste WCAG AA
- [ ] Navegación por teclado
- [ ] Labels en todos los formularios
- [ ] Focus visible en elementos interactivos

### 5.2 Test con persona no-técnica

Simular: abogado de 60 años, primera vez:
- ¿Puede crear un caso sin ayuda?
- ¿Puede generar un documento?
- ¿Puede encontrar un caso creado ayer?
- ¿Entiende qué es un "plazo"?

---

## ENTREGABLES v7

| # | Archivo | Descripción |
|---|---------|-------------|
| 1 | `dashboard/frontend/css/styles.css` | Estilos completos, responsive, modo oscuro |
| 2 | `dashboard/frontend/index.html` | HTML reestructurado, navegación por secciones |
| 3 | `dashboard/frontend/js/app.js` | App.js completo con modales, toasts, navegación |
| 4 | `docs/MANUAL_ABOGADO_COMPLETO.md` | Manual paso a paso para abogados |
| 5 | `docs/MANUAL_HERMES_INTEGRATION.md` | Manual de uso por Telegram |
| 6 | `docs/MANUAL_TECNICO.md` | Manual técnico para instalación/soporte |
| 7 | `assets/logo-willow.png` | Logo (placeholder si no hay diseñador) |
| 8 | `docs/CHANGELOG_v7.md` | Qué cambió en esta versión |

---

## TESTS DE VERIFICACIÓN

```bash
# 1. Verificar CSS carga
ls -la dashboard/frontend/css/styles.css

# 2. Verificar HTML tiene todas las secciones
grep -c "section id=" dashboard/frontend/index.html

# 3. Verificar manuales existen
ls -la docs/MANUAL_*.md

# 4. Abrir index.html en navegador y verificar:
#    - Sidebar visible
#    - Tarjetas de resumen
#    - Navegación funciona
#    - Modal se abre
#    - Toast aparece

# 5. Test responsive (redimensionar ventana)
```

## GIT

```bash
git add -A
git commit -m "v7: Polish completo + documentación para abogados no-digital"
git push origin master
git log --oneline -3
```
