---
name: hermes-legal-pro
description: "Skill maestra de orquestación para Hermes Legal Pro — producto completo para despachos legales. Integra Google Meet, transcripción, generación de documentos, gestión de matters, calendario, y atención al cliente."
trigger: Cuando se detecte una reunión de Google Meet finalizada, cuando se solicite generar documentos post-reunión, cuando se cree un nuevo matter legal, o cuando se active el perfil legal-pro.
version: 1.0.0
author: WS Capital
license: MIT
metadata:
  hermes:
    tags: [legal, hermes-legal-pro, google-meet, transcription, documents, matter-management, calendar, client-attendant]
---

# Hermes Legal Pro — Skill Maestra de Orquestación

## 🎯 PROPÓSITO

Esta skill orquesta TODO el sistema Hermes Legal Pro. No es una skill de documentos (eso lo hace willow-legal-complete). Esta skill conecta:

1. **Google Meet** → Transcripción
2. **Transcripción** → Análisis + Resumen
3. **Análisis** → Identificación de documentos necesarios
4. **Documentos** → Generación vía Motor Kami (willow-legal-complete)
5. **Matter** → Creación/actualización en sistema
6. **Calendario** → Plazos, follow-ups, deadlines
7. **Tareas** → Lista de pendientes post-reunión
8. **Cliente** → Atención automática 24/7

## 🤖 FLUJO POST-REUNIÓN (Automático)

```
REUNIÓN FINALIZA
    ↓
[google_meet plugin] → Transcript completo
    ↓
[hermes-legal-pro skill] → PROCESAMIENTO:
    ├─ 1. EXTRAER: puntos clave, acuerdos, compromisos, fechas mencionadas
    ├─ 2. IDENTIFICAR: qué documentos se necesitan (contrato, NDA, carta, etc.)
    ├─ 3. GENERAR: borradores vía Motor Kami (willow-legal-complete)
    ├─ 4. CREAR/ACTUALIZAR: matter en sistema (Excel + JSON + carpetas)
    ├─ 5. CALENDARIZAR: plazos, follow-ups, deadlines en Google Calendar
    ├─ 6. TAREAS: lista de pendientes con prioridades
    └─ 7. NOTIFICAR: abogado recibe resumen en Telegram
```

## 📋 COMANDOS DISPONIBLES

### `/meet-finalizada [transcript_path]`
Procesa una reunión finalizada. Llama internamente a todo el pipeline.

### `/matter-nuevo [nombre_cliente] [area]`
Crea un nuevo matter legal con carpeta, Excel, y estructura completa.

### `/documento-generar [matter_id] [template_key]`
Genera un documento legal para un matter existente.

### `/plazo-crear [matter_id] [descripción] [fecha]`
Crea un plazo/deadline vinculado a un matter.

### `/cliente-consulta [mensaje_cliente]`
Atiende una consulta de cliente automáticamente.

### `/status-legal`
Muestra estado de todos los matters activos.

## 🔧 INTEGRACIÓN CON WILLOW-LEGAL-COMPLETE

Esta skill NO reemplaza willow-legal-complete. La USA como motor de documentos:

```
hermes-legal-pro (orquestación)
    ↓ llama a
willow-legal-complete (motor de documentos)
    ↓ usa
Motor Kami v3 (renderizado PDF)
```

## 📁 ESTRUCTURA DE DATOS

### Matter (JSON)
```json
{
  "id": "LEG-001",
  "client_name": "Cliente Ejemplo SA",
  "status": "active",
  "practice_area": "Mercantil",
  "deadline": "2026-06-30",
  "priority": "high",
  "next_step": "Generar contrato de prestación de servicios",
  "blocker": "none",
  "meetings": [
    {
      "date": "2026-05-01",
      "transcript_path": "/path/to/transcript.txt",
      "summary": "Resumen generado por IA",
      "documents_needed": ["prestacion_servicios", "confidencialidad"],
      "documents_generated": ["LEG-001-CTR-001.pdf"]
    }
  ],
  "tasks": [
    {"id": 1, "description": "Revisar borrador contrato", "status": "pending", "priority": "high"}
  ],
  "calendar_events": [
    {"date": "2026-05-05", "description": "Follow-up con cliente", "type": "follow-up"}
  ]
}
```

## 🚀 EJECUCIÓN

### Post-reunión automático:
```bash
# 1. El plugin google_meet guarda el transcript
# 2. Esta skill se activa automáticamente
# 3. Procesa todo el pipeline
# 4. Notifica al abogado
```

### Manual:
```bash
/hermes-legal-pro meet-finalizada /path/to/transcript.txt
```

## 📚 DEPENDENCIAS

- willow-legal-complete (skill)
- google_meet (plugin)
- Motor Kami v3 (sistema de archivos)
- Excel maestro (sistema de archivos)
- Google Calendar (API)

## 📝 NOTAS

- Todo documento generado DEBE pasar por Motor Kami
- Todo matter DEBE tener carpeta física en filesystem
- Todo plazo DEBE sincronizarse con Google Calendar
- Todo transcript DEBE almacenarse para referencia futura

---

*Hermes Legal Pro — Skill Maestra v1.0*
*Integra: Meet + Transcripción + Documentos + PM + Calendario + Cliente*
