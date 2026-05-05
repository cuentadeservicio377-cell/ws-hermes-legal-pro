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
        
        if path in self.despacho:
            return self.despacho[path]
        
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
