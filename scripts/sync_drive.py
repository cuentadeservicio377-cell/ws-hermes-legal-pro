#!/usr/bin/env python3
"""
sync_drive.py — Sincronización con Google Drive v2 (OAuth2 directo)
Hermes Legal Pro v4.0

Uso:
    python3 scripts/sync_drive.py --dry-run
    python3 scripts/sync_drive.py --sync
    python3 scripts/sync_drive.py --auth  # Forzar re-autenticación

Requiere:
    - pip3 install google-auth-oauthlib google-api-python-client
    - Client secret configurado en config/client_secret.json
    - DRIVE_FOLDER_ID en config/.env
"""

import os
import sys
import json
import argparse
from pathlib import Path

# Google APIs
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

BASE_DIR = Path(__file__).parent.parent
ENV_FILE = BASE_DIR / "config" / ".env"
CLIENT_SECRET_FILE = BASE_DIR / "config" / "client_secret.json"
TOKEN_FILE = BASE_DIR / "config" / "token.json"
CLIENTES_DIR = Path.home() / "WillowLegal" / "01_Clientes"

# OAuth scopes
SCOPES = ["https://www.googleapis.com/auth/drive"]

# ── Config ────────────────────────────────────────────────────
def load_env():
    env = {}
    if ENV_FILE.exists():
        with open(ENV_FILE, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    env[key] = value
    return env

def get_credentials(force_auth=False):
    """Obtener credenciales de Google, autenticando si es necesario"""
    creds = None
    
    # Cargar token existente
    if TOKEN_FILE.exists() and not force_auth:
        try:
            creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)
        except Exception as e:
            print(f"⚠️  Token inválido: {e}")
            creds = None
    
    # Refrescar o crear nuevo
    if creds and creds.expired and creds.refresh_token:
        try:
            creds.refresh(Request())
            print("✅ Token refrescado")
        except Exception as e:
            print(f"⚠️  No se pudo refrescar token: {e}")
            creds = None
    
    if not creds:
        if not CLIENT_SECRET_FILE.exists():
            # Intentar copiar desde gws config
            gws_secret = Path.home() / ".config" / "gws" / "client_secret.json"
            if gws_secret.exists():
                CLIENT_SECRET_FILE.parent.mkdir(parents=True, exist_ok=True)
                import shutil
                shutil.copy(gws_secret, CLIENT_SECRET_FILE)
                print(f"📋 Client secret copiado desde gws config")
            else:
                print(f"❌ No se encontró client_secret.json")
                print(f"   Ubica tu archivo de credenciales de Google OAuth y cópialo a:")
                print(f"   {CLIENT_SECRET_FILE}")
                return None
        
        print("🔐 Iniciando autenticación con Google...")
        print("   Se abrirá una ventana del navegador. Por favor inicia sesión con:")
        print("   cuenta de servicio377@gmail.com")
        print()
        
        try:
            flow = InstalledAppFlow.from_client_secrets_file(str(CLIENT_SECRET_FILE), SCOPES)
            creds = flow.run_local_server(port=0)
            
            # Guardar token
            TOKEN_FILE.parent.mkdir(parents=True, exist_ok=True)
            with open(TOKEN_FILE, "w") as token:
                token.write(creds.to_json())
            print("✅ Autenticación completada y guardada")
        except Exception as e:
            print(f"❌ Error en autenticación: {e}")
            return None
    
    return creds

# ── Drive helpers ─────────────────────────────────────────────
def get_drive_service(creds):
    return build("drive", "v3", credentials=creds, static_discovery=False)

def list_drive_files(service, folder_id):
    """Listar archivos en carpeta de Drive"""
    files = []
    page_token = None
    query = f"'{folder_id}' in parents and trashed = false"
    
    while True:
        response = service.files().list(
            q=query,
            spaces="drive",
            fields="nextPageToken, files(id, name, mimeType, modifiedTime, size)",
            pageToken=page_token,
            pageSize=100
        ).execute()
        
        files.extend(response.get("files", []))
        page_token = response.get("nextPageToken")
        if not page_token:
            break
    
    return files

def upload_file(service, local_path, folder_id):
    """Subir archivo a Drive"""
    from googleapiclient.http import MediaFileUpload
    
    file_metadata = {
        "name": local_path.name,
        "parents": [folder_id]
    }
    media = MediaFileUpload(str(local_path), resumable=True)
    
    file = service.files().create(
        body=file_metadata,
        media_body=media,
        fields="id, name, mimeType"
    ).execute()
    
    return file

def create_folder(service, name, parent_id):
    """Crear carpeta en Drive"""
    file_metadata = {
        "name": name,
        "mimeType": "application/vnd.google-apps.folder",
        "parents": [parent_id]
    }
    folder = service.files().create(body=file_metadata, fields="id, name").execute()
    return folder

# ── Sync logic ────────────────────────────────────────────────
def scan_local_files():
    archivos = []
    if CLIENTES_DIR.exists():
        for f in CLIENTES_DIR.rglob("*"):
            if f.is_file():
                archivos.append({
                    "ruta": str(f),
                    "relativa": str(f.relative_to(CLIENTES_DIR)),
                    "nombre": f.name,
                    "tamaño": f.stat().st_size,
                    "modificado": f.stat().st_mtime
                })
    return archivos

def sync_drive(dry_run=True, force_auth=False):
    env = load_env()
    folder_id = env.get("DRIVE_FOLDER_ID", "")
    
    print("☁️  Sincronización Google Drive")
    print("─" * 50)
    
    # Autenticar
    creds = get_credentials(force_auth=force_auth)
    if not creds:
        print("\n❌ No se pudieron obtener credenciales de Google")
        print("\n📋 Pasos para configurar:")
        print("   1. Asegúrate de tener config/client_secret.json")
        print("   2. Ejecuta: python3 scripts/sync_drive.py --auth")
        print("   3. Inicia sesión con cuenta de servicio377@gmail.com")
        print("   4. Copia el ID de la carpeta de Drive a config/.env:")
        print("      DRIVE_FOLDER_ID=tu_carpeta_id")
        return False
    
    print("✅ Credenciales válidas")
    
    if not folder_id:
        print("❌ DRIVE_FOLDER_ID no configurado")
        print(f"   Crea {ENV_FILE} con:")
        print("   DRIVE_FOLDER_ID=tu_carpeta_id")
        print("\n   Para obtener el ID de carpeta:")
        print("   1. Abre Drive en el navegador")
        print("   2. Navega a la carpeta WillowLegal/01_Clientes")
        print("   3. Copia el ID de la URL: .../folders/ID_AQUI")
        return False
    
    print(f"📁 Carpeta Drive: {folder_id}")
    
    service = get_drive_service(creds)
    
    # Escanear locales
    locales = scan_local_files()
    print(f"📂 Archivos locales: {len(locales)}")
    
    # Listar Drive
    try:
        drive_files = list_drive_files(service, folder_id)
        print(f"☁️  Archivos en Drive: {len(drive_files)}")
    except HttpError as e:
        print(f"⚠️  Error accediendo a Drive: {e}")
        return False
    
    # Calcular diff
    drive_names = {f["name"]: f for f in drive_files}
    para_subir = [f for f in locales if f["nombre"] not in drive_names]
    
    print("\n📊 Resumen:")
    print(f"   Nuevos para subir: {len(para_subir)}")
    print(f"   Ya en Drive: {len(locales) - len(para_subir)}")
    
    if dry_run:
        print("\n🧪 MODO DRY-RUN — No se realizarán cambios")
        if para_subir:
            print("\n📤 Archivos que se subirían:")
            for f in para_subir[:10]:
                print(f"   • {f['relativa']} ({f['tamaño']:,} bytes)")
            if len(para_subir) > 10:
                print(f"   ... y {len(para_subir) - 10} más")
        return True
    
    # Sync real
    if not para_subir:
        print("\n✅ Todo sincronizado")
        return True
    
    print(f"\n🚀 Subiendo {len(para_subir)} archivos...")
    exitosos = 0
    fallidos = 0
    
    for f in para_subir:
        try:
            upload_file(service, Path(f["ruta"]), folder_id)
            print(f"   ✅ {f['nombre']}")
            exitosos += 1
        except Exception as e:
            print(f"   ❌ {f['nombre']}: {e}")
            fallidos += 1
    
    print(f"\n✅ Sync completado: {exitosos} exitosos, {fallidos} fallidos")
    return fallidos == 0

# ── Main ──────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="Sync con Google Drive")
    parser.add_argument("--dry-run", action="store_true", help="Simular sin hacer cambios")
    parser.add_argument("--sync", action="store_true", help="Ejecutar sync real")
    parser.add_argument("--auth", action="store_true", help="Forzar re-autenticación")
    args = parser.parse_args()
    
    if args.auth:
        # Solo autenticar
        creds = get_credentials(force_auth=True)
        sys.exit(0 if creds else 1)
    
    dry_run = not args.sync
    success = sync_drive(dry_run=dry_run, force_auth=False)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
