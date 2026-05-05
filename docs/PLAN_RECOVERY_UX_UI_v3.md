# 📋 PLAN DE RECUPERACIÓN — Flujo Centrado en Reuniones (UX/UI v3.0)

## 🎯 PROBLEMA ACTUAL

El dashboard v2.0 es:
- ❌ Técnico y frío (lista de matters con IDs)
- ❌ No tiene flujo natural de trabajo
- ❌ No está centrado en la experiencia del abogado
- ❌ Requiere navegación manual entre secciones

## 🌟 FLUJO IDEAL (Recuperado del v8.1)

El flujo que funcionaba era **centrado en reuniones**:

```
1. Abogado tiene sesión Google Meet con cliente
   ↓
2. Registra la reunión (URL Meet, notas, transcript)
   ↓
3. Sistema procesa automáticamente:
   - Extrae acuerdos
   - Detecta documentos necesarios
   - Crea plazos implícitos
   - Sugiere next steps
   ↓
4. Dashboard muestra:
   - Reuniones pendientes de procesar
   - Documentos sugeridos por generar
   - Plazos detectados
   - KPIs visuales (no listas técnicas)
```

## 🎨 NUEVO DISEÑO UX/UI v3.0

### Principios
1. **Móvil primero** — El abogado usa tablet/teléfono en la oficina
2. **Visual, no textual** — Cards, iconos, colores de estado
3. **Flujo guiado** — No navegación libre, pasos secuenciales
4. **Acción inmediata** — Cada pantalla tiene CTA claro
5. **Feedback visual** — Estados con colores, no badges técnicos

### Estructura de Pantallas

#### 1. **Home / Dashboard** (Pantalla principal)
```
┌─────────────────────────────┐
│  ⚖️ Willow Legal    🔔 3    │  ← Header simple
├─────────────────────────────┤
│                             │
│  📊 RESUMEN DEL DÍA         │  ← Sección visual
│  ┌─────┐ ┌─────┐ ┌─────┐   │
│  │ 🎤  │ │ 📄  │ │ ⏰  │   │  ← KPIs como cards
│  │  2  │ │  5  │ │  3  │   │     táctiles grandes
│  │Reun │ │Docs │ │Plaz │   │
│  └─────┘ └─────┘ └─────┘   │
│                             │
│  🚨 ACCIONES URGENTES       │  ← Lista prioritaria
│  ┌───────────────────────┐   │
│  │ ⚡ Procesar reunión   │   │  ← CTA grande
│  │    con Juan Pérez     │   │     (fácil tocar)
│  └───────────────────────┘   │
│                             │
│  📅 PRÓXIMAS REUNIONES      │  ← Timeline visual
│  └── Hoy ──┘                │
│  └── Mañana ──┘             │
│                             │
│  [ + NUEVA REUNIÓN ]        │  ← FAB (Floating Action Button)
│                             │
└─────────────────────────────┘
```

#### 2. **Flujo Nueva Reunión** (Wizard de 3 pasos)
```
PASO 1: Datos básicos
┌─────────────────────────────┐
│  ← Nueva Reunión      1/3   │
├─────────────────────────────┤
│                             │
│  📅 Fecha: [Hoy        ▼]   │
│                             │
│  👤 Cliente:              │
│  [Buscar cliente...    🔍]  │  ← Autocomplete
│                             │
│  o [ + Nuevo Cliente ]      │
│                             │
│  📹 URL Meet:               │
│  [pegar link...          ]  │
│                             │
│  [ CONTINUAR → ]            │
│                             │
└─────────────────────────────┘

PASO 2: Durante/Después de la reunión
┌─────────────────────────────┐
│  ← Reunión con Juan    2/3   │
├─────────────────────────────┤
│                             │
│  🎤 TRANSCRIPT / NOTAS      │
│  ┌─────────────────────┐    │
│  │                     │    │  ← Área grande
│  │  [Pega transcript   │    │     para pegar
│  │   o escribe...]     │    │     fácilmente
│  │                     │    │
│  └─────────────────────┘    │
│                             │
│  ⚡ PROCESAR CON IA         │  ← Botón destacado
│  (extraer acuerdos          │
│   automáticamente)          │
│                             │
│  o [ GUARDAR BORRADOR ]     │
│                             │
└─────────────────────────────┘

PASO 3: Resultados procesados
┌─────────────────────────────┐
│  ← Reunión con Juan    3/3   │
├─────────────────────────────┤
│                             │
│  ✅ ACUERDOS DETECTADOS     │
│  ┌─────────────────────┐    │
│  │ ☑ Pagar anticipo    │    │  ← Checkboxes
│  │ ☑ Enviar contrato   │    │     para marcar
│  │ ☐ Revisar estatutos │    │
│  └─────────────────────┘    │
│                             │
│  📄 DOCUMENTOS SUGERIDOS    │
│  ┌─────────────────────┐    │
│  │ • Contrato de prest.│ 📄 │  ← Cards clickeables
│  │ • NDA               │ 📄 │
│  │ • Carta de términos │ 📄 │
│  └─────────────────────┘    │
│                             │
│  ⏰ PLAZOS DETECTADOS       │
│  ┌─────────────────────┐    │
│  │ 15 mayo — Pagar    │ 🔴 │  ← Urgencia visual
│  │ 20 mayo — Enviar   │ 🟡 │
│  └─────────────────────┘    │
│                             │
│  [ FINALIZAR Y CREAR MATTER ]│
│                             │
└─────────────────────────────┘
```

#### 3. **Vista Reuniones** (Lista visual)
```
┌─────────────────────────────┐
│  ← Reuniones        [+]     │
├─────────────────────────────┤
│  [Todas] [Hoy] [Pend] [Proc]│  ← Filtros tipo chips
├─────────────────────────────┤
│                             │
│  ┌─────────────────────┐    │
│  │ 🎤 Juan Pérez       │    │  ← Card grande
│  │ 📅 Hoy, 10:30 AM    │    │     fácil de tocar
│  │ ⚡ PENDIENTE         │    │     (amarillo)
│  │ 📄 3 docs sugeridos │    │
│  │ ⏰ 2 plazos          │    │
│  └─────────────────────┘    │
│                             │
│  ┌─────────────────────┐    │
│  │ 🎤 María García     │    │
│  │ 📅 Ayer, 3:00 PM    │    │
│  │ ✅ PROCESADA        │    │  ← Verde = listo
│  │ 📄 2 docs generados │    │
│  └─────────────────────┘    │
│                             │
└─────────────────────────────┘
```

#### 4. **Vista Documentos** (Asociados a reunión)
```
┌─────────────────────────────┐
│  ← Documentos       [+]     │
├─────────────────────────────┤
│  📄 De: Reunión Juan Pérez  │  ← Contexto visible
├─────────────────────────────┤
│                             │
│  ┌─────────────────────┐    │
│  │ 📄 Contrato de      │    │
│  │    Prestación        │    │
│  │    ━━━━━━━━━━       │    │  ← Preview visual
│  │    Preview...       │    │     del documento
│  │                     │    │
│  │ [👁 Ver] [✏ Editar]│    │
│  │ [📤 Enviar] [✓ Firm]│    │  ← Acciones rápidas
│  └─────────────────────┘    │
│                             │
└─────────────────────────────┘
```

## 🛠️ IMPLEMENTACIÓN TÉCNICA

### Archivos a Modificar/Crear

| Archivo | Acción | Descripción |
|---------|--------|-------------|
| `index.html` | **Reescribir** | Estructura SPA con vistas |
| `css/kami.css` | **Recuperar** | Estilos v8.1 + mejoras responsive |
| `js/app.js` | **Reescribir** | Router simple, navegación táctil |
| `js/dashboard.js` | **Reescribir** | Vista home con KPIs visuales |
| `js/reuniones.js` | **Recuperar** | Flujo wizard de 3 pasos |
| `js/documentos.js` | **Adaptar** | Vista asociada a reunión |
| `js/matters.js` | **Simplificar** | Creación automática desde reunión |
| `js/api.js` | **Mantener** | Endpoints ya funcionan |

### Cambios en Backend (mínimos)
- Los endpoints `/api/reuniones` ya existen y funcionan
- Solo necesitamos asegurar que el procesamiento de transcript extraiga:
  - Acuerdos (lista de strings)
  - Documentos sugeridos (lista de template_keys)
  - Plazos (lista de {descripcion, fecha})

### Responsive Breakpoints
```css
/* Mobile first */
:root {
  --card-padding: 16px;
  --font-base: 16px;  /* No zoom en iOS */
  --touch-min: 44px;  /* Área táctil mínima */
}

/* Tablet */
@media (min-width: 768px) {
  --card-padding: 24px;
  --sidebar-width: 280px;
}

/* Desktop */
@media (min-width: 1200px) {
  --max-width: 1400px;
  --grid-columns: 3;
}
```

## 📱 INTERACCIONES TÁCTILES

### Gestos
- **Swipe left** en card de reunión → Acciones rápidas (procesar, eliminar)
- **Pull down** en lista → Refrescar
- **Long press** en documento → Menú contextual

### Transiciones
- **Entre vistas**: Slide horizontal (como app móvil)
- **Modal**: Fade + scale desde abajo
- **Carga**: Skeleton screens, no spinners

## 🎨 PALETA DE COLORES (Kami v3)

```css
:root {
  /* Primarios */
  --color-primary: #1B365D;      /* Azul legal */
  --color-primary-light: #2a4a7a;
  
  /* Estados */
  --color-success: #059669;      /* Verde */
  --color-warning: #d97706;      /* Naranja */
  --color-danger: #dc2626;       /* Rojo */
  --color-info: #2563eb;         /* Azul info */
  
  /* Neutros */
  --color-bg: #faf9f4;           /* Papel pergamino */
  --color-card: #ffffff;
  --color-text: #1a1a18;
  --color-text-secondary: #6b6a63;
  --color-border: #e8e6dc;
  
  /* Acción */
  --color-fab: #8B0000;          /* Rojo oscuro */
}
```

## ✅ CHECKLIST DE IMPLEMENTACIÓN

### Fase 1: Estructura Base
- [ ] Reescribir `index.html` con nueva estructura SPA
- [ ] Crear `css/kami.css` con sistema de diseño
- [ ] Implementar router en `js/app.js`

### Fase 2: Dashboard
- [ ] KPIs visuales (cards grandes)
- [ ] Acciones urgentes (lista priorizada)
- [ ] Timeline de reuniones
- [ ] FAB (Floating Action Button)

### Fase 3: Flujo Reuniones
- [ ] Wizard paso 1: Datos básicos
- [ ] Wizard paso 2: Transcript + procesamiento IA
- [ ] Wizard paso 3: Resultados + acciones
- [ ] Lista de reuniones (cards visuales)
- [ ] Detalle de reunión

### Fase 4: Documentos
- [ ] Vista asociada a reunión
- [ ] Preview visual
- [ ] Acciones rápidas

### Fase 5: Polish
- [ ] Animaciones y transiciones
- [ ] Gestos táctiles
- [ ] Modo oscuro (opcional)
- [ ] Offline básico (cache)

## 🚀 ENTREGABLE

Un dashboard que:
1. Se vea como una **app móvil moderna** (no como ERP)
2. Tenga **flujo natural** desde reunión → documentos → plazos
3. Sea **100% táctil** (usable en tablet del abogado)
4. Tenga **feedback visual inmediato** (colores, animaciones)
5. **No requiera entrenamiento** (intuitivo)

## 📁 ARCHIVOS DE REFERENCIA

Para recuperar código del flujo anterior:
- `git show 75e312a:dashboard/frontend/` — FASE 4 (Reuniones)
- `git show 627a89d:dashboard/frontend/` — FASE 2 (Dashboard vivo)
- `git show 16814db:dashboard/frontend/` — v7 (Polish completo)

## ⚠️ NOTAS IMPORTANTES

1. **NO usar `design_system.css` actual** — es orfano y no está diseñado para táctil
2. **NO mantener la navegación sidebar actual** — ocupa espacio en móvil
3. **NO usar tablas ni listas técnicas** — solo cards visuales
4. **SIEMPRE mostrar contexto** — "Documentos de: Reunión con Juan"
5. **SIEMPRE tener CTA claro** — cada pantalla tiene acción principal
