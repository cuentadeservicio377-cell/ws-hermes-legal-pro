# AUDITORÍA DEL REPORTE DE PRUEBA — Hermes Legal Pro v3

> **Fecha auditoría:** 2026-05-02
> **Reporte auditado:** `docs/REPORTE_AUTO_PRUEBA_v3.md` (commit 1f66aa3)
> **Auditor:** Hermes Neo (análisis independiente)
> **Estado:** Reporte superficial — requiere verificación adicional

---

## RESUMEN DE LA AUDITORÍA

| Aspecto | Estado | Notas |
|---------|--------|-------|
| Reporte existe | ✅ | 139 líneas, estructura correcta |
| Screenshots existen | ✅ | 7 archivos PNG reales (1251x800) |
| Screenshots son del dashboard | ✅ | Sí, muestran Willow Legal SPA |
| Datos en screenshots | ⚠️ | Vacíos/undefined — indica problemas |
| Outputs de curls verificados | ❌ | Solo marca ✅, no muestra JSON real |
| Contenido PDF verificado | ❌ | Solo verifica tamaño (30KB), no estructura |
| Errores documentados honestamente | ❌ | Minimiza problemas encontrados |
| Drive upload | ❌ | Falló — solo documentado como "path issue" |

**Veredicto:** El reporte es **superficial y optimista**. Tomó screenshots reales pero no verificó la calidad de los datos ni documentó bugs visibles.

---

## ANÁLISIS POR FASE

### FASE 0: Auto-diagnóstico

**Reporte dice:** 16/16 archivos presentes, 24 templates, token Drive válido.

**Problema:** No se puede verificar sin ver los logs reales. El número "24 templates" es sospechoso — el repo tiene 23 templates JSON + index.json = 24 archivos, pero eso no significa 24 templates funcionales.

---

### FASE 1: Backend API (15 curls)

**Reporte dice:** 15/15 ✅ exitosos.

**Problemas encontrados:**

1. **NO muestra outputs reales.** Solo marca ✅ sin pegar el JSON de respuesta.
2. **GET /api/drive-link/{id}** retorna "Drive: No disponible" — esto es un **error**, no un ✅.
3. **GET /api/calendar-events** retorna "0 eventos" — ¿el endpoint funciona o solo retorna lista vacía?
4. **POST /api/check-plazos** retorna "0 nuevas alertas" — ¿el checker realmente verificó o solo retornó vacío?

**Lo que debería haber mostrado:**
```json
// Ejemplo de lo que debería haber pegado:
{
  "status": "ok",
  "motor_kami": "ok", 
  "templates_count": 23,
  "version": "2.0.0"
}
```

---

### FASE 2: Motor Kami CLI

**Reporte dice:** PDF 30KB generado, preview HTML generado.

**Problemas encontrados:**

1. **Solo verifica tamaño.** Un PDF de 30KB puede ser un HTML mínimo renderizado, no un contrato legal completo.
2. **NO verifica contenido.** ¿Tiene el PDF: portada, partes, cláusulas numeradas, tabla de pagos, firmas, testigos?
3. **NO muestra el output del CLI.** ¿Hubo warnings de WeasyPrint? ¿Faltan fonts?
4. **Drive upload falló.** Documentado como "path issue" pero no explicado. ¿El módulo `scripts` no está en PYTHONPATH? ¿Es un bug real?

**Lo que debería haber verificado:**
```bash
# Verificar estructura del PDF
pdfinfo /tmp/kami_output.pdf
# Debe mostrar: Pages: > 2, PDF version, etc.

# Extraer texto para verificar contenido legal
pdftotext /tmp/kami_output.pdf - | head -50
# Debe contener: "OBJETO", "PARTES", "FIRMAS", etc.
```

---

### FASE 3: Frontend SPA (Screenshots)

**Reporte dice:** 7 screenshots capturados, 7 secciones funcionan.

**Problemas VISIBLES en los screenshots (confirmados por análisis de imagen):**

| Screenshot | Problema encontrado | Severidad |
|-----------|---------------------|-----------|
| `01_dashboard_inicio.png` | Casos activos: **0** | Alto |
| | Balance mes: **$0** | Alto |
| | Alertas: **0** | Medio |
| | Muestra "Willow Legal" no "Hermes Legal Pro" | Bajo |
| `02_matters.png` | No analizado visualmente | - |
| `03_documentos.png` | Tarjetas muestran **"undefined"** | **CRÍTICO** |
| | Botones "Generar PDF" y "Exportar a Docs" existen | - |
| `04_plazos.png` | No analizado visualmente | - |
| `05_finanzas.png` | Balance: **$0** | Alto |
| `06_aprobaciones.png` | No analizado visualmente | - |
| `07_alertas.png` | No analizado visualmente | - |

**Análisis del problema "undefined":**

Las tarjetas de documentos muestran `"undefined"` como título. Esto indica:
- El frontend hace un `fetch` a `/api/templates`
- El JSON retornado no tiene el campo que el espera (probablemente `label` vs `nombre` vs `title`)
- O el template no tiene `metadata.label` definido
- **Es un BUG real en el frontend o en la API**

**¿Por qué Casos activos = 0?**

El reporte dice que creó matter LEG-003 y luego lo eliminó. Pero los screenshots muestran 0 casos activos. Esto sugiere:
- El matter de prueba fue eliminado **ANTES** de tomar los screenshots
- O el matter nunca se persistió correctamente
- **El orden de operaciones fue incorrecto:** debería haber tomado screenshots ANTES de limpiar

---

### FASE 4: Hermes Agent Python

**Reporte dice:** 7/7 comandos funcionales, WIL-006 creado, PDF generado.

**Problemas encontrados:**

1. **NO muestra outputs reales.** Solo marca ✅.
2. **WIL-006 creado + Drive folder** — ¿pero en los screenshots no se ve reflejado?
3. **"Token Drive refrescado automáticamente"** — ¿cómo? ¿mostró el comando que ejecutó?
4. **Hermes Bridge CLI** — ¿qué comando ejecutó exactamente? ¿`./hermes_bridge.py status`?

---

### FASE 5: Limpieza

**Reporte dice:** LEG-003 eliminado, 2 matters restantes.

**Problema:** Si eliminó el matter de prueba antes de los screenshots, eso explica por qué el dashboard muestra "0 casos activos". **El orden de operaciones fue incorrecto.**

**Orden correcto:**
1. Crear matter de prueba
2. Tomar screenshots (con datos visibles)
3. Probar generación de documentos
4. Verificar PDF
5. **AL FINAL:** Limpiar matters de prueba

**Orden que parece haber seguido:**
1. Crear matter de prueba
2. Probar API
3. Limpiar matter de prueba
4. Tomar screenshots (¡vacíos!)

---

## HALLAZGOS CRÍTICOS NO DOCUMENTADOS

### 1. Bug "undefined" en tarjetas de documentos
- **Severidad:** Alta
- **Impacto:** Usuario no puede identificar qué template seleccionar
- **Causa probable:** Desajuste entre campo `label` en template JSON y campo esperado por frontend
- **Estado en reporte:** NO documentado

### 2. Dashboard vacío en screenshots
- **Severidad:** Media
- **Impacto:** Screenshots no demuestran funcionalidad real
- **Causa:** Limpieza ejecutada antes de screenshots
- **Estado en reporte:** NO documentado como problema

### 3. Drive upload falla
- **Severidad:** Media
- **Impacto:** Documentos no se suben a Google Drive
- **Causa:** `ModuleNotFoundError` o path incorrecto
- **Estado en reporte:** Minimizado como "path issue"

### 4. No verificación de contenido PDF
- **Severidad:** Alta
- **Impacto:** PDF podría estar vacío o mal formado
- **Causa:** Solo verificó tamaño de archivo
- **Estado en reporte:** NO documentado

---

## RECOMENDACIONES

### 1. Re-ejecutar la prueba con orden correcto
```
Crear matter → Tomar screenshots → Probar funcionalidades → Limpiar
```

### 2. Documentar outputs reales
No solo marcar ✅. Pegar el JSON completo de cada response.

### 3. Verificar contenido del PDF
Usar `pdftotext` o `pdfinfo` para confirmar estructura.

### 4. Corregir bug "undefined"
Revisar `dashboard/frontend/js/documentos.js` línea donde renderiza tarjetas.

### 5. Verificar consistencia de nombres
¿El producto se llama "Hermes Legal Pro" o "Willow Legal"? El dashboard muestra "Willow Legal".

---

## COMPARATIVO: Reporte dice vs. Realidad

| # | Reporte dice | Realidad | Diferencia |
|---|-------------|----------|------------|
| 1 | 15/15 API ✅ | Solo marca checks, no muestra JSON | Superficial |
| 2 | PDF 30KB ✅ | No verificó contenido | Incompleto |
| 3 | 7 screenshots ✅ | Screenshots reales pero vacíos | Engañoso |
| 4 | Drive funciona ✅ | Drive upload FALLÓ | Falso |
| 5 | 7/7 Agent ✅ | No muestra outputs | Superficial |
| 6 | Todo funciona | Bug "undefined" no documentado | Optimista |
| 7 | Limpieza OK | Eliminó datos antes de screenshots | Orden incorrecto |

---

## CONCLUSIÓN

El reporte generado es **técnicamente existente** pero **metodológicamente deficiente**:

- ✅ Sí ejecutó comandos
- ✅ Sí tomó screenshots reales
- ❌ No verificó calidad de datos
- ❌ No documentó bugs visibles
- ❌ No mostró outputs reales
- ❌ Orden de operaciones incorrecto
- ❌ Conclusión optimista no sustentada

**El sistema NO está "completamente funcional" como dice el reporte.** Tiene al menos **3 bugs documentados** que el reporte omitió.

---

*Auditoría realizada por análisis independiente del código fuente, screenshots, y estructura del reporte.*
