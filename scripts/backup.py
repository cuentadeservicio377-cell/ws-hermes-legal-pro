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
    print(f"BACKUP CREADO: {backup_path}")
    return backup_path

def list_backups():
    config = Config.load()
    backup_dir = Path(config.datastore.backup_dir)
    if not backup_dir.exists():
        print("No hay backups")
        return
    
    backups = sorted(backup_dir.iterdir(), key=lambda p: p.stat().st_mtime, reverse=True)
    print(f"\nBACKUPS ({len(backups)}):")
    for b in backups[:10]:
        mtime = datetime.fromtimestamp(b.stat().st_mtime)
        print(f"  - {b.name} — {mtime.strftime('%Y-%m-%d %H:%M')}")
    
    # Limpiar backups antiguos (más de 30 días)
    cutoff = datetime.now().timestamp() - (30 * 86400)
    for b in backups:
        if b.stat().st_mtime < cutoff:
            import shutil
            shutil.rmtree(b)
            print(f"ELIMINADO backup antiguo: {b.name}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sistema de backup Willow Legal Pro")
    parser.add_argument("--backup", action="store_true", help="Crear backup manual")
    parser.add_argument("--list", action="store_true", help="Listar backups")
    args = parser.parse_args()
    
    if args.backup:
        backup_manual()
    elif args.list:
        list_backups()
    else:
        parser.print_help()
