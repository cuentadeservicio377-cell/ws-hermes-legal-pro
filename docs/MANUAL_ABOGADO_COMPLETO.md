# HERMES LEGAL PRO v2.0
## Manual Completo para Abogados — Sistema de Gestión Legal Inteligente
### We Law S.C. / Willow Legal | Mayo 2026

---

## 📖 ÍNDICE

1. [¿Qué es este sistema?](#qué-es-este-sistema)
2. [¿Qué hace por ti? (funciones principales)](#qué-hace-por-ti)
3. [Cómo se ve el sistema](#cómo-se-ve)
4. [Paso a paso: tu primer día](#tu-primer-día)
5. [Cada función explicada en detalle](#funciones-detalladas)
6. [Los documentos que genera](#documentos-generados)
7. [Preguntas frecuentes](#faq)
8. [Si algo sale mal](#problemas)

---

## ¿Qué es este sistema?

**Hermes Legal Pro** es como tener un despacho de abogados completo dentro de tu computadora. Es un programa que:

- **Escucha** tus reuniones con clientes (por videollamada)
- **Escribe** documentos legales por ti (contratos, cartas, actas)
- **Organiza** todos tus casos (matters) en un solo lugar
- **Recuerda** plazos, citas y tareas pendientes
- **Atiende** consultas de clientes automáticamente
- **Diseña** documentos que se ven profesionales (como si los hiciera un diseñador)

### Analogía simple
Imagina que contratas:
- Un secretario que transcribe reuniones
- Un abogado junior que redacta contratos
- Un archivo que organiza carpetas
- Un recordatorio que nunca olvida plazos
- Un recepcionista que atiende llamadas 24/7

**Hermes Legal Pro es todas esas personas en un solo programa.**

---

## ¿Qué hace por ti?

### 🎤 1. Transcripción de Reuniones

**¿Qué hace?**
Cuando tienes una reunión por videollamada (Google Meet), el sistema:
1. Entra a la reunión contigo
2. Graba TODO lo que se dice
3. Convierte el audio a texto (transcripción)
4. Resume los puntos importantes
5. Identifica qué documentos necesitas generar después

**Ejemplo real:**
> Reunión con Pragma Studio (30 minutos)
> - El sistema transcribe 30 minutos de conversación
> - Resume: "Cliente necesita contrato de prestación de servicios, acta de entrega, y protocolo de cobranza"
> - Genera automáticamente esos 3 documentos
> - Te envía un mensaje a Telegram: "Reunión procesada. 3 documentos generados. Revisa plazo del 15 de junio."

**¿Cómo lo usas?**
1. Abres Google Meet normalmente
2. Dices a Hermes (por Telegram): "Estoy en reunión con Pragma"
3. Hermes se conecta y transcribe
4. Al terminar, recibes resumen y documentos

---

### 📄 2. Generación de Documentos Legales

**¿Qué hace?**
Crea documentos legales profesionales en PDF con diseño editorial de alta calidad.

**Documentos disponibles (23 tipos):**

| # | Documento | Cuándo usarlo | Área legal |
|---|-----------|---------------|------------|
| 1 | Contrato de Prestación de Servicios | Cuando contratas a alguien o te contratan | Contratos |
| 2 | Acuerdo de Confidencialidad (NDA) | Antes de compartir información secreta | Contratos |
| 3 | NDA Corporativo | Versión formal para empresas | Contratos |
| 4 | Contrato de Trabajo | Al contratar empleados | Laboral |
| 5 | Contrato de Arrendamiento | Para rentar inmuebles | Inmobiliario |
| 6 | Pagaré | Para deudas con plazo de pago | Cobranza |
| 7 | Carta de Cobranza | Para exigir pago amablemente | Cobranza |
| 8 | Convenio de Pagos | Para acordar pagos a plazos | Cobranza |
| 9 | Acta de Asamblea | Para juntas de accionistas | Corporativo |
| 10 | Poder Notarial | Para dar poder a alguien | Corporativo |
| 11 | Estatutos Sociales | Para constituir una empresa | Corporativo |
| 12 | Convenio de Accionistas | Para reglas entre socios | Corporativo |
| 13 | Reglamento Interior | Para reglas de la empresa | Laboral |
| 14 | Finiquito | Para finiquitar empleados | Laboral |
| 15 | NDA Laboral | Para confidencialidad con empleados | Laboral |
| 16 | Garantía | Para garantizar cumplimiento | Civil |
| 17 | Calendario de Cobranza | Para programar cobros | Cobranza |
| 18 | Bitácora de Entregas | Para documentar entregas | Corporativo |
| 19 | Expediente de Materialidad | Para trámites ante SAT | Fiscal |
| 20 | Carta SAT | Para comunicaciones fiscales | Fiscal |
| 21 | Aviso de Privacidad | Para protección de datos | Privacidad |
| 22 | Formato ARCO | Para derechos de datos personales | Privacidad |
| 23 | Términos y Condiciones | Para sitios web o servicios | Corporativo |

**¿Cómo se ve el PDF?**
- Papel color pergamino (como documento formal antiguo)
- Tipografía elegante (Playfair Display + Inter)
- Numeración legal profesional (1., 1.1, 1.2, a), b), c))
- Tablas con bordes sólidos para pagos y obligaciones
- Firmas con espacio para 2 testigos
- Números de página y encabezados

**Ejemplo real:**
> "Generar contrato de prestación de servicios para Pragma Studio"
> 
> Resultado: PDF de 5 páginas con:
> - Portada con logo y título
> - Partes identificadas (We Law S.C. y Pragma Studio)
> - 10 cláusulas numeradas (Objeto, Pago, Plazo, Entregables, Propiedad Intelectual, Confidencialidad, Responsabilidad, Terminación, Mediación, Disposiciones)
> - Tabla de pagos con montos y fechas
> - Firmas para ambas partes + 2 testigos

---

### 📁 3. Gestión de Matters (Casos)

**¿Qué es un "matter"?**
Un matter es un caso legal. Cada cliente tiene uno o más matters.

**¿Qué hace el sistema?**
- Crea una carpeta digital para cada cliente
- Guarda todos los documentos relacionados
- Rastrea el estado (activo, cerrado, urgente)
- Calcula días restantes para deadlines
- Muestra documentos pendientes

**Estructura de carpetas automática:**

```
WillowLegal/
├── 01_Clientes/
│   └── Pragma Studio/
│       ├── 01_Intake/
│       │   └── Datos del cliente, notas iniciales
│       ├── 02_Contratos/
│       │   ├── Borradores/
│       │   │   └── Contrato_v1.pdf, Contrato_v2.pdf
│       │   ├── Firmados/
│       │   │   └── Contrato_firmado.pdf
│       │   └── Anexos/
│       ├── 03_Correspondencia/
│       │   ├── Entrante/
│       │   └── Saliente/
│       ├── 04_Litigio/
│       │   ├── Demandas/
│       │   ├── Contestaciones/
│       │   ├── Pruebas/
│       │   └── Audiencias/
│       ├── 05_Facturacion/
│       │   ├── Cotizaciones/
│       │   ├── Facturas/
│       │   └── Pagos/
│       ├── 06_Entregables/
│       │   ├── Documentos_Finales/
│       │   ├── Presentaciones/
│       │   └── Reportes/
│       └── 07_Archivo/
│           └── Cerrado/
```

**Ejemplo real:**
> Matter PRAG-001: Pragma Studio
> - Cliente: Juan Antonio Angel Ramirez
> - Área: Mercantil / Contratos / Cobranza
> - Status: Activo, prioridad ALTA
> - Deadline: 15 de junio 2026
> - Documentos pendientes: 3 (contrato, acta de entrega, protocolo de cobranza)
> - Plazos vencidos: 1 (respuesta a disputa Andy)
> - Carpeta: C:\WillowLegal\01_Clientes\Pragma Studio

---

### 📅 4. Calendario y Plazos

**¿Qué hace?**
- Crea recordatorios automáticos después de cada reunión
- Calcula días restantes para cada deadline
- Alerta cuando un plazo está por vencer (7 días, 3 días, 1 día)
- Sincroniza con Google Calendar

**Tipos de plazos:**
- **Follow-up**: "Llamar al cliente en 3 días"
- **Deadline**: "Entregar contrato antes del 15"
- **Audiencia**: "Audiencia el 20 de junio a las 10:00"
- **Vencimiento**: "El pagaré vence el 30"

**Ejemplo real:**
> Después de reunión con Pragma:
> - Plazo 1: "Enviar borrador de contrato" — 3 días
> - Plazo 2: "Revisar cláusula de intereses" — 5 días
> - Plazo 3: "Entrega final paquete legal" — 15 de junio
>
> Alertas automáticas:
> - "⚠️ Plazo vence en 3 días: Enviar borrador de contrato"
> - "🔴 Plazo vencido: Respuesta a disputa Andy (176 días)"

---

### 🤖 5. Atención al Cliente 24/7

**¿Qué hace?**
- Responde mensajes de clientes automáticamente
- Responde preguntas frecuentes (horarios, costos, procesos)
- Agenda citas en tu calendario
- Escalate a ti cuando la pregunta es compleja
- Da seguimiento a casos automáticamente

**Ejemplo real:**
> Cliente escribe a las 11 PM: "¿Cuándo estará listo mi contrato?"
>
> Hermes responde automáticamente:
> "Buenas noches. Su contrato está en revisión final. Estará listo el jueves 15 de mayo. ¿Necesita algo más?"
>
> Si el cliente pregunta algo complejo:
> "Voy a consultar con el abogado y le respondo mañana antes de las 10:00 AM."
> → Te envía notificación a ti para que respondas

---

### 📊 6. Dashboard de Control

**¿Qué es?**
Una página web que ves en tu navegador (Chrome, Safari) donde ves TODO tu despacho de un vistazo.

**¿Qué muestra?**

**KPIs (números principales):**
- Matters activos: 5
- Matters urgentes: 2 (en rojo)
- Reuniones hoy: 1
- Documentos pendientes: 8
- Alertas activas: 3

**Próximos plazos:**
- PRAG-001: Entregar contrato — vence en 3 días
- CLI-002: Audiencia preparatoria — vence en 5 días
- ABC-003: Responder demanda — vencido (en rojo)

**Reuniones recientes:**
- Pragma Studio — 2 de mayo — 3 documentos generados
- Cliente ABC — 28 de abril — 1 acta generada

**Alertas:**
- "⚠️ Disputa Andy requiere atención inmediata"
- "📄 Contrato Pragma vence en 3 días"

---

## Cómo se ve

### Por Telegram (en tu celular)

```
Tú: Estoy en reunión con Pragma
Hermes: ✅ Conectado a Google Meet. Transcribiendo...

[30 minutos después]

Hermes: ✅ Reunión finalizada
📋 Resumen:
• Cliente necesita contrato ligero (no el de 24 páginas)
• Solicitó acta de entrega por fase
• Mencionó disputa con Andy (urgente)
• Plazo: entrega 15 de junio

📄 Documentos generados:
1. Contrato_Prestacion_Servicios_PRAGMA.pdf
2. Acta_Entrega_Fase_Conceptual.pdf
3. Protocolo_Cobranza_Escalonada.pdf

⏰ Plazos creados:
• Enviar borrador — 3 días
• Revisar cláusula intereses — 5 días
• Entrega final — 15 de junio

📁 Guardado en: C:\WillowLegal\01_Clientes\Pragma Studio
```

### Por Dashboard (en tu computadora)

```
┌─────────────────────────────────────────────┐
│  HERMES LEGAL PRO                    ⚙️ 👤  │
├─────────────────────────────────────────────┤
│  MATTERS  REUNIONES  DOCUMENTOS  CALENDARIO │
├─────────────────────────────────────────────┤
│                                             │
│  📊 KPIs                            📅 HOY  │
│  ┌────────┐ ┌────────┐ ┌────────┐  2 mayo  │
│  │   5    │ │   2    │ │   1    │          │
│  │Activos │ │Urgentes│ │Reunion │  10:00   │
│  └────────┘ └────────┘ └────────┘  Pragma │
│  ┌────────┐ ┌────────┐            15:00   │
│  │   8    │ │   3    │            ABC     │
│  │Pendient│ │Alertas │                     │
│  └────────┘ └────────┘                     │
│                                             │
│  ⚠️ PRÓXIMOS PLAZOS (7 días)               │
│  ┌─────────────────────────────────────┐   │
│  │ 🔴 PRAG-001  Contrato  3 días      │   │
│  │ 🟡 CLI-002   Audiencia 5 días      │   │
│  │ 🔴 ABC-003   VENCIDO   176 días    │   │
│  └─────────────────────────────────────┘   │
│                                             │
│  📋 REUNIONES RECIENTES                   │
│  ┌─────────────────────────────────────┐   │
│  │ Pragma Studio    2 mayo    3 docs    │   │
│  │ Cliente ABC     28 abr    1 acta    │   │
│  └─────────────────────────────────────┘   │
│                                             │
└─────────────────────────────────────────────┘
```

---

## Tu primer día

### Paso 1: Abrir el sistema

**Por Telegram (más fácil):**
1. Abre Telegram en tu celular
2. Busca tu bot (nombre que te dimos)
3. Escribe: `/start`

**Por Dashboard:**
1. Abre Chrome o Safari
2. Escribe: `http://localhost:8082`
3. Verás el dashboard con tus matters

### Paso 2: Crear tu primer matter

**Por Telegram:**
```
Tú: Nuevo matter para Cliente ABC
Hermes: ¿Área de práctica? (Mercantil, Laboral, Civil, etc.)
Tú: Mercantil
Hermes: ¿Descripción breve?
Tú: Contrato de prestación de servicios
Hermes: ✅ Matter ABC-001 creado. Carpeta creada en C:\WillowLegal\01_Clientes\Cliente ABC
```

**Por Dashboard:**
1. Click en botón "+ Nuevo Matter"
2. Llena: Nombre del cliente, área, descripción
3. Click "Crear"
4. Listo

### Paso 3: Generar tu primer documento

**Por Telegram:**
```
Tú: Generar contrato para ABC-001
Hermes: ¿Qué tipo de contrato?
1. Prestación de Servicios
2. Confidencialidad
3. Arrendamiento
...
Tú: 1
Hermes: Generando... ✅ Listo.
📄 Contrato_ABC-001_Prestacion_Servicios_20260502.pdf
📁 Guardado en: 02_Contratos/Borradores/
```

**Por Dashboard:**
1. Ve a Matters → ABC-001
2. Click "Generar Documento"
3. Selecciona "Contrato de Prestación de Servicios"
4. Click "Generar"
5. Descarga el PDF

### Paso 4: Revisar plazos

**Por Telegram:**
```
Tú: Alertas de hoy
Hermes: 📅 Alertas para 2 de mayo:
• PRAG-001: Contrato vence en 3 días
• ABC-001: Revisar borrador (creado hoy)
```

---

## Funciones detalladas

### Transcripción de reuniones (paso a paso técnico)

**Antes de la reunión:**
1. Abres Google Meet
2. Dices a Hermes: "Reunión con [nombre del cliente]"
3. Hermes se conecta como participante

**Durante la reunión:**
- Hermes escucha y transcribe en tiempo real
- No interrumpe, no habla, solo escucha
- Detecta automáticamente: acuerdos, plazos, documentos mencionados

**Después de la reunión:**
1. Recibes resumen en Telegram (1-2 minutos)
2. Recibes lista de documentos sugeridos
3. Puedes decir: "Genera todos" o "Genera solo el contrato"
4. Los PDFs se generan y se guardan automáticamente

**Qué NO hace:**
- ❌ No graba video (solo audio)
- ❌ No interrumpe la conversación
- ❌ No reemplaza tu criterio legal (tú revisas antes de firmar)

---

### Generación de documentos (cómo funciona por dentro)

**Paso 1: Validación de sustancia**
Antes de generar cualquier documento, el sistema verifica:
- ✅ ¿Hay partes identificadas? (nombre, RFC, domicilio)
- ✅ ¿Hay objeto del contrato?
- ✅ ¿Hay forma de pago?
- ✅ ¿Hay plazo?
- ✅ ¿Hay entregables?
- ✅ ¿Hay propiedad intelectual?
- ✅ ¿Hay confidencialidad?
- ✅ ¿Hay limitación de responsabilidad?
- ✅ ¿Hay suspensión y terminación?
- ✅ ¿Hay mediación y jurisdicción?
- ✅ ¿Hay disposiciones generales?
- ✅ ¿Hay firmas + testigos?
- ✅ ¿No hay metáforas ni explicaciones didácticas?

Si falta algo → Te dice exactamente qué falta y no genera el documento.

**Paso 2: Composición de bloques**
El documento se arma como bloques de Lego:
- Portada (cover_page)
- Partes (parties_block)
- Cláusula 1: Objeto (clause_section)
- Cláusula 2: Pago (clause_section + payment_table)
- Cláusula 3: Plazo (clause_section)
- ...
- Firmas (signature_block)

**Paso 3: Diseño Kami**
Se aplica el sistema de diseño:
- Fondo pergamino #faf8f0
- Tipografía Playfair Display (elegante, serif)
- Numeración legal profesional
- Tablas con bordes sólidos
- Diagramas de flujo si es necesario

**Paso 4: Output PDF**
Resultado: PDF profesional, listo para imprimir o enviar.

---

## Documentos generados

### Contrato de Prestación de Servicios (ejemplo completo)

**Estructura:**
1. **Portada**: Logo, título, fecha, número de contrato
2. **Partes**: 
   - Prestador: We Law S.C. (RFC, domicilio, representante)
   - Cliente: [Nombre] (RFC, domicilio, representante)
3. **Antecedentes**: 1 párrafo breve
4. **Cláusula 1: Objeto y Alcance**
   - 1.1 Servicios a prestar
   - 1.2 Alcance específico
   - 1.3 Exclusiones
5. **Cláusula 2: Forma de Pago**
   - 2.1 Monto total
   - 2.2 Forma de pago (tabla: concepto, monto, fecha)
   - 2.3 Anticipo
   - 2.4 Pagos posteriores
   - 2.5 Intereses moratorios
6. **Cláusula 3: Plazo**
   - Fecha de inicio, fecha de término, prórroga
7. **Cláusula 4: Entregables y Aceptación**
   - Lista de entregables con fechas
   - Proceso de aceptación
8. **Cláusula 5: Propiedad Intelectual**
   - Quién es dueño de qué
9. **Cláusula 6: Confidencialidad**
   - Qué es confidencial, por cuánto tiempo
10. **Cláusula 7: Limitación de Responsabilidad**
    - Hasta cuánto responde cada parte
11. **Cláusula 8: Suspensión y Terminación**
    - Causas de suspensión, causas de terminación
12. **Cláusula 9: Mediación y Jurisdicción**
    - CDMX, tribunales competentes
13. **Cláusula 10: Disposiciones Generales**
    - Modificaciones, notificaciones, interpretación
14. **Firmas**: 
    - Prestador + Testigo 1 + Testigo 2
    - Cliente + Testigo 1 + Testigo 2

**Diseño visual:**
- Papel color pergamino cálido
- Títulos en azul marino (#1B365D)
- Texto principal en negro editorial (#1a1a18)
- Tablas con encabezado oscuro y filas alternadas
- Firmas en grilla 2×2 con líneas de firma

---

## FAQ

### ¿Necesito internet?
- Para transcribir reuniones: Sí (Google Meet)
- Para generar documentos: No (todo es local)
- Para Telegram: Sí
- Para dashboard: No (funciona en tu computadora)

### ¿Mis datos están seguros?
- Sí. Todo se guarda en TU computadora.
- No va a la nube.
- No compartimos información con terceros.
- Los PDFs están en tus carpetas.

### ¿Qué pasa si se apaga la computadora?
- Todo se guarda en archivos (Excel, JSON, PDFs)
- Al prender, todo sigue ahí
- No se pierde nada

### ¿Puedo usarlo en mi celular?
- Sí, por Telegram
- El dashboard es mejor en computadora (pantalla grande)
- Los PDFs los puedes ver en cualquier dispositivo

### ¿Cuánto tiempo tarda en generar un documento?
- Contrato simple: 30 segundos
- Contrato complejo: 1-2 minutos
- Acta simple: 15 segundos

### ¿Puedo editar el documento después?
- Sí. El sistema genera:
  - PDF final (para enviar)
  - HTML editable (para modificar)
- Puedes editar el HTML y regenerar el PDF

### ¿Qué pasa si el cliente no tiene RFC?
- El sistema pone "[PENDIENTE]" y te alerta
- Tú lo llenas manualmente después
- No genera documentos incompletos sin avisarte

### ¿Funciona para cualquier área legal?
- Sí: Mercantil, Civil, Laboral, Fiscal, Corporativo, Inmobiliario, Privacidad
- Cada área tiene templates específicos

### ¿Puedo agregar mis propios templates?
- Sí. Son archivos JSON que puedes copiar y modificar
- Te enseñamos cómo en la capacitación

---

## Problemas

### "No se conecta a Google Meet"
1. Verifica que Chrome esté abierto
2. Verifica que estés logueado en Google
3. Dile a Hermes: "Conectar Meet" de nuevo

### "No genera el PDF"
1. Verifica que el template exista (lista con `/templates`)
2. Verifica que el matter tenga datos del cliente
3. Revisa el mensaje de error exacto

### "No veo el dashboard"
1. Abre Chrome o Safari
2. Escribe exactamente: `http://localhost:8082`
3. Si no carga, el backend no está corriendo
4. Abre Terminal y ejecuta: `python3 app.py`

### "Telegram no responde"
1. Verifica que el bot esté activo
2. Escribe `/start` de nuevo
3. Si sigue sin responder, reinicia el gateway

### "Los documentos salen en inglés"
- Todos los templates están en español
- Si salen en inglés, hay un error de configuración
- Contacta soporte

---

## 📞 Soporte

**Si algo no funciona:**
1. Revisa este manual primero (FAQ y Problemas)
2. Si persiste, envía mensaje a Telegram con:
   - Qué intentaste hacer
   - Qué error apareció (texto exacto)
   - Captura de pantalla si es posible

**Contacto:**
- Email: soporte@wscapital.ai
- Telegram: @HermesLegalProBot

---

*Hermes Legal Pro v2.0*
*Producto de WS Capital — 2026*
*Diseñado para abogados mexicanos*
