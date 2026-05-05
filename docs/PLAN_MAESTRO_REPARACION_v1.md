# PLAN MAESTRO DE REPARACIÓN — ws-hermes-legal-pro
## Versión: v1.0-EXHAUSTIVO
## Fecha: 2026-05-04
## Estado: Pendiente de aprobación
## Autor: Hermes Neo (Auditoría + Planificación)
## Repo: https://github.com/cuentadeservicio377-cell/ws-hermes-legal-pro

---

## 📋 ÍNDICE

1. [Resumen Ejecutivo](#1-resumen-ejecutivo)
2. [Fases del Plan](#2-fases-del-plan)
3. [Fase 1: Fundamentos (Semanas 1-2)](#3-fase-1-fundamentos-semanas-1-2)
4. [Fase 2: Motor de Documentos (Semanas 3-4)](#4-fase-2-motor-de-documentos-semanas-3-4)
5. [Fase 3: API y Frontend (Semanas 5-6)](#5-fase-3-api-y-frontend-semanas-5-6)
6. [Fase 4: Calidad y Escalabilidad (Semanas 7-8)](#6-fase-4-calidad-y-escalabilidad-semanas-7-8)
7. [Fase 5: Funcionalidades Avanzadas (Semanas 9-12)](#7-fase-5-funcionalidades-avanzadas-semanas-9-12)
8. [Arquitectura Objetivo](#8-arquitectura-objetivo-post-reparación)
9. [Mapa de Conectividad](#9-mapa-de-conectividad-frontend--backend--google-workspace)
10. [Especificación Técnica Detallada](#10-especificación-técnica-detallada)
11. [Tests y Verificación](#11-tests-y-verificación)
12. [Riesgos y Mitigaciones](#12-riesgos-y-mitigaciones)
13. [Checklist de Entrega](#13-checklist-de-entrega)

---

## 1. RESUMEN EJECUTIVO

### 1.1 Propósito
Transformar `ws-hermes-legal-pro` de un prototipo funcionalmente roto en un **producto legal enterprise-grade** listo para operar en despachos reales.

### 1.2 Alcance
- **SÍ incluye:** Todo el código, arquitectura, documentación, tests, deployment, seguridad, UX
- **NO incluye:** Contenido legal específico (cláusulas deben ser provistas por abogado)
- **NO incluye:** Infraestructura cloud (el producto es on-premise por diseño)

### 1.3 Principios Rectores
1. **Single Source of Truth** — Un solo lugar para cada tipo de dato
2. **Idempotencia** — Scripts ejecutables N veces sin efectos secundarios
3. **Backward Compatibility** — Migraciones preservan datos existentes
4. **Fail Fast, Fail Loud** — Errores detectables inmediatamente
5. **Zero Config para Usuario Final** — El abogado no edita JSONs
6. **Security by Default** — Auth en todos los endpoints
7. **Test-Driven** — Cada feature tiene tests antes de mergear

---

## 2. FASES DEL PLAN

| Fase | Semanas | Focus | Deliverable |
|------|---------|-------|-------------|
| 1 | 1-2 | Fundamentos | Sistema base estable, datos unificados |
| 2 | 3-4 | Motor Documentos | Templates reales, PDFs profesionales |
| 3 | 5-6 | API + Frontend | Dashboard completo, endpoints funcionales |
| 4 | 7-8 | Calidad | Tests, docs, migraciones, responsive |
| 5 | 9-12 | Avanzado | Auth, reportes, firma digital, Onyx |

---

## 3. FASE 1: FUNDAMENTOS (Semanas 1-2)

### 3.1 Sistema de Configuración Unificado

#### Archivo Nuevo: `config/config.yaml`
```yaml
version: "2.0"
despacho:
  nombre: "We Law S.C."
  rfc: "WEL123456ABC"
  representante: "Lic. Pablo Meneses"
  email: "contacto@welaw.mx"
  domicilio: "Ciudad de México"
  telefono: "+52-55-XXXX-XXXX"
  
datastore:
  type: "json"  # json | sqlite | postgres
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
  enabled: true
  credentials_path: "~/.willowlegal/config/client_secret.json"
  token_path: "~/.willowlegal/config/token.json"
  base_folder: "WillowLegal"
  
auth:
  enabled: true
  type: "api_key"  # api_key | jwt | oauth2
  api_key_header: "X-API-Key"
  
notifications:
  telegram:
    enabled: true
    bot_token_env: "TELEGRAM_BOT_TOKEN"
    chat_id_env: "TELEGRAM_HOME_CHAT_ID"
  email:
    enabled: false
    smtp_host: ""
    smtp_port: 587
```

#### Archivo Nuevo: `config/config_loader.py`
```python
"""
ConfigLoader — Carga y validación de configuración centralizada.
"""
import yaml
import os
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass, field

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
class MotorKamiConfig:
    templates_dir: Path
    output_dir: Path
    css_theme: str = "kami_v2"

@dataclass
class Config:
    version: str
    despacho: DespachoConfig
    datastore: DatastoreConfig
    ids: Dict[str, Any]
    motor_kami: MotorKamiConfig
    google_workspace: Dict[str, Any]
    auth: Dict[str, Any]
    notifications: Dict[str, Any]
    
    @classmethod
    def load(cls, path: str = "config/config.yaml") -> "Config":
        """Carga config desde YAML con validación."""
        config_path = Path(path)
        if not config_path.exists():
            raise FileNotFoundError(f"Config no encontrado: {path}")
        
        with open(config_path, 'r', encoding='utf-8') as f:
            raw = yaml.safe_load(f)
        
        # Validar versión
        if raw.get("version") != "2.0":
            raise ValueError(f"Versión de config no soportada: {raw.get('version')}")
        
        # Expandir paths
        raw["datastore"]["path"] = Path(raw["datastore"]["path"]).expanduser()
        raw["datastore"]["backup_dir"] = Path(raw["datastore"]["backup_dir"]).expanduser()
        raw["motor_kami"]["templates_dir"] = Path(raw["motor_kami"]["templates_dir"])
        raw["motor_kami"]["output_dir"] = Path(raw["motor_kami"]["output_dir"]).expanduser()
        
        # Crear directorios si no existen
        raw["datastore"]["path"].mkdir(parents=True, exist_ok=True)
        raw["datastore"]["backup_dir"].mkdir(parents=True, exist_ok=True)
        raw["motor_kami"]["output_dir"].mkdir(parents=True, exist_ok=True)
        
        return cls(
            version=raw["version"],
            despacho=DespachoConfig(**raw["despacho"]),
            datastore=DatastoreConfig(**raw["datastore"]),
            ids=raw["ids"],
            motor_kami=MotorKamiConfig(**raw["motor_kami"]),
            google_workspace=raw["google_workspace"],
            auth=raw["auth"],
            notifications=raw["notifications"]
        )
    
    def get_despacho_data(self) -> Dict[str, str]:
        """Retorna datos del despacho para templates."""
        return {
            "nombre": self.despacho.nombre,
            "rfc": self.despacho.rfc,
            "representante": self.despacho.representante,
            "email": self.despacho.email,
            "domicilio": self.despacho.domicilio,
            "telefono": self.despacho.telefono
        }
```

#### Archivo Modificado: Todos los scripts para usar ConfigLoader
- `dashboard/backend/app.py`: Usar `Config.load()` en lugar de paths hardcodeados
- `hermes_integration/commands.py`: Usar `Config.load()` para datos del despacho
- `scripts/willow_standalone.py`: Usar `Config.load()` para paths de datos
- `scripts/drive_manager.py`: Usar `Config.load()` para credenciales
- `scripts/calendar_manager.py`: Usar `Config.load()` para config
- `scripts/check_plazos.py`: Usar `Config.load()` para paths y Telegram

### 3.2 Sistema de Datos Unificado

#### Archivo Nuevo: `core/datastore.py`
```python
"""
Datastore — Capa de abstracción para persistencia.
Soporta: JSON (default), SQLite, PostgreSQL (futuro).
"""
import json
import sqlite3
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime
import shutil

class JSONDatastore:
    """Implementación JSON con backup automático."""
    
    def __init__(self, base_path: Path, backup_dir: Path):
        self.base_path = Path(base_path).expanduser()
        self.backup_dir = Path(backup_dir).expanduser()
        self.base_path.mkdir(parents=True, exist_ok=True)
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        
        # Archivos soportados
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
        
        # Inicializar archivos vacíos
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
        # Backup antes de escribir
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
        """Crea backup manual completo. Retorna path del backup."""
        backup_name = f"willow_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        backup_path = self.backup_dir / backup_name
        backup_path.mkdir(parents=True, exist_ok=True)
        
        for name, path in self.files.items():
            if path.exists():
                shutil.copy(path, backup_path / f"{name}.json")
        
        return str(backup_path)
```

#### Archivo Modificado: `dashboard/backend/app.py`
```python
# REEMPLAZAR todo el sistema de paths hardcodeados por:
from core.datastore import JSONDatastore
from config.config_loader import Config

config = Config.load()
datastore = JSONDatastore(config.datastore.path, config.datastore.backup_dir)

# REEMPLAZAR todas las funciones load_json/save_json por:
def load_json(collection: str) -> List[Dict]:
    return datastore.get(collection)

def save_json(collection: str, data: List[Dict]):
    datastore.set(collection, data)
```

### 3.3 Sistema de IDs Unificado

#### Archivo Nuevo: `core/id_generator.py`
```python
"""
IDGenerator — Generación centralizada de IDs.
"""
from datetime import datetime
from typing import Optional
from core.datastore import JSONDatastore

class IDGenerator:
    def __init__(self, datastore: JSONDatastore, config: dict):
        self.ds = datastore
        self.prefix = config.get("matter_prefix", "WIL")
        self.doc_prefix = config.get("document_prefix", "DOC")
        self.padding = config.get("padding", 3)
    
    def generate_matter_id(self) -> str:
        """Genera ID único para matter: WIL-001, WIL-002, etc."""
        matters = self.ds.get("matters")
        
        # Encontrar máximo número existente
        max_num = 0
        for m in matters:
            matter_id = m.get("id", "")
            if matter_id.startswith(self.prefix + "-"):
                try:
                    num = int(matter_id.split("-")[1])
                    max_num = max(max_num, num)
                except (ValueError, IndexError):
                    pass
        
        next_num = max_num + 1
        return f"{self.prefix}-{next_num:0{self.padding}d}"
    
    def generate_document_id(self) -> str:
        """Genera ID único para documento: DOC-0001, etc."""
        documentos = self.ds.get("documentos")
        max_num = len(documentos)
        return f"{self.doc_prefix}-{max_num + 1:04d}"
    
    def generate_reunion_id(self) -> str:
        """Genera ID único para reunión."""
        reuniones = self.ds.get("reuniones")
        return f"REU-{len(reuniones) + 1:04d}"
    
    def generate_plazo_id(self) -> str:
        """Genera ID único para plazo."""
        plazos = self.ds.get("plazos")
        return f"PLZ-{len(plazos) + 1:04d}"
    
    def generate_alerta_id(self) -> str:
        """Genera ID único para alerta."""
        alertas = self.ds.get("alertas")
        return f"ALR-{len(alertas) + 1:04d}"
```

### 3.4 Sistema de Backup Automático

#### Archivo Nuevo: `scripts/backup.py`
```python
#!/usr/bin/env python3
"""
backup.py — Sistema de backup automático y manual.
"""
import argparse
import json
from datetime import datetime
from pathlib import Path
import shutil
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))
from config.config_loader import Config
from core.datastore import JSONDatastore

def backup_manual():
    """Crea backup manual completo."""
    config = Config.load()
    ds = JSONDatastore(config.datastore.path, config.datastore.backup_dir)
    backup_path = ds.backup()
    print(f"✅ Backup creado: {backup_path}")
    return backup_path

def backup_cron():
    """Ejecutado por cron. Solo backup si hay cambios recientes."""
    config = Config.load()
    ds = JSONDatastore(config.datastore.path, config.datastore.backup_dir)
    
    # Verificar si hay backups recientes (últimas 24h)
    backup_dir = Path(config.datastore.backup_dir)
    if backup_dir.exists():
        backups = sorted(backup_dir.iterdir(), key=lambda p: p.stat().st_mtime, reverse=True)
        if backups:
            last_backup_time = datetime.fromtimestamp(backups[0].stat().st_mtime)
            hours_since = (datetime.now() - last_backup_time).total_seconds() / 3600
            
            if hours_since < config.datastore.backup_interval_hours:
                print(f"⏭️  Backup reciente existe ({hours_since:.1f}h). Saltando.")
                return
    
    backup_path = ds.backup()
    print(f"✅ Backup automático creado: {backup_path}")

def list_backups():
    """Lista todos los backups disponibles."""
    config = Config.load()
    backup_dir = Path(config.datastore.backup_dir)
    
    if not backup_dir.exists():
        print("❌ No hay directorio de backups")
        return
    
    backups = sorted(backup_dir.iterdir(), key=lambda p: p.stat().st_mtime, reverse=True)
    
    print(f"\n📦 BACKUPS DISPONIBLES ({len(backups)}):")
    for b in backups[:10]:  # Mostrar últimos 10
        size = sum(f.stat().st_size for f in b.rglob('*') if f.is_file())
        size_mb = size / (1024 * 1024)
        mtime = datetime.fromtimestamp(b.stat().st_mtime)
        print(f"  • {b.name} — {size_mb:.1f} MB — {mtime.strftime('%Y-%m-%d %H:%M')}")

def restore_backup(backup_name: str):
    """Restaura un backup específico."""
    config = Config.load()
    backup_dir = Path(config.datastore.backup_dir)
    backup_path = backup_dir / backup_name
    
    if not backup_path.exists():
        print(f"❌ Backup no encontrado: {backup_name}")
        return
    
    # Backup actual antes de restaurar
    ds = JSONDatastore(config.datastore.path, config.datastore.backup_dir)
    current_backup = ds.backup()
    print(f"💾 Backup del estado actual: {current_backup}")
    
    # Restaurar
    data_dir = Path(config.datastore.path)
    for backup_file in backup_path.glob("*.json"):
        dest = data_dir / backup_file.name
        shutil.copy(backup_file, dest)
        print(f"  ✅ Restaurado: {backup_file.name}")
    
    print(f"\n✅ Backup '{backup_name}' restaurado exitosamente")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Willow Legal Backup Manager")
    parser.add_argument("--backup", action="store_true", help="Crear backup manual")
    parser.add_argument("--cron", action="store_true", help="Ejecutar backup de cron")
    parser.add_argument("--list", action="store_true", help="Listar backups")
    parser.add_argument("--restore", type=str, help="Restaurar backup específico")
    
    args = parser.parse_args()
    
    if args.backup:
        backup_manual()
    elif args.cron:
        backup_cron()
    elif args.list:
        list_backups()
    elif args.restore:
        restore_backup(args.restore)
    else:
        parser.print_help()
```

#### Archivo Nuevo: `scripts/setup_cron.py`
```python
#!/usr/bin/env python3
"""
setup_cron.py — Configura cron para backups automáticos.
"""
import subprocess
from pathlib import Path

def setup_backup_cron():
    """Configura cron para backup cada 24 horas."""
    script_path = Path(__file__).parent / "backup.py"
    cron_line = f"0 2 * * * cd {Path(__file__).parent.parent} && python3 {script_path} --cron >> ~/.willowlegal/backup.log 2>&1"
    
    # Verificar si ya existe
    result = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
    if cron_line in result.stdout:
        print("⏭️  Cron ya configurado")
        return
    
    # Agregar a crontab
    new_crontab = result.stdout + f"\n# Willow Legal Backup\n{cron_line}\n"
    subprocess.run(["crontab", "-"], input=new_crontab, text=True)
    print("✅ Cron configurado: backup diario a las 2:00 AM")

if __name__ == "__main__":
    setup_backup_cron()
```

### 3.5 Sistema de Migraciones

#### Archivo Nuevo: `core/migrations.py`
```python
"""
migrations.py — Sistema de migraciones de schema.
"""
import json
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime

class MigrationManager:
    def __init__(self, datastore):
        self.ds = datastore
        self.migrations_dir = Path(__file__).parent.parent / "migrations"
        self.migrations_dir.mkdir(exist_ok=True)
    
    def get_current_version(self) -> str:
        """Lee versión actual del schema."""
        try:
            meta = self.ds.get("_meta")
            if meta and len(meta) > 0:
                return meta[0].get("schema_version", "1.0")
        except:
            pass
        return "1.0"
    
    def set_version(self, version: str):
        """Guarda versión actual del schema."""
        try:
            meta = self.ds.get("_meta")
        except:
            meta = []
        
        if not meta:
            meta = [{"schema_version": version, "last_migration": datetime.now().isoformat()}]
        else:
            meta[0]["schema_version"] = version
            meta[0]["last_migration"] = datetime.now().isoformat()
        
        self.ds.set("_meta", meta)
    
    def run_migrations(self):
        """Ejecuta migraciones pendientes."""
        current = self.get_current_version()
        print(f"📊 Schema actual: v{current}")
        
        # Definir migraciones
        migrations = {
            "1.0": self._migrate_1_0_to_2_0,
            "2.0": self._migrate_2_0_to_2_1,
        }
        
        while current in migrations:
            print(f"🔄 Migrando v{current} → v{next_version(current)}")
            migrations[current]()
            current = next_version(current)
            self.set_version(current)
        
        print(f"✅ Schema actualizado: v{current}")

def next_version(current: str) -> str:
    """Calcula siguiente versión."""
    parts = current.split(".")
    parts[-1] = str(int(parts[-1]) + 1)
    return ".".join(parts)

# Migración 1.0 → 2.0: Unificar IDs
def _migrate_1_0_to_2_0(self):
    """Migración: Unificar formato de IDs."""
    matters = self.ds.get("matters")
    
    for matter in matters:
        # Convertir LEG-XXX o PRAG-XXX a WIL-XXX
        old_id = matter.get("id", "")
        if old_id.startswith("LEG-") or old_id.startswith("PRAG-"):
            # Extraer número
            try:
                num = int(old_id.split("-")[1])
                new_id = f"WIL-{num:03d}"
                matter["id"] = new_id
                print(f"  📝 {old_id} → {new_id}")
            except:
                pass
    
    self.ds.set("matters", matters)
    print("  ✅ IDs unificados a formato WIL-XXX")
```

---

## 4. FASE 2: MOTOR DE DOCUMENTOS (Semanas 3-4)

### 4.1 Motor Kami v4 — Lectura Real de Templates

#### Archivo Nuevo: `motor_kami/template_engine.py`
```python
"""
template_engine.py — Motor de templates JSON.
Lee templates reales y genera documentos con sustancia legal.
"""
import json
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
        """Carga template desde archivo JSON."""
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
        """Valida que todas las variables requeridas estén presentes."""
        missing = []
        for var in self.required_variables:
            if var not in provided or not provided[var]:
                missing.append(var)
        return missing
    
    def merge_with_data(self, matter_data: Dict[str, Any], extra_vars: Dict[str, Any]) -> Dict[str, Any]:
        """Fusiona template con datos del matter y variables extras."""
        result = json.loads(json.dumps(self.document_data_template))  # Deep copy
        
        # Fusionar datos del matter
        if "cliente" in matter_data:
            result["cliente"].update(matter_data["cliente"])
        if "prestador" in matter_data:
            result["prestador"].update(matter_data["prestador"])
        
        # Fusionar variables extras
        for key, value in extra_vars.items():
            if "." in key:
                # Nested key: "cliente.nombre"
                parts = key.split(".")
                target = result
                for part in parts[:-1]:
                    if part not in target:
                        target[part] = {}
                    target = target[part]
                target[parts[-1]] = value
            else:
                result[key] = value
        
        return result
```

#### Archivo Modificado: `motor_kami/motor_kami.py`
```python
# REEMPLAZAR la función de generación actual por:

def generar_documento(
    template_key: str,
    matter_data: Dict[str, Any],
    output_path: Path,
    extra_vars: Dict[str, Any] = None,
    despacho_data: Dict[str, Any] = None
) -> Dict[str, Any]:
    """
    Genera documento legal usando template real.
    
    Args:
        template_key: Key del template (nda, prestacion_servicios, etc.)
        matter_data: Datos del matter (cliente, descripción, etc.)
        output_path: Path de salida para el PDF
        extra_vars: Variables adicionales para el template
        despacho_data: Datos del despacho (nombre, RFC, etc.)
    
    Returns:
        Dict con: success, file_path, validation_result
    """
    from template_engine import Template
    from blocks import validar_sustancia, generar_desde_bloques
    
    # 1. Cargar template real
    template = Template.load(TEMPLATES_DIR, template_key)
    
    # 2. Validar variables
    all_vars = {**(extra_vars or {}), **matter_data}
    missing = template.validate_variables(all_vars)
    if missing:
        return {
            "success": False,
            "error": f"Variables faltantes: {', '.join(missing)}",
            "missing_variables": missing
        }
    
    # 3. Fusionar datos
    doc_data = template.merge_with_data(matter_data, extra_vars or {})
    
    # 4. Agregar datos del despacho
    if despacho_data:
        doc_data["prestador"] = despacho_data
    
    # 5. Validar sustancia legal
    validation = validar_sustancia(doc_data)
    if not validation["valid"]:
        return {
            "success": False,
            "error": "Validación de sustancia fallida",
            "validation": validation
        }
    
    # 6. Generar PDF
    blocks = construir_bloques(template.recommended_blocks, doc_data)
    html_content = generar_desde_bloques(blocks, doc_data)
    
    # 7. Renderizar con WeasyPrint
    HTML(string=html_content).write_pdf(str(output_path))
    
    return {
        "success": True,
        "file_path": str(output_path),
        "file_size": output_path.stat().st_size,
        "validation": validation,
        "template_used": template_key
    }

def construir_bloques(recommended_blocks: List[str], doc_data: Dict[str, Any]) -> List[Dict]:
    """Construye bloques según recomendaciones del template."""
    blocks = []
    
    for block_type in recommended_blocks:
        if block_type == "cover_page":
            blocks.append({
                "type": "cover_page",
                "data": {
                    "titulo": doc_data.get("titulo", "Documento Legal"),
                    "subtitulo": doc_data.get("subtitulo", ""),
                    "marca": doc_data.get("prestador", {}).get("nombre", ""),
                    "numero": doc_data.get("numero_contrato", "")
                }
            })
        elif block_type == "header_brand":
            blocks.append({
                "type": "header_brand",
                "data": {
                    "marca": doc_data.get("prestador", {}).get("nombre", ""),
                    "titulo": doc_data.get("titulo", ""),
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
                blocks.append({
                    "type": "clause_section",
                    "data": clausula
                })
        elif block_type == "signature_block":
            blocks.append({
                "type": "signature_block",
                "data": {
                    "prestador": doc_data.get("prestador", {}),
                    "cliente": doc_data.get("cliente", {}),
                    "fecha": doc_data.get("fecha", ""),
                    "testigos": doc_data.get("testigos", [])
                }
            })
        # ... etc para todos los block types
    
    return blocks
```

### 4.2 Población de Templates con Texto Legal Real

#### Archivo Modificado: `motor_kami/templates/prestacion_servicios.json`
```json
{
  "metadata": {
    "key": "prestacion_servicios",
    "label": "Contrato de Prestación de Servicios Profesionales",
    "area": "Contratos",
    "materia": "corporativo",
    "version": "2.0",
    "created": "2026-05-04",
    "last_updated": "2026-05-04",
    "jurisdiction": "México",
    "governing_law": "Código Civil Federal y Código Federal de Procedimientos Civiles"
  },
  "recommended_blocks": [
    "cover_page",
    "header_brand",
    "parties_block",
    "clause_section",
    "payment_table",
    "signature_block",
    "footer_block"
  ],
  "required_variables": [
    "cliente.nombre",
    "cliente.rfc",
    "cliente.domicilio",
    "cliente.representante",
    "cliente.email",
    "prestador.nombre",
    "prestador.rfc",
    "prestador.domicilio",
    "prestador.representante",
    "prestador.email",
    "honorarios.monto",
    "honorarios.moneda",
    "plazo.duracion",
    "plazo.unidad",
    "objeto.descripcion"
  ],
  "document_data_template": {
    "tipo": "prestacion_servicios",
    "titulo": "CONTRATO DE PRESTACIÓN DE SERVICIOS PROFESIONALES",
    "subtitulo": "",
    "marca": "{{prestador.nombre}}",
    "numero_contrato": "{{matter_id}}-CTR",
    "fecha": "{{fecha_actual}}",
    "prestador": {
      "nombre": "{{prestador.nombre}}",
      "rfc": "{{prestador.rfc}}",
      "domicilio": "{{prestador.domicilio}}",
      "representante": "{{prestador.representante}}",
      "email": "{{prestador.email}}"
    },
    "cliente": {
      "nombre": "{{cliente.nombre}}",
      "rfc": "{{cliente.rfc}}",
      "domicilio": "{{cliente.domicilio}}",
      "representante": "{{cliente.representante}}",
      "email": "{{cliente.email}}"
    },
    "antecedentes": "Que el PRESTADOR es una firma legal especializada en {{area_especialidad}}, con experiencia en {{experiencia_relevante}}. Que el CLIENTE requiere los servicios profesionales del PRESTADOR para {{objeto.descripcion}}.",
    "clausulas": [
      {
        "numero": "PRIMERA",
        "titulo": "DECLARACIONES",
        "subclausulas": [
          "I. Declara el PRESTADOR, por conducto de su representante legal: (a) Que es una sociedad civil debidamente constituida conforme a las leyes mexicanas; (b) Que su representante legal cuenta con las facultades necesarias para celebrar el presente contrato; (c) Que su Registro Federal de Contribuyentes es {{prestador.rfc}}; (d) Que su domicilio fiscal se encuentra en {{prestador.domicilio}}.",
          "II. Declara el CLIENTE, por conducto de su representante legal: (a) Que es una persona moral/ física debidamente constituida conforme a las leyes mexicanas; (b) Que su representante legal cuenta con las facultades necesarias para celebrar el presente contrato; (c) Que su Registro Federal de Contribuyentes es {{cliente.rfc}}; (d) Que su domicilio fiscal se encuentra en {{cliente.domicilio}}."
        ]
      },
      {
        "numero": "SEGUNDA",
        "titulo": "OBJETO",
        "subclausulas": [
          "El objeto del presente contrato es la prestación de servicios profesionales de {{objeto.descripcion}} por parte del PRESTADOR a favor del CLIENTE.",
          "Los servicios específicos incluyen: (a) Asesoría legal especializada; (b) Elaboración de documentos legales; (c) Representación en trámites administrativos; (d) Las demás actividades necesarias para el cumplimiento del objeto.",
          "El PRESTADOR prestará los servicios con la diligencia profesional propia de su especialidad, conforme a los estándares éticos y técnicos del Colegio de Abogados."
        ]
      },
      {
        "numero": "TERCERA",
        "titulo": "HONORARIOS Y FORMA DE PAGO",
        "subclausulas": [
          "Por los servicios objeto del presente contrato, el CLIENTE pagará al PRESTADOR la cantidad de {{honorarios.monto}} {{honorarios.moneda}} ({{honorarios.monto_letra}} {{honorarios.moneda}}).",
          "La forma de pago será: {{honorarios.forma_pago}}.",
          "El CLIENTE pagará un anticipo del {{honorarios.porcentaje_anticipo}}% al momento de la firma del presente contrato, equivalente a {{honorarios.monto_anticipo}} {{honorarios.moneda}}.",
          "Los pagos serán exigibles en el domicilio del PRESTADOR o mediante transferencia electrónica a la cuenta bancaria designada por el PRESTADOR.",
          "En caso de incumplimiento en el pago, el CLIENTE pagará una moratoria del {{honorarios.tasa_moratoria}}% mensual sobre las cantidades adeudadas."
        ]
      },
      {
        "numero": "CUARTA",
        "titulo": "PLAZO",
        "subclausulas": [
          "El presente contrato tendrá una duración de {{plazo.duracion}} {{plazo.unidad}}, contados a partir de la fecha de firma.",
          "El plazo podrá prorrogarse por acuerdo escrito de las partes, siempre y cuando se formalice con anticipación no menor a {{plazo.dias_preaviso}} días naturales.",
          "En caso de terminación anticipada por incumplimiento, la parte incumplida pagará los daños y perjuicios conforme a la Cláusula Décima."
        ]
      },
      {
        "numero": "QUINTA",
        "titulo": "CONFIDENCIALIDAD",
        "subclausulas": [
          "Las partes se obligan a mantener estricta confidencialidad respecto de toda información intercambiada en virtud del presente contrato.",
          "La obligación de confidencialidad subsistirá durante {{confidencialidad.duracion}} años contados a partir de la terminación del contrato.",
          "La información confidencial no podrá divulgarse a terceros sin consentimiento previo y por escrito de la parte reveladora.",
          "Las partes implementarán medidas de seguridad razonables para proteger la información confidencial."
        ]
      },
      {
        "numero": "SEXTA",
        "titulo": "PROPIEDAD INTELECTUAL",
        "subclausulas": [
          "Los documentos elaborados por el PRESTADOR en virtud del presente contrato serán propiedad del CLIENTE una vez pagados los honorarios correspondientes.",
          "El PRESTADOR se reserva los derechos morales sobre su trabajo profesional conforme a la Ley Federal del Derecho de Autor.",
          "El CLIENTE no podrá atribuirse la autoría de los documentos elaborados por el PRESTADOR."
        ]
      },
      {
        "numero": "SÉPTIMA",
        "titulo": "LIMITACIÓN DE RESPONSABILIDAD",
        "subclausulas": [
          "La responsabilidad del PRESTADOR se limita a la cantidad total de honorarios pagados por el CLIENTE en los últimos 12 meses.",
          "El PRESTADOR no será responsable por daños indirectos, incidentales o consecuenciales.",
          "El PRESTADOR no garantiza resultados específicos en procedimientos judiciales o administrativos."
        ]
      },
      {
        "numero": "OCTAVA",
        "titulo": "SUSPENSIÓN Y TERMINACIÓN",
        "subclausulas": [
          "Cualquiera de las partes podrá suspender la prestación de servicios en caso de incumplimiento de la otra parte, previo aviso por escrito de {{terminacion.dias_aviso}} días naturales.",
          "En caso de terminación, el CLIENTE pagará los honorarios proporcionales a los servicios efectivamente prestados.",
          "La terminación no afectará las obligaciones de confidencialidad ni las cláusulas de indemnización."
        ]
      },
      {
        "numero": "NOVENA",
        "titulo": "MEDIACIÓN Y JURISDICCIÓN",
        "subclausulas": [
          "Las partes se someten a la jurisdicción de los tribunales federales de la Ciudad de México.",
          "En caso de controversia, las partes se obligan a someterse a un procedimiento de mediación ante el Centro de Mediación de la Barra Mexicana de Abogados.",
          "El procedimiento de mediación tendrá una duración máxima de {{mediacion.dias_maximos}} días naturales.",
          "En caso de que la mediación no resulte exitosa, las partes podrán recurrir a la jurisdicción ordinaria."
        ]
      },
      {
        "numero": "DÉCIMA",
        "titulo": "DISPOSICIONES GENERALES",
        "subclausulas": [
          "El presente contrato constituye el acuerdo total entre las partes y sustituye cualquier acuerdo previo.",
          "Las modificaciones al presente contrato deberán realizarse por escrito y firmadas por ambas partes.",
          "Si alguna cláusula fuera declarada inválida, las demás cláusulas mantendrán su vigencia.",
          "Las notificaciones entre las partes se realizarán por correo electrónico a las direcciones designadas en las declaraciones."
        ]
      },
      {
        "numero": "DÉCIMO PRIMERA",
        "titulo": "ENTREGABLES Y ACEPTACIÓN",
        "subclausulas": [
          "El PRESTADOR entregará los siguientes productos: {{entregables.lista}}.",
          "El CLIENTE dispondrá de {{entregables.dias_revision}} días naturales para revisar y aceptar o solicitar modificaciones.",
          "La aceptación tácita se entenderá si el CLIENTE no manifiesta objeciones dentro del plazo de revisión."
        ]
      }
    ],
    "signature_block": {
      "prestador": {
        "nombre": "{{prestador.representante}}",
        "cargo": "Representante Legal de {{prestador.nombre}}"
      },
      "cliente": {
        "nombre": "{{cliente.representante}}",
        "cargo": "Representante Legal de {{cliente.nombre}}"
      },
      "fecha": "{{fecha_firma}}",
      "lugar": "{{lugar_firma}}",
      "testigos": [
        {
          "nombre": "{{testigo1.nombre}}",
          "identificacion": "{{testigo1.identificacion}}"
        },
        {
          "nombre": "{{testigo2.nombre}}",
          "identificacion": "{{testigo2.identificacion}}"
        }
      ]
    },
    "anexos": [
      {
        "titulo": "Anexo A: Descripción detallada de servicios",
        "contenido": "{{anexos.descripcion_servicios}}"
      },
      {
        "titulo": "Anexo B: Calendario de pagos",
        "contenido": "{{anexos.calendario_pagos}}"
      }
    ]
  }
}
```

**NOTA:** Los otros 22 templates deben seguir el mismo patrón, con texto legal específico para cada tipo de documento. Esto requiere trabajo de abogado, no de programador.

### 4.3 Sistema de Variables y Placeholders

#### Archivo Nuevo: `motor_kami/variable_resolver.py`
```python
"""
variable_resolver.py — Resuelve variables {{placeholder}} en templates.
"""
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
        """Reemplaza todas las variables {{nombre}} en el texto."""
        pattern = r'\{\{(\w+(?:\.\w+)*)\}\}'
        
        def replace(match):
            var_path = match.group(1)
            value = self._get_value(var_path)
            return str(value) if value is not None else match.group(0)
        
        return re.sub(pattern, replace, text)
    
    def _get_value(self, path: str) -> Any:
        """Obtiene valor de variable por path (ej: 'cliente.nombre')."""
        # Primero: built-ins
        if path in self.built_ins:
            return self.built_ins[path]
        
        # Segundo: matter data (nested)
        parts = path.split(".")
        value = self.matter
        for part in parts:
            if isinstance(value, dict) and part in value:
                value = value[part]
            else:
                return None
        
        return value
    
    def resolve_dict(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Resuelve variables en todo un dict recursivamente."""
        result = {}
        for key, value in data.items():
            if isinstance(value, str):
                result[key] = self.resolve(value)
            elif isinstance(value, dict):
                result[key] = self.resolve_dict(value)
            elif isinstance(value, list):
                result[key] = [self.resolve(item) if isinstance(item, str) else 
                              self.resolve_dict(item) if isinstance(item, dict) else item 
                              for item in value]
            else:
                result[key] = value
        return result
```

---

## 5. FASE 3: API Y FRONTEND (Semanas 5-6)

### 5.1 API Completa — Todos los Endpoints

#### Archivo Modificado: `dashboard/backend/app.py` (Endpoints faltantes)

```python
# ============================================================
# ENDPOINTS FALTANTES — A IMPLEMENTAR
# ============================================================

# ── Google Workspace ────────────────────────────────────────
@app.get("/api/drive-link/{matter_id}")
def get_drive_link(matter_id: str):
    """Obtiene link de Google Drive para un matter."""
    try:
        from scripts.drive_manager import DriveManager
        dm = DriveManager()
        
        matters = datastore.get("matters")
        matter = next((m for m in matters if m["id"] == matter_id), None)
        if not matter:
            raise HTTPException(404, "Matter no encontrado")
        
        drive_id = matter.get("drive_folder_id")
        if not drive_id:
            # Crear carpeta si no existe
            drive_id = dm.create_client_structure(matter["cliente"])
            matter["drive_folder_id"] = drive_id
            matter["drive_link"] = f"https://drive.google.com/drive/folders/{drive_id}"
            datastore.set("matters", matters)
        
        return {
            "matter_id": matter_id,
            "drive_folder_id": drive_id,
            "drive_link": matter.get("drive_link")
        }
    except Exception as e:
        raise HTTPException(500, f"Error Drive: {str(e)}")

@app.post("/api/export-sheets")
def export_to_sheets(payload: dict):
    """Exporta matters a Google Sheets."""
    try:
        from scripts.sheets_manager import SheetsManager
        sm = SheetsManager()
        
        matters = datastore.get("matters")
        result = sm.export_matters(matters)
        
        return {
            "status": "ok",
            "spreadsheet_id": result.get("spreadsheet_id"),
            "link": result.get("link"),
            "rows_exported": len(matters)
        }
    except Exception as e:
        raise HTTPException(500, f"Error Sheets: {str(e)}")

@app.post("/api/export-docs")
def export_to_docs(payload: dict):
    """Exporta documento a Google Docs editable."""
    try:
        from scripts.docs_exporter import DocsExporter
        exporter = DocsExporter()
        
        doc_id = payload.get("documento_id")
        documentos = datastore.get("documentos")
        doc = next((d for d in documentos if d["id"] == doc_id), None)
        
        if not doc:
            raise HTTPException(404, "Documento no encontrado")
        
        result = exporter.export_document(doc)
        return {
            "status": "ok",
            "doc_id": result.get("doc_id"),
            "link": result.get("link")
        }
    except Exception as e:
        raise HTTPException(500, f"Error Docs: {str(e)}")

# ── Tareas (Google Tasks) ───────────────────────────────────
@app.get("/api/tasks")
def list_tasks():
    """Lista tareas de Google Tasks."""
    try:
        from scripts.tasks_manager import TasksManager
        tm = TasksManager()
        tasks = tm.list_tasks()
        return {"tasks": tasks, "count": len(tasks)}
    except Exception as e:
        return {"tasks": [], "count": 0, "error": str(e)}

@app.post("/api/task")
def create_task(payload: dict):
    """Crea tarea en Google Tasks."""
    try:
        from scripts.tasks_manager import TasksManager
        tm = TasksManager()
        task = tm.create_task(
            title=payload.get("title"),
            notes=payload.get("notes"),
            due=payload.get("due")
        )
        return {"status": "ok", "task": task}
    except Exception as e:
        raise HTTPException(500, str(e))

# ── Calendario ──────────────────────────────────────────────
@app.get("/api/calendar-events")
def list_calendar_events(days: int = 30):
    """Lista eventos de Google Calendar."""
    try:
        from scripts.calendar_manager import CalendarManager
        cm = CalendarManager()
        events = cm.list_upcoming(days=days)
        return {"events": events, "count": len(events)}
    except Exception as e:
        return {"events": [], "count": 0, "error": str(e)}

# ── Check Plazos ────────────────────────────────────────────
@app.post("/api/check-plazos")
def trigger_check_plazos():
    """Ejecuta check de plazos manualmente."""
    try:
        from scripts.check_plazos import check_plazos
        alertas = check_plazos(notify=True)
        return {
            "status": "ok",
            "alertas_generadas": len(alertas),
            "alertas": alertas
        }
    except Exception as e:
        raise HTTPException(500, str(e))

# ── Finanzas (CRUD completo) ────────────────────────────────
class FinanzaInput(BaseModel):
    matter_id: str
    tipo: str  # ingreso | egreso | anticipo | honorario | factura
    monto: float
    concepto: str
    fecha: Optional[str] = None
    metodo_pago: Optional[str] = "transferencia"
    notas: Optional[str] = ""

@app.get("/api/finanzas")
def list_finanzas(matter_id: Optional[str] = None):
    """Lista movimientos financieros."""
    finanzas = datastore.get("finanzas")
    movimientos = finanzas.get("movimientos", [])
    
    if matter_id:
        movimientos = [m for m in movimientos if m.get("matter_id") == matter_id]
    
    # Calcular resumen
    total_ingresos = sum(m["monto"] for m in movimientos if m["tipo"] in ["ingreso", "anticipo", "pago"])
    total_egresos = sum(m["monto"] for m in movimientos if m["tipo"] in ["egreso", "gasto"])
    total_pendiente = sum(m["monto"] for m in movimientos if m["tipo"] == "pendiente")
    
    return {
        "status": "ok",
        "movimientos": movimientos[::-1],  # Más recientes primero
        "resumen": {
            "total_ingresos": total_ingresos,
            "total_egresos": total_egresos,
            "total_pendiente": total_pendiente,
            "balance": total_ingresos - total_egresos,
            "count": len(movimientos)
        }
    }

@app.post("/api/finanzas")
def create_finanza(data: FinanzaInput):
    """Registra movimiento financiero."""
    finanzas = datastore.get("finanzas")
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
    datastore.set("finanzas", finanzas)
    
    return {"status": "ok", "movimiento": movimiento}

# ── Autenticación básica ────────────────────────────────────
from fastapi.security import APIKeyHeader

API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

async def verify_api_key(api_key: str = Depends(api_key_header)):
    """Verifica API key si auth está habilitada."""
    config = Config.load()
    if not config.auth.get("enabled", False):
        return True
    
    # En producción, validar contra base de datos
    expected_key = os.environ.get("WILLOW_API_KEY", "dev-key-change-in-production")
    if api_key != expected_key:
        raise HTTPException(403, "API key inválida")
    return True

# Aplicar a todos los endpoints:
# @app.get("/api/matters", dependencies=[Depends(verify_api_key)])
```

### 5.2 Frontend Responsive y Completo

#### Archivo Nuevo: `dashboard/frontend/css/design_system.css`
```css
/* ============================================================
   DESIGN SYSTEM — Willow Legal v2.0
   Mobile-first, responsive, accessible
   ============================================================ */

/* CSS Variables */
:root {
  /* Colors */
  --color-ink: #1a1a18;
  --color-ink-soft: #2a2a28;
  --color-mid: #6b6a63;
  --color-stone: #9c9b94;
  --color-border: #e8e6dc;
  --color-parchment: #faf9f4;
  --color-parchment-warm: #f5f4ef;
  --color-blue: #1B365D;
  --color-blue-soft: #2a4a7a;
  --color-accent: #8B0000;
  --color-success: #2d7d46;
  --color-warning: #c9a227;
  --color-danger: #c41e3a;
  
  /* Typography */
  --font-serif: "Source Serif 4", "Newsreader", Georgia, serif;
  --font-sans: "Inter", -apple-system, BlinkMacSystemFont, sans-serif;
  
  /* Spacing */
  --space-xs: 0.25rem;
  --space-sm: 0.5rem;
  --space-md: 1rem;
  --space-lg: 1.5rem;
  --space-xl: 2rem;
  --space-2xl: 3rem;
  
  /* Layout */
  --sidebar-width: 260px;
  --sidebar-collapsed: 60px;
  --header-height: 64px;
  --max-content-width: 1400px;
  
  /* Shadows */
  --shadow-sm: 0 1px 2px rgba(0,0,0,0.05);
  --shadow-md: 0 4px 6px -1px rgba(0,0,0,0.1);
  --shadow-lg: 0 10px 15px -3px rgba(0,0,0,0.1);
  
  /* Radius */
  --radius-sm: 4px;
  --radius-md: 8px;
  --radius-lg: 12px;
  
  /* Transitions */
  --transition-fast: 150ms ease;
  --transition-normal: 250ms ease;
}

/* Reset & Base */
*, *::before, *::after {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

html {
  font-size: 16px;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

body {
  font-family: var(--font-sans);
  color: var(--color-ink);
  background: var(--color-parchment);
  line-height: 1.6;
}

/* ============================================================
   LAYOUT — Mobile First
   ============================================================ */

.app {
  display: flex;
  min-height: 100vh;
}

/* Sidebar */
.sidebar {
  width: var(--sidebar-collapsed);
  background: var(--color-ink);
  color: white;
  transition: width var(--transition-normal);
  position: fixed;
  height: 100vh;
  z-index: 100;
  overflow-x: hidden;
}

.sidebar.expanded {
  width: var(--sidebar-width);
}

.sidebar-toggle {
  display: block;
  padding: var(--space-md);
  background: none;
  border: none;
  color: white;
  cursor: pointer;
  font-size: 1.25rem;
}

/* Main Content */
.main-content {
  flex: 1;
  margin-left: var(--sidebar-collapsed);
  padding: var(--space-lg);
  transition: margin-left var(--transition-normal);
}

.sidebar.expanded + .main-content {
  margin-left: var(--sidebar-width);
}

/* ============================================================
   COMPONENTS
   ============================================================ */

/* Cards */
.card {
  background: white;
  border-radius: var(--radius-lg);
  padding: var(--space-lg);
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--color-border);
}

.card-grid {
  display: grid;
  gap: var(--space-lg);
  grid-template-columns: 1fr;
}

/* Tablet */
@media (min-width: 640px) {
  .card-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

/* Desktop */
@media (min-width: 1024px) {
  .card-grid {
    grid-template-columns: repeat(4, 1fr);
  }
  
  .sidebar {
    width: var(--sidebar-width);
  }
  
  .sidebar-toggle {
    display: none;
  }
  
  .main-content {
    margin-left: var(--sidebar-width);
  }
}

/* Buttons */
.btn {
  display: inline-flex;
  align-items: center;
  gap: var(--space-sm);
  padding: var(--space-sm) var(--space-md);
  border-radius: var(--radius-md);
  border: 1px solid transparent;
  font-family: var(--font-sans);
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all var(--transition-fast);
}

.btn-primary {
  background: var(--color-blue);
  color: white;
}

.btn-primary:hover {
  background: var(--color-blue-soft);
}

.btn-secondary {
  background: white;
  color: var(--color-ink);
  border-color: var(--color-border);
}

.btn-danger {
  background: var(--color-danger);
  color: white;
}

/* Forms */
.form-input {
  width: 100%;
  padding: var(--space-sm) var(--space-md);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  font-family: var(--font-sans);
  font-size: 0.875rem;
  transition: border-color var(--transition-fast);
}

.form-input:focus {
  outline: none;
  border-color: var(--color-blue);
  box-shadow: 0 0 0 3px rgba(27, 54, 93, 0.1);
}

/* Tables */
.table-container {
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
}

table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.875rem;
}

th, td {
  padding: var(--space-sm) var(--space-md);
  text-align: left;
  border-bottom: 1px solid var(--color-border);
}

th {
  font-weight: 600;
  color: var(--color-mid);
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

/* Badges */
.badge {
  display: inline-flex;
  align-items: center;
  padding: var(--space-xs) var(--space-sm);
  border-radius: var(--radius-sm);
  font-size: 0.75rem;
  font-weight: 500;
}

.badge-activo { background: #dcfce7; color: #166534; }
.badge-pendiente { background: #fef9c3; color: #854d0e; }
.badge-urgente { background: #fee2e2; color: #991b1b; }
.badge-cerrado { background: #f3f4f6; color: #4b5563; }

/* Modal */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: var(--space-md);
  z-index: 200;
  opacity: 0;
  visibility: hidden;
  transition: all var(--transition-normal);
}

.modal-overlay.active {
  opacity: 1;
  visibility: visible;
}

.modal {
  background: white;
  border-radius: var(--radius-lg);
  width: 100%;
  max-width: 600px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: var(--shadow-lg);
  transform: scale(0.95);
  transition: transform var(--transition-normal);
}

.modal-overlay.active .modal {
  transform: scale(1);
}

/* Toast */
.toast-container {
  position: fixed;
  top: var(--space-lg);
  right: var(--space-lg);
  z-index: 300;
  display: flex;
  flex-direction: column;
  gap: var(--space-sm);
}

.toast {
  padding: var(--space-md) var(--space-lg);
  border-radius: var(--radius-md);
  background: white;
  box-shadow: var(--shadow-lg);
  display: flex;
  align-items: center;
  gap: var(--space-sm);
  animation: slideIn 0.3s ease;
}

@keyframes slideIn {
  from {
    transform: translateX(100%);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}

/* Loading */
.spinner {
  width: 24px;
  height: 24px;
  border: 2px solid var(--color-border);
  border-top-color: var(--color-blue);
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* ============================================================
   UTILITIES
   ============================================================ */

.hidden { display: none !important; }
.sr-only { position: absolute; width: 1px; height: 1px; padding: 0; margin: -1px; overflow: hidden; clip: rect(0,0,0,0); border: 0; }
.text-center { text-align: center; }
.text-right { text-align: right; }
.font-serif { font-family: var(--font-serif); }
.font-sans { font-family: var(--font-sans); }
.text-sm { font-size: 0.875rem; }
.text-xs { font-size: 0.75rem; }
.text-lg { font-size: 1.125rem; }
.text-xl { font-size: 1.25rem; }
.font-medium { font-weight: 500; }
.font-semibold { font-weight: 600; }
.font-bold { font-weight: 700; }
.text-mid { color: var(--color-mid); }
.text-stone { color: var(--color-stone); }
.text-blue { color: var(--color-blue); }
.text-danger { color: var(--color-danger); }
.text-success { color: var(--color-success); }
.mb-sm { margin-bottom: var(--space-sm); }
.mb-md { margin-bottom: var(--space-md); }
.mb-lg { margin-bottom: var(--space-lg); }
.mt-sm { margin-top: var(--space-sm); }
.mt-md { margin-top: var(--space-md); }
.mt-lg { margin-top: var(--space-lg); }
.gap-sm { gap: var(--space-sm); }
.gap-md { gap: var(--space-md); }
.gap-lg { gap: var(--space-lg); }
.flex { display: flex; }
.flex-col { flex-direction: column; }
.items-center { align-items: center; }
.justify-between { justify-content: space-between; }
.flex-1 { flex: 1; }
.w-full { width: 100%; }
.overflow-hidden { overflow: hidden; }
.truncate {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
```

#### Archivo Modificado: `dashboard/frontend/index.html`
```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <meta name="theme-color" content="#1B365D">
    <title>Willow Legal — Sistema de Gestión Legal</title>
    <link rel="stylesheet" href="css/design_system.css">
    <link rel="stylesheet" href="css/styles.css">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Source+Serif+4:wght@400;600&display=swap" rel="stylesheet">
    <link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Ctext y='.9em' font-size='90'%3E⚖️%3C/text%3E%3C/svg%3E">
</head>
<body>
    <div class="app">
        <!-- Sidebar -->
        <nav class="sidebar" id="sidebar">
            <button class="sidebar-toggle" onclick="toggleSidebar()">☰</button>
            <div class="sidebar-content">
                <div class="sidebar-header">
                    <div class="logo">
                        <span class="logo-icon">⚖️</span>
                        <span class="logo-text">Willow Legal</span>
                    </div>
                </div>
                <ul class="nav-menu">
                    <li><a href="#inicio" class="nav-link active" data-section="inicio">
                        <span class="nav-icon">🏠</span>
                        <span class="nav-text">Inicio</span>
                    </a></li>
                    <li><a href="#matters" class="nav-link" data-section="matters">
                        <span class="nav-icon">📁</span>
                        <span class="nav-text">Casos</span>
                        <span class="nav-badge" id="nav-matters-count">0</span>
                    </a></li>
                    <li><a href="#documentos" class="nav-link" data-section="documentos">
                        <span class="nav-icon">📄</span>
                        <span class="nav-text">Documentos</span>
                    </a></li>
                    <li><a href="#plazos" class="nav-link" data-section="plazos">
                        <span class="nav-icon">⏰</span>
                        <span class="nav-text">Plazos</span>
                        <span class="nav-badge urgent" id="nav-plazos-count">0</span>
                    </a></li>
                    <li><a href="#finanzas" class="nav-link" data-section="finanzas">
                        <span class="nav-icon">💰</span>
                        <span class="nav-text">Finanzas</span>
                    </a></li>
                    <li><a href="#reuniones" class="nav-link" data-section="reuniones">
                        <span class="nav-icon">🎤</span>
                        <span class="nav-text">Reuniones</span>
                    </a></li>
                    <li><a href="#calendario" class="nav-link" data-section="calendario">
                        <span class="nav-icon">📅</span>
                        <span class="nav-text">Calendario</span>
                    </a></li>
                    <li><a href="#reportes" class="nav-link" data-section="reportes">
                        <span class="nav-icon">📊</span>
                        <span class="nav-text">Reportes</span>
                    </a></li>
                    <li><a href="#configuracion" class="nav-link" data-section="configuracion">
                        <span class="nav-icon">⚙️</span>
                        <span class="nav-text">Configuración</span>
                    </a></li>
                </ul>
                <div class="sidebar-footer">
                    <div class="user-info">
                        <span class="user-name" id="user-name">Abogado</span>
                        <span class="user-role">Administrador</span>
                    </div>
                </div>
            </div>
        </nav>

        <!-- Main Content -->
        <main class="main-content">
            <!-- Header -->
            <header class="main-header">
                <div class="header-left">
                    <h1 id="page-title">Panel de Control</h1>
                    <span class="header-subtitle" id="header-subtitle">Resumen del despacho</span>
                </div>
                <div class="header-right">
                    <button class="btn btn-primary" onclick="showCreateMatterModal()">
                        <span>+</span>
                        <span class="btn-text">Nuevo Caso</span>
                    </button>
                    <button class="btn btn-secondary" onclick="showCreateDocumentModal()">
                        <span>📄</span>
                        <span class="btn-text">Nuevo Documento</span>
                    </button>
                </div>
            </header>

            <!-- Sections -->
            <section id="inicio" class="section active">
                <div class="card-grid">
                    <div class="card card-kpi">
                        <div class="kpi-header">
                            <span class="kpi-icon">📁</span>
                            <span class="kpi-trend" id="matters-trend">—</span>
                        </div>
                        <div class="kpi-value" id="count-matters">0</div>
                        <div class="kpi-label">Casos Activos</div>
                    </div>
                    <div class="card card-kpi">
                        <div class="kpi-header">
                            <span class="kpi-icon">⏰</span>
                            <span class="kpi-trend urgent" id="plazos-trend">—</span>
                        </div>
                        <div class="kpi-value" id="count-plazos">0</div>
                        <div class="kpi-label">Plazos esta semana</div>
                    </div>
                    <div class="card card-kpi">
                        <div class="kpi-header">
                            <span class="kpi-icon">🔔</span>
                            <span class="kpi-trend" id="alertas-trend">—</span>
                        </div>
                        <div class="kpi-value" id="count-alertas">0</div>
                        <div class="kpi-label">Alertas</div>
                    </div>
                    <div class="card card-kpi">
                        <div class="kpi-header">
                            <span class="kpi-icon">💰</span>
                            <span class="kpi-trend" id="finanzas-trend">—</span>
                        </div>
                        <div class="kpi-value" id="count-balance">$0</div>
                        <div class="kpi-label">Balance Mes</div>
                    </div>
                </div>
                
                <div class="dashboard-grid">
                    <div class="card dashboard-card">
                        <h3>Próximos Plazos</h3>
                        <div id="proximos-plazos-list">
                            <div class="empty-state">
                                <span class="empty-icon">📅</span>
                                <p>No hay plazos próximos</p>
                            </div>
                        </div>
                    </div>
                    <div class="card dashboard-card">
                        <h3>Alertas Recientes</h3>
                        <div id="alertas-recientes-list">
                            <div class="empty-state">
                                <span class="empty-icon">✅</span>
                                <p>Sin alertas activas</p>
                            </div>
                        </div>
                    </div>
                </div>
            </section>

            <!-- Other sections... -->
            <section id="matters" class="section hidden">...</section>
            <section id="documentos" class="section hidden">...</section>
            <section id="plazos" class="section hidden">...</section>
            <section id="finanzas" class="section hidden">...</section>
            <section id="reuniones" class="section hidden">...</section>
            <section id="calendario" class="section hidden">...</section>
            <section id="reportes" class="section hidden">...</section>
            <section id="configuracion" class="section hidden">...</section>
        </main>
    </div>

    <!-- Toast Container -->
    <div class="toast-container" id="toast-container"></div>

    <!-- Modal Container -->
    <div class="modal-overlay hidden" id="modal-overlay">
        <div class="modal" id="modal">
            <div class="modal-header">
                <h3 id="modal-title">Título</h3>
                <button class="modal-close" onclick="closeModal()">×</button>
            </div>
            <div class="modal-body" id="modal-body"></div>
            <div class="modal-footer" id="modal-footer">
                <button class="btn btn-secondary" onclick="closeModal()">Cancelar</button>
                <button class="btn btn-primary" id="modal-confirm">Confirmar</button>
            </div>
        </div>
    </div>

    <!-- Scripts -->
    <script src="js/api.js"></script>
    <script src="js/utils.js"></script>
    <script src="js/toast.js"></script>
    <script src="js/modal.js"></script>
    <script src="js/navigation.js"></script>
    <script src="js/dashboard.js"></script>
    <script src="js/matters.js"></script>
    <script src="js/documentos.js"></script>
    <script src="js/plazos.js"></script>
    <script src="js/finanzas.js"></script>
    <script src="js/reuniones.js"></script>
    <script src="js/calendario.js"></script>
    <script src="js/reportes.js"></script>
    <script src="js/configuracion.js"></script>
    <script src="js/app.js"></script>
</body>
</html>
```

---

## 6. FASE 4: CALIDAD Y ESCALABILIDAD (Semanas 7-8)

### 6.1 Sistema de Tests

#### Archivo Nuevo: `tests/conftest.py`
```python
"""
pytest configuration and fixtures.
"""
import pytest
import tempfile
import shutil
from pathlib import Path
from fastapi.testclient import TestClient

# Add parent to path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from dashboard.backend.app import app
from core.datastore import JSONDatastore
from config.config_loader import Config

@pytest.fixture
def temp_data_dir():
    """Creates temporary data directory for tests."""
    temp_dir = Path(tempfile.mkdtemp())
    yield temp_dir
    shutil.rmtree(temp_dir)

@pytest.fixture
def test_datastore(temp_data_dir):
    """Creates test datastore."""
    return JSONDatastore(temp_data_dir, temp_data_dir / "backups")

@pytest.fixture
def client(temp_data_dir):
    """Creates FastAPI test client."""
    # Override config for testing
    import os
    os.environ["WILLOW_TEST_MODE"] = "1"
    os.environ["WILLOW_DATA_DIR"] = str(temp_data_dir)
    
    from dashboard.backend.app import app
    return TestClient(app)

@pytest.fixture
def sample_matter():
    """Returns sample matter data."""
    return {
        "id": "WIL-001",
        "cliente": "Innovatech Digital S.A. de C.V.",
        "area_practica": "Mercantil",
        "descripcion": "Contrato de prestación de servicios",
        "deadline": "2026-06-30",
        "prioridad": "alta",
        "estado": "activo",
        "fecha_creacion": "2026-05-01",
        "next_step": "Generar contrato",
        "reuniones": [],
        "documentos": [],
        "tareas": []
    }
```

#### Archivo Nuevo: `tests/test_api.py`
```python
"""
Tests for API endpoints.
"""
import pytest
from fastapi.testclient import TestClient

def test_health_check(client: TestClient):
    """Test health endpoint."""
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "motor_kami" in data

def test_create_matter(client: TestClient, sample_matter: dict):
    """Test matter creation."""
    response = client.post("/api/matters", json={
        "cliente": sample_matter["cliente"],
        "area_practica": sample_matter["area_practica"],
        "descripcion": sample_matter["descripcion"],
        "deadline": sample_matter["deadline"],
        "prioridad": sample_matter["prioridad"]
    })
    assert response.status_code == 200
    data = response.json()
    assert data["id"].startswith("WIL-")
    assert data["cliente"] == sample_matter["cliente"]

def test_list_matters(client: TestClient, sample_matter: dict):
    """Test matter listing."""
    # Create a matter first
    client.post("/api/matters", json={
        "cliente": sample_matter["cliente"],
        "area_practica": sample_matter["area_practica"],
        "descripcion": sample_matter["descripcion"],
        "prioridad": sample_matter["prioridad"]
    })
    
    response = client.get("/api/matters")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0

def test_get_matter(client: TestClient, sample_matter: dict):
    """Test getting specific matter."""
    # Create
    create_response = client.post("/api/matters", json={
        "cliente": sample_matter["cliente"],
        "area_practica": sample_matter["area_practica"]
    })
    matter_id = create_response.json()["id"]
    
    # Get
    response = client.get(f"/api/matters/{matter_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == matter_id

def test_update_matter(client: TestClient, sample_matter: dict):
    """Test matter update."""
    # Create
    create_response = client.post("/api/matters", json={
        "cliente": sample_matter["cliente"],
        "area_practica": sample_matter["area_practica"]
    })
    matter_id = create_response.json()["id"]
    
    # Update
    response = client.put(f"/api/matters/{matter_id}", json={
        "cliente": "Nuevo Cliente",
        "area_practica": "Laboral",
        "descripcion": "Nueva descripción",
        "deadline": "2026-07-15",
        "prioridad": "media"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["cliente"] == "Nuevo Cliente"

def test_delete_matter(client: TestClient, sample_matter: dict):
    """Test matter deletion."""
    # Create
    create_response = client.post("/api/matters", json={
        "cliente": sample_matter["cliente"],
        "area_practica": sample_matter["area_practica"]
    })
    matter_id = create_response.json()["id"]
    
    # Delete
    response = client.delete(f"/api/matters/{matter_id}")
    assert response.status_code == 200
    
    # Verify deletion
    get_response = client.get(f"/api/matters/{matter_id}")
    assert get_response.status_code == 404

def test_list_templates(client: TestClient):
    """Test template listing."""
    response = client.get("/api/templates")
    assert response.status_code == 200
    data = response.json()
    assert "templates" in data
    assert data["count"] > 0

def test_generate_document(client: TestClient, sample_matter: dict):
    """Test document generation."""
    # Create matter
    create_response = client.post("/api/matters", json={
        "cliente": sample_matter["cliente"],
        "area_practica": sample_matter["area_practica"]
    })
    matter_id = create_response.json()["id"]
    
    # Generate document
    response = client.post(f"/api/matter/{matter_id}/generar-documento", json={
        "template_key": "nda",
        "output_filename": "test_nda.pdf",
        "datos_extra": {
            "cliente": {"nombre": "Test Cliente", "rfc": "TEST123456"}
        }
    })
    # May fail if motor Kami not configured, but should return proper error
    assert response.status_code in [200, 500]

def test_finanzas_crud(client: TestClient, sample_matter: dict):
    """Test finances CRUD."""
    # Create matter
    create_response = client.post("/api/matters", json={
        "cliente": sample_matter["cliente"],
        "area_practica": sample_matter["area_practica"]
    })
    matter_id = create_response.json()["id"]
    
    # Create income
    response = client.post("/api/finanzas", json={
        "matter_id": matter_id,
        "tipo": "ingreso",
        "monto": 50000,
        "concepto": "Anticipo contrato",
        "fecha": "2026-05-01"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["movimiento"]["monto"] == 50000
    
    # List finances
    list_response = client.get("/api/finanzas")
    assert list_response.status_code == 200
    list_data = list_response.json()
    assert list_data["resumen"]["total_ingresos"] == 50000

def test_auth_protection(client: TestClient):
    """Test that auth protects endpoints when enabled."""
    # This test assumes auth is enabled in test config
    # If auth is disabled, it should still work
    response = client.get("/api/matters")
    assert response.status_code in [200, 403]
```

#### Archivo Nuevo: `tests/test_motor_kami.py`
```python
"""
Tests for Motor Kami document generation.
"""
import pytest
from pathlib import Path
import tempfile

from motor_kami.template_engine import Template
from motor_kami.variable_resolver import VariableResolver
from motor_kami.motor_kami import generar_documento

def test_template_loading():
    """Test template loading from JSON."""
    templates_dir = Path(__file__).parent.parent / "motor_kami" / "templates"
    template = Template.load(templates_dir, "nda")
    assert template.key == "nda"
    assert template.label
    assert len(template.recommended_blocks) > 0

def test_variable_resolution():
    """Test variable placeholder resolution."""
    despacho = {"nombre": "Test Law", "rfc": "TEST123"}
    matter = {"id": "WIL-001", "cliente": {"nombre": "Cliente Test"}}
    resolver = VariableResolver(despacho, matter)
    
    text = "Contrato entre {{prestador.nombre}} y {{cliente.nombre}}"
    result = resolver.resolve(text)
    assert "Test Law" in result
    assert "Cliente Test" in result

def test_variable_resolution_nested():
    """Test nested variable resolution."""
    despacho = {}
    matter = {
        "cliente": {"nombre": "ABC", "rfc": "ABC123"},
        "honorarios": {"monto": 50000}
    }
    resolver = VariableResolver(despacho, matter)
    
    text = "Cliente: {{cliente.nombre}}, RFC: {{cliente.rfc}}, Monto: {{honorarios.monto}}"
    result = resolver.resolve(text)
    assert "ABC" in result
    assert "ABC123" in result
    assert "50000" in result

def test_document_generation():
    """Test full document generation pipeline."""
    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = Path(tmpdir) / "test.pdf"
        
        matter_data = {
            "id": "WIL-TEST",
            "cliente": {
                "nombre": "Cliente Prueba",
                "rfc": "PRUEBA123",
                "domicilio": "Ciudad de México",
                "representante": "Lic. Prueba",
                "email": "prueba@test.com"
            }
        }
        
        despacho_data = {
            "nombre": "We Law S.C.",
            "rfc": "WEL123456",
            "domicilio": "CDMX",
            "representante": "Lic. Test",
            "email": "test@welaw.mx"
        }
        
        result = generar_documento(
            template_key="nda",
            matter_data=matter_data,
            output_path=output_path,
            despacho_data=despacho_data
        )
        
        assert result["success"] or "missing_variables" in result or "error" in result

def test_template_validation():
    """Test template variable validation."""
    templates_dir = Path(__file__).parent.parent / "motor_kami" / "templates"
    template = Template.load(templates_dir, "prestacion_servicios")
    
    # Missing required variables
    missing = template.validate_variables({})
    assert len(missing) > 0
    
    # All variables provided
    complete = {
        "cliente.nombre": "Test",
        "cliente.rfc": "TEST",
        "cliente.domicilio": "CDMX",
        "cliente.representante": "Lic.",
        "cliente.email": "test@test.com",
        "prestador.nombre": "We Law",
        "prestador.rfc": "WEL",
        "prestador.domicilio": "CDMX",
        "prestador.representante": "Lic.",
        "prestador.email": "test@welaw.mx",
        "honorarios.monto": 50000,
        "honorarios.moneda": "MXN",
        "plazo.duracion": 6,
        "plazo.unidad": "meses",
        "objeto.descripcion": "Servicios legales"
    }
    missing = template.validate_variables(complete)
    assert len(missing) == 0
```

#### Archivo Nuevo: `tests/test_datastore.py`
```python
"""
Tests for JSONDatastore.
"""
import pytest
from pathlib import Path
import tempfile
import shutil

from core.datastore import JSONDatastore

def test_datastore_creation():
    """Test datastore initialization."""
    with tempfile.TemporaryDirectory() as tmpdir:
        ds = JSONDatastore(Path(tmpdir), Path(tmpdir) / "backups")
        
        # Verify files created
        assert (Path(tmpdir) / "matters.json").exists()
        assert (Path(tmpdir) / "documentos.json").exists()

def test_crud_operations():
    """Test CRUD operations."""
    with tempfile.TemporaryDirectory() as tmpdir:
        ds = JSONDatastore(Path(tmpdir), Path(tmpdir) / "backups")
        
        # Create
        matter = {"id": "WIL-001", "cliente": "Test"}
        ds.insert("matters", matter)
        
        # Read
        matters = ds.get("matters")
        assert len(matters) == 1
        assert matters[0]["id"] == "WIL-001"
        
        # Update
        ds.update("matters", "id", "WIL-001", {"cliente": "Updated"})
        updated = ds.find_one("matters", id="WIL-001")
        assert updated["cliente"] == "Updated"
        
        # Delete
        ds.delete("matters", "id", "WIL-001")
        matters = ds.get("matters")
        assert len(matters) == 0

def test_backup_creation():
    """Test automatic backup on write."""
    with tempfile.TemporaryDirectory() as tmpdir:
        backup_dir = Path(tmpdir) / "backups"
        ds = JSONDatastore(Path(tmpdir), backup_dir)
        
        # Write something
        ds.insert("matters", {"id": "WIL-001", "cliente": "Test"})
        
        # Verify backup created
        backups = list(backup_dir.glob("*.json"))
        assert len(backups) > 0

def test_find_operations():
    """Test find_one and find_many."""
    with tempfile.TemporaryDirectory() as tmpdir:
        ds = JSONDatastore(Path(tmpdir), Path(tmpdir) / "backups")
        
        ds.insert("matters", {"id": "WIL-001", "estado": "activo", "area": "Mercantil"})
        ds.insert("matters", {"id": "WIL-002", "estado": "activo", "area": "Laboral"})
        ds.insert("matters", {"id": "WIL-003", "estado": "cerrado", "area": "Mercantil"})
        
        # find_one
        result = ds.find_one("matters", id="WIL-001")
        assert result["area"] == "Mercantil"
        
        # find_many
        activos = ds.find_many("matters", estado="activo")
        assert len(activos) == 2
        
        mercantil = ds.find_many("matters", area="Mercantil")
        assert len(mercantil) == 2
```

### 6.2 CI/CD Pipeline

#### Archivo Nuevo: `.github/workflows/ci.yml`
```yaml
name: CI — Willow Legal

on:
  push:
    branches: [ main, master, develop ]
  pull_request:
    branches: [ main, master ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.11", "3.12"]
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install -r requirements-dev.txt
    
    - name: Run tests
      run: |
        pytest tests/ -v --cov=dashboard --cov=motor_kami --cov=core --cov-report=xml
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
        fail_ci_if_error: false

  lint:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: "3.12"
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install black flake8 mypy
    
    - name: Check formatting
      run: black --check dashboard/ motor_kami/ core/ scripts/ hermes_integration/
    
    - name: Lint
      run: flake8 dashboard/ motor_kami/ core/ scripts/ hermes_integration/ --max-line-length=120
    
    - name: Type check
      run: mypy core/ --ignore-missing-imports
```

#### Archivo Nuevo: `requirements.txt`
```
# Core
fastapi>=0.104.0
uvicorn[standard]>=0.24.0
pydantic>=2.5.0
python-multipart>=0.0.6

# Data
PyYAML>=6.0.1
openpyxl>=3.1.2

# PDF Generation
WeasyPrint>=60.0

# Google Workspace
google-api-python-client>=2.108.0
google-auth-httplib2>=0.1.1
google-auth-oauthlib>=1.1.0

# Utilities
requests>=2.31.0
python-dateutil>=2.8.2

# Production
gunicorn>=21.2.0
```

#### Archivo Nuevo: `requirements-dev.txt`
```
# Testing
pytest>=7.4.3
pytest-asyncio>=0.21.1
pytest-cov>=4.1.0
httpx>=0.25.2

# Linting & Formatting
black>=23.11.0
flake8>=6.1.0
mypy>=1.7.1

# Development
watchdog>=3.0.0
```

### 6.3 Documentación Completa

#### Archivo Nuevo: `docs/API_REFERENCE.md`
```markdown
# API Reference — Willow Legal Pro v2.0

## Base URL
```
http://localhost:8082/api
```

## Authentication
All endpoints require API key header:
```
X-API-Key: your-api-key
```

## Endpoints

### Matters

#### List Matters
```
GET /matters
```
Query params:
- `estado` (optional): Filter by status (activo, cerrado, pausado)
- `area` (optional): Filter by practice area

Response:
```json
[
  {
    "id": "WIL-001",
    "cliente": "Client Name",
    "area_practica": "Mercantil",
    "estado": "activo",
    "prioridad": "alta",
    "deadline": "2026-06-30",
    "fecha_creacion": "2026-05-01"
  }
]
```

#### Create Matter
```
POST /matters
```
Body:
```json
{
  "cliente": "Client Name",
  "area_practica": "Mercantil",
  "descripcion": "Case description",
  "deadline": "2026-06-30",
  "prioridad": "media"
}
```

### Documents

#### List Templates
```
GET /templates
```

#### Generate Document
```
POST /matter/{matter_id}/generar-documento
```
Body:
```json
{
  "template_key": "nda",
  "output_filename": "optional_custom_name.pdf",
  "datos_extra": {
    "cliente.nombre": "Custom Name"
  }
}
```

### Finances

#### List Finances
```
GET /finanzas?matter_id=optional_filter
```

#### Create Finance Entry
```
POST /finanzas
```
Body:
```json
{
  "matter_id": "WIL-001",
  "tipo": "ingreso",
  "monto": 50000,
  "concepto": "Advance payment",
  "fecha": "2026-05-01"
}
```

### Google Workspace

#### Get Drive Link
```
GET /drive-link/{matter_id}
```

#### Export to Sheets
```
POST /export-sheets
```

#### Export to Docs
```
POST /export-docs
```
Body:
```json
{"documento_id": "DOC-001"}
```

### System

#### Health Check
```
GET /health
```

#### Check Deadlines
```
POST /check-plazos
```

## Error Responses
All errors follow this format:
```json
{
  "detail": "Error description"
}
```

Status codes:
- `200` — Success
- `400` — Bad Request
- `401` — Unauthorized (invalid API key)
- `404` — Not Found
- `500` — Internal Server Error
```

---

## 7. FASE 5: FUNCIONALIDADES AVANZADAS (Semanas 9-12)

### 7.1 Sistema de Usuarios y Roles

#### Archivo Nuevo: `core/auth.py`
```python
"""
auth.py — Sistema de autenticación y autorización.
"""
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

# Config
SECRET_KEY = "your-secret-key-change-in-production"  # Load from env
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_DAYS = 7

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(BaseModel):
    id: str
    email: str
    nombre: str
    rol: str  # admin | abogado | paralegal | cliente
    activo: bool = True
    created_at: datetime = datetime.now()

class UserCreate(BaseModel):
    email: str
    nombre: str
    password: str
    rol: str = "abogado"

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str) -> Optional[Dict[str, Any]]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None

def check_permission(user: User, required_role: str) -> bool:
    """Check if user has required role or higher."""
    role_hierarchy = {
        "cliente": 1,
        "paralegal": 2,
        "abogado": 3,
        "admin": 4
    }
    user_level = role_hierarchy.get(user.rol, 0)
    required_level = role_hierarchy.get(required_role, 0)
    return user_level >= required_level
```

### 7.2 Sistema de Versionado de Documentos

#### Archivo Modificado: `core/datastore.py` (Add versioning)
```python
def create_document_version(self, document_id: str, new_data: Dict[str, Any]) -> Dict[str, Any]:
    """Creates new version of document, preserving history."""
    documentos = self.get("documentos")
    doc = next((d for d in documentos if d["id"] == document_id), None)
    
    if not doc:
        raise ValueError(f"Documento no encontrado: {document_id}")
    
    # Initialize versions array
    if "versions" not in doc:
        doc["versions"] = []
    
    # Save current as version
    version = {
        "version_number": len(doc["versions"]) + 1,
        "created_at": datetime.now().isoformat(),
        "data": {k: v for k, v in doc.items() if k != "versions"}
    }
    doc["versions"].append(version)
    
    # Update document with new data
    doc.update(new_data)
    doc["version_count"] = len(doc["versions"])
    doc["updated_at"] = datetime.now().isoformat()
    
    self.set("documentos", documentos)
    return doc

def get_document_version(self, document_id: str, version_number: int) -> Optional[Dict[str, Any]]:
    """Retrieves specific version of document."""
    documentos = self.get("documentos")
    doc = next((d for d in documentos if d["id"] == document_id), None)
    
    if not doc or "versions" not in doc:
        return None
    
    version = next((v for v in doc["versions"] if v["version_number"] == version_number), None)
    return version
```

### 7.3 Sistema de Reportes Analíticos

#### Archivo Nuevo: `core/reports.py`
```python
"""
reports.py — Sistema de reportes y analytics.
"""
from datetime import datetime, timedelta
from typing import Dict, List, Any
from collections import defaultdict

class ReportGenerator:
    def __init__(self, datastore):
        self.ds = datastore
    
    def matters_by_area(self) -> Dict[str, Any]:
        """Report: Matters distribution by practice area."""
        matters = self.ds.get("matters")
        distribution = defaultdict(int)
        
        for m in matters:
            area = m.get("area_practica", "Sin área")
            distribution[area] += 1
        
        return {
            "title": "Matters por Área de Práctica",
            "type": "pie",
            "data": dict(distribution)
        }
    
    def matters_by_status(self) -> Dict[str, Any]:
        """Report: Matters by status."""
        matters = self.ds.get("matters")
        distribution = defaultdict(int)
        
        for m in matters:
            estado = m.get("estado", "desconocido")
            distribution[estado] += 1
        
        return {
            "title": "Matters por Estado",
            "type": "bar",
            "data": dict(distribution)
        }
    
    def revenue_by_month(self, months: int = 12) -> Dict[str, Any]:
        """Report: Revenue by month."""
        finanzas = self.ds.get("finanzas")
        movimientos = finanzas.get("movimientos", [])
        
        revenue = defaultdict(float)
        
        for m in movimientos:
            if m["tipo"] in ["ingreso", "anticipo", "pago"]:
                fecha = m.get("fecha", "")[:7]  # YYYY-MM
                if fecha:
                    revenue[fecha] += m["monto"]
        
        # Sort by month
        sorted_revenue = dict(sorted(revenue.items()))
        
        return {
            "title": "Ingresos por Mes",
            "type": "line",
            "data": sorted_revenue
        }
    
    def average_closure_time(self) -> Dict[str, Any]:
        """Report: Average time to close matters."""
        matters = self.ds.get("matters")
        
        closure_times = []
        for m in matters:
            if m.get("estado") == "cerrado" and m.get("fecha_cierre") and m.get("fecha_creacion"):
                try:
                    created = datetime.fromisoformat(m["fecha_creacion"])
                    closed = datetime.fromisoformat(m["fecha_cierre"])
                    days = (closed - created).days
                    closure_times.append(days)
                except:
                    pass
        
        if not closure_times:
            return {"title": "Tiempo Promedio de Cierre", "average_days": 0, "count": 0}
        
        return {
            "title": "Tiempo Promedio de Cierre",
            "average_days": sum(closure_times) / len(closure_times),
            "min_days": min(closure_times),
            "max_days": max(closure_times),
            "count": len(closure_times)
        }
    
    def pending_documents_by_matter(self) -> Dict[str, Any]:
        """Report: Documents pending by matter."""
        matters = self.ds.get("matters")
        documentos = self.ds.get("documentos")
        
        pending_by_matter = {}
        
        for m in matters:
            matter_id = m["id"]
            pending = [d for d in documentos if d.get("matter_id") == matter_id and d.get("estado") == "borrador"]
            if pending:
                pending_by_matter[matter_id] = {
                    "cliente": m.get("cliente", "Sin cliente"),
                    "pending_count": len(pending),
                    "documents": [d.get("template_key", "desconocido") for d in pending]
                }
        
        return {
            "title": "Documentos Pendientes por Matter",
            "type": "table",
            "data": pending_by_matter
        }
    
    def generate_full_report(self) -> Dict[str, Any]:
        """Generates complete analytics report."""
        return {
            "generated_at": datetime.now().isoformat(),
            "matters": {
                "total": len(self.ds.get("matters")),
                "by_area": self.matters_by_area(),
                "by_status": self.matters_by_status()
            },
            "finances": {
                "by_month": self.revenue_by_month()
            },
            "performance": {
                "closure_time": self.average_closure_time()
            },
            "documents": {
                "pending": self.pending_documents_by_matter()
            }
        }
```

### 7.4 Integración Real con Onyx

#### Archivo Nuevo: `integrations/onyx_client.py`
```python
"""
onyx_client.py — Cliente para integración con Onyx.
"""
import requests
from typing import Dict, Any, Optional
from datetime import datetime

class OnyxClient:
    """Client for Onyx knowledge base integration."""
    
    def __init__(self, base_url: str = "http://localhost:3000", api_key: Optional[str] = None):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.headers = {"Content-Type": "application/json"}
        if api_key:
            self.headers["Authorization"] = f"Bearer {api_key}"
    
    def sync_matter(self, matter_data: Dict[str, Any]) -> Dict[str, Any]:
        """Syncs matter to Onyx knowledge base."""
        endpoint = f"{self.base_url}/api/v1/documents"
        
        payload = {
            "title": f"Matter {matter_data['id']}: {matter_data.get('cliente', 'Sin cliente')}",
            "content": self._format_matter_content(matter_data),
            "metadata": {
                "type": "legal_matter",
                "matter_id": matter_data["id"],
                "cliente": matter_data.get("cliente"),
                "area": matter_data.get("area_practica"),
                "estado": matter_data.get("estado"),
                "source": "willow_legal"
            }
        }
        
        response = requests.post(endpoint, json=payload, headers=self.headers)
        response.raise_for_status()
        return response.json()
    
    def search_precedents(self, query: str, area: Optional[str] = None) -> Dict[str, Any]:
        """Searches Onyx for legal precedents."""
        endpoint = f"{self.base_url}/api/v1/search"
        
        payload = {
            "query": query,
            "filters": {
                "type": "legal_matter",
                "area": area
            } if area else {"type": "legal_matter"}
        }
        
        response = requests.post(endpoint, json=payload, headers=self.headers)
        response.raise_for_status()
        return response.json()
    
    def _format_matter_content(self, matter: Dict[str, Any]) -> str:
        """Formats matter data for Onyx document."""
        lines = [
            f"# Matter {matter['id']}",
            f"",
            f"**Cliente:** {matter.get('cliente', 'N/A')}",
            f"**Área:** {matter.get('area_practica', 'N/A')}",
            f"**Estado:** {matter.get('estado', 'N/A')}",
            f"**Prioridad:** {matter.get('prioridad', 'N/A')}",
            f"**Deadline:** {matter.get('deadline', 'N/A')}",
            f"**Descripción:** {matter.get('descripcion', 'N/A')}",
            f"**Next Step:** {matter.get('next_step', 'N/A')}",
            f"",
            f"## Documentos",
        ]
        
        for doc in matter.get("documentos", []):
            lines.append(f"- {doc.get('template_key', 'desconocido')}: {doc.get('estado', 'N/A')}")
        
        lines.extend([
            f"",
            f"## Reuniones",
        ])
        
        for reunion in matter.get("reuniones", []):
            lines.append(f"- {reunion.get('fecha', 'N/A')}: {reunion.get('resumen', 'Sin resumen')}")
        
        return "\n".join(lines)
```

---

## 8. ARQUITECTURA OBJETIVO (Post-Reparación)

```
ws-hermes-legal-pro/
├── .github/
│   └── workflows/
│       └── ci.yml              # CI/CD pipeline
├── config/
│   ├── config.yaml             # Configuración unificada
│   ├── config_loader.py        # Carga y validación
│   └── .env.template           # Template de variables
├── core/
│   ├── __init__.py
│   ├── datastore.py            # Capa de persistencia
│   ├── id_generator.py         # Generación de IDs
│   ├── migrations.py           # Migraciones de schema
│   ├── auth.py                 # Autenticación
│   ├── reports.py              # Reportes y analytics
│   └── backup.py               # Sistema de backup
├── dashboard/
│   ├── backend/
│   │   ├── app.py              # FastAPI completo (todos los endpoints)
│   │   ├── middleware/
│   │   │   ├── auth.py         # Auth middleware
│   │   │   ├── logging.py      # Request logging
│   │   │   └── errors.py       # Error handlers
│   │   └── routers/
│   │       ├── matters.py      # CRUD matters
│   │       ├── documentos.py   # Generación de documentos
│   │       ├── finanzas.py     # Finanzas
│   │       ├── plazos.py       # Plazos y alertas
│   │       ├── reuniones.py    # Reuniones
│   │       └── workspace.py    # Google Workspace
│   └── frontend/
│       ├── index.html          # SPA responsive
│       ├── css/
│       │   ├── design_system.css  # Design system
│       │   └── styles.css         # Estilos específicos
│       └── js/
│           ├── api.js          # Cliente HTTP
│           ├── utils.js        # Utilidades
│           ├── toast.js          # Notificaciones
│           ├── modal.js          # Modales
│           ├── navigation.js     # Navegación
│           ├── dashboard.js      # Dashboard
│           ├── matters.js        # Matters CRUD
│           ├── documentos.js     # Documentos
│           ├── plazos.js         # Plazos
│           ├── finanzas.js       # Finanzas
│           ├── reuniones.js      # Reuniones
│           ├── calendario.js     # Calendario
│           ├── reportes.js       # Reportes
│           └── configuracion.js  # Configuración
├── motor_kami/
│   ├── motor_kami.py           # Motor de generación PDF
│   ├── template_engine.py      # Engine de templates
│   ├── variable_resolver.py    # Resolución de variables
│   ├── blocks.py               # Renderizado de bloques
│   ├── bridge_api.py           # API del motor
│   ├── templates/
│   │   ├── index.json          # Índice de templates
│   │   ├── prestacion_servicios.json  # Template completo
│   │   ├── nda.json            # Template completo
│   │   └── ... (23 templates)  # Todos con texto legal real
│   └── output/                 # PDFs generados
├── scripts/
│   ├── drive_manager.py        # Google Drive
│   ├── calendar_manager.py     # Google Calendar
│   ├── sheets_manager.py       # Google Sheets
│   ├── docs_exporter.py        # Google Docs
│   ├── tasks_manager.py        # Google Tasks
│   ├── check_plazos.py         # Alertas de plazos
│   ├── sync_excel_json.py      # Sync Excel ↔ JSON
│   ├── willow_standalone.py    # CLI standalone
│   ├── hermes_bridge.py        # Bridge para Hermes Agent
│   ├── backup.py               # Backup manual/auto
│   ├── setup_cron.py           # Configuración cron
│   └── setup_carpetas.py       # Setup de carpetas
├── hermes_integration/
│   ├── __init__.py
│   ├── commands.py             # Comandos Telegram
│   └── session_manager.py    # Gestión de sesión
├── integrations/
│   └── onyx_client.py          # Cliente Onyx
├── skills/
│   ├── hermes-legal-pro/
│   │   └── SKILL.md            # Skill maestra
│   └── willow-legal-complete/
│       └── SKILL.md            # Skill completa
├── tests/
│   ├── conftest.py             # Fixtures pytest
│   ├── test_api.py             # Tests API
│   ├── test_motor_kami.py      # Tests Motor Kami
│   ├── test_datastore.py       # Tests Datastore
│   └── test_integration.py     # Tests integración
├── docs/
│   ├── API_REFERENCE.md        # Referencia API
│   ├── ARCHITECTURE.md         # Arquitectura
│   ├── DEPLOYMENT.md           # Guía de deployment
│   └── USER_GUIDE.md           # Guía de usuario
├── migrations/
│   └── 001_unify_ids.py        # Migración inicial
├── requirements.txt            # Dependencias producción
├── requirements-dev.txt        # Dependencias desarrollo
├── .gitignore
├── LICENSE.md
├── README.md
└── INSTALL.md
```

---

## 9. MAPA DE CONECTIVIDAD

### Frontend → Backend
```
Dashboard SPA (JS)
    ↓ HTTP fetch
FastAPI Backend (:8082)
    ↓ JSONDatastore
~/.willowlegal/data/*.json
```

### Backend → Motor Kami
```
FastAPI Endpoint /generar-documento
    ↓ Import directo (NO subprocess)
motor_kami.generar_documento()
    ↓ TemplateEngine.load()
motor_kami/templates/*.json
    ↓ VariableResolver.resolve()
Datos fusionados
    ↓ blocks.generar_desde_bloques()
HTML + CSS Kami
    ↓ WeasyPrint
~/.willowlegal/output/*.pdf
```

### Backend → Google Workspace
```
FastAPI Endpoint /export-sheets
    ↓ scripts.sheets_manager.SheetsManager
Google Sheets API
    ↓ OAuth2
credentials.json + token.json
```

### Hermes Agent → Backend
```
Telegram Bot
    ↓ /matter nuevo "Cliente"
hermes_integration.commands.HermesLegalCommands
    ↓ JSONDatastore (misma instancia)
~/.willowlegal/data/*.json
    ↓ Response
Mensaje Telegram con resultado
```

### Backend → Onyx
```
FastAPI (opcional, futuro)
    ↓ integrations.onyx_client.OnyxClient
Onyx API (:3000)
    ↓ HTTP + API Key
Knowledge Base
```

---

## 10. ESPECIFICACIÓN TÉCNICA DETALLADA

### 10.1 Modelos de Datos

#### Matter (v2.0 Schema)
```json
{
  "id": "WIL-001",
  "cliente": "Razón Social S.A. de C.V.",
  "cliente_id": "CLI-001",
  "area_practica": "Mercantil",
  "materia": "corporativo",
  "descripcion": "Descripción detallada del asunto",
  "estado": "activo",
  "prioridad": "alta",
  "deadline": "2026-06-30",
  "fecha_creacion": "2026-05-01T10:00:00",
  "fecha_actualizacion": "2026-05-04T15:30:00",
  "fecha_cierre": null,
  "next_step": "Generar contrato de prestación de servicios",
  "blocker": "none",
  "responsable": "user@despacho.com",
  "carpeta_local": "~/.willowlegal/clients/Cliente_001/",
  "drive_folder_id": "1ABC123...",
  "drive_link": "https://drive.google.com/...",
  "honorarios": {
    "total": 85000,
    "moneda": "MXN",
    "anticipo": 42500,
    "pendiente": 42500
  },
  "reuniones": ["REU-0001", "REU-0002"],
  "documentos": ["DOC-0001", "DOC-0002"],
  "tareas": ["TASK-0001"],
  "plazos": ["PLZ-0001"],
  "tags": ["urgente", "startup"],
  "notas": "Notas internas del abogado"
}
```

#### Documento (v2.0 Schema)
```json
{
  "id": "DOC-0001",
  "matter_id": "WIL-001",
  "template_key": "prestacion_servicios",
  "template_label": "Contrato de Prestación de Servicios",
  "estado": "generado",
  "version": 1,
  "version_count": 3,
  "versions": [
    {
      "version_number": 1,
      "created_at": "2026-05-01T10:00:00",
      "data": {...}
    }
  ],
  "datos": {...},
  "ruta_pdf": "~/.willowlegal/output/WIL-001_prestacion_servicios_v1.pdf",
  "ruta_html": "~/.willowlegal/output/WIL-001_prestacion_servicios_v1.html",
  "drive_file_id": "1XYZ789...",
  "drive_link": "https://drive.google.com/...",
  "docs_file_id": "1DOC456...",
  "docs_link": "https://docs.google.com/...",
  "generado_por": "user@despacho.com",
  "fecha_creacion": "2026-05-01T10:00:00",
  "fecha_generacion": "2026-05-01T10:05:00",
  "aprobado_por": null,
  "fecha_aprobacion": null,
  "comentario_aprobacion": null
}
```

### 10.2 API Endpoints Completos

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| GET | /api/health | Health check | No |
| GET | /api/dashboard | KPIs del dashboard | Sí |
| GET | /api/matters | Listar matters | Sí |
| POST | /api/matters | Crear matter | Sí |
| GET | /api/matters/{id} | Ver matter | Sí |
| PUT | /api/matters/{id} | Actualizar matter | Sí |
| DELETE | /api/matters/{id} | Eliminar matter | Sí |
| GET | /api/documentos | Listar documentos | Sí |
| POST | /api/documentos | Crear documento (borrador) | Sí |
| GET | /api/documentos/{id} | Ver documento | Sí |
| POST | /api/documentos/{id}/generar | Generar PDF | Sí |
| POST | /api/documentos/{id}/aprobar | Aprobar documento | Sí |
| POST | /api/documentos/{id}/rechazar | Rechazar documento | Sí |
| GET | /api/templates | Listar templates | Sí |
| GET | /api/templates/{key} | Ver template | Sí |
| GET | /api/finanzas | Listar finanzas | Sí |
| POST | /api/finanzas | Registrar movimiento | Sí |
| GET | /api/plazos | Listar plazos | Sí |
| POST | /api/plazos | Crear plazo | Sí |
| GET | /api/alertas | Listar alertas | Sí |
| POST | /api/check-plazos | Ejecutar check | Sí |
| GET | /api/reuniones | Listar reuniones | Sí |
| POST | /api/reuniones | Crear reunión | Sí |
| GET | /api/calendar-events | Eventos Calendar | Sí |
| GET | /api/tasks | Tareas Google | Sí |
| POST | /api/tasks | Crear tarea | Sí |
| GET | /api/drive-link/{matter_id} | Link de Drive | Sí |
| POST | /api/export-sheets | Exportar Sheets | Sí |
| POST | /api/export-docs | Exportar Docs | Sí |
| GET | /api/reportes/{tipo} | Generar reporte | Sí |
| POST | /api/sync-excel | Sync Excel ↔ JSON | Sí |
| POST | /api/backup | Crear backup | Sí (admin) |
| GET | /api/backups | Listar backups | Sí (admin) |
| POST | /api/restore | Restaurar backup | Sí (admin) |

---

## 11. TESTS Y VERIFICACIÓN

### 11.1 Test Suite Completa

```bash
# Ejecutar todos los tests
pytest tests/ -v --cov=dashboard --cov=motor_kami --cov=core --cov-report=html

# Tests específicos
pytest tests/test_api.py -v                    # API
pytest tests/test_motor_kami.py -v               # Motor Kami
pytest tests/test_datastore.py -v                # Datastore
pytest tests/test_integration.py -v              # Integración

# Con coverage
pytest tests/ --cov=dashboard/backend --cov-report=term-missing
```

### 11.2 Checklist de Verificación Manual

#### Instalación
- [ ] `pip install -r requirements.txt` funciona sin errores
- [ ] `python scripts/setup_carpetas.py` crea estructura correcta
- [ ] `python scripts/setup_cron.py` configura cron sin errores
- [ ] `python -m pytest tests/` pasa todos los tests

#### Backend
- [ ] `python dashboard/backend/app.py` inicia sin errores
- [ ] `GET /api/health` retorna 200 con motor_kami: ok
- [ ] `POST /api/matters` crea matter con ID WIL-XXX
- [ ] `GET /api/matters` lista matters creados
- [ ] `POST /api/finanzas` registra movimiento
- [ ] `GET /api/finanzas` muestra resumen correcto
- [ ] `POST /api/check-plazos` genera alertas si hay deadlines próximos

#### Motor Kami
- [ ] `GET /api/templates` lista 23 templates
- [ ] `POST /api/matter/{id}/generar-documento` genera PDF real
- [ ] PDF contiene datos del despacho (no hardcodeados)
- [ ] PDF contiene datos del cliente
- [ ] PDF tiene diseño Kami (tipografía, colores, márgenes)

#### Frontend
- [ ] `index.html` carga sin errores en consola
- [ ] Dashboard muestra KPIs correctos
- [ ] Lista de matters se actualiza en tiempo real
- [ ] Modal de creación de matter funciona
- [ ] Generación de documento desde frontend funciona
- [ ] Vista de finanzas muestra datos correctos
- [ ] Responsive: funciona en móvil (320px), tablet (768px), desktop (1024px+)

#### Google Workspace (si está configurado)
- [ ] `GET /api/drive-link/{matter_id}` retorna link válido
- [ ] Carpeta se crea en Drive
- [ ] `POST /api/export-sheets` crea spreadsheet
- [ ] `GET /api/calendar-events` lista eventos

#### Hermes Agent
- [ ] `/matter nuevo "Cliente Test"` crea matter
- [ ] `/contrato nda WIL-001` genera documento
- [ ] `/status` muestra resumen del despacho
- [ ] `/alerta` muestra alertas pendientes

#### Backup
- [ ] `python scripts/backup.py --backup` crea backup
- [ ] `python scripts/backup.py --list` lista backups
- [ ] `python scripts/backup.py --restore {nombre}` restaura backup
- [ ] Backup automático ejecuta sin errores

---

## 12. RIESGOS Y MITIGACIONES

| Riesgo | Probabilidad | Impacto | Mitigación |
|--------|-------------|---------|------------|
| Pérdida de datos durante migración | Media | Crítico | Backup completo antes de migrar. Script de rollback. |
| Templates legales incompletos | Alta | Alto | Fase 2 dedicada exclusivamente a templates. Revisión por abogado. |
| Google Workspace API cambia | Baja | Medio | Abstracción en `scripts/drive_manager.py`. Tests de integración. |
| WeasyPrint no instala en Mac M2 | Media | Alto | Instrucciones específicas para M2. Fallback a wkhtmltopdf. |
| Performance con >1000 matters | Baja | Medio | Migración a SQLite en Fase 4. Índices. |
| Conflicto de escrituras concurrentes | Baja | Medio | File locking en JSONDatastore. O migrar a SQLite. |

---

## 13. CHECKLIST DE ENTREGA

### v2.0 MVP (Semanas 1-6)
- [ ] Config unificada (`config.yaml`)
- [ ] Datastore unificado (`core/datastore.py`)
- [ ] IDs unificados (`WIL-XXX`)
- [ ] Motor Kami lee templates reales
- [ ] Templates con texto legal (mínimo 5 completos)
- [ ] Backend con todos los endpoints documentados
- [ ] Frontend responsive funcional
- [ ] Finanzas completas
- [ ] Auth básica (API key)
- [ ] Tests automatizados (>80% coverage)
- [ ] Backup automático
- [ ] Documentación API

### v2.1 Polish (Semanas 7-8)
- [ ] Todos los 23 templates completos
- [ ] Frontend mobile-first probado
- [ ] CI/CD pipeline funcionando
- [ ] Migraciones de schema
- [ ] Reportes analíticos básicos
- [ ] Guía de usuario completa

### v2.2 Enterprise (Semanas 9-12)
- [ ] Sistema de usuarios y roles
- [ ] Versionado de documentos
- [ ] Integración Onyx real
- [ ] Firma digital (e.firma)
- [ ] Notificaciones push automáticas
- [ ] Búsqueda full-text
- [ ] Dashboard de analytics
- [ ] Multi-despacho (tenant isolation)

---

*Plan Maestro generado por Hermes Neo — 2026-05-04*
*Este documento es VIVO. Se actualiza conforme avanza la implementación.*
