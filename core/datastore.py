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
            "expedientes": self.base_path / "expedientes.json",
            "documentos": self.base_path / "documentos.json",
            "reuniones": self.base_path / "reuniones.json",
            "alertas": self.base_path / "alertas.json",
            "finanzas": self.base_path / "finanzas.json",
            "plazos": self.base_path / "plazos.json",
            "aprobaciones": self.base_path / "aprobaciones.json",
            "usuarios": self.base_path / "usuarios.json",
            "clientes": self.base_path / "clientes.json",
            "session": self.base_path / "session.json"
        }
        
        for name, path in self.files.items():
            if not path.exists():
                self._write_json(path, self._default_data(name))
    
    def _default_data(self, name: str) -> Any:
        defaults = {
            "matters": [],
            "expedientes": [],
            "documentos": [],
            "reuniones": [],
            "alertas": [],
            "finanzas": {"movimientos": [], "resumen": {}},
            "plazos": [],
            "aprobaciones": [],
            "usuarios": [],
            "clientes": [],
            "session": {"matter_active": None, "expediente_activo": None}
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
