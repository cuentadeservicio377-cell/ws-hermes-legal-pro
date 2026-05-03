# CASO DE PRUEBA REAL — "BARBERÍA DON RAMÓN"

> **Propósito:** Caso legal completo para probar TODO el sistema Hermes Legal Pro v3.
> **Cliente:** Barbería "Don Ramón" (ficticio pero realista)
> **Área:** Corporativo + Laboral + Mercantil
> **Documentos necesarios:** 6 documentos interrelacionados
> **Fecha de prueba:** 2026-05-02

---

## 1. DATOS DEL CLIENTE (Inyectar, no inventar)

### Información del negocio
- **Nombre del negocio:** Barbería "Don Ramón" S.A.S. de C.V.
- **RFC:** BDR261202ABC
- **Dirección fiscal:** Calle Revolución 123, Col. Centro, Ciudad de México, CP 06000
- **Representante legal:** Ramón Ernesto Gómez Pérez
- **Email del representante:** ramon.gomez@donramon.barber
- **Teléfono:** +52 55 1234 5678
- **Giro:** Servicios de barbería y estética masculina
- **Empleados actuales:** 3 barberos + 1 recepcionista
- **Sucursales:** 1 (matriz), plan de abrir 2 más en 2026

### Situación legal actual
- No tiene contratos escritos con empleados
- No tiene reglamento interno
- No tiene aviso de privacidad para clientes
- Quiere abrir franquicia pero no tiene contrato de franquicia
- Arrienda el local comercial sin contrato formal
- Necesita proteger su marca "Don Ramón"

### Transcript de reunión inicial (simulado)

```
FECHA: 2026-05-02
CLIENTE: Ramón Gómez
ABOGADO: WS Capital Legal

RAMÓN: "Oye, mira, yo tengo la barbería ya hace 3 años, todo bien, pero 
        ahora quiero crecer. Quiero abrir dos sucursales más y luego 
        franquiciar. Pero no tengo nada en orden, todo es de palabra."

ABOGADO: "¿Qué documentos tienes actualmente?"

RAMÓN: "Nada. Los barberos trabajan sin contrato. El local lo rento y 
         el dueño es buena onda, pero no tenemos contrato. Los clientes 
         dan sus datos para citas pero no sé si necesito aviso de 
         privacidad. Y mi marca 'Don Ramón' no está registrada."

ABOGADO: "¿Cuántos empleados?"

RAMÓN: "Tengo 3 barberos: Juan, Pedro y Luis. Y una chica en recepción, 
         María. Todos son de confianza pero quiero formalizar."

ABOGADO: "¿Honorarios mensuales?"

RAMÓN: "Cada barbero gana $12,000 pesos al mes más propinas. María 
         gana $10,000. Yo les pago en efectivo cada quincena."

ABOGADO: "¿El local es tuyo o rentado?"

RAMÓN: "Rentado. Pago $25,000 al mes al señor Hernández. Llevamos 3 
         años así, nunca hemos firmado nada. Él me dijo que si 
         quiero renovar por 3 años más, necesitamos hacerlo formal."

ABOGADO: "¿Cuándo quieres abrir las nuevas sucursales?"

RAMÓN: "La primera en agosto de este año, la segunda en enero del 
         que entra. Pero para eso necesito todo en orden. También 
         quiero registrar 'Don Ramón' como marca para que nadie 
         me la copie."

ABOGADO: "¿Tienes logo registrado?"

RAMÓN: "Sí, tengo un logo con una navaja y el nombre. Mi primo me 
         lo diseñó."

ABOGADO: "¿Los barberos usan uniforme? ¿Tienen horario fijo?"

RAMÓN: "Sí, camisa negra con el logo. Horario 10am a 8pm, lunes a 
         sábado. Domingo cerrado."

ABOGADO: "¿Les das días de descanso? ¿Vacaciones?"

RAMÓN: "Un día a la semana, rotativo. Vacaciones... la verdad no 
         les he dado vacaciones formales. Me dicen cuando necesitan 
         y les doy el día, pero sin goce de sueldo."

ABOGADO: "¿Hay algún problema actual con algún empleado o el arrendador?"

RAMÓN: "No, todo bien. Pero quiero prevenir. Mi primo abrió una 
         barbería en Guadalajara y le copiaron el nombre. No quiero 
         que me pase."

ABOGADO: "¿Tienes algún contrato con proveedores? ¿Inventario?"

RAMÓN: "Compro productos a un distribuidor, todo de contado. No tengo 
         contratos. Inventario lo controlo yo en una libreta."

ABOGADO: "¿Aceptas tarjeta? ¿Facturas?"

RAMÓN: "Sí, tengo terminal. Facturo cuando me piden. Uso un sistema 
         de citas online donde los clientes dejan nombre y teléfono."

ABOGADO: "Perfecto. Te propongo este paquete documental:
         1. Contrato de arrendamiento comercial (3 años)
         2. Contratos de trabajo para los 4 empleados
         3. Reglamento interno de trabajo
         4. NDA para empleados (protege tu método y clientes)
         5. Aviso de privacidad para clientes
         6. Contrato de franquicia (para cuando estés listo)
         7. Registro de marca en IMPI
         
         ¿Te parece?"

RAMÓN: "Sí, todo eso necesito. ¿Cuánto tiempo y cuánto cuesta?"

ABOGADO: "2 semanas para documentos. Honorarios: $45,000 pesos. 
         Incluye todas las revisiones y una sesión de explicación."

RAMÓN: "Va. Empezamos."
```

---

## 2. MATER CREADO EN EL SISTEMA

### Datos exactos del matter
```json
{
  "id": "BDR-001",
  "nombre": "Barbería Don Ramón - Paquete Apertura y Formalización",
  "cliente": "Barbería Don Ramón S.A.S. de C.V.",
  "representante": "Ramón Ernesto Gómez Pérez",
  "email": "ramon.gomez@donramon.barber",
  "telefono": "+52 55 1234 5678",
  "rfc_cliente": "BDR261202ABC",
  "area": "Corporativo",
  "materia": "corporativo",
  "submateria": "constitucion_empresas",
  "prioridad": "alta",
  "estado": "Activo",
  "descripcion": "Paquete documental para formalizar barbería: arrendamiento, contratos laborales, reglamento interno, NDA, aviso de privacidad, franquicia, registro de marca",
  "honorarios": 45000,
  "moneda": "MXN",
  "forma_pago": "50% anticipo, 50% contra entrega",
  "fecha_inicio": "2026-05-02",
  "deadline": "2026-05-16",
  "next_step": "Generar contrato de arrendamiento",
  "blocker": "none",
  "origen": "Referido - Cliente existente",
  "notas_reunion": "Cliente quiere crecer: 2 sucursales + franquicia. Todo informal hasta ahora. Urgente formalizar antes de agosto 2026."
}
```

---

## 3. PAQUETE DOCUMENTAL (6 documentos interrelacionados)

### Secuencia de generación
| Orden | Documento | Template | Dependencia | Status |
|-------|-----------|----------|-------------|--------|
| 1 | Contrato de arrendamiento | `arrendamiento` | Ninguna | Pendiente |
| 2 | Contrato de trabajo (Juan) | `contrato_trabajo` | Ninguna | Pendiente |
| 3 | Contrato de trabajo (Pedro) | `contrato_trabajo` | Ninguna | Pendiente |
| 4 | Contrato de trabajo (Luis) | `contrato_trabajo` | Ninguna | Pendiente |
| 5 | Contrato de trabajo (María) | `contrato_trabajo` | Ninguna | Pendiente |
| 6 | Reglamento interno | `reglamento_interior` | Contratos de trabajo | Pendiente |
| 7 | NDA empleados | `nda_laboral` | Contratos de trabajo | Pendiente |
| 8 | Aviso de privacidad | `aviso_privacidad` | Ninguna | Pendiente |
| 9 | Contrato de franquicia | `contrato_franquicia` | Arrendamiento | Pendiente |

### Variables compartidas entre documentos
```json
{
  "empresa": {
    "nombre": "Barbería Don Ramón S.A.S. de C.V.",
    "rfc": "BDR261202ABC",
    "domicilio": "Calle Revolución 123, Col. Centro, Ciudad de México, CP 06000",
    "representante": "Ramón Ernesto Gómez Pérez",
    "email_representante": "ramon.gomez@donramon.barber"
  },
  "arrendador": {
    "nombre": "José Hernández López",
    "domicilio": "Av. Insurgentes 456, CDMX"
  },
  "local": {
    "direccion": "Calle Revolución 123, Col. Centro, CDMX",
    "superficie": "80 m2",
    "uso": "Barbería y estética masculina",
    "renta_mensual": 25000,
    "duracion": "3 años",
    "deposito": 50000
  },
  "empleados": [
    {
      "nombre": "Juan Carlos Morales",
      "puesto": "Barbero",
      "salario": 12000,
      "horario": "10:00-20:00",
      "dias_descanso": "1 día rotativo",
      "fecha_ingreso": "2023-01-15"
    },
    {
      "nombre": "Pedro Antonio Sánchez",
      "puesto": "Barbero",
      "salario": 12000,
      "horario": "10:00-20:00",
      "dias_descanso": "1 día rotativo",
      "fecha_ingreso": "2023-03-01"
    },
    {
      "nombre": "Luis Fernando Castillo",
      "puesto": "Barbero",
      "salario": 12000,
      "horario": "10:00-20:00",
      "dias_descanso": "1 día rotativo",
      "fecha_ingreso": "2024-02-01"
    },
    {
      "nombre": "María Elena Ruiz",
      "puesto": "Recepcionista",
      "salario": 10000,
      "horario": "10:00-20:00",
      "dias_descanso": "domingos",
      "fecha_ingreso": "2023-06-01"
    }
  ],
  "marca": {
    "nombre": "Don Ramón",
    "logo_descripcion": "Navaja de afeitar estilizada con nombre 'Don Ramón'",
    "clases_impi": ["Clase 44: Servicios de peluquería y barbería"]
  }
}
```

---

## 4. PLAZOS Y DEADLINES

| Plazo | Fecha | Descripción | Prioridad |
|-------|-------|-------------|-----------|
| P1 | 2026-05-05 | Entregar borrador arrendamiento | Alta |
| P2 | 2026-05-07 | Entregar borradores contratos trabajo | Alta |
| P3 | 2026-05-09 | Entregar reglamento interno + NDA | Media |
| P4 | 2026-05-12 | Entregar aviso de privacidad | Media |
| P5 | 2026-05-14 | Entregar contrato franquicia | Baja |
| P6 | 2026-05-16 | **DEADLINE FINAL** — Todo el paquete | **CRÍTICA** |
| P7 | 2026-05-20 | Presentar registro marca IMPI | Media |

---

## 5. FINANZAS DEL MATTER

| Concepto | Tipo | Monto | Fecha |
|----------|------|-------|-------|
| Anticipo 50% | Ingreso | $22,500 | 2026-05-02 |
| Gastos notariales | Egreso | $3,500 | 2026-05-03 |
| Honorarios IMPI | Egreso | $5,800 | 2026-05-04 |
| Pago final 50% | Ingreso | $22,500 | 2026-05-16 |

**Balance proyectado:** $35,700 MXN (ingresos: $45,000 — egresos: $9,300)

---

## 6. REUNIONES AGENDADAS

| # | Fecha | Tipo | Tema | Estado |
|---|-------|------|------|--------|
| 1 | 2026-05-02 | Inicial | Intake y definición de paquete | Completada |
| 2 | 2026-05-05 | Revisión | Revisar borrador arrendamiento | Pendiente |
| 3 | 2026-05-09 | Revisión | Revisar contratos laborales | Pendiente |
| 4 | 2026-05-12 | Revisión | Revisar reglamento + NDA | Pendiente |
| 5 | 2026-05-16 | Entrega | Entrega final y firma | Pendiente |

---

## 7. CHECKLIST DE PRUEBA POR FASE

### FASE A: Crear matter con datos completos
- [ ] POST /api/matters con JSON del caso Don Ramón
- [ ] Verificar matter creado con id BDR-001
- [ ] Verificar carpeta física creada en ~/WillowLegal/01_Clientes/
- [ ] Verificar carpeta en Google Drive creada

### FASE B: Generar documentos
- [ ] Generar contrato de arrendamiento (template: arrendamiento)
- [ ] Generar 4 contratos de trabajo (template: contrato_trabajo)
- [ ] Generar reglamento interno (template: reglamento_interior)
- [ ] Generar NDA laboral (template: nda_laboral)
- [ ] Generar aviso de privacidad (template: aviso_privacidad)
- [ ] Verificar que cada PDF tenga: PARTES, CLÁUSULAS, FIRMAS

### FASE C: Crear plazos
- [ ] POST /api/plazo para cada uno de los 6 plazos
- [ ] Verificar plazos en calendario

### FASE D: Registrar finanzas
- [ ] POST /api/finanzas para anticipo
- [ ] POST /api/finanzas para gastos notariales
- [ ] Verificar balance calculado correctamente

### FASE E: Crear reuniones
- [ ] POST /api/reuniones para reunión inicial
- [ ] Verificar reuniones en vista Reuniones

### FASE F: Verificar dashboard
- [ ] GET /api/dashboard — debe mostrar: 1 matter activo, 6 plazos, $45,000 ingresos
- [ ] Screenshot de dashboard con datos reales (no vacíos)

### FASE G: Verificar frontend
- [ ] Abrir localhost:8082
- [ ] Navegar a Matters — debe mostrar BDR-001
- [ ] Navegar a Documentos — debe mostrar 6+ documentos generados
- [ ] Navegar a Plazos — debe mostrar 6 plazos
- [ ] Navegar a Finanzas — debe mostrar $45,000 ingresos, $9,300 egresos
- [ ] Navegar a Reuniones — debe mostrar reunión del 2026-05-02
- [ ] Screenshot de cada vista

### FASE H: Verificar PDFs generados
- [ ] Abrir PDF de arrendamiento
- [ ] Verificar: datos del arrendador, local, renta, duración
- [ ] Verificar: cláusulas numeradas, firmas, testigos
- [ ] Abrir PDF de contrato de trabajo
- [ ] Verificar: nombre del empleado, salario, horario, puesto
- [ ] Screenshot de cada PDF

### FASE I: Verificar Google Drive
- [ ] Abrir carpeta de BDR-001 en Drive
- [ ] Verificar que PDFs están subidos
- [ ] Verificar links compartidos funcionan

### FASE J: Limpiar
- [ ] Eliminar matter BDR-001
- [ ] Eliminar plazos asociados
- [ ] Eliminar documentos asociados
- [ ] Verificar dashboard vacío al final

---

## 8. DATOS PARA INYECCIÓN DIRECTA

### Crear matter (curl exacto)
```bash
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
  }'
```

### Crear plazos (curls exactos)
```bash
# Guardar MATTER_ID del response anterior

# Plazo 1: Arrendamiento
curl -s -X POST http://localhost:8082/api/plazo \
  -H "Content-Type: application/json" \
  -d "{\"matter_id\":\"$MATTER_ID\",\"titulo\":\"Entregar borrador arrendamiento\",\"descripcion\":\"Borrador de contrato de arrendamiento comercial para revisión del cliente\",\"fecha\":\"2026-05-05\",\"prioridad\":\"alta\"}"

# Plazo 2: Contratos trabajo
curl -s -X POST http://localhost:8082/api/plazo \
  -H "Content-Type: application/json" \
  -d "{\"matter_id\":\"$MATTER_ID\",\"titulo\":\"Entregar contratos trabajo\",\"descripcion\":\"Borradores de 4 contratos de trabajo para revisión\",\"fecha\":\"2026-05-07\",\"prioridad\":\"alta\"}"

# Plazo 3: Reglamento + NDA
curl -s -X POST http://localhost:8082/api/plazo \
  -H "Content-Type: application/json" \
  -d "{\"matter_id\":\"$MATTER_ID\",\"titulo\":\"Entregar reglamento y NDA\",\"descripcion\":\"Reglamento interno y NDA laboral\",\"fecha\":\"2026-05-09\",\"prioridad\":\"media\"}"

# Plazo 4: Aviso privacidad
curl -s -X POST http://localhost:8082/api/plazo \
  -H "Content-Type: application/json" \
  -d "{\"matter_id\":\"$MATTER_ID\",\"titulo\":\"Entregar aviso de privacidad\",\"descripcion\":\"Aviso de privacidad para clientes de la barbería\",\"fecha\":\"2026-05-12\",\"prioridad\":\"media\"}"

# Plazo 5: Franquicia
curl -s -X POST http://localhost:8082/api/plazo \
  -H "Content-Type: application/json" \
  -d "{\"matter_id\":\"$MATTER_ID\",\"titulo\":\"Entregar contrato franquicia\",\"descripcion\":\"Contrato de franquicia para expansión futura\",\"fecha\":\"2026-05-14\",\"prioridad\":\"baja\"}"

# Plazo 6: DEADLINE FINAL
curl -s -X POST http://localhost:8082/api/plazo \
  -H "Content-Type: application/json" \
  -d "{\"matter_id\":\"$MATTER_ID\",\"titulo\":\"DEADLINE FINAL - Entrega completa\",\"descripcion\":\"Entrega de todo el paquete documental firmado\",\"fecha\":\"2026-05-16\",\"prioridad\":\"alta\"}"
```

### Registrar finanzas
```bash
# Anticipo
curl -s -X POST http://localhost:8082/api/finanzas \
  -H "Content-Type: application/json" \
  -d "{\"matter_id\":\"$MATTER_ID\",\"tipo\":\"ingreso\",\"concepto\":\"Anticipo 50% honorarios\",\"monto\":22500,\"fecha\":\"2026-05-02\"}"

# Gastos notariales
curl -s -X POST http://localhost:8082/api/finanzas \
  -H "Content-Type: application/json" \
  -d "{\"matter_id\":\"$MATTER_ID\",\"tipo\":\"egreso\",\"concepto\":\"Gastos notariales\",\"monto\":3500,\"fecha\":\"2026-05-03\"}"

# Honorarios IMPI
curl -s -X POST http://localhost:8082/api/finanzas \
  -H "Content-Type: application/json" \
  -d "{\"matter_id\":\"$MATTER_ID\",\"tipo\":\"egreso\",\"concepto\":\"Honorarios registro IMPI\",\"monto\":5800,\"fecha\":\"2026-05-04\"}"
```

### Crear reunión
```bash
curl -s -X POST http://localhost:8082/api/reuniones \
  -H "Content-Type: application/json" \
  -d "{\"matter_id\":\"$MATTER_ID\",\"cliente\":\"Ramón Ernesto Gómez Pérez\",\"fecha\":\"2026-05-02\",\"resumen\":\"Reunión inicial de intake. Cliente tiene barbería informal con 4 empleados. Quiere abrir 2 sucursales y franquiciar. Necesita: arrendamiento formal, contratos laborales, reglamento, NDA, aviso de privacidad, franquicia, registro de marca.\",\"acuerdos\":[\"Paquete de 6 documentos + registro marca\",\"Honorarios $45,000 MXN\",\"Entrega 16 mayo 2026\"],\"documentos_necesarios\":[\"Contrato arrendamiento\",\"Contratos trabajo (4)\",\"Reglamento interno\",\"NDA laboral\",\"Aviso privacidad\",\"Contrato franquicia\"],\"plazos\":[{\"descripcion\":\"Entrega arrendamiento\",\"fecha\":\"2026-05-05\"}]}"
```

---

## 9. VERIFICACIONES FINALES

### Dashboard debe mostrar:
- **Matters activos:** 1 (BDR-001)
- **Documentos generados:** 6+
- **Plazos esta semana:** según fecha actual
- **Alertas:** según plazos próximos
- **Balance mes:** $35,700 (si se registraron finanzas)

### Verificaciones de PDF:
Cada PDF generado DEBE contener:
- [ ] Portada con título del documento
- [ ] Bloque de PARTES (nombre, RFC, domicilio, representante)
- [ ] ANTECEDENTES (breve)
- [ ] CLÁUSULAS numeradas (1., 1.1, 1.2, etc.)
- [ ] FORMA DE PAGO (tabla si aplica)
- [ ] PLAZO (cláusula separada)
- [ ] DISPOSICIONES GENERALES
- [ ] FIRMAS (2 partes + 2 testigos)
- [ ] Pie de página con numeración

---

*Caso de prueba completo — Barbería Don Ramón*
*Datos inyectados, no inventados*
*Listo para prueba end-to-end del sistema*
