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
