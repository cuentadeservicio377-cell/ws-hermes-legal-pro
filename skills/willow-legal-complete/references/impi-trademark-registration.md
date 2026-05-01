---
name: ws-impi-trademark-registration
description: Investigación y preparación de solicitudes de registro de marca ante el IMPI (Instituto Mexicano de la Propiedad Industrial). Incluye investigación de Clasificación de Niza, análisis del formulario IMPI-00-001-A, estrategia de marca madre, guía de llenado, y verificación de logos. Complementa a willow-legal-complete para trámites de propiedad intelectual.
trigger: Cuando el usuario necesite registrar una marca, aviso comercial o nombre comercial ante el IMPI; investigar clases Niza para un signo distintivo; preparar formulario IMPI-00-001-A; o definir estrategia de registro de marca en México.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [impi, trademark, marca, niza, propiedad-intelectual, registro, signos-distintivos, mexican-law, willow-legal]
---

# Registro de Marca ante el IMPI — Sistema de Investigación y Preparación

Skill complementaria a `willow-legal-complete` para trámites de **propiedad intelectual** (registro de marcas, avisos comerciales, nombres comerciales).

---

## 1. FLUJO DE TRABAJO ESTÁNDAR

```
1. RECIBIR MATERIALES DEL CLIENTE
   └── Transcripción de reunión, logos, datos del solicitante

2. INVESTIGAR CLASIFICACIÓN NIZA
   └── Identificar clases correctas para productos/servicios
   └── Extraer términos específicos de NCLPub (WIPO)

3. ANALIZAR FORMULARIO IMPI-00-001-A
   └── Extraer campos requeridos
   └── Identificar documentación necesaria

4. DEFINIR ESTRATEGIA DE MARCA
   └── Marca madre vs marca compuesta
   └── Palabras no registrables
   └── Colores (blanco y negro recomendado)

5. PREPARAR GUÍA DE LLENADO
   └── Documento completo con todos los campos
   └── Checklist de documentos pendientes
   └── Timeline estimado

6. ENTREGAR AL CLIENTE / ABOGADO
   └── Investigación jurídica en Markdown
   └── Logos organizados para adjunto
   └── Próximos pasos claros
```

---

## 2. INVESTIGACIÓN DE CLASIFICACIÓN NIZA

### 2.1 Fuente oficial

**NCLPub (WIPO Nice Classification):**
- URL base: https://nclpub.wipo.int/enfr/
- Versión vigente: 2026 (Edition 13)
- Parámetros de URL: `?class_number=X&version=20260101&lang=en`

### 2.2 Método de extracción

Usar `browser_navigate` o `curl` para acceder a NCLPub, luego extraer términos relevantes con herramientas de texto. Ejemplo de URL para Clase 44:

```
https://nclpub.wipo.int/enfr/?basic_numbers=show&class_number=44&explanatory_notes=show&lang=en&menulang=en&mode=flat&notion=&pagination=no&version=20260101
```

Buscar términos específicos en el HTML resultante usando herramientas de búsqueda de texto.

### 2.3 Clases comunes para clientes WS Capital

| Industria | Clase | Términos clave NCL |
|-----------|-------|-------------------|
| Barbería/Peluquería | **44** | barber shop services (440249), hairdressing (440034), beauty salon services (440020), facial treatment services (440283) |
| Cosméticos/Cuidado personal | **3** | after-shave lotions, shaving preparations, cosmetic preparations for skin care, massage gels (non-medicated), cosmetics |
| Venta online/Retail | **35** | retail services, online retail services, provision of an online marketplace |
| Restaurantes/Alimentos | **43** | restaurant services, café services, bar services |
| Software/Tecnología | **9** | computer software, applications, downloadable apps |
| Consultoría | **35** | business consultancy, management consulting |

### 2.4 Notas explicativas importantes

- **Clase 44:** "hygienic and beauty care for human beings" — incluye barbería, peluquería, tratamientos faciales
- **Clase 3:** "cleaning preparations and cosmetic preparations used for personal hygiene and beautification" — aftershave, geles, cremas
- **Clase 35:** "services rendered by persons or organizations principally with the object of help in the working or management of a commercial undertaking" — venta, distribución comercial

**Regla crítica:** Si un producto tiene efectos terapéuticos/medicinales → **Clase 5** (farmacéuticos). Si es puramente cosmético → **Clase 3**. La descripción en la solicitud debe evitar términos médicos.

---

## 3. FORMULARIO IMPI-00-001-A

### 3.1 Estructura

| Página | Contenido |
|--------|-----------|
| 1 | Datos del solicitante (física/moral), domicilio, notificaciones |
| 2 | Datos del signo: tipo, clase, productos/servicios, denominación, representación, elementos no reservables |
| 3 | Documentos anexos: pago, poder, reglas de uso, actas, traducciones |
| 4 | Instrucciones de llenado |

### 3.2 Requisitos formales

| Requisito | Especificación |
|-----------|---------------|
| Idioma | Español |
| Medio | Mismo medio de inicio a fin (no mezclar digital con manuscrito) |
| Copias | Duplicado (2 ejemplares) |
| Impresión | Doble cara, papel oficio blanco |
| Firma | Autógrafa en ambos ejemplares (o electrónica con CURP) |
| Logo | Etiqueta física 4cm×4cm mínimo, 10cm×10cm máximo |
| Colores | Blanco y negro recomendado para flexibilidad |

### 3.3 Campos críticos

**Datos del solicitante:**
- Persona física: CURP, nombre completo, nacionalidad, teléfono
- Persona moral: RFC, denominación/razón social, nacionalidad, teléfono
- Domicilio: CP, calle, número exterior/interior, colonia, municipio, entidad federativa, país
- Domicilio para notificaciones: debe estar en territorio nacional
- Correo electrónico: obligatorio

**Datos del signo:**
- Tipo: Registro de Marca / Marca Colectiva / Marca de Certificación / Aviso Comercial / Nombre Comercial
- Clase: número de 1 o 2 dígitos (consultar Niza)
- Productos/Servicios: descripción libre o términos NCL
- Denominación: palabra exacta a proteger
- Representación: etiqueta con el logo (4cm×4cm mínimo)
- Elementos no reservables: palabras genéricas/descriptivas que aparecen en el logo pero no se protegen
- Fecha de primer uso: DD/MM/AAAA o "No se ha usado"

---

## 4. ESTRATEGIA DE MARCA MADRE ("JOSÉ CUERVO")

### 4.1 Fundamento

Registrar solo la **palabra central** (marca madre) permite:
1. Proteger la marca en su forma más amplia
2. Agregar productos/servicios posteriormente sin nuevos registros
3. Oponerse a terceros que usen la marca + cualquier complemento

### 4.2 Ejemplo: José Cuervo

- Registró: **"Cuervo"** (no "José Cuervo Tequila")
- Resultado: ningún alcohol puede llamarse "Cuervo" aunque sea vodka
- Extensión: "Cuervo Negro", "Cuervo Especial" → todos protegidos

### 4.3 Aplicación a Cervus

| Opción | Registro | Protección |
|--------|----------|------------|
| ❌ Débil | "Servus Barbería" | Solo protege esa combinación exacta |
| ❌ Débil | "Servus Botica Oficinal" | Solo protege esa combinación exacta |
| ✅ Fuerte | **"SERVUS"** | Protege "SERVUS" + cualquier complemento en las clases registradas |

### 4.4 Elementos no registrables

Palabras que se usan en el logo/etiqueta pero **no se protegen**:
- "Barbería" → descriptivo del servicio
- "Botica Oficinal" → descriptivo del tipo de establecimiento
- "Hecho en México", "Natural", "Orgánico" → genéricos

**En el formulario IMPI:**
- Recuadro "Elementos no reservables": listar todas las palabras genéricas
- En la representación del signo: señalar con líneas discontinuas los elementos no protegidos

---

## 5. LOGOS Y REPRESENTACIÓN DEL SIGNO

### 5.1 Especificaciones técnicas

| Parámetro | Requerimiento |
|-----------|---------------|
| Formato | Etiqueta física adherida al formulario |
| Tamaño mínimo | 4 cm × 4 cm |
| Tamaño máximo | 10 cm × 10 cm |
| Color recomendado | Blanco y negro |
| Resolución | Clara, nítida, sin pixeles |

### 5.2 Ventaja del blanco y negro

> "Si lo registras en blanco y negro lo puedes usar con el color que quieras. Si lo registraste rosa, no lo puedes usar de otro color."

**Regla:** Registrar en B/N = flexibilidad total de colores. Registrar en color = limitado a ese color.

### 5.3 Tipos de signo

| Tipo | Descripción | Cuándo usar |
|------|-------------|-------------|
| **Marca nominativa** | Solo palabra(s) | Cuando la palabra es lo distintivo |
| **Marca mixta** | Palabra + figura | Cuando el conjunto palabra+logo es distintivo |
| **Marca figurativa** | Solo imagen | Cuando la imagen sola es distintiva |
| **Marca tridimensional** | Forma del producto/envase | Envases únicos reconocibles |

---

## 6. DOCUMENTACIÓN REQUERIDA

### 6.1 Del solicitante (persona física)

| Documento | Tipo | Notas |
|-----------|------|-------|
| Identificación oficial (INE) | Copia | Vigente |
| CURP | Copia | |
| RFC | Copia | |
| Comprobante de domicilio | Copia | Reciente (<3 meses) |

### 6.2 Del solicitante (persona moral)

| Documento | Tipo | Notas |
|-----------|------|-------|
| Acta constitutiva | Copia certificada | |
| RFC de la empresa | Copia | |
| Poder del representante legal | Original o copia certificada | |

### 6.3 Del mandatario (apoderado)

| Documento | Tipo | Notas |
|-----------|------|-------|
| Poder notarial o carta poder | Original o copia certificada | |
| Identificación del apoderado | Copia | |

### 6.4 Pagos

| Concepto | Tarifa aprox. (2026) |
|----------|---------------------|
| Solicitud de registro (por clase) | ~$2,500 MXN |
| Derechos de registro (si se concede, por clase) | ~$4,500 MXN |

**Fuente:** https://www.impi.gob.mx/tramites-y-servicios/tarifas

---

## 7. TIMELINE ESTIMADO

| Fase | Duración | Actividades |
|------|----------|-------------|
| Preparación | 3-5 días | Recopilar documentos, convertir logos, preparar poder |
| Llenado y revisión | 2-3 días | Llenar formularios, revisar con cliente, firmar |
| Presentación | 1 día | Pago, presentación en IMPI, acuse |
| Respuesta IMPI | 4 meses | Plazo de primera respuesta oficial |
| Requerimientos (si los hay) | 1-2 meses | Responder, corregir, presentar adicionales |
| Concesión y registro | 1-2 meses | Pagar derechos, obtener título |
| **Total estimado** | **6-8 meses** | Desde presentación hasta título |

---

## 8. CHECKLIST DE ENTREGA AL CLIENTE

- [ ] Investigación de Clasificación de Niza completa
- [ ] Clases identificadas con términos NCL específicos
- [ ] Formulario IMPI-00-001-A analizado campo por campo
- [ ] Guía de llenado personalizada para el cliente
- [ ] Estrategia de marca madre definida
- [ ] Elementos no registrables identificados
- [ ] Logos verificados (tamaño, color, formato)
- [ ] Lista de documentos pendientes del cliente
- [ ] Costos estimados desglosados
- [ ] Timeline con próximos pasos
- [ ] Fuentes oficiales citadas (WIPO NCLPub, IMPI)

---

## 9. ANTI-PATRONES A EVITAR

| Anti-patrón | Por qué es malo | Solución |
|-------------|----------------|----------|
| Registrar marca compuesta completa | Limita protección a esa combinación exacta | Registrar solo la palabra madre |
| Registrar en color | Limita uso a ese color específico | Registrar en blanco y negro |
| Describir productos con términos médicos | Puede forzar Clase 5 (farmacéuticos) | Usar términos cosméticos: "no medicinales" |
| Omitir elementos no registrables | IMPI puede objetar por descriptividad | Declarar explícitamente palabras genéricas |
| Presentar sin duplicado | IMPI rechaza | Siempre 2 ejemplares firmados |
| Mezclar medios de llenado | Formulario inválido | Un solo medio: todo digital o todo manuscrito |

---

## 10. RELACIÓN CON OTRAS SKILLS

| Skill | Rol | Cuándo usar juntas |
|-------|-----|-------------------|
| `willow-legal-complete` | Sistema legal completo (contratos, Kami, Onyx) | Cuando el registro de marca es parte de un matter legal más amplio |
| `ws-impi-trademark-registration` | Trámites de PI específicos | Cuando el foco es solo registro de marca/aviso/nombre comercial |
| `ws-brain-dump` | Capturar ideas sueltas del cliente | Al inicio del intake, antes de formalizar la solicitud |
| `project-continuity` | Seguimiento entre sesiones | Para trackear estado del trámite a lo largo de meses |

---

*Skill complementaria al ecosistema Willow Legal / WS Capital. No reemplaza asesoría legal profesional.*
