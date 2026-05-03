# PROMPT EJECUTABLE — PRUEBA REAL CON CASO INYECTADO
# Barbería Don Ramón — Paquete documental completo

> **Instrucción:** Ejecutar prueba end-to-end usando el caso "Barbería Don Ramón" del archivo `docs/CASO_PRUEBA_DON_RAMON.md`. NO inventar datos. Usar los datos exactos proporcionados.

---

## ANTES DE EMPEZAR

1. Leer completamente `docs/CASO_PRUEBA_DON_RAMON.md`
2. Guardar los datos del cliente, matter, plazos, finanzas, y reuniones
3. Usar ESOS datos exactos en cada curl/operación
4. NO crear datos diferentes. NO usar "Cliente Test". NO usar "Matter Prueba".

---

## ORDEN CORRECTO DE OPERACIONES (Crítico)

```
1. FASE A: Crear matter (datos exactos del caso)
2. FASE B: Crear plazos (6 plazos del caso)
3. FASE C: Registrar finanzas (3 transacciones del caso)
4. FASE D: Crear reunión (datos exactos del caso)
5. FASE E: Generar documentos (6 documentos del caso)
6. FASE F: Verificar dashboard con datos
7. FASE G: Tomar screenshots del frontend CON datos visibles
8. FASE H: Verificar PDFs generados
9. FASE I: Verificar Google Drive
10. FASE J: Limpiar (AL FINAL, no antes)
```

**REGLA DE ORO:** NO limpiar matter ANTES de tomar screenshots.

---

## FASE A: CREAR MATTER (Datos exactos del caso)

```bash
cd ~/ws-hermes-legal-pro

# Verificar backend corriendo
curl -s http://localhost:8082/api/health | head -1 || {
  echo "Iniciando backend..."
  cd dashboard/backend
  nohup uvicorn app:app --host 0.0.0.0 --port 8082 > /tmp/backend.log 2>&1 &
  sleep 3
}

# Crear matter con datos EXACTOS del caso Don Ramón
curl -s -X POST http://localhost:8082/api/matters \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Barbería Don Ramón - Paquete Apertura",
    "cliente": "Barbería Don Ramón S.A.S. de C.V.",
    "representante": "Ramón Ernesto Gómez Pérez",
    "email": "ramon.gomez@donramon.barber",
    "telefono": "+52 55 1234 5678",
    "rfc_cliente": "BDR261202ABC",
    "area": "Corporativo",
    "materia": "corporativo",
    "prioridad": "alta",
    "estado": "Activo",
    "descripcion": "Paquete documental para formalizar barbería: arrendamiento, contratos laborales, reglamento interno, NDA, aviso de privacidad, franquicia",
    "honorarios": 45000,
    "moneda": "MXN",
    "forma_pago": "50% anticipo, 50% contra entrega",
    "fecha_inicio": "2026-05-02",
    "deadline": "2026-05-16",
    "next_step": "Generar contrato de arrendamiento",
    "notas_reunion": "Cliente quiere crecer: 2 sucursales + franquicia. Todo informal hasta ahora. Urgente formalizar antes de agosto 2026. Empleados: 3 barberos + 1 recepcionista. Local rentado $25,000/mes."
  }' | tee /tmp/fase_a_matter.json | python3 -m json.tool

# Guardar MATTER_ID
MATTER_ID=$(cat /tmp/fase_a_matter.json | python3 -c "import sys,json; print(json.load(sys.stdin).get('id',''))")
echo "MATTER_ID=$MATTER_ID"
echo "$MATTER_ID" > /tmp/matter_id.txt
```

**Verificación obligatoria:**
- Response debe tener `id` no vacío
- `cliente` debe ser "Barbería Don Ramón S.A.S. de C.V."
- `honorarios` debe ser 45000
- `estado` debe ser "Activo"

**Si falla:** Documentar error, NO continuar hasta resolver.

---

## FASE B: CREAR 6 PLAZOS (Datos exactos del caso)

```bash
MATTER_ID=$(cat /tmp/matter_id.txt)

echo "=== Plazo 1: Arrendamiento ==="
curl -s -X POST http://localhost:8082/api/plazo \
  -H "Content-Type: application/json" \
  -d "{\"matter_id\":\"$MATTER_ID\",\"titulo\":\"Entregar borrador arrendamiento\",\"descripcion\":\"Borrador de contrato de arrendamiento comercial para revisión del cliente\",\"fecha\":\"2026-05-05\",\"prioridad\":\"alta\"}" | tee /tmp/plazo1.json | python3 -m json.tool

echo "=== Plazo 2: Contratos trabajo ==="
curl -s -X POST http://localhost:8082/api/plazo \
  -H "Content-Type: application/json" \
  -d "{\"matter_id\":\"$MATTER_ID\",\"titulo\":\"Entregar contratos trabajo\",\"descripcion\":\"Borradores de 4 contratos de trabajo para revisión\",\"fecha\":\"2026-05-07\",\"prioridad\":\"alta\"}" | tee /tmp/plazo2.json | python3 -m json.tool

echo "=== Plazo 3: Reglamento + NDA ==="
curl -s -X POST http://localhost:8082/api/plazo \
  -H "Content-Type: application/json" \
  -d "{\"matter_id\":\"$MATTER_ID\",\"titulo\":\"Entregar reglamento y NDA\",\"descripcion\":\"Reglamento interno y NDA laboral\",\"fecha\":\"2026-05-09\",\"prioridad\":\"media\"}" | tee /tmp/plazo3.json | python3 -m json.tool

echo "=== Plazo 4: Aviso privacidad ==="
curl -s -X POST http://localhost:8082/api/plazo \
  -H "Content-Type: application/json" \
  -d "{\"matter_id\":\"$MATTER_ID\",\"titulo\":\"Entregar aviso de privacidad\",\"descripcion\":\"Aviso de privacidad para clientes de la barbería\",\"fecha\":\"2026-05-12\",\"prioridad\":\"media\"}" | tee /tmp/plazo4.json | python3 -m json.tool

echo "=== Plazo 5: Franquicia ==="
curl -s -X POST http://localhost:8082/api/plazo \
  -H "Content-Type: application/json" \
  -d "{\"matter_id\":\"$MATTER_ID\",\"titulo\":\"Entregar contrato franquicia\",\"descripcion\":\"Contrato de franquicia para expansión futura\",\"fecha\":\"2026-05-14\",\"prioridad\":\"baja\"}" | tee /tmp/plazo5.json | python3 -m json.tool

echo "=== Plazo 6: DEADLINE FINAL ==="
curl -s -X POST http://localhost:8082/api/plazo \
  -H "Content-Type: application/json" \
  -d "{\"matter_id\":\"$MATTER_ID\",\"titulo\":\"DEADLINE FINAL - Entrega completa\",\"descripcion\":\"Entrega de todo el paquete documental firmado\",\"fecha\":\"2026-05-16\",\"prioridad\":\"alta\"}" | tee /tmp/plazo6.json | python3 -m json.tool

echo "=== Verificar plazos creados ==="
curl -s http://localhost:8082/api/plazos | python3 -c "import sys,json; d=json.load(sys.stdin); print(f'Total plazos: {len(d)}'); [print(f'  {p[\"id\"]}: {p[\"titulo\"]} ({p[\"fecha\"]})') for p in d if p.get('matter_id') == '$MATTER_ID']"
```

**Verificación:** Deben crearse 6 plazos. Si se crean menos, documentar cuál falló.

---

## FASE C: REGISTRAR FINANZAS (3 transacciones exactas)

```bash
MATTER_ID=$(cat /tmp/matter_id.txt)

echo "=== Transacción 1: Anticipo ==="
curl -s -X POST http://localhost:8082/api/finanzas \
  -H "Content-Type: application/json" \
  -d "{\"matter_id\":\"$MATTER_ID\",\"tipo\":\"ingreso\",\"concepto\":\"Anticipo 50% honorarios\",\"monto\":22500,\"fecha\":\"2026-05-02\"}" | tee /tmp/fin1.json | python3 -m json.tool

echo "=== Transacción 2: Gastos notariales ==="
curl -s -X POST http://localhost:8082/api/finanzas \
  -H "Content-Type: application/json" \
  -d "{\"matter_id\":\"$MATTER_ID\",\"tipo\":\"egreso\",\"concepto\":\"Gastos notariales\",\"monto\":3500,\"fecha\":\"2026-05-03\"}" | tee /tmp/fin2.json | python3 -m json.tool

echo "=== Transacción 3: Honorarios IMPI ==="
curl -s -X POST http://localhost:8082/api/finanzas \
  -H "Content-Type: application/json" \
  -d "{\"matter_id\":\"$MATTER_ID\",\"tipo\":\"egreso\",\"concepto\":\"Honorarios registro IMPI\",\"monto\":5800,\"fecha\":\"2026-05-04\"}" | tee /tmp/fin3.json | python3 -m json.tool

echo "=== Verificar balance ==="
curl -s http://localhost:8082/api/finanzas | python3 -c "
import sys, json
d = json.load(sys.stdin)
ingresos = sum(t['monto'] for t in d if t['tipo'] == 'ingreso')
egresos = sum(t['monto'] for t in d if t['tipo'] == 'egreso')
print(f'Ingresos: ${ingresos}')
print(f'Egresos: ${egresos}')
print(f'Balance: ${ingresos - egresos}')
print(f'Esperado: $35700')
"
```

**Verificación:** Balance debe ser $35,700 ($45,000 - $9,300).

---

## FASE D: CREAR REUNIÓN (Datos exactos del caso)

```bash
MATTER_ID=$(cat /tmp/matter_id.txt)

curl -s -X POST http://localhost:8082/api/reuniones \
  -H "Content-Type: application/json" \
  -d "{\"matter_id\":\"$MATTER_ID\",\"cliente\":\"Ramón Ernesto Gómez Pérez\",\"fecha\":\"2026-05-02\",\"resumen\":\"Reunión inicial de intake. Cliente tiene barbería informal con 4 empleados. Quiere abrir 2 sucursales y franquiciar. Necesita: arrendamiento formal, contratos laborales, reglamento, NDA, aviso de privacidad, franquicia, registro de marca.\",\"acuerdos\":[\"Paquete de 6 documentos + registro marca\",\"Honorarios $45,000 MXN\",\"Entrega 16 mayo 2026\"],\"documentos_necesarios\":[\"Contrato arrendamiento\",\"Contratos trabajo (4)\",\"Reglamento interno\",\"NDA laboral\",\"Aviso privacidad\",\"Contrato franquicia\"],\"plazos\":[{\"descripcion\":\"Entrega arrendamiento\",\"fecha\":\"2026-05-05\"}]}" | tee /tmp/reunion.json | python3 -m json.tool
```

---

## FASE E: GENERAR DOCUMENTOS (6 documentos del paquete)

### E.1: Contrato de arrendamiento
```bash
MATTER_ID=$(cat /tmp/matter_id.txt)

curl -s -X POST "http://localhost:8082/api/matter/$MATTER_ID/generar-documento" \
  -H "Content-Type: application/json" \
  -d '{
    "template_key": "arrendamiento",
    "datos_extra": {
      "arrendador": {"nombre": "José Hernández López", "domicilio": "Av. Insurgentes 456, CDMX"},
      "arrendatario": {"nombre": "Barbería Don Ramón S.A.S. de C.V.", "rfc": "BDR261202ABC", "domicilio": "Calle Revolución 123, Col. Centro, CDMX"},
      "local": {"direccion": "Calle Revolución 123, Col. Centro, CDMX", "superficie": "80 m2", "uso": "Barbería y estética masculina"},
      "renta_mensual": 25000,
      "duracion": "3 años",
      "deposito": 50000,
      "fecha_inicio": "2026-06-01"
    }
  }' | tee /tmp/doc_arrendamiento.json | python3 -m json.tool
```

### E.2: Contrato de trabajo (Juan Carlos Morales)
```bash
curl -s -X POST "http://localhost:8082/api/matter/$MATTER_ID/generar-documento" \
  -H "Content-Type: application/json" \
  -d '{
    "template_key": "contrato_trabajo",
    "datos_extra": {
      "empleador": {"nombre": "Barbería Don Ramón S.A.S. de C.V.", "rfc": "BDR261202ABC", "domicilio": "Calle Revolución 123, CDMX", "representante": "Ramón Ernesto Gómez Pérez"},
      "empleado": {"nombre": "Juan Carlos Morales", "puesto": "Barbero", "salario": 12000, "horario": "10:00-20:00", "dias_descanso": "1 día rotativo", "fecha_ingreso": "2023-01-15"}
    }
  }' | tee /tmp/doc_juan.json | python3 -m json.tool
```

### E.3: Contrato de trabajo (Pedro Antonio Sánchez)
```bash
curl -s -X POST "http://localhost:8082/api/matter/$MATTER_ID/generar-documento" \
  -H "Content-Type: application/json" \
  -d '{
    "template_key": "contrato_trabajo",
    "datos_extra": {
      "empleador": {"nombre": "Barbería Don Ramón S.A.S. de C.V.", "rfc": "BDR261202ABC", "domicilio": "Calle Revolución 123, CDMX", "representante": "Ramón Ernesto Gómez Pérez"},
      "empleado": {"nombre": "Pedro Antonio Sánchez", "puesto": "Barbero", "salario": 12000, "horario": "10:00-20:00", "dias_descanso": "1 día rotativo", "fecha_ingreso": "2023-03-01"}
    }
  }' | tee /tmp/doc_pedro.json | python3 -m json.tool
```

### E.4: Contrato de trabajo (Luis Fernando Castillo)
```bash
curl -s -X POST "http://localhost:8082/api/matter/$MATTER_ID/generar-documento" \
  -H "Content-Type: application/json" \
  -d '{
    "template_key": "contrato_trabajo",
    "datos_extra": {
      "empleador": {"nombre": "Barbería Don Ramón S.A.S. de C.V.", "rfc": "BDR261202ABC", "domicilio": "Calle Revolución 123, CDMX", "representante": "Ramón Ernesto Gómez Pérez"},
      "empleado": {"nombre": "Luis Fernando Castillo", "puesto": "Barbero", "salario": 12000, "horario": "10:00-20:00", "dias_descanso": "1 día rotativo", "fecha_ingreso": "2024-02-01"}
    }
  }' | tee /tmp/doc_luis.json | python3 -m json.tool
```

### E.5: Contrato de trabajo (María Elena Ruiz)
```bash
curl -s -X POST "http://localhost:8082/api/matter/$MATTER_ID/generar-documento" \
  -H "Content-Type: application/json" \
  -d '{
    "template_key": "contrato_trabajo",
    "datos_extra": {
      "empleador": {"nombre": "Barbería Don Ramón S.A.S. de C.V.", "rfc": "BDR261202ABC", "domicilio": "Calle Revolución 123, CDMX", "representante": "Ramón Ernesto Gómez Pérez"},
      "empleado": {"nombre": "María Elena Ruiz", "puesto": "Recepcionista", "salario": 10000, "horario": "10:00-20:00", "dias_descanso": "domingos", "fecha_ingreso": "2023-06-01"}
    }
  }' | tee /tmp/doc_maria.json | python3 -m json.tool
```

### E.6: Reglamento interno
```bash
curl -s -X POST "http://localhost:8082/api/matter/$MATTER_ID/generar-documento" \
  -H "Content-Type: application/json" \
  -d '{
    "template_key": "reglamento_interior",
    "datos_extra": {
      "empresa": {"nombre": "Barbería Don Ramón S.A.S. de C.V.", "rfc": "BDR261202ABC", "domicilio": "Calle Revolución 123, CDMX"},
      "empleados": [
        {"nombre": "Juan Carlos Morales", "puesto": "Barbero"},
        {"nombre": "Pedro Antonio Sánchez", "puesto": "Barbero"},
        {"nombre": "Luis Fernando Castillo", "puesto": "Barbero"},
        {"nombre": "María Elena Ruiz", "puesto": "Recepcionista"}
      ],
      "horario_general": "10:00-20:00, lunes a sábado",
      "uniforme": "Camisa negra con logo Don Ramón"
    }
  }' | tee /tmp/doc_reglamento.json | python3 -m json.tool
```

### E.7: NDA laboral
```bash
curl -s -X POST "http://localhost:8082/api/matter/$MATTER_ID/generar-documento" \
  -H "Content-Type: application/json" \
  -d '{
    "template_key": "nda_laboral",
    "datos_extra": {
      "empresa": {"nombre": "Barbería Don Ramón S.A.S. de C.V.", "rfc": "BDR261202ABC", "domicilio": "Calle Revolución 123, CDMX", "representante": "Ramón Ernesto Gómez Pérez"},
      "confidencialidad": "Base de datos de clientes, métodos de corte, proveedores, estrategias de marketing"
    }
  }' | tee /tmp/doc_nda.json | python3 -m json.tool
```

### E.8: Aviso de privacidad
```bash
curl -s -X POST "http://localhost:8082/api/matter/$MATTER_ID/generar-documento" \
  -H "Content-Type: application/json" \
  -d '{
    "template_key": "aviso_privacidad",
    "datos_extra": {
      "empresa": {"nombre": "Barbería Don Ramón S.A.S. de C.V.", "rfc": "BDR261202ABC", "domicilio": "Calle Revolución 123, CDMX", "email": "ramon.gomez@donramon.barber"},
      "responsable": "Ramón Ernesto Gómez Pérez",
      "datos_recabados": ["Nombre", "Teléfono", "Correo electrónico", "Historial de citas"],
      "finalidad": "Agendamiento de citas, envío de promociones, historial de servicios"
    }
  }' | tee /tmp/doc_privacidad.json | python3 -m json.tool
```

**Verificación de documentos:**
```bash
echo "=== Verificar documentos generados ==="
ls -lh ~/ws-hermes-legal-pro/motor_kami/output/*.pdf 2>/dev/null | head -10
ls -lh ~/ws-hermes-legal-pro/motor_kami/output/*.pdf 2>/dev/null | wc -l | xargs echo "Total PDFs:"
```

**Deben generarse 8 PDFs.** Si se generan menos, documentar cuál falló.

---

## FASE F: VERIFICAR DASHBOARD CON DATOS REALES

```bash
echo "=== Dashboard KPIs ==="
curl -s http://localhost:8082/api/dashboard | python3 -m json.tool

echo "=== Matters ==="
curl -s http://localhost:8082/api/matters | python3 -c "import sys,json; d=json.load(sys.stdin); print(f'Matters: {len(d)}'); [print(f'  {m[\"id\"]}: {m[\"nombre\"]} - {m[\"estado\"]}') for m in d]"

echo "=== Documentos ==="
curl -s http://localhost:8082/api/documentos | python3 -c "import sys,json; d=json.load(sys.stdin); print(f'Documentos: {len(d)}'); [print(f'  {doc[\"id\"]}: {doc.get(\"template_key\",\"?\")}') for doc in d[-8:]]"

echo "=== Plazos ==="
curl -s http://localhost:8082/api/plazos | python3 -c "import sys,json; d=json.load(sys.stdin); print(f'Plazos: {len(d)}'); [print(f'  {p[\"id\"]}: {p[\"titulo\"]} ({p[\"fecha\"]})') for p in d]"

echo "=== Finanzas ==="
curl -s http://localhost:8082/api/finanzas | python3 -c "
import sys, json
d = json.load(sys.stdin)
ingresos = sum(t['monto'] for t in d if t['tipo'] == 'ingreso')
egresos = sum(t['monto'] for t in d if t['tipo'] == 'egreso')
print(f'Transacciones: {len(d)}')
print(f'Ingresos: ${ingresos}')
print(f'Egresos: ${egresos}')
print(f'Balance: ${ingresos - egresos}')
"
```

**Verificaciones obligatorias:**
- [ ] Matters: 1 (BDR-001)
- [ ] Documentos: 8 generados
- [ ] Plazos: 6
- [ ] Finanzas: 3 transacciones, balance $35,700
- [ ] Alertas: generadas automáticamente

---

## FASE G: SCREENSHOTS DEL FRONTEND (CON DATOS REALES)

**Abrir navegador en `http://localhost:8082`**

### G.1: Screenshot Dashboard
- Debe mostrar: 1 matter activo, 6 plazos, alertas, balance $35,700
- Guardar: `docs/screenshots/01_dashboard_datos_reales.png`

### G.2: Screenshot Matters
- Debe mostrar: BDR-001 "Barbería Don Ramón - Paquete Apertura"
- Guardar: `docs/screenshots/02_matter_don_ramon.png`

### G.3: Screenshot Documentos
- Debe mostrar: 8 documentos generados (arrendamiento, 4 contratos, reglamento, NDA, privacidad)
- **NO debe mostrar "undefined"**
- Guardar: `docs/screenshots/03_documentos_generados.png`

### G.4: Screenshot Plazos
- Debe mostrar: 6 plazos con fechas del caso
- Guardar: `docs/screenshots/04_plazos_don_ramon.png`

### G.5: Screenshot Finanzas
- Debe mostrar: $22,500 ingreso, $9,300 egresos, $35,700 balance
- Guardar: `docs/screenshots/05_finanzas_don_ramon.png`

### G.6: Screenshot Reuniones
- Debe mostrar: Reunión con Ramón Gómez del 2026-05-02
- Guardar: `docs/screenshots/06_reunion_don_ramon.png`

### G.7: Screenshot Alertas
- Debe mostrar: Alertas generadas por plazos próximos
- Guardar: `docs/screenshots/07_alertas_don_ramon.png`

**REGLA:** Si algún screenshot muestra datos vacíos o "undefined", documentar como BUG.

---

## FASE H: VERIFICAR PDFs GENERADOS

### H.1: Verificar existencia
```bash
ls -lh ~/ws-hermes-legal-pro/motor_kami/output/BDR*.pdf 2>/dev/null || ls -lh ~/ws-hermes-legal-pro/motor_kami/output/*.pdf | grep -E "arrendamiento|contrato|reglamento|nda|privacidad"
```

### H.2: Verificar contenido del PDF de arrendamiento
```bash
# Extraer texto
python3 -c "
import sys
sys.path.insert(0, '/usr/local/lib/python3.11/site-packages')
try:
    import fitz  # PyMuPDF
    doc = fitz.open('/tmp/test.pdf')  # o la ruta real
    text = ''
    for page in doc:
        text += page.get_text()
    print(text[:2000])
except:
    print('PyMuPDF no disponible')
" 2>/dev/null

# O usar pdftotext si está instalado
pdftotext ~/ws-hermes-legal-pro/motor_kami/output/*.pdf - 2>/dev/null | head -100 || echo "pdftotext no disponible"
```

### H.3: Verificar estructura del PDF
Abrir PDF en navegador/visor y verificar visualmente:
- [ ] Portada con título
- [ ] Bloque de PARTES (Ramón Gómez, José Hernández)
- [ ] Cláusulas numeradas
- [ ] Tabla de renta ($25,000)
- [ ] Firmas (2 partes + 2 testigos)

**Screenshot:** `docs/screenshots/08_pdf_arrendamiento.png`

---

## FASE I: VERIFICAR GOOGLE DRIVE (Condicional)

```bash
# Solo si hay token
curl -s "http://localhost:8082/api/matter/$MATTER_ID/drive-folder" | python3 -m json.tool
```

Si funciona: abrir link en navegador, verificar PDFs subidos.
Si falla: documentar error exacto.

---

## FASE J: LIMPIEZA (AL FINAL)

**SOLO DESPUÉS de tomar todos los screenshots y verificar todo.**

```bash
MATTER_ID=$(cat /tmp/matter_id.txt)

echo "=== Eliminando matter de prueba ==="
curl -s -X DELETE "http://localhost:8082/api/matters/$MATTER_ID" | python3 -m json.tool

echo "=== Verificar limpieza ==="
curl -s http://localhost:8082/api/matters | python3 -c "import sys,json; d=json.load(sys.stdin); print(f'Matters restantes: {len(d)}')"
curl -s http://localhost:8082/api/dashboard | python3 -m json.tool | head -20
```

---

## GENERACIÓN DEL REPORTE FINAL

Crear `docs/REPORTE_PRUEBA_DON_RAMON_v3.md`:

```markdown
# Reporte de Prueba — Caso Barbería Don Ramón

**Fecha:** {fecha}
**Caso:** Barbería Don Ramón S.A.S. de C.V.
**Matter ID:** BDR-001
**Tester:** Hermes AutoTest

## Datos del Cliente (Inyectados)

- **Cliente:** Barbería Don Ramón S.A.S. de C.V.
- **RFC:** BDR261202ABC
- **Representante:** Ramón Ernesto Gómez Pérez
- **Honorarios:** $45,000 MXN
- **Paquete:** 6 documentos + registro de marca

## Resultados por Fase

### Fase A: Matter creado
- ID: {MATTER_ID}
- Estado: {ok/error}
- Carpeta creada: {si/no}

### Fase B: Plazos creados
- Total: {X}/6
- Listado: {pegar lista}

### Fase C: Finanzas registradas
- Total transacciones: {X}/3
- Balance: ${monto}
- Esperado: $35,700

### Fase D: Reunión creada
- ID: {X}
- Fecha: 2026-05-02

### Fase E: Documentos generados
- Total PDFs: {X}/8
- Listado: {pegar lista}
- Tamaños: {pegar tamaños}

### Fase F: Dashboard verificado
- Matters activos: {X}
- Documentos: {X}
- Plazos: {X}
- Balance: ${X}

### Fase G: Screenshots
- Dashboard: {ruta}
- Matters: {ruta}
- Documentos: {ruta}
- Plazos: {ruta}
- Finanzas: {ruta}
- Reuniones: {ruta}
- Alertas: {ruta}

### Fase H: PDFs verificados
- Arrendamiento: {ruta} — {estado}
- Contratos trabajo: {ruta} — {estado}
- Reglamento: {ruta} — {estado}
- NDA: {ruta} — {estado}
- Privacidad: {ruta} — {estado}

### Fase I: Google Drive
- Estado: {ok/falló}
- Error (si aplica): {mensaje}

### Fase J: Limpieza
- Matter eliminado: {si/no}
- Datos restantes: {X} matters

## Hallazgos

### ✅ Funcionando correctamente
{listar}

### ⚠️ Advertencias
{listar}

### ❌ Errores encontrados
{listar con mensaje exacto}

## Screenshots

{listar rutas y descripciones}

## Conclusión

{Sistema operativo para caso real / Requiere correcciones}
```

Commitear y pushear:
```bash
cd ~/ws-hermes-legal-pro
git add docs/REPORTE_PRUEBA_DON_RAMON_v3.md docs/screenshots/
git commit -m "TEST: Reporte prueba caso real Don Ramón — $(date +%Y-%m-%d)"
git push origin master
```

---

## REGLAS ESTRICTAS

1. **NO inventar datos.** Usar SOLO los datos del caso Don Ramón.
2. **NO limpiar antes de screenshots.** Orden: datos → screenshots → limpieza.
3. **NO marcar ✅ sin verificar.** Pegar output real del comando.
4. **Documentar errores exactos.** Copiar stderr completo.
5. **Si falla generación de PDF:** Documentar template, error, y continuar con el siguiente.
6. **Si frontend muestra "undefined":** Documentar como BUG crítico.
7. **Si balance no es $35,700:** Documentar discrepancia.

---

*Prompt ejecutable con caso inyectado — Barbería Don Ramón*
*Datos exactos, no inventados*
