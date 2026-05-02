# Manual de Usuario — Willow Legal

## 1. ¿Qué es Willow Legal?

Willow Legal es tu sistema de gestión de despacho. Te ayuda a organizar tus casos, generar documentos legales, controlar plazos y llevar tus finanzas — todo desde un solo lugar.

Si sabes usar WhatsApp y Excel, sabes usar Willow. Si no sabes algo, presiona el botón **❓ Ayuda** en la barra izquierda.

---

## 2. Primeros pasos

### 2.1 Abrir el sistema

1. Abre tu navegador (Chrome, Safari, Edge)
2. Escribe en la barra de direcciones: **http://localhost:8082**
3. Presiona Enter
4. Verás la pantalla principal (el "Dashboard")

> 📌 **¿Qué es localhost?** Es una dirección que abre el sistema en tu computadora. No es un sitio web público. Solo tú puedes verlo.

### 2.2 Tu pantalla principal

Cuando entras, ves:

- **Barra izquierda (Sidebar)** — Menú con todas las secciones: Inicio, Casos, Documentos, Plazos, Finanzas, Aprobaciones, Alertas
- **Parte superior** — Título de la sección y botones de acción rápida: + Nuevo Caso, + Nuevo Documento, + Nuevo Plazo
- **Centro** — 4 tarjetas grandes con números: Casos Activos, Plazos, Alertas, Balance del mes
- **Abajo** — Tablas, formularios y contenido de cada sección

### 2.3 Crear tu primer Caso

1. Haz clic en el botón azul **"+ Nuevo Caso"** (arriba a la derecha)
2. Se abre una ventana. Llena los campos:
   - **Nombre del caso** — Ej: "Contrato IBM" (obligatorio)
   - **Cliente** — Nombre de la empresa o persona
   - **Área** — Selecciona: Corporativo, Litigio, Fiscal, Laboral
   - **Responsable** — Quién lleva el caso
   - **Descripción** — Detalles importantes
3. Haz clic en **"Confirmar"**
4. Verás un mensaje verde: "✅ Caso creado exitosamente"

¡Listo! Tu primer caso aparece en la tabla de Casos.

---

## 3. Casos (Matters)

### 3.1 Ver mis casos

Haz clic en **📁 Casos (Matters)** en el menú izquierdo. Verás una tabla con todos tus casos.

### 3.2 Crear un caso nuevo

Desde cualquier sección, puedes presionar **"+ Nuevo Caso"** en la parte superior.

### 3.3 Editar un caso

En la tabla de casos, busca el caso y haz clic en **"Editar"**. Cambia los campos y presiona Confirmar.

### 3.4 Buscar un caso

En la sección de Casos, escribe en la caja **"Buscar caso..."** y la tabla se filtrará automáticamente.

### 3.5 Cerrar o eliminar un caso

Para eliminar un caso, haz clic en el botón rojo **"Eliminar"** en la tabla. Confirma la acción. El caso se elimina permanentemente.

---

## 4. Documentos

### 4.1 Generar un documento

Willow Legal tiene modelos (templates) de documentos legales listos para usar:

1. Ve a **📄 Documentos** en el menú
2. Verás botones para generar: NDA, Contrato, Carta Cobranza
3. Haz clic en el que necesites
4. Ingresa el ID del caso (Ej: LEG-001)
5. Presiona Confirmar
6. El documento se genera y se guarda automáticamente

### 4.2 Ver documentos en Google Drive

Todos tus documentos se guardan en Google Drive automáticamente. Para verlos:
1. Abre [drive.google.com](https://drive.google.com)
2. Busca la carpeta **WillowLegal > 01_Clientes > [Tu Cliente]**

### 4.3 Editar un documento

Si necesitas hacer cambios:
1. Ve a Google Drive (link arriba)
2. Abre el documento con Google Docs
3. Edita lo que necesites
4. Se guarda automáticamente

---

## 5. Plazos

### 5.1 Crear un plazo

Los plazos te ayudan a no olvidar fechas importantes:

1. Ve a **⏰ Plazos** en el menú
2. Haz clic en **"+ Crear plazo"**
3. Llena:
   - Mater ID (número de caso)
   - Título (Ej: "Vencimiento contrato")
   - Fecha de vencimiento
   - Tipo (General, Judicial, Contractual, Fiscal)
4. Presiona Confirmar

### 5.2 Ver plazos en calendario

Cada plazo se sincroniza con Google Calendar. Para verlos:
1. Abre [calendar.google.com](https://calendar.google.com)
2. Verás tus plazos con recordatorios (3 días antes y 1 día antes)

### 5.3 Recibir alertas de plazos

Google Calendar te envía notificaciones por email automáticamente. También verás alertas en la sección **🔔 Alertas** del menú.

---

## 6. Finanzas

### 6.1 Registrar un cobro

1. Ve a **💰 Finanzas** en el menú
2. Haz clic en **"+ Registrar Ingreso"**
3. Llena los datos del pago

### 6.2 Registrar un gasto

1. En Finanzas, haz clic en **"+ Registrar Egreso"**
2. Llena los datos del gasto

### 6.3 Ver balance

En la sección de Finanzas verás 3 tarjetas:
- **Ingresos** — Lo que has cobrado
- **Pendiente** — Lo que falta por cobrar
- **Balance** — La diferencia (verde = positivo, rojo = negativo)

---

## 7. Aprobaciones

### 7.1 Aprobar un documento

Cuando generas un documento, queda en estado "pendiente de aprobación".

1. Ve a **✅ Aprobaciones** en el menú
2. Verás una lista de documentos por aprobar
3. Revisa el documento en Google Drive
4. Si está bien, márcalo como Aprobado

### 7.2 Ver historial

Cada documento guarda quién lo aprobó y cuándo. El historial completo está en la sección de Documentos.

---

## 8. Alertas

### 8.1 Entender las alertas

Las alertas te avisan de:
- 🔴 **Plazos vencidos** — Urgente, tomar acción
- 🟡 **Plazos próximos** — Revisar, planificar
- 🟢 **Información** — Recordatorios

### 8.2 Configurar alertas

Las alertas se configuran automáticamente al crear plazos. Para modificar, contacta a soporte.

---

## 9. Problemas comunes

### 9.1 "No puedo entrar"

1. Verifica que la terminal esté abierta
2. Verifica que el backend esté corriendo: `python3 dashboard/backend/app.py`
3. Intenta de nuevo en http://localhost:8082

### 9.2 "No veo mi caso"

- Revisa el filtro de búsqueda (quizás esté filtrando por texto)
- Ve a Casos y busca por el nombre del cliente
- Si no aparece, créalo de nuevo

### 9.3 "El documento no se generó"

1. Verifica que el caso (Matter ID) exista
2. Ve a Documentos y selecciona el template correcto
3. Si persiste, contacta soporte

### 9.4 "No me llegan alertas"

- Las alertas se envían por email a través de Google Calendar
- Revisa tu bandeja de spam
- Verifica que hayas creado plazos en el sistema

### 9.5 "Todo está muy lento"

- Cierra otras pestañas del navegador
- Reinicia el backend: cierra la terminal y vuelve a abrir con `python3 dashboard/backend/app.py`
- Si persiste, contacta soporte

---

## 10. Glosario

| Término | Significado |
|---------|-------------|
| **Matter** | Caso o asunto legal |
| **Template** | Modelo de documento listo para usar |
| **Plazo** | Fecha límite o vencimiento |
| **NDA** | Acuerdo de Confidencialidad (Non-Disclosure Agreement) |
| **Dashboard** | Pantalla principal con resumen |
| **KPI** | Indicador numérico (ej: casos activos) |
| **Drive** | Google Drive — donde se guardan los documentos |

---

## 11. Soporte

- 📧 **Email**: soporte@wscapital.mx
- 📱 **WhatsApp**: +52 1 55 XXXX XXXX
- 📁 **Documentación completa**: En la carpeta `docs/` del sistema
- 🤖 **Hermes (Telegram)**: Escribe `/ayuda` para comandos disponibles

---

*Willow Legal v7 — Sistema de Gestión Legal*
*WS Capital © 2026*
