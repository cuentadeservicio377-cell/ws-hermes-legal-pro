# HERMES LEGAL PRO v3.0
## Plan de Construcción — Dashboard Interactivo Completo
### Diseñado para OpenCode Go | MacBook Air M2

---

## 📋 RESUMEN EJECUTIVO

**Objetivo:** Construir un dashboard legal realmente interactivo que un abogado mexicano pueda usar sin saber tecnología.

**Stack:**
- Backend: FastAPI (Python) — ya existe, se extiende
- Frontend: HTML5 + Vanilla JS (sin frameworks) — máxima compatibilidad
- Estilos: CSS con sistema de diseño Kami v3
- Datos: JSON local + Excel maestro
- Motor: Kami v3 (WeasyPrint) — ya existe

**Entregable:** Un solo archivo `index.html` funcional que se conecta a la API y hace TODO.

---

## 🏗️ ARQUITECTURA FRONTEND v3.0

### Patrón: SPA (Single Page Application)
Una sola página HTML que cambia de "pantalla" sin recargar.

```
┌─────────────────────────────────────────────────────────────┐
│  HERMES LEGAL PRO v3.0                                      │
├─────────────────────────────────────────────────────────────┤
│  [Dashboard] [Matters] [Reuniones] [Documentos] [Calendario]│
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  CONTENIDO DINÁMICO (cambia según pestaña)          │   │
│  │                                                     │   │
│  │  • Dashboard: KPIs reales + alertas + plazos        │   │
│  │  • Matters: Lista + crear + editar + eliminar       │   │
│  │  • Reuniones: Registrar + transcript + resumen      │   │
│  │  • Documentos: Generar + descargar + historial     │   │
│  │  • Calendario: Vista mensual + plazos + crear       │   │
│  │                                                     │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Flujo de datos real:
```
Usuario hace click → JavaScript fetch() → FastAPI endpoint → JSON response → JavaScript actualiza DOM
```

---

## 📁 ESTRUCTURA DE ARCHIVOS

```
dashboard/
├── backend/
│   └── app.py              # API FastAPI v3.0 (extendido)
├── frontend/
│   ├── index.html          # SPA principal (único archivo)
│   ├── css/
│   │   └── kami.css        # Sistema de diseño Kami v3
│   └── js/
│       ├── app.js          # Router + estado global
│       ├── api.js          # Cliente HTTP (fetch wrapper)
│       ├── dashboard.js    # Vista Dashboard
│       ├── matters.js      # Vista Matters (CRUD completo)
│       ├── reuniones.js    # Vista Reuniones
│       ├── documentos.js   # Vista Documentos
│       ├── calendario.js   # Vista Calendario
│       └── utils.js        # Helpers (fechas, moneda, etc.)
└── spa/
    └── index.html          # Fallback si el JS falla
```

---

## 🎨 SISTEMA DE DISEÑO KAMI v3 (Frontend)

### Paleta de colores
```css
:root {
  --ink-blue: #1B365D;        /* Azul marino - títulos, botones */
  --corporate-blue: #2F5496;  /* Azul corporativo - hover */
  --success-green: #548235;   /* Verde - éxito, completado */
  --warning-yellow: #FFC000;  /* Amarillo - alerta, pendiente */
  --alert-red: #C00000;       /* Rojo - urgente, vencido */
  --bg-warm: #faf8f0;         /* Pergamino - fondo general */
  --bg-white: #ffffff;        /* Blanco - tarjetas */
  --text-primary: #1a1a18;    /* Negro editorial - texto */
  --text-secondary: #5a5a56;  /* Gris - metadata */
  --border-light: #e0ddd5;    /* Borde suave */
}
```

### Tipografía
- **Títulos:** Playfair Display (serif elegante) o Inter (sans-serif limpio)
- **Cuerpo:** Inter 14px
- **Metadata:** Inter 12px, color secundario

### Componentes UI
- **Botón primario:** Fondo ink-blue, texto blanco, radio 8px
- **Botón secundario:** Fondo blanco, borde ink-blue, texto ink-blue
- **Tarjeta (card):** Fondo blanco, sombra suave, radio 12px
- **Input:** Borde gris, radio 8px, focus ink-blue
- **Tabla:** Header ink-blue, filas alternadas, hover suave
- **Alerta:** Borde izquierdo 4px + icono + texto
- **Modal:** Overlay oscuro + tarjeta centrada + animación

---

## 🔌 API ENDPOINTS (Backend v3.0)

### Endpoints existentes (ya funcionan):
```
GET  /api/health              → Estado del sistema
GET  /api/dashboard           → KPIs + alertas + plazos
GET  /api/matters             → Lista matters
POST /api/matters             → Crear matter
GET  /api/matters/{id}        → Ver matter
GET  /api/reuniones           → Lista reuniones
POST /api/reuniones           → Crear reunión
GET  /api/documentos          → Lista documentos
POST /api/documentos          → Crear documento (registro)
GET  /api/templates           → Lista templates
GET  /api/templates/{key}     → Ver template
GET  /api/carpetas/{matter}   → Explorar carpeta
GET  /api/alertas             → Lista alertas
```

### Endpoints NUEVOS (se agregan en v3.0):
```
PUT    /api/matters/{id}              → Actualizar matter
DELETE /api/matters/{id}              → Eliminar matter
POST   /api/matter/{id}/generar-doc   → Generar PDF real
GET    /api/matter/{id}/documentos    → Documentos del matter
POST   /api/reuniones/{id}/procesar   → Procesar transcript
GET    /api/calendario/{mes}/{anio}   → Eventos del mes
POST   /api/calendario/evento         → Crear evento
DELETE /api/calendario/evento/{id}    → Eliminar evento
POST   /api/upload/{matter}           → Subir archivo
GET    /api/download/{ruta}           → Descargar archivo
```

---

## 📱 VISTAS (Pantallas)

### 1. DASHBOARD (Pantalla principal)

**Layout:**
```
┌─────────────────────────────────────────────────────────────┐
│  Buenos días, [Nombre]          [🔔 3] [⚙️] [👤]           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐  │
│  │   5    │ │   2    │ │   1    │ │   8    │ │   3    │  │
│  │Activos │ │Urgentes│ │Hoy     │ │Pendient│ │Alertas │  │
│  │ Matters│ │ Matters│ │Reunion │ │  Docs  │ │Activas │  │
│  └────────┘ └────────┘ └────────┘ └────────┘ └────────┘  │
│                                                             │
│  ┌─────────────────────┐  ┌─────────────────────┐            │
│  │ ⚠️ PRÓXIMOS PLAZOS │  │ 📅 HOY              │            │
│  │                     │  │                     │            │
│  │ 🔴 PRAG-001  2 días │  │ 10:00 Pragma       │            │
│  │ 🟡 CLI-002   5 días │  │ 15:00 ABC Corp     │            │
│  │ 🔴 ABC-003 VENCIDO  │  │                     │            │
│  │                     │  │                     │            │
│  └─────────────────────┘  └─────────────────────┘            │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ 📋 REUNIONES RECIENTES                             │   │
│  │                                                     │   │
│  │ Pragma Studio    2 mayo    ✅ Procesada  3 docs    │   │
│  │ Cliente ABC     28 abr     ✅ Procesada  1 acta    │   │
│  │                                                     │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**Funcionalidad:**
- KPIs con números reales de la API
- Plazos ordenados por urgencia (rojo = vencido, amarillo = próximo)
- Reuniones con badge de estado
- Click en cualquier tarjeta → va a esa vista

---

### 2. MATTERS (Gestión de Casos)

**Layout:**
```
┌─────────────────────────────────────────────────────────────┐
│  MATTERS                                [+ Nuevo Matter]   │
├─────────────────────────────────────────────────────────────┤
│  🔍 Buscar...    [Todos ▼] [Mercantil ▼] [Activo ▼]       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ 🔴 PRAG-001  Pragma Studio          Mercantil  2d   │   │
│  │    Juan Antonio Angel Ramirez    │ Prioridad: ALTA   │   │
│  │    3 docs pendientes              │ Deadline: 15 jun  │   │
│  │    [Ver] [Editar] [Generar Doc]   [📁 Abrir Carpeta]│   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ 🟡 CLI-002  Cliente ABC            Laboral    5d   │   │
│  │    María González                │ Prioridad: MEDIA  │   │
│  │    1 doc pendiente               │ Deadline: 20 jun  │   │
│  │    [Ver] [Editar] [Generar Doc]   [📁 Abrir Carpeta]│   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**Funcionalidad CRUD:**
- **Crear:** Modal con formulario (nombre, área, descripción, deadline, prioridad)
- **Leer:** Lista con filtros y búsqueda
- **Actualizar:** Modal de edición inline
- **Eliminar:** Confirmación con "¿Estás seguro?"
- **Generar Doc:** Dropdown de templates → botón generar → descarga PDF
- **Abrir Carpeta:** Link que abre Finder/Explorer

---

### 3. REUNIONES (Registro y Procesamiento)

**Layout:**
```
┌─────────────────────────────────────────────────────────────┐
│  REUNIONES                              [+ Nueva Reunión]    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ 📹 Pragma Studio — 2 de mayo, 10:00                 │   │
│  │    Matter: PRAG-001                                 │   │
│  │    Meet: meet.google.com/abc-defg-hij              │   │
│  │                                                     │   │
│  │    [📝 Ver Transcript]  [📄 Ver Resumen]            │   │
│  │                                                     │   │
│  │    Documentos sugeridos:                            │   │
│  │    ✅ Contrato de Prestación de Servicios (generado)│   │
│  │    ✅ Acta de Entrega Fase 1 (generado)             │   │
│  │    ⏳ Protocolo de Cobranza (pendiente)             │   │
│  │                                                     │   │
│  │    Acuerdos:                                        │   │
│  │    • Entregar borrador en 3 días                   │   │
│  │    • Revisar cláusula de intereses                 │   │
│  │                                                     │   │
│  │    [📁 Abrir Carpeta]  [🗑️ Eliminar]               │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**Funcionalidad:**
- **Nueva reunión:** Formulario (cliente, fecha, meet URL, transcript)
- **Procesar transcript:** Botón que analiza texto y sugiere documentos
- **Ver resumen:** Acordeón con puntos clave
- **Generar documentos sugeridos:** Checkboxes + botón "Generar seleccionados"

---

### 4. DOCUMENTOS (Generación y Gestión)

**Layout:**
```
┌─────────────────────────────────────────────────────────────┐
│  DOCUMENTOS                             [+ Generar Nuevo]    │
├─────────────────────────────────────────────────────────────┤
│  🔍 Buscar...    [Todos ▼] [Borrador ▼] [PDF ▼]            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ 📄 Contrato_Prestacion_Servicios_PRAGMA.pdf        │   │
│  │    Matter: PRAG-001    Template: Prestación       │   │
│  │    Estado: ✅ Generado  Fecha: 2 mayo 2026         │   │
│  │    Tamaño: 145 KB                                  │   │
│  │                                                     │   │
│  │    [👁️ Previsualizar]  [⬇️ Descargar]  [🗑️]        │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ 📄 Acta_Entrega_Fase_1.pdf                         │   │
│  │    Matter: PRAG-001    Template: Acta Entrega      │   │
│  │    Estado: 🟡 Borrador   Fecha: 2 mayo 2026        │   │
│  │                                                     │   │
│  │    [✏️ Editar]  [⬇️ Descargar]  [✅ Finalizar]      │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**Funcionalidad:**
- **Generar nuevo:** Wizard de 3 pasos
  1. Seleccionar matter
  2. Seleccionar template (con preview de campos)
  3. Revisar datos → Generar → Descargar
- **Previsualizar:** Abre PDF en nueva pestaña
- **Editar:** Abre HTML editable (motor Kami)
- **Finalizar:** Cambia estado a "firmado" y mueve a carpeta

---

### 5. CALENDARIO (Vista Mensual)

**Layout:**
```
┌─────────────────────────────────────────────────────────────┐
│  CALENDARIO                    [◀ Mayo 2026 ▶]  [+ Evento]  │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Lun  Mar  Mié  Jue  Vie  Sáb  Dom                         │
│                                                             │
│              1    2    3    4    5                          │
│         ┌────┐                                              │
│         │ 🔴 │  🔴  🟡                                    │
│         │PLZ │ PRG  ABC                                    │
│         └────┘                                              │
│   6    7    8    9   10   11   12                         │
│                    🟡                                       │
│                    ENT                                      │
│  13   14   15   16   17   18   19                         │
│       🔴                                                    │
│       AUD                                                   │
│  20   21   22   23   24   25   26                         │
│                                                             │
│  27   28   29   30   31                                   │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│  Leyenda: 🔴 Urgente / Vencido  🟡 Próximo  ⚪ Normal      │
└─────────────────────────────────────────────────────────────┘
```

**Funcionalidad:**
- **Navegación:** Flechas mes anterior/siguiente
- **Click en día:** Muestra eventos de ese día + botón "+ Añadir"
- **Eventos:** Plazos, reuniones, deadlines, follow-ups
- **Colores:** Automático según urgencia
- **Modal de evento:** Título, fecha, tipo, matter relacionado

---

## 🔄 FLUJOS DE USUARIO (User Flows)

### Flujo 1: Abogado llega por la mañana
```
1. Abre dashboard → Ve KPIs (5 matters activos, 2 urgentes)
2. Ve alerta roja "PRAG-001 vence en 2 días"
3. Click en alerta → Va a matter PRAG-001
4. Ve 3 documentos pendientes
5. Click "Generar Doc" → Selecciona "Contrato Prestación Servicios"
6. Revisa datos del cliente → Click "Generar"
7. Espera 30 segundos (spinner) → PDF listo
8. Descarga PDF → Lo envía al cliente por email
9. Marca documento como "enviado"
10. Dashboard actualiza: documentos pendientes = 2
```

### Flujo 2: Después de reunión con cliente
```
1. Abogado entra a Google Meet
2. Termina reunión
3. Abre dashboard → Reuniones → "+ Nueva Reunión"
4. Pega transcript (o sube archivo .txt)
5. Click "Procesar"
6. Sistema analiza y sugiere 3 documentos
7. Abogado revisa sugerencias → Marca los que quiere generar
8. Click "Generar seleccionados"
9. Sistema genera 3 PDFs
10. Abogado descarga y revisa cada uno
```

### Flujo 3: Cliente pregunta por WhatsApp/Telegram
```
1. Cliente escribe: "¿Cómo va mi caso?"
2. Hermes responde automáticamente:
   "Su caso PRAG-001 está activo. Tenemos 2 documentos pendientes:
   - Contrato de prestación de servicios (en revisión)
   - Acta de entrega (pendiente)
   El deadline es 15 de junio. ¿Necesita algo más?"
3. Si cliente pregunta algo complejo → Hermes notifica al abogado
4. Abogado responde desde dashboard o Telegram
```

---

## 🧪 TESTS POR FASE

### Test 1: Dashboard carga
```
Entrada: Abrir http://localhost:8082
Esperado: Ver 5 KPIs con números reales (no mockup)
Verificado: Sí / No
```

### Test 2: Crear matter
```
Entrada: Click "+ Nuevo Matter" → Llenar formulario → Guardar
Esperado: Matter aparece en lista + carpeta creada en disco
Verificado: Sí / No
```

### Test 3: Generar documento
```
Entrada: Matter PRAG-001 → "Generar Doc" → "Contrato Prestación Servicios"
Esperado: PDF generado en motor_kami/output/ + descarga automática
Verificado: Sí / No
```

### Test 4: Calendario muestra plazos
```
Entrada: Abrir Calendario → Ver mes actual
Esperado: Días con eventos marcados en colores
Verificado: Sí / No
```

### Test 5: Subir archivo
```
Entrada: Matter → "Subir Archivo" → Seleccionar PDF → Subir
Esperado: Archivo aparece en carpeta del cliente
Verificado: Sí / No
```

---

## 📅 FASES DE CONSTRUCCIÓN

### FASE 1: Fundamentos (Día 1)
**Objetivo:** Estructura base que funcione

**Tareas OpenCode Go:**
1. Crear `frontend/js/api.js` — Cliente HTTP que llama a todos los endpoints
2. Crear `frontend/js/app.js` — Router simple (cambia vistas sin recargar)
3. Crear `frontend/js/utils.js` — Helpers (formatear fechas, moneda, etc.)
4. Crear `frontend/css/kami.css` — Sistema de diseño completo
5. Actualizar `index.html` — Estructura base con navegación

**Tests:**
- [ ] Dashboard carga sin errores en consola
- [ ] Navegación entre pestañas funciona
- [ ] API responde a todas las llamadas

---

### FASE 2: Dashboard Vivo (Día 2)
**Objetivo:** KPIs reales, alertas funcionales

**Tareas OpenCode Go:**
1. Implementar `dashboard.js` — Carga datos reales de `/api/dashboard`
2. Implementar KPIs con números dinámicos
3. Implementar lista de plazos con colores (rojo/amarillo/verde)
4. Implementar reuniones recientes
5. Implementar alertas con badges

**Tests:**
- [ ] KPIs muestran números reales (no 0 ni undefined)
- [ ] Plazos se ordenan por urgencia
- [ ] Alertas parpadean o destacan si son críticas
- [ ] Click en tarjeta navega a vista correcta

---

### FASE 3: Matters CRUD (Día 3-4)
**Objetivo:** Crear, leer, actualizar, eliminar matters

**Tareas OpenCode Go:**
1. Implementar `matters.js` — Lista con filtros y búsqueda
2. Implementar modal "Crear Matter" con formulario completo
3. Implementar modal "Editar Matter" (precarga datos)
4. Implementar eliminación con confirmación
5. Implementar botón "Generar Doc" con dropdown de templates
6. Implementar botón "Abrir Carpeta" (abre Finder/Explorer)

**Tests:**
- [ ] Crear matter → Aparece en lista → Carpeta creada en disco
- [ ] Editar matter → Cambios persisten después de recargar
- [ ] Eliminar matter → Desaparece de lista → Carpeta sigue (no borrar)
- [ ] Generar doc → PDF generado → Descarga automática
- [ ] Abrir carpeta → Se abre Finder/Explorer

---

### FASE 4: Reuniones (Día 5)
**Objetivo:** Registrar y procesar reuniones

**Tareas OpenCode Go:**
1. Implementar `reuniones.js` — Lista de reuniones
2. Implementar modal "Nueva Reunión" (formulario + textarea para transcript)
3. Implementar botón "Procesar Transcript" (llama a endpoint)
4. Implementar vista de resumen con acordeón
5. Implementar lista de documentos sugeridos con checkboxes
6. Implementar "Generar seleccionados"

**Tests:**
- [ ] Crear reunión → Aparece en lista
- [ ] Pegar transcript → Procesar → Muestra resumen
- [ ] Documentos sugeridos aparecen con checkboxes
- [ ] Generar seleccionados → Crea PDFs → Descarga

---

### FASE 5: Documentos (Día 6)
**Objetivo:** Generar, previsualizar, descargar

**Tareas OpenCode Go:**
1. Implementar `documentos.js` — Lista con filtros
2. Implementar wizard "Generar Nuevo" (3 pasos)
3. Implementar previsualización de PDF (iframe o nueva pestaña)
4. Implementar descarga directa
5. Implementar cambio de estado (borrador → revisión → firmado)

**Tests:**
- [ ] Wizard completa 3 pasos sin errores
- [ ] Generar documento → PDF creado en 30 segundos
- [ ] Previsualizar → Muestra PDF correcto
- [ ] Descargar → Archivo se guarda en Downloads
- [ ] Cambiar estado → Persiste en JSON

---

### FASE 6: Calendario (Día 7)
**Objetivo:** Vista mensual con eventos

**Tareas OpenCode Go:**
1. Implementar `calendario.js` — Grid mensual
2. Implementar navegación mes anterior/siguiente
3. Implementar renderizado de eventos en días
4. Implementar modal "Nuevo Evento"
5. Implementar colores automáticos según urgencia

**Tests:**
- [ ] Calendario muestra mes correcto
- [ ] Eventos aparecen en días correctos
- [ ] Colores: rojo=vencido, amarillo=próximo, verde=normal
- [ ] Navegación mes anterior/siguiente funciona
- [ ] Crear evento → Aparece en calendario

---

### FASE 7: Polish + Tests finales (Día 8)
**Objetivo:** Que se sienta como producto terminado

**Tareas OpenCode Go:**
1. Animaciones suaves (transiciones entre vistas)
2. Estados de carga (spinners, skeletons)
3. Manejo de errores (mensajes amigables, no técnicos)
4. Responsive (funciona en iPad/MacBook)
5. Modo oscuro (opcional)
6. Tests end-to-end de todos los flujos

**Tests finales:**
- [ ] Flujo mañana completo (Dashboard → Matter → Generar → Descargar)
- [ ] Flujo post-reunión completo (Reunión → Procesar → Generar)
- [ ] Flujo calendario completo (Crear evento → Ver en calendario)
- [ ] Sin errores en consola del navegador
- [ ] Tiempo de carga < 2 segundos por vista

---

## 📝 INSTRUCCIONES PARA OPENCODE GO

### Setup inicial:
```bash
# 1. Clonar repo (si no lo tiene)
cd ~
git clone https://github.com/cuentadeservicio377-cell/ws-hermes-legal-pro.git
cd ws-hermes-legal-pro

# 2. Verificar estructura
ls dashboard/
# Debe tener: backend/, frontend/, spa/

# 3. Instalar dependencias si faltan
pip3 install fastapi uvicorn pydantic

# 4. Verificar que Motor Kami existe
ls motor_kami/
# Debe tener: motor_kami.py, blocks.py, bridge_api.py, templates/
```

### Por cada fase:
1. Leer este plan
2. Implementar los archivos indicados
3. Correr tests de esa fase
4. Si pasa todos → commit
5. Si falla alguno → corregir hasta pasar
6. Avanzar a siguiente fase

### Comando para probar:
```bash
# Terminal 1: Backend
cd ~/ws-hermes-legal-pro/dashboard/backend
python3 app.py

# Terminal 2: Frontend (abrir en navegador)
open http://localhost:8082

# Ver consola del navegador (Cmd+Option+J en Chrome)
# Buscar errores rojos
```

---

## ✅ CHECKLIST FINAL DE PRODUCTO

Antes de decir "está listo", verificar:

- [ ] Un abogado puede crear un matter sin ayuda
- [ ] Un abogado puede generar un contrato sin ayuda
- [ ] Un abogado puede ver sus plazos sin ayuda
- [ ] Un abogado puede subir un archivo sin ayuda
- [ ] Todo funciona sin internet (después de cargar)
- [ ] Los datos no se pierden al cerrar el navegador
- [ ] El diseño se ve profesional (no como programa de los 90)
- [ ] Los errores son en español y amigables
- [ ] Funciona en Chrome, Safari y Firefox
- [ ] Funciona en MacBook Air M2 (rendimiento fluido)

---

*Plan v3.0 — Diseñado por Hermes Neo para WS Capital*
*Mayo 2026*
