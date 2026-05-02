#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hermes Bridge — Entry point para comandos desde Hermes Agent.

Uso desde Hermes:
    python3 scripts/hermes_bridge.py matter nuevo "Cliente S.A."
    python3 scripts/hermes_bridge.py contrato nda WIL-001
    python3 scripts/hermes_bridge.py plazo WIL-001 "Audiencia" 2026-05-20
    python3 scripts/hermes_bridge.py status
    python3 scripts/hermes_bridge.py alerta
"""

import sys
import os
from pathlib import Path

# Añadir repo al path
REPO_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(REPO_DIR))

from hermes_integration.commands import HermesLegalCommands
from hermes_integration.session_manager import LegalSessionManager


def print_usage():
    print("""
Uso: hermes_bridge.py <comando> [args...]

Comandos:
  matter nuevo <nombre> [area=...] [prioridad=...]
  matter list
  matter <id>
  
  contrato <template> [matter_id]
  templates
  
  plazo <matter_id> <descripcion> <fecha>
  alerta [matter_id]
  
  anticipo <matter_id> <monto> <concepto>
  honorario <matter_id> <monto> <concepto>
  factura <matter_id> <monto> <concepto>
  finanzas [matter_id]
  
  status
  
Ejemplos:
  python3 scripts/hermes_bridge.py matter nuevo "Innovatech" area=Corporativo
  python3 scripts/hermes_bridge.py contrato nda
  python3 scripts/hermes_bridge.py plazo WIL-001 "Audiencia" 2026-05-20
  python3 scripts/hermes_bridge.py status
""")


def parse_kwargs(args):
    """Parsear argumentos tipo key=value."""
    kwargs = {}
    clean_args = []
    for arg in args:
        if '=' in arg:
            key, value = arg.split('=', 1)
            kwargs[key] = value
        else:
            clean_args.append(arg)
    return clean_args, kwargs


def main():
    if len(sys.argv) < 2:
        print_usage()
        sys.exit(1)
    
    cmd = sys.argv[1]
    args, kwargs = parse_kwargs(sys.argv[2:])
    
    # Inicializar
    commands = HermesLegalCommands()
    session = LegalSessionManager()
    
    # ============================================================
    # MATTER
    # ============================================================
    if cmd == "matter":
        if not args:
            print("❌ Falta subcomando. Uso: matter nuevo|list|<id>")
            sys.exit(1)
        
        subcmd = args[0]
        
        if subcmd == "nuevo":
            if len(args) < 2:
                print("❌ Falta nombre del matter")
                sys.exit(1)
            nombre = " ".join(args[1:])
            result = commands.crear_matter(nombre, **kwargs)
            if result["status"] == "ok":
                session.set_matter(result["matter_id"])
            print(result["mensaje"])
        
        elif subcmd == "list":
            result = commands.listar_matters()
            print(result["mensaje"])
        
        else:
            # Ver matter específico
            matter_id = subcmd
            result = commands.ver_matter(matter_id)
            print(result["mensaje"])
    
    # ============================================================
    # CONTRATO / DOCUMENTO
    # ============================================================
    elif cmd == "contrato":
        if not args:
            print("❌ Falta template. Uso: contrato <template> [matter_id]")
            sys.exit(1)
        
        template = args[0]
        matter_id = args[1] if len(args) > 1 else session.get_matter()
        
        if not matter_id:
            print("❌ No hay matter activo. Usa 'matter nuevo' primero, o especifica matter_id")
            sys.exit(1)
        
        result = commands.generar_documento(template, matter_id, **kwargs)
        print(result["mensaje"])
    
    elif cmd == "templates":
        result = commands.listar_templates()
        print(result["mensaje"])
    
    # ============================================================
    # PLAZO / ALERTA
    # ============================================================
    elif cmd == "plazo":
        if len(args) < 3:
            print("❌ Uso: plazo <matter_id> <descripcion> <fecha>")
            sys.exit(1)
        
        matter_id = args[0]
        descripcion = args[1]
        fecha = args[2]
        
        result = commands.crear_plazo(matter_id, descripcion, fecha, **kwargs)
        print(result["mensaje"])
    
    elif cmd == "alerta":
        matter_id = args[0] if args else None
        result = commands.ver_alertas(matter_id)
        print(result["mensaje"])
    
    # ============================================================
    # FINANZAS
    # ============================================================
    elif cmd in ("anticipo", "honorario", "factura"):
        if len(args) < 3:
            print(f"❌ Uso: {cmd} <matter_id> <monto> <concepto>")
            sys.exit(1)
        
        matter_id = args[0]
        monto = args[1]
        concepto = " ".join(args[2:])
        
        result = commands.registrar_finanza(matter_id, monto, concepto, tipo=cmd, **kwargs)
        print(result["mensaje"])
    
    elif cmd == "finanzas":
        matter_id = args[0] if args else None
        result = commands.ver_finanzas(matter_id)
        print(result["mensaje"])
    
    # ============================================================
    # STATUS
    # ============================================================
    elif cmd == "status":
        result = commands.status_despacho()
        print(result["mensaje"])
    
    else:
        print(f"❌ Comando desconocido: {cmd}")
        print_usage()
        sys.exit(1)


if __name__ == "__main__":
    main()
