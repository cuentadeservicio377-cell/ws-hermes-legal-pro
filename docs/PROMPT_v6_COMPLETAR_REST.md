# PROMPT EJECUTABLE v6 — COMPLETAR REST API + FRONTEND

## Contexto
Hermes Legal Pro v3 DUAL funciona. Motor Kami genera PDFs y los sube a Drive. Falta:
1. Backend: PUT/DELETE para matters, endpoints faltantes (/plazo, /aprobacion)
2. Frontend: finanzas.js, integración completa de UI

## Tareas (ejecutar en orden)

### Tarea 1: Completar backend REST API

**Archivo**: `dashboard/backend/app.py`

Agregar estos endpoints que faltan:

```python
# PUT /matter/<id> — actualizar matter existente
@app.route('/matter/<id>', methods=['PUT'])
def update_matter(id):
    """Actualiza campos de un matter existente"""
    data = request.get_json()
    matters = load_matters()
    matter = next((m for m in matters if m['id'] == id), None)
    if not matter:
        return jsonify({'error': 'Matter no encontrado'}), 404
    
    # Campos permitidos para actualizar
    campos_permitidos = ['nombre', 'cliente', 'area', 'estado', 'responsable', 'descripcion']
    for campo in campos_permitidos:
        if campo in data:
            matter[campo] = data[campo]
    
    matter['updated_at'] = datetime.now().isoformat()
    save_matters(matters)
    return jsonify({'matter': matter, 'message': 'Matter actualizado'})

# DELETE /matter/<id> — eliminar matter
@app.route('/matter/<id>', methods=['DELETE'])
def delete_matter(id):
    """Elimina un matter y su carpeta local"""
    matters = load_matters()
    matter = next((m for m in matters if m['id'] == id), None)
    if not matter:
        return jsonify({'error': 'Matter no encontrado'}), 404
    
    # Eliminar carpeta local si existe
    matter_path = f"dashboard/datos/matters/{id}"
    if os.path.exists(matter_path):
        import shutil
        shutil.rmtree(matter_path)
    
    matters = [m for m in matters if m['id'] != id]
    save_matters(matters)
    return jsonify({'message': f'Matter {id} eliminado', 'id': id})

# GET /plazos — listar todos los plazos
@app.route('/plazos', methods=['GET'])
def list_plazos():
    """Lista todos los plazos activos"""
    plazos = load_plazos()
    return jsonify({'plazos': plazos, 'count': len(plazos)})

# POST /plazo — crear nuevo plazo
@app.route('/plazo', methods=['POST'])
def create_plazo():
    """Crea un nuevo plazo/vencimiento"""
    data = request.get_json()
    plazos = load_plazos()
    
    plazo = {
        'id': f"PLZ-{len(plazos)+1:03d}",
        'matter_id': data.get('matter_id'),
        'titulo': data.get('titulo', 'Plazo sin título'),
        'fecha_vencimiento': data.get('fecha_vencimiento'),
        'tipo': data.get('tipo', 'general'),
        'estado': 'pendiente',
        'notas': data.get('notas', ''),
        'created_at': datetime.now().isoformat()
    }
    plazos.append(plazo)
    save_plazos(plazos)
    
    # Crear evento en Calendar si hay credenciales
    try:
        from scripts.calendar_manager import CalendarManager
        cal = CalendarManager()
        event_link = cal.create_event(
            title=plazo['titulo'],
            date=plazo['fecha_vencimiento'],
            description=f"Plazo para matter {plazo['matter_id']}"
        )
        plazo['calendar_event_link'] = event_link
    except Exception as e:
        plazo['calendar_error'] = str(e)
    
    return jsonify({'plazo': plazo, 'message': 'Plazo creado'})

# GET /aprobaciones — listar aprobaciones pendientes
@app.route('/aprobaciones', methods=['GET'])
def list_aprobaciones():
    """Lista documentos pendientes de aprobación"""
    aprobaciones = load_aprobaciones()
    return jsonify({'aprobaciones': aprobaciones, 'count': len(aprobaciones)})

# POST /aprobacion/<id>/aprobar — aprobar documento
@app.route('/aprobacion/<id>/aprobar', methods=['POST'])
def aprobar_documento(id):
    """Aprueba un documento pendiente"""
    aprobaciones = load_aprobaciones()
    apr = next((a for a in aprobaciones if a['id'] == id), None)
    if not apr:
        return jsonify({'error': 'Aprobación no encontrada'}), 404
    
    apr['estado'] = 'aprobado'
    apr['fecha_aprobacion'] = datetime.now().isoformat()
    save_aprobaciones(aprobaciones)
    
    # Mover de pendientes a aprobados en Drive
    try:
        from scripts.drive_manager import DriveManager
        drive = DriveManager()
        drive.move_file(apr['drive_file_id'], apr['carpeta_aprobados_id'])
    except Exception as e:
        apr['drive_error'] = str(e)
    
    return jsonify({'aprobacion': apr, 'message': 'Documento aprobado'})
```

**Nota**: Si las funciones `load_plazos()`, `save_plazos()`, `load_aprobaciones()`, `save_aprobaciones()` no existen, créalas siguiendo el patrón de `load_matters()`/`save_matters()`.

### Tarea 2: Crear finanzas.js

**Archivo nuevo**: `dashboard/frontend/js/finanzas.js`

```javascript
// finanzas.js — Módulo de finanzas para Willow Legal Dashboard

const FinanzasAPI = {
    baseUrl: '/api',
    
    async cargarResumen() {
        const res = await fetch(`${this.baseUrl}/finanzas`);
        return res.json();
    },
    
    async cargarTransacciones(matterId = null) {
        const url = matterId 
            ? `${this.baseUrl}/finanzas?matter_id=${matterId}`
            : `${this.baseUrl}/finanzas`;
        const res = await fetch(url);
        return res.json();
    },
    
    async registrarIngreso(data) {
        const res = await fetch(`${this.baseUrl}/finanza`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                ...data,
                tipo: 'ingreso'
            })
        });
        return res.json();
    },
    
    async registrarEgreso(data) {
        const res = await fetch(`${this.baseUrl}/finanza`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                ...data,
                tipo: 'egreso'
            })
        });
        return res.json();
    }
};

const FinanzasUI = {
    async renderResumen() {
        const container = document.getElementById('finanzas-resumen');
        if (!container) return;
        
        try {
            const data = await FinanzasAPI.cargarResumen();
            container.innerHTML = `
                <div class="finanzas-cards">
                    <div class="card ingresos">
                        <h4>Ingresos</h4>
                        <p class="monto">$${data.ingresos?.toLocaleString() || 0}</p>
                    </div>
                    <div class="card egresos">
                        <h4>Egresos</h4>
                        <p class="monto">$${data.egresos?.toLocaleString() || 0}</p>
                    </div>
                    <div class="card balance">
                        <h4>Balance</h4>
                        <p class="monto ${data.balance >= 0 ? 'positivo' : 'negativo'}">
                            $${data.balance?.toLocaleString() || 0}
                        </p>
                    </div>
                </div>
            `;
        } catch (e) {
            container.innerHTML = `<p class="error">Error cargando finanzas: ${e.message}</p>`;
        }
    },
    
    async renderTabla(matterId = null) {
        const container = document.getElementById('finanzas-tabla');
        if (!container) return;
        
        try {
            const data = await FinanzasAPI.cargarTransacciones(matterId);
            const transacciones = data.transacciones || [];
            
            container.innerHTML = `
                <table class="finanzas-table">
                    <thead>
                        <tr>
                            <th>Fecha</th>
                            <th>Concepto</th>
                            <th>Matter</th>
                            <th>Tipo</th>
                            <th>Monto</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${transacciones.map(t => `
                            <tr class="${t.tipo}">
                                <td>${t.fecha || '-'}</td>
                                <td>${t.concepto}</td>
                                <td>${t.matter_id || '-'}</td>
                                <td><span class="badge ${t.tipo}">${t.tipo}</span></td>
                                <td class="monto ${t.tipo}">$${t.monto?.toLocaleString() || 0}</td>
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
            `;
        } catch (e) {
            container.innerHTML = `<p class="error">Error cargando transacciones: ${e.message}</p>`;
        }
    }
};

// Exportar para uso global
window.FinanzasAPI = FinanzasAPI;
window.FinanzasUI = FinanzasUI;
```

### Tarea 3: Actualizar index.html para incluir finanzas.js

En `dashboard/frontend/index.html`, agregar:
```html
<script src="js/finanzas.js"></script>
```

Después de los demás `<script>` tags.

### Tarea 4: Verificar CORS y conectividad

Asegurar que `app.py` tenga:
```python
from flask_cors import CORS
CORS(app)
```

### Tarea 5: Test de integridad

Ejecutar en terminal:
```bash
# 1. Verificar backend levanta
python3 dashboard/backend/app.py &
sleep 3
curl -s http://localhost:5000/matters | head -c 200

# 2. Test PUT matter
curl -X PUT http://localhost:5000/matter/WIL-005 \
  -H "Content-Type: application/json" \
  -d '{"estado": "activo", "responsable": "Pablo"}' | python3 -m json.tool

# 3. Test DELETE matter (crear uno de prueba primero)
# 4. Test plazos
curl -s http://localhost:5000/plazos | python3 -m json.tool

# 5. Verificar finanzas.js carga en navegador (abrir index.html)
```

## Tests de verificación

- [ ] PUT /matter/WIL-005 actualiza estado y responsable
- [ ] DELETE /matter/WIL-TEST elimina matter y carpeta local
- [ ] GET /plazos retorna lista (vacía o con datos)
- [ ] POST /plazo crea plazo con evento Calendar
- [ ] GET /aprobaciones retorna lista
- [ ] POST /aprobacion/XXX/aprobar cambia estado
- [ ] finanzas.js se carga sin errores en consola
- [ ] Tabla de finanzas renderiza con datos reales

## Git

```bash
git add -A
git commit -m "v6: REST API completa (PUT/DELETE matters, plazos, aprobaciones) + finanzas.js"
git push origin master
```

## Reportar resultado

Ejecutar `git log --oneline -3` y pegar output.
