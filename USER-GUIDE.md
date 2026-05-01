# USER-GUIDE.md — Guía de Uso para Abogados
# Hermes Legal Pro v1.0.0

---

## 🎯 BIENVENIDO

Hermes Legal Pro es tu **asistente legal inteligente**. No es un software complicado — es como tener un paralegal, un secretario, y un diseñador de documentos trabajando para ti 24/7.

### Lo que hace por ti:
- ✅ Transcribe tus reuniones con clientes
- ✅ Genera documentos legales profesionales
- ✅ Organiza tus casos y plazos
- ✅ Atiende consultas de clientes automáticamente
- ✅ Te recuerda deadlines y follow-ups

### Lo que NO tienes que hacer:
- ❌ Escribir contratos desde cero
- ❌ Organizar carpetas manualmente
- ❌ Recordar todos los plazos
- ❌ Responder consultas repetitivas

---

## 📱 CÓMO ACCEDER

### Por Telegram (recomendado)
1. Abre Telegram en tu celular o computadora
2. Busca tu bot (te lo daremos el nombre)
3. Envía `/start`
4. ¡Listo! Ya puedes usar Hermes

### Por la terminal (avanzado)
Si prefieres usar la computadora directamente:
```bash
hermes profile use legal-pro
hermes chat
```

---

## 🎤 REUNIONES CON CLIENTES

### Antes de la reunión
1. Abre Google Chrome
2. Asegúrate de estar logueado en tu cuenta Google
3. Entra a la reunión de Google Meet normalmente

### Durante la reunión
- **Hermes transcribe TODO automáticamente**
- No necesitas hacer nada especial
- Habla normalmente con tu cliente

### Después de la reunión
- En 2-3 minutos recibes en Telegram:
  - 📋 **Resumen** de lo que se habló
  - 📄 **Documentos** generados (si se necesitan)
  - ✅ **Tareas** que debes hacer
  - 📅 **Plazos** y fechas importantes

### Ejemplo de mensaje que recibes:
```
Reunión con Cliente Ejemplo SA finalizada.

📋 RESUMEN:
- Acordaron contrato de prestación de servicios
- Monto: $50,000 MXN
- Plazo: 30 días naturales

📄 DOCUMENTOS GENERADOS:
- Contrato de prestación de servicios (borrador)
- Acuerdo de confidencialidad

✅ TAREAS PENDIENTES:
1. [ALTA] Revisar borrador de contrato
2. [MEDIA] Enviar NDA a cliente para firma
3. [BAJA] Programar follow-up para el 15 de mayo

📅 PRÓXIMOS PLAZOS:
- 15 mayo: Firma de contrato
- 30 mayo: Entrega de servicios
```

---

## 📁 GESTIÓN DE CASOS (MATTERS)

### Crear un caso nuevo
```
/matter-nuevo "Cliente Ejemplo SA" "Mercantil"
```
Hermes crea:
- Carpeta en tu computadora
- Entrada en el sistema
- Estructura organizada

### Ver todos tus casos
```
/status-legal
```
Recibes:
```
MATTERS ACTIVOS:

LEG-001: Cliente Ejemplo SA
  Área: Mercantil
  Status: Activo
  Próximo paso: Revisar contrato
  Deadline: 15 mayo

LEG-002: Cliente ABC SRL
  Área: Laboral
  Status: Intake
  Próximo paso: Entrevista inicial
  Deadline: 20 mayo
```

### Generar un documento
```
/documento-generar LEG-001 prestacion_servicios
```
Hermes:
1. Busca los datos del caso
2. Selecciona el template
3. Genera el documento
4. Te envía el PDF

### Crear un plazo/deadline
```
/plazo-crear LEG-001 "Firma de contrato" "2026-05-15"
```
Hermes:
1. Guarda el plazo en el sistema
2. Lo agrega a tu calendario
3. Te recordará antes de la fecha

---

## 📄 DOCUMENTOS LEGALES

### Templates disponibles (23)

| # | Documento | Cuándo usar |
|---|-----------|-------------|
| 1 | Contrato de prestación de servicios | Cuando contratas a alguien |
| 2 | Acuerdo de confidencialidad (NDA) | Cuando compartes información sensible |
| 3 | Contrato de trabajo | Cuando contratas empleados |
| 4 | Carta de cobranza | Cuando cobras una deuda |
| 5 | Pagaré | Cuando formalizas un préstamo |
| 6 | Convenio de pagos | Cuando acuerdas pagos a plazos |
| 7 | Acta de asamblea | Cuando tienes junta de socios |
| 8 | Poder notarial | Cuando delegas facultades |
| 9 | Estatutos sociales | Cuando constituyes una empresa |
| 10 | Convenio de accionistas | Cuando hay varios socios |
| 11 | Reglamento interior | Normas de la empresa |
| 12 | Finiquito | Cuando termina relación laboral |
| 13 | NDA laboral | Confidencialidad con empleados |
| 14 | Arrendamiento | Cuando rentas un local |
| 15 | Garantía | Cuando pides garantía |
| 16 | Calendario de cobranza | Plan de pagos |
| 17 | Bitácora de entregas | Control de entregas |
| 18 | Expediente de materialidad | Para SAT |
| 19 | Carta SAT | Comunicación con SAT |
| 20 | Aviso de privacidad | Obligatorio por ley |
| 21 | Formato ARCO | Derechos de datos personales |
| 22 | Acta constitutiva | Constitución de empresa |
| 23 | Contrato de franquicia | Franquicias |

### Cómo generar un documento

**Opción 1: Después de reunión (automático)**
Hermes detecta qué documentos se necesitan y los genera solo.

**Opción 2: Manual**
```
/documento-generar [matter] [tipo]
```
Ejemplo:
```
/documento-generar LEG-001 nda
```

**Opción 3: Por descripción**
```
Necesito un contrato de confidencialidad para mi cliente del caso LEG-001
```

---

## 🤖 ATENCIÓN AL CLIENTE

### Cómo funciona
1. Tu cliente escribe al bot de Telegram (o al número que le des)
2. Hermes responde automáticamente
3. Si es algo complejo, te notifica a ti

### Ejemplos de consultas que Hermes maneja solo:
- "¿En qué va mi caso?"
- "¿Cuándo es la próxima reunión?"
- "¿Me puedes enviar el contrato?"
- "¿Qué documentos necesito traer?"

### Ejemplos que escalana a ti:
- "Quiero demandar a mi ex socio"
- "¿Cuánto me costaría un juicio?"
- "Necesito hablar urgente con el abogado"

### Cómo revisar consultas pendientes
```
/consultas-pendientes
```

---

## 📅 CALENDARIO Y PLAZOS

### Ver calendario
```
/calendario
```
Recibes:
```
PRÓXIMOS PLAZOS:

Hoy:
- Reunión con Cliente Ejemplo SA (3:00 PM)

Esta semana:
- Deadline: Firma contrato LEG-001 (15 mayo)
- Follow-up: Cliente ABC (17 mayo)

Próxima semana:
- Audiencia: Caso LEG-003 (22 mayo)
```

### Crear recordatorio
```
/recordatorio "Llamar a Cliente Ejemplo" "mañana 10am"
```

---

## 💡 COMANDOS RÁPIDOS

| Comando | Qué hace |
|---------|---------|
| `/start` | Iniciar conversación |
| `/help` | Ver todos los comandos |
| `/matter-nuevo [cliente] [área]` | Crear caso nuevo |
| `/documento-generar [matter] [tipo]` | Generar documento |
| `/plazo-crear [matter] [desc] [fecha]` | Crear deadline |
| `/status-legal` | Ver todos los casos |
| `/calendario` | Ver calendario |
| `/consultas-pendientes` | Ver consultas de clientes |
| `/recordatorio [desc] [cuándo]` | Crear recordatorio |
| `/buscar [término]` | Buscar en documentos |

---

## ❓ FAQ

### ¿Mis datos están seguros?
**Sí.** Todo corre en tu MacBook. Nada sale a la nube. Tus documentos y conversaciones nunca salen de tu computadora.

### ¿Necesito saber de tecnología?
**No.** Si sabes usar Telegram, ya sabes usar Hermes. Todo es por mensajes de texto.

### ¿Cuánto cuesta?
La licencia anual incluye todo. No hay costos escondidos. Solo pagas las API keys de los modelos de IA (aprox $50-100/mes dependiendo del uso).

### ¿Puedo usarlo en mi celular?
**Sí.** Todo funciona por Telegram. Desde tu celular puedes ver casos, documentos, y recibir notificaciones.

### ¿Qué pasa si no tengo internet?
Los documentos generados quedan en tu computadora. Puedes consultarlos sin internet. Para generar nuevos documentos sí necesitas internet.

### ¿Puedo compartir documentos con clientes?
**Sí.** Los PDFs generados están en tu computadora. Puedes enviarlos por email, WhatsApp, o como prefieras.

### ¿Qué tan buenos son los documentos?
Muy buenos. Usan templates reales de abogados mexicanos, con numeralia correcta, cláusulas legales válidas, y diseño profesional.

### ¿Puedo editar los documentos?
**Sí.** Son PDFs, pero puedes pedir a Hermes que genere la versión editable (Word) si necesitas modificar algo.

### ¿Y si Hermes se equivoca?
Hermes es un asistente, no un abogado. Siempre revisa los documentos antes de enviarlos. Si ves algo raro, díselo y lo corrige.

---

## 📞 SOPORTE

¿Tienes problemas o dudas?

1. **Revisa este manual** — La respuesta probablemente está aquí
2. **Pregunta a Hermes** — Escribe tu duda y te ayuda
3. **Contacta soporte** — soporte@wscapital.ai

---

## 🎓 TIPS DE PRODUCTIVIDAD

### Tip 1: Usa la voz
En Telegram puedes enviar mensajes de voz. Hermes los transcribe y entiende. Es más rápido que escribir.

### Tip 2: Sé específico
Cuanto más específico seas, mejor te ayuda Hermes.
- ❌ "Necesito un contrato"
- ✅ "Necesito un contrato de prestación de servicios para un desarrollador de software, pago mensual de $30,000 MXN, plazo de 6 meses"

### Tip 3: Revisa antes de enviar
Hermes genera borradores. Siempre revisa antes de enviar al cliente.

### Tip 4: Organiza por cliente
Cada cliente tiene su propio caso (matter). Todo queda organizado automáticamente.

### Tip 5: Aprovecha el calendario
Deja que Hermes maneje los plazos. Tú concéntrate en el trabajo legal.

---

*Hermes Legal Pro — Guía de Usuario v1.0*
*Para abogados que quieren trabajar más inteligentemente*
