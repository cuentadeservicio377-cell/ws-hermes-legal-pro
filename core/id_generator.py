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
