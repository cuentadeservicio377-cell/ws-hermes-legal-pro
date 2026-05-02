#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session Manager — Gestión de contexto entre Hermes y Legal.

Mantiene el matter activo para comandos subsiguientes.
"""

import json
from pathlib import Path
from datetime import datetime


class LegalSessionManager:
    """
    Mantiene contexto de sesión legal activa entre interacciones.
    
    Uso:
        session = LegalSessionManager()
        session.set_matter("WIL-001")  # Fijar contexto
        
        # En comandos subsiguientes:
        matter_id = session.get_matter()  # "WIL-001"
    """
    
    def __init__(self, session_file="~/.hermes/legal_session.json"):
        self.session_file = Path(session_file).expanduser()
        self.session = self._load()
    
    def _load(self) -> dict:
        """Cargar sesión existente o crear nueva."""
        if self.session_file.exists():
            try:
                with open(self.session_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        return {
            "matter_active": None,
            "usuario": "hermes",
            "historial": [],
            "creado": datetime.now().isoformat()
        }
    
    def set_matter(self, matter_id: str):
        """Fijar matter activo."""
        self.session["matter_active"] = matter_id
        self.session["historial"].append({
            "accion": "set_matter",
            "matter_id": matter_id,
            "timestamp": datetime.now().isoformat()
        })
        self._save()
    
    def get_matter(self) -> str:
        """Obtener matter activo actual."""
        return self.session.get("matter_active")
    
    def clear_matter(self):
        """Limpiar matter activo."""
        self.session["matter_active"] = None
        self.session["historial"].append({
            "accion": "clear_matter",
            "timestamp": datetime.now().isoformat()
        })
        self._save()
    
    def get_historial(self, limite: int = 10) -> list:
        """Obtener últimas acciones."""
        return self.session["historial"][-limite:]
    
    def _save(self):
        """Guardar sesión a disco."""
        self.session_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.session_file, 'w', encoding='utf-8') as f:
            json.dump(self.session, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    # Test
    sm = LegalSessionManager()
    sm.set_matter("WIL-TEST-001")
    print(f"Matter activo: {sm.get_matter()}")
    print(f"Historial: {len(sm.get_historial())} acciones")
    sm.clear_matter()
    print(f"Después de clear: {sm.get_matter()}")
