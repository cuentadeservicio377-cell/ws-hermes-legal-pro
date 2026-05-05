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
        
        meta = data.get("metadata", {})
        return cls(
            key=key,
            label=meta.get("label", key),
            area=meta.get("area", "General"),
            materia=meta.get("materia", "General"),
            metadata=meta,
            recommended_blocks=data.get("recommended_blocks", []),
            document_data_template=data.get("document_data_template", {}),
            required_variables=data.get("required_variables", [])
        )
    
    def validate_variables(self, provided: Dict[str, Any]) -> List[str]:
        missing = []
        for var in self.required_variables:
            parts = var.split(".")
            value = provided
            for part in parts:
                if isinstance(value, dict):
                    value = value.get(part)
                else:
                    value = None
                    break
            if not value:
                missing.append(var)
        return missing
