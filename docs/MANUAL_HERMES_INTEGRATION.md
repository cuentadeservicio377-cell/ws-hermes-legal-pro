# Manual — Willow Legal por Telegram

## 1. ¿Qué es Hermes?

Hermes es tu asistente virtual en Telegram. Puedes operar todo tu despacho desde el celular, sin abrir la computadora. Funciona con comandos de texto: le escribes `/matter nuevo "Cliente S.A."` y Hermes crea el caso, la carpeta en Drive, y te avisa.

---

## 2. Comandos disponibles

### `/matter` — Gestionar casos

```bash
# Crear un caso nuevo
/matter nuevo "Innovatech Digital" area=Corporativo

# Ver todos los casos
/matter list

# Ver un caso específico
/matter WIL-001
```

### `/contrato` — Generar documentos

```bash
# Generar un NDA para un caso
/contrato nda WIL-001

# Generar contrato de servicios
/contrato prestacion_servicios WIL-001

# Ver templates disponibles
/templates
```

### `/plazo` — Crear plazos

```bash
# Crear un plazo con fecha
/plazo WIL-001 "Audiencia inicial" 2026-06-15
```

### `/alerta` — Ver alertas

```bash
# Ver alertas de un caso
/alerta WIL-001

# Ver todas las alertas
/alerta
```

### `/status` — Ver estado general

```bash
# Ver estado completo del despacho
/status
```

### `/anticipo` — Finanzas

```bash
# Registrar un anticipo
/anticipo WIL-001 25000 "Pago inicial"

# Ver finanzas de un caso
/finanzas WIL-001
```

### `/honorario` y `/factura`

```bash
/honorario WIL-001 50000 "Honorarios mes 1"
/factura WIL-001 50000 "Factura mayo 2026"
```

---

## 3. Conversaciones de ejemplo

### Ejemplo 1: Recibir un cliente nuevo

> **Abogado**: `/matter nuevo "Pragma Studio" area=Corporativo`
>
> **Hermes**: ✅ Matter creado: WIL-005
> 📁 Carpeta: ~/WillowLegal/01_Clientes/Pragma_Studio
> 📁 Drive: https://drive.google.com/drive/folders/1ABC...
> 📋 Next step: Intake inicial pendiente
> 🏷️  Área: Corporativo

### Ejemplo 2: Generar una NDA urgente

> **Abogado**: `/contrato nda WIL-005`
>
> **Hermes**: 📝 Documento generado:
> Template: NDA / Acuerdo de confidencialidad
> 📄 WIL-005_nda.pdf
> 📁 motor_kami/output/
> 📤 Drive: https://drive.google.com/file/d/1XYZ...

### Ejemplo 3: Registrar un plazo judicial

> **Abogado**: `/plazo WIL-005 "Audiencia" 2026-07-20`
>
> **Hermes**: 📅 Plazo creado: ALERT-003
> Matter: WIL-005
> 📌 Audiencia
> 📆 Fecha límite: 2026-07-20
> 📅 Calendar: https://www.google.com/calendar/event?eid=...

### Ejemplo 4: Cobrar a un cliente

> **Abogado**: `/anticipo WIL-005 35000 "Pago honorarios"`
>
> **Hermes**: ✅ ANTICIPO registrado: FIN-005 — $35,000.00 MXN
> Matter: WIL-005
> Concepto: Pago honorarios

### Ejemplo 5: Revisar el despacho desde el celular

> **Abogado**: `/status`
>
> **Hermes**: 📊 ESTADO DEL DESPACHO
> ────────────────────
> 🟢 Casos activos: 3
> ⏰ Plazos pendientes: 2
> 💰 Total facturado: $122,871.00
> Buen trabajo esta semana. Quedan 2 plazos por atender.

---

## 4. Cómo recibir PDFs

Cuando generas un documento por Telegram:
1. Hermes genera el PDF
2. Lo sube a Google Drive automáticamente
3. Te envía el link directo para abrir desde el celular
4. También puedes abrirlo en Google Docs para editar

---

## 5. Configurar alertas automáticas

Hermes revisa plazos automáticamente. Para activar notificaciones:
1. Configura las variables de Telegram en `config/.env`
2. Ejecuta: `python3 scripts/check_plazos.py --notify`
3. Las alertas se enviarán a Telegram cuando haya plazos próximos

---

*Willow Legal v7 — Hermes Agent*
*WS Capital © 2026*
