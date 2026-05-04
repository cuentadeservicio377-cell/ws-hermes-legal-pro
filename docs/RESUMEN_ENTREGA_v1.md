# WILLOW LEGAL — Sistema Standalone v1.0
## We Law S.C. | Fecha: 30 Abr 2026

---

## ✅ ESTADO ACTUAL: OPERATIVO

| Componente | Estado | Detalle |
|-----------|--------|---------|
| **Dashboard Web** | ✅ Funcionando | http://localhost:8081 |
| **Backend API** | ✅ 9 endpoints | FastAPI + JSON local |
| **Frontend SPA** | ✅ Completo | 6 vistas + modo edición |
| **Motor Documentos** | ✅ Kami v3 | 23 templates, validación sustancia |
| **Base de datos** | ✅ JSON + Excel | Persistencia local, sin PostgreSQL |
| **Scripts CLI** | ✅ 7 comandos | status, alertas, generar, abrir, crear |
| **Estructura carpetas** | ✅ Existente | C:\WillowLegal con Pragma Studio |
| **Excel Maestro** | ✅ v4.0 | 12 hojas con fórmulas y validaciones |
| **Skill Hermes** | ✅ Creada | willow-legal-standalone |

---

## 📊 DATOS REALES CARGADOS

### Cliente: Pragma Studio (PRAG-001)
- **Representante:** Juan Antonio Angel Ramirez
- **Email:** contacto@wscapital.ai
- **Área:** Mercantil / Contratos / Cobranza
- **Status:** Active | Prioridad: HIGH

### Problemas identificados: 8
| # | Problema | Prioridad | Documento requerido |
|---|----------|-----------|---------------------|
| 1 | Contrato 24 páginas "hostil" | high | Contrato ligero + T&C |
| 2 | Sin actas de entrega | high | 3 actas por fase |
| 3 | Sin protocolo cobranza | medium | Protocolo + plantillas |
| 4 | Sin intereses moratorios | medium | Contrato con intereses |
| 5 | Sin contrato subcontratistas | medium | Contrato subcontratación |
| 6 | **Disputa Andy** | **critical** | Estrategia + correo |
| 7 | Sin acta cierre | low | Acta cierre |
| 8 | Clientes USA sin mediación | low | Cláusula ICC |

### Documentos pendientes: 8
Todos en status "pendiente". Fecha límite original: 2025-12-15 (vencidos).

### Plazos vencidos: 3 (crítico)
- PLZ-001: Respuesta Andy — VENCIDO 176 días 🔴 CRITICAL
- PLZ-002: Borrador contrato — VENCIDO 166 días 🟡 HIGH
- PLZ-003: Paquete legal completo — VENCIDO 136 días 🟡 HIGH

### Finanzas
- Total proyecto: $353,080 MXN
- Anticipo recibido: $122,871 MXN
- Adeudo: $230,209 MXN
- Disputa Andy: $80,000-$200,000 en riesgo

---

## 🚀 CÓMO USAR EL SISTEMA

### Desde Telegram (Hermes)
- "Status de Pragma" → Resumen del matter
- "Alertas de Willow" → Alertas del día
- "Generar contrato para PRAG-001" → PDF generado

### Desde Dashboard Web
1. Abrir http://localhost:8081
2. Ver KPIs en Dashboard
3. Navegar a Matters → Ver PRAG-001
4. Click "Generar Doc" → Seleccionar template → PDF
5. Click "Abrir Carpeta" → Abre en Windows

### Desde Terminal
```bash
cd /root/ws-willow-standalone/scripts
python3 willow_standalone.py --status PRAG-001
python3 willow_standalone.py --alertas
python3 willow_standalone.py --generar PRAG-001 prestacion_servicios
```

---

## 📁 ESTRUCTURA DEL WORKSPACE

```
ws-willow-standalone/
├── dashboard/
│   ├── app.py              # FastAPI backend (9 endpoints)
│   └── spa/
│       └── index.html      # Frontend completo (6 vistas)
├── motor_kami/
│   ├── blocks.py           # Motor de generación PDF
│   ├── bridge_api.py       # API Kami (legacy)
│   ├── motor_kami.py       # Motor legacy
│   ├── templates/          # 23 templates JSON
│   └── output/             # PDFs generados
├── scripts/
│   └── willow_standalone.py # CLI principal
├── datos/
│   └── matters.json         # Datos de matters (Pragma Studio)
├── excel/
│   └── Centro_Operativo_Maestro_Willow_v4.xlsx
└── docs/
    └── PLAN_CONSTRUCCION.md
```

---

## 🎯 PRÓXIMAS MEJORAS (FASE 5+)

1. **Múltiples matters** — Actualmente solo Pragma Studio
2. **Edición inline** — Formularios en frontend para actualizar datos
3. **Sync Excel ↔ JSON** — Bidireccional en tiempo real
4. **Notificaciones** — Alertas automáticas por Telegram
5. **Integración Onyx** — Cuando esté disponible

---

## 📞 CONTACTO

- **Firma:** We Law S.C. / Willow Legal
- **Email:** hola@welaw.com.mx
- **Soporte técnico:** Hermes Neo / WS Capital
- **Dashboard:** http://localhost:8081
