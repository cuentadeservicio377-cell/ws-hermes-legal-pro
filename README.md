# HERMES LEGAL PRO v1.0.0
## Producto Completo para Despachos Legales

---

## 🎯 QUÉ ES

Hermes Legal Pro es un **sistema operativo completo para despachos de abogados** basado en inteligencia artificial.

### Funcionalidades principales:
- **🎤 Transcripción de reuniones** — Entra a Google Meet, transcribe todo, genera resumen
- **📄 Generación de documentos** — Crea contratos, NDAs, cartas legales con diseño profesional
- **📁 Gestión de matters** — Organiza casos, carpetas, documentos, y seguimientos
- **📅 Calendario inteligente** — Plazos, deadlines, follow-ups automáticos
- **🤖 Atención al cliente 24/7** — Responde consultas, agenda citas, da seguimiento
- **📊 Dashboard de control** — Visibilidad completa del despacho

### Diferenciador:
No es un SaaS en la nube. Es **on-premise** — corre en tu MacBook Air M2. Tus datos NUNCA salen de tu computadora. Privacidad total.

---

## 📦 CONTENIDO DEL PAQUETE

```
hermes-legal-pro-v1.0.0/
├── README.md                    # Este archivo
├── INSTALL.md                   # Guía de instalación para técnico
├── USER-GUIDE.md                # Guía de uso para abogado
├── LICENSE.md                   # Licencia comercial
│
├── hermes-legal-pro-profile.tar.gz    # Perfil preconfigurado
│
├── installer/
│   └── install-mac.sh          # Script de instalación macOS
│
├── config/
│   ├── config.yaml             # Configuración optimizada
│   └── .env.template           # Template de variables de entorno
│
├── skills/
│   ├── hermes-legal-pro/       # Skill maestra de orquestación
│   └── willow-legal-complete/  # Sistema legal completo
│
├── templates/                   # 23 templates legales mexicanos
├── excel/                       # Excel maestro preconfigurado
├── scripts/                     # Scripts utilitarios
└── docs/                        # Documentación adicional
```

---

## 🚀 INSTALACIÓN RÁPIDA (para técnicos)

```bash
# 1. Descomprimir
tar -xzf hermes-legal-pro-v1.0.0.tar.gz
cd hermes-legal-pro-v1.0.0

# 2. Ejecutar instalador
chmod +x installer/install-mac.sh
./installer/install-mac.sh

# 3. Configurar API keys
cp config/.env.template ~/.hermes/.env
# Editar ~/.hermes/.env con tus keys

# 4. Iniciar
hermes profile use legal-pro
hermes gateway start
```

Ver `INSTALL.md` para instrucciones detalladas.

---

## 👤 USO (para abogados)

### 1. Conectar Telegram
- Abre Telegram, busca tu bot
- Envía `/start` para iniciar

### 2. Entrar a reunión Google Meet
- Únete a la reunión normalmente
- Hermes transcribe automáticamente

### 3. Al terminar la reunión
- Recibes en Telegram:
  - Resumen de la reunión
  - Documentos generados (PDF)
  - Tareas pendientes
  - Próximos plazos

### 4. Gestionar matters
- `/matter-nuevo [cliente]` — Crear caso nuevo
- `/documento-generar [matter] [tipo]` — Generar documento
- `/plazo-crear [matter] [descripción] [fecha]` — Crear deadline
- `/status-legal` — Ver estado de todos los casos

### 5. Atender clientes
- Los clientes escriben al bot
- Hermes responde automáticamente
- Si es complejo, te notifica

Ver `USER-GUIDE.md` para guía completa.

---

## 💰 LICENCIA Y PRECIO

**Licencia anual:** $2,500 USD
**Incluye:**
- Software completo
- 23 templates legales mexicanos
- Motor de documentos Kami v3
- Soporte técnico (3 meses)
- Actualizaciones (1 año)

**Servicios adicionales:**
- Instalación y configuración: $500 USD
- Capacitación: $300 USD
- Personalización: $200 USD/template

---

## 📞 SOPORTE

- **Técnico:** Ver `TROUBLESHOOTING.md`
- **Usuario:** Ver `USER-GUIDE.md` FAQ
- **Ventas:** contacto@wscapital.ai

---

*Hermes Legal Pro v1.0.0*
*Producto de WS Capital — 2026*
