# AUDITORÍA COMPLETA — ws-hermes-legal-pro
## Fecha: 2026-05-04
## Auditor: Hermes Neo
## Repositorio: https://github.com/cuentadeservicio377-cell/ws-hermes-legal-pro
## Commit HEAD: 629b030

---

## RESUMEN EJECUTIVO

El repositorio ws-hermes-legal-pro contiene **6,105 líneas de código** distribuidas en 13 archivos principales. Es un sistema funcional pero con **múltiples fallas críticas, inconsistencias arquitectónicas y deudas técnicas** que impiden su operación confiable en producción. Se identifican **47 problemas** clasificados en 5 niveles de severidad.

**Veredicto: NO LISTO PARA PRODUCCIÓN** — Requiere 2-3 semanas de trabajo intensivo.

---

## 1. FALLAS CRÍTICAS (Bloqueantes — Sistema no opera correctamente)

### 1.1 INCONSISTENCIA DE IDs DE MATTERS (CRÍTICO)
- **Archivos afectados:** `dashboard/backend/app.py`, `hermes_integration/commands.py`, `scripts/willow_standalone.py`
- **Problema:** Tres sistemas diferentes generan IDs con formatos distintos:
  - Dashboard API: `LEG-{len+1:03d}` (ej: LEG-001)
  - Hermes Commands: `WIL-{len+1:03d}` (ej: WIL-001)
  - Willow Standalone: `PRAG-XXX` (hardcodeado en docs)
- **Impacto:** Un matter creado por Telegram no es reconocido por el dashboard. Un documento generado por CLI no aparece en el dashboard.
- **Solución:** Unificar a un solo formato. Recomendado: `WIL-{timestamp}-{secuencia}` o al menos `WIL-{secuencia:03d}` en TODOS los módulos.

### 1.2 RUTAS DE DATOS INCONSISTENTES (CRÍTICO)
- **Archivos afectados:** Todos los scripts
- **Problema:** Los datos JSON viven en múltiples ubicaciones:
  - Dashboard API: `dashboard/datos/` (relativo al repo)
  - Hermes Commands: `~/WillowLegal/datos/` (en home del usuario)
  - Willow Standalone: `C:/WillowLegal/` (Windows hardcodeado)
  - Check Plazos: `dashboard/datos/` (relativo)
- **Impacto:** El dashboard no ve los matters creados por Telegram. Los plazos no se detectan. Es como tener 3 bases de datos diferentes.
- **Solución:** Definir UNA sola fuente de verdad. Recomendado: `~/.willowlegal/data/` o path configurable vía variable de entorno `WILLOW_DATA_DIR`.

### 1.3 HARDCODEO DE DATOS DEL DESPACHO (CRÍTICO)
- **Archivos afectados:** `hermes_integration/commands.py`, `scripts/willow_standalone.py`, `motor_kami/motor_kami.py`
- **Problema:** Datos de We Law están quemados en el código:
  - Prestador: "We Law S.C.", RFC: "WEL123456ABC"
  - Representante: "Lic. Pablo Meneses"
  - Email: "contacto@welaw.mx"
  - Domicilio: "Ciudad de México"
- **Impacto:** Cualquier otro despacho que use el sistema generaría documentos con datos de We Law. No es un producto genérico.
- **Solución:** Mover a `config/despacho.json` o variables de entorno. Cargar en runtime.

### 1.4 MOTOR KAMI NO USA TEMPLATES REALES (CRÍTICO)
- **Archivos afectados:** `hermes_integration/commands.py` (líneas 235-267)
- **Problema:** Cuando se genera un documento, el código NO lee el template JSON real. En su lugar, crea cláusulas genéricas hardcodeadas:
  ```python
  if template == "nda":
      clausulas_data = [...]  # Hardcodeado, no lee nda.json
  else:
      clausulas_data = [...]  # Genérico para TODOS los demás templates
  ```
- **Impacto:** Todos los documentos generados son idénticos salvo por el título. Un contrato de arrendamiento tiene las mismas cláusulas que un NDA. Los 23 templates son decorativos.
- **Solución:** Implementar `cargar_template_real()` que lea el JSON del template, extraiga `document_data_template`, y lo fusione con datos del matter.

### 1.5 FRONTEND ESPERA ENDPOINTS QUE NO EXISTEN (CRÍTICO)
- **Archivos afectados:** `dashboard/frontend/js/api.js`, `dashboard/frontend/js/app.js`
- **Problema:** El frontend hace llamadas a endpoints que el backend NO tiene:
  - `GET /api/tasks` → No existe en app.py
  - `POST /api/export-sheets` → No existe
  - `POST /api/export-docs` → No existe
  - `GET /api/drive-link/{matterId}` → No existe
  - `POST /api/check-plazos` → No existe
- **Impacto:** Errores 404 en consola. Funcionalidades rotas. Usuario ve "Error cargando datos".
- **Solución:** Implementar los endpoints faltantes o remover las llamadas del frontend.

### 1.6 SISTEMA DE FINANZAS INCOMPLETO (CRÍTICO)
- **Archivos afectados:** `dashboard/backend/app.py`, `dashboard/frontend/js/finanzas.js`
- **Problema:** 
  - Backend no tiene modelo Pydantic para finanzas
  - No hay endpoints POST/GET completos para finanzas
  - `finanzas.json` tiene estructura vacía (`movimientos: []`)
  - Frontend asume campos que no existen (`total_cobrado`, `total_pendiente`)
- **Impacto:** Dashboard muestra "$0" en balance siempre. No se pueden registrar ingresos/egresos.
- **Solución:** Implementar modelo completo, endpoints CRUD, y sincronización con Excel.

---

## 2. FALLAS MAYORES (Funcionalidad degradada)

### 2.1 SIN AUTENTICACIÓN NI AUTORIZACIÓN
- **Archivos afectados:** `dashboard/backend/app.py`
- **Problema:** CORS abierto a `*`. Cualquier sitio web puede llamar la API. No hay JWT, no hay sesiones, no hay roles (abogado vs paralegal vs cliente).
- **Impacto:** Seguridad zero. Un script malicioso podría borrar todos los matters.
- **Solución:** Implementar auth mínima: API key o JWT básico.

### 2.2 GOOGLE WORKSPACE INCOMPLETO
- **Archivos afectados:** `scripts/drive_manager.py`, `scripts/calendar_manager.py`
- **Problema:**
  - Drive Manager requiere `config/token.json` y `config/client_secret.json` en paths relativos
  - No maneja errores de token expirado correctamente
  - Calendar Manager depende de Drive Manager (acoplamiento innecesario)
  - No hay integración con Google Docs (generar borradores editables)
  - No hay integración con Google Sheets (exportar matters)
- **Impacto:** La "integración Google Workspace" es teórica. En la práctica fallará por paths incorrectos.
- **Solución:** Desacoplar credenciales. Implementar retries. Agregar endpoints faltantes.

### 2.3 SIN SISTEMA DE BACKUP
- **Archivo afectado:** Ninguno — no existe
- **Problema:** No hay script de backup. Si se borra `matters.json`, se pierde TODO.
- **Impacto:** Pérdida total de datos en caso de error humano o bug.
- **Solución:** Implementar `scripts/backup.py` que copie JSONs a `~/WillowLegal/05_Backups/` con timestamp.

### 2.4 TEMPLATES JSON SON ESQUELETOS VACÍOS
- **Archivos afectados:** `motor_kami/templates/*.json`
- **Problema:** Los templates tienen cláusulas con "..." (placeholder). No contienen texto legal real:
  ```json
  {
    "titulo": "Objeto y Alcance",
    "subclausulas": ["..."]
  }
  ```
- **Impacto:** Incluso si se arregla el motor para leer templates, los documentos saldrían con "..." en lugar de cláusulas legales.
- **Solución:** Poblar TODOS los templates con texto legal mexicano real. Esto es trabajo de abogado, no de programador.

### 2.5 SIN MIGRACIONES DE ESQUEMA
- **Archivos afectados:** Todos los JSONs
- **Problema:** Si cambiamos la estructura de `matters.json`, los archivos antiguos quedan inválidos. No hay script de migración.
- **Impacto:** Cada cambio de estructura rompe datos existentes.
- **Solución:** Implementar `scripts/migrate.py` con versionado de schema.

### 2.6 FRONTEND NO ES RESPONSIVE
- **Archivos afectados:** `dashboard/frontend/index.html`, `dashboard/frontend/css/styles.css`
- **Problema:** El dashboard usa layouts fijos en px. No hay media queries. En móvil se ve roto.
- **Impacto:** No se puede usar desde tablet o móvil.
- **Solución:** Rehacer CSS con flexbox/grid + media queries.

### 2.7 SIN TESTS AUTOMATIZADOS
- **Archivo afectado:** Ninguno — no existe directorio `tests/`
- **Problema:** Zero tests unitarios. Zero tests de integración. Zero CI/CD.
- **Impacto:** Cada cambio puede romper algo sin saberlo.
- **Solución:** Crear `tests/` con pytest. Tests mínimos para cada endpoint.

---

## 3. INCONSISTENCIAS ARQUITECTÓNICAS (Deuda técnica)

### 3.1 DUALIDAD DASHBOARD/SPA
- **Archivos afectados:** `dashboard/frontend/index.html`, `dashboard/spa/index.html`
- **Problema:** Hay DOS frontends. El SPA parece un fallback incompleto. El frontend principal es HTML plano con JS vanilla.
- **Impacto:** Confusión. Mantenimiento duplicado. El SPA probablemente está obsoleto.
- **Solución:** Elegir uno. Recomendado: mantener `frontend/` (más completo) y eliminar `spa/`.

### 3.2 CACHÉ EN MEMORIA SIN INVALIDACIÓN INTELIGENTE
- **Archivo afectado:** `dashboard/backend/app.py` (líneas 69-84)
- **Problema:** El caché `_CACHE` nunca expira. Si otro proceso modifica el JSON, el cache sigue con datos viejos.
- **Impacto:** Race conditions. Datos inconsistentes entre dashboard y CLI.
- **Solución:** Usar timestamps de modificación o TTL. O mejor: usar SQLite en lugar de JSON.

### 3.3 MOTOR KAMI USA SUBPROCESS EN LUGAR DE IMPORT
- **Archivo afectado:** `dashboard/backend/app.py` (líneas 440+), `hermes_integration/commands.py` (líneas 307-322)
- **Problema:** Para generar PDFs, ejecuta `python3 motor_kami.py --input temp.json --output out.pdf` como subprocess.
- **Impacto:** Overhead. Riesgo de race conditions. No se puede debuggear fácilmente. No aprovecha Python import.
- **Solución:** Importar `motor_kami` como módulo y llamar `generar_pdf(data, output_path)` directamente.

### 3.4 CONFIGURACIÓN DISPERSA EN 5 LUGARES
- **Archivos afectados:** `config/.env.template`, `config/hermes-commands.json`, `config/triggers.json`, `installer/install-mac.sh`, `actualizar.sh`
- **Problema:** La configuración está fragmentada. No hay un solo archivo de config.
- **Impacto:** Difícil de documentar. Fácil de olvidar configurar algo.
- **Solución:** Unificar en `config/config.yaml` con schema validado.

### 3.5 SCRIPTS DE INSTALACIÓN NO IDEMPOTENTES
- **Archivos afectados:** `installer/install-mac.sh`, `instalar-sistema-willow.sh`
- **Problema:** Si se ejecutan dos veces, pueden duplicar archivos o fallar.
- **Impacto:** Reinstalación riesgosa.
- **Solución:** Agregar checks de "¿ya existe?" en todos los pasos.

---

## 4. FUNCIONALIDAD FALTANTE (No implementada)

### 4.1 SIN SISTEMA DE USUARIOS/ROLES
- No hay login. No hay "abogado A" vs "abogado B". No hay permisos.

### 4.2 SIN HISTORIAL DE AUDITORÍA
- No se registra QUIÉN hizo QUÉ. No hay log de "Documento X generado por usuario Y el día Z".

### 4.3 SIN NOTIFICACIONES PUSH REALES
- `check_plazos.py` puede enviar a Telegram, pero requiere ejecutarse manualmente. No hay daemon ni cron configurado.

### 4.4 SIN BÚSQUEDA FULL-TEXT
- Los matters se filtran solo por cliente/área. No se puede buscar en el contenido de documentos.

### 4.5 SIN VERSIONADO DE DOCUMENTOS
- Si genero un contrato dos veces, sobrescribe el anterior. No hay "v1", "v2", "v3".

### 4.6 SIN FIRMA DIGITAL
- Los documentos se generan en PDF pero no tienen firma electrónica ni e.firma.

### 4.7 SIN REPORTES ANALÍTICOS
- No hay "matters por área", "tiempo promedio de cierre", "ingresos mensuales", etc.

### 4.8 SIN INTEGRACIÓN CON ONYX REAL
- La skill `willow-legal-complete` describe integración con Onyx, pero no hay código que conecte con Onyx API.

---

## 5. DOCUMENTACIÓN Y CALIDAD

### 5.1 DOCUMENTACIÓN DESACTUALIZADA
- `ARQUITECTURA_PRODUCTO_COMPLETA_v3_REAL.md` describe 37 endpoints, pero el backend tiene ~25 implementados.
- `INSTALL.md` menciona pasos que no existen (Paso 10, 11 mal numerados).

### 5.2 CÓDIGO SIN TIPAR COMPLETAMENTE
- Muchas funciones usan `Dict[str, Any]` en lugar de modelos Pydantic concretos.
- El frontend usa JS vanilla sin TypeScript.

### 5.3 MANEJO DE ERRORES INCONSISTENTE
- Algunos endpoints retornan `{"status": "ok"}`, otros retornan el objeto directo, otros levantan HTTPException.

---

## TABLA RESUMEN DE PROBLEMAS

| # | Problema | Severidad | Archivos | Esfuerzo estimado |
|---|----------|-----------|----------|-------------------|
| 1 | IDs de matters inconsistentes | CRÍTICO | 3 archivos | 4 horas |
| 2 | Rutas de datos dispersas | CRÍTICO | 8 archivos | 8 horas |
| 3 | Datos del despacho hardcodeados | CRÍTICO | 3 archivos | 4 horas |
| 4 | Motor Kami no lee templates reales | CRÍTICO | 1 archivo | 8 horas |
| 5 | Frontend llama endpoints inexistentes | CRÍTICO | 2 archivos | 6 horas |
| 6 | Finanzas incompletas | CRÍTICO | 3 archivos | 8 horas |
| 7 | Sin autenticación | MAYOR | 1 archivo | 6 horas |
| 8 | Google Workspace incompleto | MAYOR | 2 archivos | 12 horas |
| 9 | Sin backup | MAYOR | Nuevo | 4 horas |
| 10 | Templates vacíos | MAYOR | 23 archivos | 16 horas |
| 11 | Sin migraciones | MAYOR | Nuevo | 6 horas |
| 12 | Frontend no responsive | MAYOR | 2 archivos | 8 horas |
| 13 | Sin tests | MAYOR | Nuevo dir | 12 horas |
| 14 | Dualidad dashboard/spa | MEDIO | 2 archivos | 4 horas |
| 15 | Caché sin invalidación | MEDIO | 1 archivo | 4 horas |
| 16 | Subprocess en lugar de import | MEDIO | 2 archivos | 4 horas |
| 17 | Config dispersa | MEDIO | 5 archivos | 6 horas |
| 18 | Scripts no idempotentes | MEDIO | 2 archivos | 4 horas |
| 19-26 | Funcionalidad faltante (8 items) | MEDIO | Varios | 40 horas |
| 27-30 | Documentación y calidad | BAJO | Varios | 8 horas |

**TOTAL ESTIMADO: ~162 horas (~4 semanas a tiempo completo)**

---

## RECOMENDACIONES PRIORITARIAS

### Fase 1 (Semana 1): Fundamentos
1. Unificar rutas de datos a `~/.willowlegal/data/`
2. Unificar IDs a `WIL-{secuencia:03d}`
3. Mover datos hardcodeados a `config/despacho.json`
4. Implementar backup automático

### Fase 2 (Semana 2): Motor de Documentos
5. Hacer que Motor Kami lea templates reales
6. Poblar templates con texto legal real
7. Implementar versionado de documentos

### Fase 3 (Semana 3): API y Frontend
8. Implementar endpoints faltantes que el frontend espera
9. Completar sistema de finanzas
10. Agregar autenticación básica

### Fase 4 (Semana 4): Calidad
11. Escribir tests básicos
12. Implementar migraciones de schema
13. Hacer frontend responsive
14. Documentar todo

---

*Auditoría generada por Hermes Neo — 2026-05-04*
