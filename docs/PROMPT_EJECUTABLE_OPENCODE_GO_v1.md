# PROMPT EJECUTABLE — OpenCode Go
## Willow Legal Pro v2.0 — Implementación Completa
## Fecha: 2026-05-04
## Contexto: Este prompt contiene TODA la información necesaria. No requiere acceso a documentación externa.

---

## TU IDENTIDAD

Eres un agente de implementación de software. Tu trabajo es:
1. Leer este prompt COMPLETO antes de empezar
2. Seguir las instrucciones paso a paso
3. Escribir código funcional, no pseudocódigo
4. Verificar que cada paso funciona antes de continuar
5. Reportar progreso y bloqueos

---

## CONTEXTO DEL PROYECTO

### Repositorio
- **URL:** `https://github.com/cuentadeservicio377-cell/ws-hermes-legal-pro`
- **Cuenta GitHub:** `cuentadeservicio377-cell`
- **Email:** `cuentadeservicio377@gmail.com`
- **Branch de trabajo:** `master` (para este prompt, luego crearemos `v2.0-dev`)

### Estado Actual del Repo
El repositorio tiene un sistema legal con:
- Dashboard FastAPI en `dashboard/backend/app.py` (~1021 líneas)
- Motor Kami v3 en `motor_kami/motor_kami.py` (~528 líneas)
- 23 templates JSON en `motor_kami/templates/`
- Frontend JS en `dashboard/frontend/`
- Scripts de Google Workspace en `scripts/`
- Integración Hermes en `hermes_integration/`

### Problemas Críticos a Resolver
1. **IDs inconsistentes:** Dashboard usa `LEG-001`, Hermes usa `WIL-001`, standalone usa `PRAG-XXX`
2. **Rutas de datos dispersas:** 3 ubicaciones diferentes para los mismos JSON
3. **Datos hardcodeados:** "We Law S.C." quemado en el código
4. **Motor Kami no lee templates reales:** Genera cláusulas genéricas en lugar de leer los JSON
5. **Frontend llama endpoints inexistentes:** `GET /api/tasks`, `POST /api/export-sheets`, etc.
6. **Finanzas incompletas:** No hay modelo, endpoints ni datos reales

---

## ARQUITECTURA OBJETIVO

```
ws-hermes-legal-pro/
├── config/
│   ├── config.yaml              ← NUEVO: Configuración unificada
│   └── config_loader.py         ← NUEVO: Carga y validación
├── core/
│   ├── __init__.py
│   ├── datastore.py             ← NUEVO: Capa de persistencia JSON
│   ├── id_generator.py          ← NUEVO: Generación centralizada de IDs
│   └── migrations.py            ← NUEVO: Migraciones de schema
├── dashboard/
│   ├── backend/
│   │   └── app.py               ← MODIFICAR: Usar core.*, endpoints completos
│   └── frontend/
│       ├── index.html           ← MODIFICAR: Responsive, completo
│       ├── css/
│       │   └── design_system.css  ← NUEVO: Sistema de diseño
│       └── js/
│           ├── api.js             ← MODIFICAR: Todos los endpoints
│           └── app.js             ← MODIFICAR: Usar api.js correctamente
├── motor_kami/
│   ├── motor_kami.py            ← MODIFICAR: Leer templates reales
│   ├── template_engine.py       ← NUEVO: Engine de templates
│   ├── variable_resolver.py     ← NUEVO: Resolución de {{variables}}
│   └── templates/
│       └── prestacion_servicios.json  ← MODIFICAR: Texto legal real
├── scripts/
│   ├── backup.py                ← NUEVO: Backup automático
│   └── setup_cron.py            ← NUEVO: Configurar cron
├── tests/
│   ├── conftest.py              ← NUEVO: Fixtures pytest
│   ├── test_api.py              ← NUEVO: Tests API
│   ├── test_datastore.py        ← NUEVO: Tests datastore
│   └── test_motor_kami.py       ← NUEVO: Tests motor
├── requirements.txt             ← NUEVO: Dependencias
└── requirements-dev.txt         ← NUEVO: Dependencias dev
```

---

## PASO 0: PREPARACIÓN (Ejecutar primero)

```bash
# 1. Clonar repo si no existe
if [ ! -d "ws-hermes-legal-pro" ]; then
    git clone https://github.com/cuentadeservicio377-cell/ws-hermes-legal-pro.git
fi

cd ws-hermes-legal-pro

# 2. Crear branch de trabajo
git checkout -b v2.0-dev

# 3. Verificar estructura actual
ls -la
git log --oneline -5

# 4. Instalar dependencias base
pip install fastapi uvicorn pydantic weasyprint pyyaml openpyxl pytest
```

---

## PASO 1: CONFIGURACIÓN UNIFICADA

### 1.1 Crear `config/config.yaml`

Escribe este archivo EXACTAMENTE:

```yaml
version: "2.0"
despacho:
  nombre: "We Law S.C."
  rfc: "WEL123456ABC"
  representante: "Lic. Pablo Meneses"
  email: "contacto@welaw.mx"
  domicilio: "Ciudad de México"
  telefono: ""

datastore:
  type: "json"
  path: "~/.willowlegal/data/"
  backup_dir: "~/.willowlegal/backups/"
  backup_interval_hours: 24

ids:
  matter_prefix: "WIL"
  document_prefix: "DOC"
  padding: 3

motor_kami:
  templates_dir: "motor_kami/templates/"
  output_dir: "~/.willowlegal/output/"
  css_theme: "kami_v2"

google_workspace:
  enabled: false
  credentials_path: "~/.willowlegal/config/client_secret.json"
  token_path: "~/.willowlegal/config/token.json"
  base_folder: "WillowLegal"

auth:
  enabled: false
  type: "api_key"
  api_key_header: "X-API-Key"

notifications:
  telegram:
    enabled: false
    bot_token_env: "TELEGRAM_BOT_TOKEN"
    chat_id_env: "TELEGRAM_HOME_CHAT_ID"
```

### 1.2 Crear `config/config_loader.py`

```python
#!/usr/bin/env python3
"""ConfigLoader — Carga y validación de configuración centralizada."""
import yaml
import os
from pathlib import Path
from typing import Dict, Any
from dataclasses import dataclass

@dataclass
class DespachoConfig:
    nombre: str
    rfc: str
    representante: str
    email: str
    domicilio: str
    telefono: str = ""

@dataclass
class DatastoreConfig:
    type: str = "json"
    path: Path = Path("~/.willowlegal/data").expanduser()
    backup_dir: Path = Path("~/.willowlegal/backups").expanduser()
    backup_interval_hours: int = 24

@dataclass
class Config:
    version: str
    despacho: DespachoConfig
    datastore: DatastoreConfig
    ids: Dict[str, Any]
    motor_kami: Dict[str, Any]
    google_workspace: Dict[str, Any]
    auth: Dict[str, Any]
    notifications: Dict[str, Any]
    
    @classmethod
    def load(cls, path: str = "config/config.yaml") -> "Config":
        config_path = Path(path)
        if not config_path.exists():
            raise FileNotFoundError(f"Config no encontrado: {path}")
        
        with open(config_path, 'r', encoding='utf-8') as f:
            raw = yaml.safe_load(f)
        
        if raw.get("version") != "2.0":
            raise ValueError(f"Versión no soportada: {raw.get('version')}")
        
        # Expandir paths
        raw["datastore"]["path"] = Path(raw["datastore"]["path"]).expanduser()
        raw["datastore"]["backup_dir"] = Path(raw["datastore"]["backup_dir"]).expanduser()
        raw["motor_kami"]["output_dir"] = Path(raw["motor_kami"]["output_dir"]).expanduser()
        
        # Crear directorios
        raw["datastore"]["path"].mkdir(parents=True, exist_ok=True)
        raw["datastore"]["backup_dir"].mkdir(parents=True, exist_ok=True)
        raw["motor_kami"]["output_dir"].mkdir(parents=True, exist_ok=True)
        
        return cls(
            version=raw["version"],
            despacho=DespachoConfig(**raw["despacho"]),
            datastore=DatastoreConfig(**raw["datastore"]),
            ids=raw["ids"],
            motor_kami=raw["motor_kami"],
            google_workspace=raw["google_workspace"],
            auth=raw["auth"],
            notifications=raw["notifications"]
        )
    
    def get_despacho_data(self) -> Dict[str, str]:
        return {
            "nombre": self.despacho.nombre,
            "rfc": self.despacho.rfc,
            "representante": self.despacho.representante,
            "email": self.despacho.email,
            "domicilio": self.despacho.domicilio,
            "telefono": self.despacho.telefono
        }
```

### 1.3 Verificar

```bash
python3 -c "from config.config_loader import Config; c = Config.load(); print('Config OK:', c.despacho.nombre)"
```

---

## PASO 2: DATASTORE UNIFICADO

### 2.1 Crear directorio `core/`

```bash
mkdir -p core
```

### 2.2 Crear `core/__init__.py`

```python
"""Core package for Willow Legal Pro."""
```

### 2.3 Crear `core/datastore.py`

```python
#!/usr/bin/env python3
"""Datastore — Capa de abstracción para persistencia JSON."""
import json
import shutil
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime

class JSONDatastore:
    """JSON storage with automatic backup."""
    
    def __init__(self, base_path: Path, backup_dir: Path):
        self.base_path = Path(base_path).expanduser()
        self.backup_dir = Path(backup_dir).expanduser()
        self.base_path.mkdir(parents=True, exist_ok=True)
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        
        self.files = {
            "matters": self.base_path / "matters.json",
            "documentos": self.base_path / "documentos.json",
            "reuniones": self.base_path / "reuniones.json",
            "alertas": self.base_path / "alertas.json",
            "finanzas": self.base_path / "finanzas.json",
            "plazos": self.base_path / "plazos.json",
            "aprobaciones": self.base_path / "aprobaciones.json",
            "usuarios": self.base_path / "usuarios.json",
            "session": self.base_path / "session.json"
        }
        
        for name, path in self.files.items():
            if not path.exists():
                self._write_json(path, self._default_data(name))
    
    def _default_data(self, name: str) -> Any:
        defaults = {
            "matters": [],
            "documentos": [],
            "reuniones": [],
            "alertas": [],
            "finanzas": {"movimientos": [], "resumen": {}},
            "plazos": [],
            "aprobaciones": [],
            "usuarios": [],
            "session": {"matter_active": None}
        }
        return defaults.get(name, [])
    
    def _read_json(self, path: Path) -> Any:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def _write_json(self, path: Path, data: Any):
        if path.exists():
            backup_name = f"{path.stem}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            shutil.copy(path, self.backup_dir / backup_name)
        
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def get(self, collection: str) -> List[Dict]:
        path = self.files.get(collection)
        if not path:
            raise ValueError(f"Colección desconocida: {collection}")
        return self._read_json(path)
    
    def set(self, collection: str, data: List[Dict]):
        path = self.files.get(collection)
        if not path:
            raise ValueError(f"Colección desconocida: {collection}")
        self._write_json(path, data)
    
    def find_one(self, collection: str, **filters) -> Optional[Dict]:
        items = self.get(collection)
        for item in items:
            if all(item.get(k) == v for k, v in filters.items()):
                return item
        return None
    
    def find_many(self, collection: str, **filters) -> List[Dict]:
        items = self.get(collection)
        return [item for item in items if all(item.get(k) == v for k, v in filters.items())]
    
    def insert(self, collection: str, item: Dict) -> Dict:
        items = self.get(collection)
        items.append(item)
        self.set(collection, items)
        return item
    
    def update(self, collection: str, id_field: str, id_value: str, updates: Dict) -> Optional[Dict]:
        items = self.get(collection)
        for item in items:
            if item.get(id_field) == id_value:
                item.update(updates)
                self.set(collection, items)
                return item
        return None
    
    def delete(self, collection: str, id_field: str, id_value: str) -> bool:
        items = self.get(collection)
        original_len = len(items)
        items = [item for item in items if item.get(id_field) != id_value]
        if len(items) < original_len:
            self.set(collection, items)
            return True
        return False
    
    def backup(self) -> str:
        backup_name = f"willow_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        backup_path = self.backup_dir / backup_name
        backup_path.mkdir(parents=True, exist_ok=True)
        
        for name, path in self.files.items():
            if path.exists():
                shutil.copy(path, backup_path / f"{name}.json")
        
        return str(backup_path)
```

### 2.4 Crear `core/id_generator.py`

```python
#!/usr/bin/env python3
"""IDGenerator — Generación centralizada de IDs."""
from typing import Optional

class IDGenerator:
    def __init__(self, datastore, config: dict):
        self.ds = datastore
        self.prefix = config.get("matter_prefix", "WIL")
        self.doc_prefix = config.get("document_prefix", "DOC")
        self.padding = config.get("padding", 3)
    
    def generate_matter_id(self) -> str:
        matters = self.ds.get("matters")
        max_num = 0
        for m in matters:
            matter_id = m.get("id", "")
            if matter_id.startswith(self.prefix + "-"):
                try:
                    num = int(matter_id.split("-")[1])
                    max_num = max(max_num, num)
                except (ValueError, IndexError):
                    pass
        return f"{self.prefix}-{max_num + 1:0{self.padding}d}"
    
    def generate_document_id(self) -> str:
        documentos = self.ds.get("documentos")
        return f"{self.doc_prefix}-{len(documentos) + 1:04d}"
    
    def generate_reunion_id(self) -> str:
        reuniones = self.ds.get("reuniones")
        return f"REU-{len(reuniones) + 1:04d}"
    
    def generate_plazo_id(self) -> str:
        plazos = self.ds.get("plazos")
        return f"PLZ-{len(plazos) + 1:04d}"
    
    def generate_alerta_id(self) -> str:
        alertas = self.ds.get("alertas")
        return f"ALR-{len(alertas) + 1:04d}"
```

### 2.5 Verificar

```bash
python3 -c "
from core.datastore import JSONDatastore
from core.id_generator import IDGenerator
from pathlib import Path
import tempfile

with tempfile.TemporaryDirectory() as tmpdir:
    ds = JSONDatastore(Path(tmpdir), Path(tmpdir) / 'backups')
    id_gen = IDGenerator(ds, {'matter_prefix': 'WIL', 'document_prefix': 'DOC', 'padding': 3})
    print('Matter ID:', id_gen.generate_matter_id())
    print('Doc ID:', id_gen.generate_document_id())
    print('Datastore OK')
"
```

---

## PASO 3: MODIFICAR BACKEND PARA USAR CORE

### 3.1 Hacer backup del backend actual

```bash
cp dashboard/backend/app.py dashboard/backend/app.py.v1.backup
```

### 3.2 Modificar `dashboard/backend/app.py`

Las modificaciones clave son:

**A. Agregar imports al inicio:**
```python
import sys
from pathlib import Path

# Add parent to path for core imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from config.config_loader import Config
from core.datastore import JSONDatastore
from core.id_generator import IDGenerator
```

**B. Reemplazar paths hardcodeados:**
```python
# REEMPLAZAR:
# BASE_DIR = Path(__file__).parent.parent
# DATA_DIR = BASE_DIR / "datos"
# MATTERS_FILE = DATA_DIR / "matters.json"
# ... etc

# POR:
config = Config.load()
datastore = JSONDatastore(config.datastore.path, config.datastore.backup_dir)
id_generator = IDGenerator(datastore, config.ids)
```

**C. Reemplazar funciones load_json/save_json:**
```python
# REEMPLAZAR las funciones load_json y save_json actuales por:

def load_json(collection: str):
    return datastore.get(collection)

def save_json(collection: str, data):
    datastore.set(collection, data)
```

**D. Modificar crear matter para usar IDGenerator:**
```python
# REEMPLAZAR:
# nuevo_id = f"LEG-{len(matters)+1:03d}"

# POR:
nuevo_id = id_generator.generate_matter_id()
```

**E. Modificar health check:**
```python
@app.get("/api/health")
def health():
    motor_ok = (Path(config.motor_kami['templates_dir']) / "index.json").exists()
    templates_count = len(list(Path(config.motor_kami['templates_dir']).glob("*.json")))
    return {
        "status": "ok",
        "producto": "Hermes Legal Pro",
        "version": "2.0.0",
        "motor_kami": "ok" if motor_ok else "no_encontrado",
        "templates_disponibles": templates_count,
        "datastore": str(config.datastore.path)
    }
```

### 3.3 Verificar backend

```bash
cd dashboard/backend
python3 -c "from app import app; print('Backend imports OK')"
```

---

## PASO 4: MOTOR KAMI v4 — LEER TEMPLATES REALES

### 4.1 Crear `motor_kami/template_engine.py`

```python
#!/usr/bin/env python3
"""template_engine.py — Motor de templates JSON."""
import json
import re
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

@dataclass
class Template:
    key: str
    label: str
    area: str
    materia: str
    metadata: Dict[str, Any]
    recommended_blocks: List[str]
    document_data_template: Dict[str, Any]
    required_variables: List[str]
    
    @classmethod
    def load(cls, templates_dir: Path, key: str) -> "Template":
        template_path = templates_dir / f"{key}.json"
        if not template_path.exists():
            raise FileNotFoundError(f"Template no encontrado: {key}")
        
        with open(template_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        return cls(
            key=key,
            label=data["metadata"]["label"],
            area=data["metadata"]["area"],
            materia=data["metadata"]["materia"],
            metadata=data["metadata"],
            recommended_blocks=data.get("recommended_blocks", []),
            document_data_template=data.get("document_data_template", {}),
            required_variables=data.get("required_variables", [])
        )
    
    def validate_variables(self, provided: Dict[str, Any]) -> List[str]:
        missing = []
        for var in self.required_variables:
            if var not in provided or not provided[var]:
                missing.append(var)
        return missing
```

### 4.2 Crear `motor_kami/variable_resolver.py`

```python
#!/usr/bin/env python3
"""variable_resolver.py — Resuelve variables {{placeholder}}."""
import re
from datetime import datetime
from typing import Dict, Any

class VariableResolver:
    def __init__(self, despacho_data: Dict[str, str], matter_data: Dict[str, Any]):
        self.despacho = despacho_data
        self.matter = matter_data
        self.built_ins = {
            "fecha_actual": datetime.now().strftime("%d de %B de %Y"),
            "fecha_actual_iso": datetime.now().isoformat(),
            "anio_actual": str(datetime.now().year),
            "matter_id": matter_data.get("id", ""),
        }
    
    def resolve(self, text: str) -> str:
        pattern = r'\{\{(\w+(?:\.\w+)*)\}\}'
        
        def replace(match):
            var_path = match.group(1)
            value = self._get_value(var_path)
            return str(value) if value is not None else match.group(0)
        
        return re.sub(pattern, replace, text)
    
    def _get_value(self, path: str) -> Any:
        if path in self.built_ins:
            return self.built_ins[path]
        
        # Check despacho (flat)
        if path in self.despacho:
            return self.despacho[path]
        
        # Check matter (nested)
        parts = path.split(".")
        value = self.matter
        for part in parts:
            if isinstance(value, dict) and part in value:
                value = value[part]
            else:
                return None
        return value
    
    def resolve_dict(self, data: Dict[str, Any]) -> Dict[str, Any]:
        result = {}
        for key, value in data.items():
            if isinstance(value, str):
                result[key] = self.resolve(value)
            elif isinstance(value, dict):
                result[key] = self.resolve_dict(value)
            elif isinstance(value, list):
                result[key] = [
                    self.resolve(item) if isinstance(item, str) else
                    self.resolve_dict(item) if isinstance(item, dict) else item
                    for item in value
                ]
            else:
                result[key] = value
        return result
```

### 4.3 Modificar `motor_kami/motor_kami.py`

**A. Agregar imports:**
```python
from template_engine import Template
from variable_resolver import VariableResolver
```

**B. Modificar función principal de generación:**

Busca la función que genera documentos y reemplázala por:

```python
def generar_documento_real(
    template_key: str,
    matter_data: Dict[str, Any],
    output_path: Path,
    extra_vars: Optional[Dict[str, Any]] = None,
    despacho_data: Optional[Dict[str, str]] = None
) -> Dict[str, Any]:
    """Genera documento usando template real."""
    
    # 1. Cargar template
    try:
        template = Template.load(TEMPLATES_DIR, template_key)
    except FileNotFoundError as e:
        return {"success": False, "error": str(e)}
    
    # 2. Preparar variables
    all_vars = {**(extra_vars or {}), **matter_data}
    if despacho_data:
        all_vars["prestador"] = despacho_data
    
    # 3. Validar
    missing = template.validate_variables(all_vars)
    if missing:
        return {
            "success": False,
            "error": f"Variables faltantes: {', '.join(missing)}",
            "missing_variables": missing
        }
    
    # 4. Resolver variables en template
    resolver = VariableResolver(despacho_data or {}, matter_data)
    doc_data = resolver.resolve_dict(template.document_data_template)
    
    # 5. Generar HTML usando blocks.py
    from blocks import generar_desde_bloques
    
    blocks = []
    for block_type in template.recommended_blocks:
        if block_type == "cover_page":
            blocks.append({
                "type": "cover_page",
                "data": {
                    "titulo": doc_data.get("titulo", "Documento Legal"),
                    "marca": doc_data.get("prestador", {}).get("nombre", ""),
                    "numero": doc_data.get("numero_contrato", "")
                }
            })
        elif block_type == "parties_block":
            blocks.append({
                "type": "parties_block",
                "data": {
                    "prestador": doc_data.get("prestador", {}),
                    "cliente": doc_data.get("cliente", {})
                }
            })
        elif block_type == "clause_section":
            for clausula in doc_data.get("clausulas", []):
                blocks.append({"type": "clause_section", "data": clausula})
        elif block_type == "signature_block":
            blocks.append({
                "type": "signature_block",
                "data": doc_data.get("signature_block", {})
            })
    
    html_content = generar_desde_bloques(blocks, doc_data)
    
    # 6. Generar PDF
    try:
        HTML(string=html_content).write_pdf(str(output_path))
        return {
            "success": True,
            "file_path": str(output_path),
            "file_size": output_path.stat().st_size,
            "template_used": template_key
        }
    except Exception as e:
        return {"success": False, "error": f"Error generando PDF: {str(e)}"}
```

### 4.4 Verificar motor

```bash
cd motor_kami
python3 -c "
from template_engine import Template
from pathlib import Path
t = Template.load(Path('templates'), 'nda')
print('Template OK:', t.label)
print('Blocks:', t.recommended_blocks)
"
```

---

## PASO 5: COMPLETAR ENDPOINTS FALTANTES

### 5.1 Agregar a `dashboard/backend/app.py`

**Endpoint: Finanzas completo**
```python
class FinanzaInput(BaseModel):
    matter_id: str
    tipo: str  # ingreso | egreso | anticipo | honorario
    monto: float
    concepto: str
    fecha: Optional[str] = None
    metodo_pago: Optional[str] = "transferencia"
    notas: Optional[str] = ""

@app.get("/api/finanzas")
def list_finanzas(matter_id: Optional[str] = None):
    finanzas = load_json("finanzas")
    movimientos = finanzas.get("movimientos", [])
    
    if matter_id:
        movimientos = [m for m in movimientos if m.get("matter_id") == matter_id]
    
    total_ingresos = sum(m["monto"] for m in movimientos if m["tipo"] in ["ingreso", "anticipo", "pago"])
    total_egresos = sum(m["monto"] for m in movimientos if m["tipo"] in ["egreso", "gasto"])
    
    return {
        "status": "ok",
        "movimientos": movimientos[::-1],
        "resumen": {
            "total_ingresos": total_ingresos,
            "total_egresos": total_egresos,
            "balance": total_ingresos - total_egresos,
            "count": len(movimientos)
        }
    }

@app.post("/api/finanzas")
def create_finanza(data: FinanzaInput):
    finanzas = load_json("finanzas")
    movimientos = finanzas.get("movimientos", [])
    
    movimiento = {
        "id": f"FIN-{len(movimientos)+1:04d}",
        "matter_id": data.matter_id,
        "tipo": data.tipo,
        "monto": data.monto,
        "concepto": data.concepto,
        "fecha": data.fecha or datetime.now().isoformat(),
        "metodo_pago": data.metodo_pago,
        "notas": data.notas,
        "creado": datetime.now().isoformat()
    }
    
    movimientos.append(movimiento)
    finanzas["movimientos"] = movimientos
    save_json("finanzas", finanzas)
    
    return {"status": "ok", "movimiento": movimiento}
```

**Endpoint: Drive Link**
```python
@app.get("/api/drive-link/{matter_id}")
def get_drive_link(matter_id: str):
    matters = load_json("matters")
    matter = next((m for m in matters if m["id"] == matter_id), None)
    if not matter:
        raise HTTPException(404, "Matter no encontrado")
    
    return {
        "matter_id": matter_id,
        "drive_folder_id": matter.get("drive_folder_id"),
        "drive_link": matter.get("drive_link")
    }
```

**Endpoint: Check Plazos**
```python
@app.post("/api/check-plazos")
def trigger_check_plazos():
    try:
        import subprocess
        result = subprocess.run(
            [sys.executable, "scripts/check_plazos.py", "--notify"],
            capture_output=True,
            text=True,
            cwd=str(Path(__file__).parent.parent.parent)
        )
        return {"status": "ok", "output": result.stdout}
    except Exception as e:
        raise HTTPException(500, str(e))
```

### 5.2 Verificar endpoints

```bash
cd dashboard/backend
python3 -c "
from app import app
from fastapi.testclient import TestClient
client = TestClient(app)

# Test health
r = client.get('/api/health')
print('Health:', r.status_code, r.json())

# Test create matter
r = client.post('/api/matters', json={
    'cliente': 'Test Client',
    'area_practica': 'Mercantil',
    'descripcion': 'Test',
    'prioridad': 'media'
})
print('Create matter:', r.status_code, r.json())

# Test finanzas
r = client.get('/api/finanzas')
print('Finanzas:', r.status_code, r.json())
"
```

---

## PASO 6: FRONTEND RESPONSIVE

### 6.1 Crear `dashboard/frontend/css/design_system.css`

Escribe un CSS completo con:
- CSS variables para colores, tipografía, spacing
- Layout mobile-first con sidebar colapsable
- Cards grid responsive
- Buttons, forms, tables, badges, modals, toasts
- Media queries: mobile (<640px), tablet (640-1024px), desktop (>1024px)

### 6.2 Modificar `dashboard/frontend/index.html`

- Agregar viewport meta tag
- Agregar fonts (Inter, Source Serif 4)
- Hacer sidebar colapsable con toggle
- Usar CSS variables del design system

### 6.3 Modificar `dashboard/frontend/js/api.js`

Asegurar que todos los métodos usen el baseUrl correcto:
```javascript
const API = {
  baseUrl: 'http://localhost:8082/api',
  
  async get(endpoint) {
    const res = await fetch(`${this.baseUrl}${endpoint}`);
    if (!res.ok) throw new Error(`Error ${res.status}`);
    return res.json();
  },
  
  async post(endpoint, data) {
    const res = await fetch(`${this.baseUrl}${endpoint}`, {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify(data)
    });
    if (!res.ok) throw new Error(`Error ${res.status}`);
    return res.json();
  },
  
  // Matters
  getMatters() { return this.get('/matters'); },
  createMatter(data) { return this.post('/matters', data); },
  
  // Documentos
  getTemplates() { return this.get('/templates'); },
  generateDocument(matterId, templateId) {
    return this.post(`/matter/${matterId}/generar-documento`, {template_key: templateId});
  },
  
  // Finanzas
  getFinanzas() { return this.get('/finanzas'); },
  createFinanza(data) { return this.post('/finanzas', data); },
  
  // Plazos
  getPlazos() { return this.get('/plazos'); },
  
  // Alertas
  getAlertas() { return this.get('/alertas'); },
  checkPlazos() { return this.post('/check-plazos'); },
  
  // Google Workspace
  getDriveLink(matterId) { return this.get(`/drive-link/${matterId}`); },
  exportSheets() { return this.post('/export-sheets'); },
  
  // Tareas
  getTasks() { return this.get('/tasks'); },
  createTask(data) { return this.post('/task', data); },
  
  // Calendario
  getCalendarEvents() { return this.get('/calendar-events'); }
};

window.API = API;
```

---

## PASO 7: TESTS

### 7.1 Crear `tests/conftest.py`

```python
import pytest
import tempfile
import shutil
from pathlib import Path
from fastapi.testclient import TestClient
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from config.config_loader import Config
from core.datastore import JSONDatastore

@pytest.fixture
def temp_data_dir():
    temp_dir = Path(tempfile.mkdtemp())
    yield temp_dir
    shutil.rmtree(temp_dir)

@pytest.fixture
def test_datastore(temp_data_dir):
    return JSONDatastore(temp_data_dir, temp_data_dir / "backups")

@pytest.fixture
def client(temp_data_dir):
    import os
    os.environ["WILLOW_DATA_DIR"] = str(temp_data_dir)
    from dashboard.backend.app import app
    return TestClient(app)
```

### 7.2 Crear `tests/test_api.py`

```python
def test_health_check(client):
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"

def test_create_matter(client):
    response = client.post("/api/matters", json={
        "cliente": "Test Client",
        "area_practica": "Mercantil",
        "descripcion": "Test",
        "prioridad": "media"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["id"].startswith("WIL-")
    assert data["cliente"] == "Test Client"

def test_finanzas(client):
    # Create matter first
    client.post("/api/matters", json={
        "cliente": "Test",
        "area_practica": "Mercantil",
        "prioridad": "media"
    })
    
    # Create finance entry
    response = client.post("/api/finanzas", json={
        "matter_id": "WIL-001",
        "tipo": "ingreso",
        "monto": 50000,
        "concepto": "Test payment"
    })
    assert response.status_code == 200
    
    # List finances
    response = client.get("/api/finanzas")
    assert response.status_code == 200
    data = response.json()
    assert data["resumen"]["total_ingresos"] == 50000
```

### 7.3 Ejecutar tests

```bash
pytest tests/ -v
```

---

## PASO 8: BACKUP Y UTILIDADES

### 8.1 Crear `scripts/backup.py`

```python
#!/usr/bin/env python3
"""backup.py — Sistema de backup."""
import argparse
from pathlib import Path
from datetime import datetime
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))
from config.config_loader import Config
from core.datastore import JSONDatastore

def backup_manual():
    config = Config.load()
    ds = JSONDatastore(config.datastore.path, config.datastore.backup_dir)
    backup_path = ds.backup()
    print(f"✅ Backup creado: {backup_path}")
    return backup_path

def list_backups():
    config = Config.load()
    backup_dir = Path(config.datastore.backup_dir)
    if not backup_dir.exists():
        print("❌ No hay backups")
        return
    
    backups = sorted(backup_dir.iterdir(), key=lambda p: p.stat().st_mtime, reverse=True)
    print(f"\n📦 BACKUPS ({len(backups)}):")
    for b in backups[:10]:
        mtime = datetime.fromtimestamp(b.stat().st_mtime)
        print(f"  • {b.name} — {mtime.strftime('%Y-%m-%d %H:%M')}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--backup", action="store_true")
    parser.add_argument("--list", action="store_true")
    args = parser.parse_args()
    
    if args.backup:
        backup_manual()
    elif args.list:
        list_backups()
    else:
        parser.print_help()
```

### 8.2 Crear `requirements.txt`

```
fastapi>=0.104.0
uvicorn[standard]>=0.24.0
pydantic>=2.5.0
PyYAML>=6.0.1
openpyxl>=3.1.2
WeasyPrint>=60.0
requests>=2.31.0
python-dateutil>=2.8.2
```

### 8.3 Crear `requirements-dev.txt`

```
pytest>=7.4.3
pytest-asyncio>=0.21.1
httpx>=0.25.2
black>=23.11.0
flake8>=6.1.0
```

---

## PASO 9: COMMIT Y PUSH

```bash
# Verificar cambios
git status

# Agregar todo
git add -A

# Commit
git commit -m "v2.0: Fundamentos — Config unificada, Datastore, IDs, Motor Kami real

- config.yaml + config_loader.py: Configuración centralizada
- core/datastore.py: Persistencia JSON unificada con backup
- core/id_generator.py: IDs WIL-XXX centralizados
- motor_kami/template_engine.py: Lee templates reales
- motor_kami/variable_resolver.py: Resuelve {{variables}}
- Backend usa core.* en lugar de paths hardcodeados
- Endpoints completos: finanzas, drive-link, check-plazos
- Frontend api.js actualizado
- Tests pytest
- scripts/backup.py"

# Push
git push origin v2.0-dev
```

---

## VERIFICACIÓN FINAL

Ejecuta esta secuencia y reporta resultados:

```bash
cd ws-hermes-legal-pro

# 1. Tests
pytest tests/ -v

# 2. Backend importa
python3 -c "from dashboard.backend.app import app; print('✅ Backend OK')"

# 3. Config carga
python3 -c "from config.config_loader import Config; c = Config.load(); print('✅ Config OK:', c.despacho.nombre)"

# 4. Datastore funciona
python3 -c "
from core.datastore import JSONDatastore
from core.id_generator import IDGenerator
from pathlib import Path
import tempfile
with tempfile.TemporaryDirectory() as tmpdir:
    ds = JSONDatastore(Path(tmpdir), Path(tmpdir))
    idg = IDGenerator(ds, {'matter_prefix': 'WIL', 'document_prefix': 'DOC', 'padding': 3})
    print('✅ Datastore OK, ID:', idg.generate_matter_id())
"

# 5. Motor Kami lee templates
python3 -c "
from motor_kami.template_engine import Template
from pathlib import Path
t = Template.load(Path('motor_kami/templates'), 'nda')
print('✅ Motor Kami OK:', t.label)
"

# 6. Verificar estructura
ls -la config/
ls -la core/
ls -la tests/
```

---

## REPORTE DE PROGRESO

Después de completar cada paso, reporta:
1. ¿Qué archivos creaste/modificaste?
2. ¿Hubo errores? ¿Cuáles?
3. ¿Qué paso sigue?

Si encuentras un bloqueo que no puedes resolver en 3 intentos, reporta:
- Archivo afectado
- Error exacto (copia el traceback)
- Qué intentaste

---

## NOTAS IMPORTANTES

1. **No uses subprocess** para llamar motor_kami. Importa directamente.
2. **No hardcodees paths** como `C:/WillowLegal/`. Usa `Path.home()` o config.
3. **No hardcodees datos del despacho**. Lee de `config.yaml`.
4. **Cada cambio en JSON debe hacer backup automático**. El datastore ya lo hace.
5. **IDs deben ser WIL-XXX**. No LEG-XXX, no PRAG-XXX.
6. **Si un endpoint no existe, créalo**. No dejes el frontend llamando al vacío.

---

*Prompt generado por Hermes Neo — 2026-05-04*
*Este prompt es AUTO-CONTENIDO. No requiere documentación externa.*
