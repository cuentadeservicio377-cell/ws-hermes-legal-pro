#!/usr/bin/env python3
"""
Drive Manager — Google Drive como filesystem principal del despacho.

Todo documento generado se sube automáticamente a Drive.
Estructura:
    WillowLegal/
    ├── 01_Clientes/
    │   └── {Cliente}/
    │       ├── 01_Intake/
    │       ├── 02_Contratos/
    │       │   ├── Borradores/
    │       │   └── Firmados/
    │       ├── 03_Correspondencia/
    │       ├── 04_Litigio/
    │       ├── 05_Facturacion/
    │       ├── 06_Entregables/
    │       │   └── Documentos_Finales/
    │       └── 07_Archivo/
    └── 02_Administracion/
"""

import os
import json
from pathlib import Path
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = [
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/documents',
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/calendar',
    'https://www.googleapis.com/auth/tasks'
]

class DriveManager:
    def __init__(self, base_folder_name="WillowLegal"):
        self.creds = self._get_credentials()
        self.service = build('drive', 'v3', credentials=self.creds)
        self.base_folder_id = self._get_or_create_folder(base_folder_name)
        
    def _get_credentials(self):
        """Obtener credenciales OAuth2 usando token existente."""
        token_path = Path("config/token.json")
        creds_path = Path("config/client_secret.json")
        
        # PRIORIDAD 1: Usar token existente
        if token_path.exists():
            try:
                creds = Credentials.from_authorized_user_file(str(token_path), SCOPES)
                if creds and creds.valid:
                    print("✅ Token existente válido")
                    return creds
                elif creds and creds.expired and creds.refresh_token:
                    print("🔄 Refrescando token...")
                    creds.refresh(Request())
                    # Guardar token refrescado
                    with open(token_path, 'w') as token:
                        token.write(creds.to_json())
                    print("✅ Token refrescado")
                    return creds
            except Exception as e:
                print(f"⚠️  Error con token existente: {e}")
        
        # PRIORIDAD 2: Autenticar nuevo (solo si no hay token)
        if creds_path.exists():
            print("🔐 Iniciando autenticación nueva...")
            flow = InstalledAppFlow.from_client_secrets_file(str(creds_path), SCOPES)
            creds = flow.run_local_server(port=0)
            
            # Guardar token
            token_path.parent.mkdir(parents=True, exist_ok=True)
            with open(token_path, 'w') as token:
                token.write(creds.to_json())
            print("✅ Nuevo token guardado")
            return creds
        else:
            raise FileNotFoundError(f"No existe {creds_path}. Descargar de Google Cloud Console.")
    
    def _get_or_create_folder(self, name, parent_id=None):
        """Obtener o crear carpeta en Drive."""
        query = f"mimeType='application/vnd.google-apps.folder' and name='{name}' and trashed=false"
        if parent_id:
            query += f" and '{parent_id}' in parents"
        
        results = self.service.files().list(q=query, spaces='drive', fields='files(id, name)').execute()
        items = results.get('files', [])
        
        if items:
            return items[0]['id']
        
        # Crear carpeta
        metadata = {
            'name': name,
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': [parent_id] if parent_id else []
        }
        folder = self.service.files().create(body=metadata, fields='id').execute()
        return folder['id']
    
    def create_client_structure(self, client_name):
        """Crear estructura completa de carpetas para un cliente."""
        # Carpeta del cliente
        client_folder_id = self._get_or_create_folder(client_name, self.base_folder_id)
        
        # Subcarpetas
        subfolders = [
            "01_Intake",
            "02_Contratos",
            "03_Correspondencia",
            "04_Litigio",
            "05_Facturacion",
            "06_Entregables",
            "07_Archivo"
        ]
        
        for subfolder in subfolders:
            self._get_or_create_folder(subfolder, client_folder_id)
        
        # Subcarpetas especiales
        contratos_id = self._get_or_create_folder("02_Contratos", client_folder_id)
        self._get_or_create_folder("Borradores", contratos_id)
        self._get_or_create_folder("Firmados", contratos_id)
        
        entregables_id = self._get_or_create_folder("06_Entregables", client_folder_id)
        self._get_or_create_folder("Documentos_Finales", entregables_id)
        
        return client_folder_id
    
    def upload_pdf(self, pdf_path, client_name, subfolder="06_Entregables/Documentos_Finales"):
        """Subir PDF a carpeta del cliente en Drive."""
        from googleapiclient.http import MediaFileUpload
        
        # Navegar a subcarpeta
        client_folder_id = self._get_or_create_folder(client_name, self.base_folder_id)
        current_id = client_folder_id
        for part in subfolder.split('/'):
            current_id = self._get_or_create_folder(part, current_id)
        
        # Subir archivo
        file_metadata = {
            'name': Path(pdf_path).name,
            'parents': [current_id]
        }
        media = MediaFileUpload(pdf_path, mimetype='application/pdf')
        file = self.service.files().create(body=file_metadata, media_body=media, fields='id, webViewLink').execute()
        
        return {
            'id': file['id'],
            'link': file.get('webViewLink', ''),
            'mensaje': f"📄 PDF subido a Drive: {file['webViewLink']}"
        }
    
    def list_client_files(self, client_name):
        """Listar archivos de un cliente."""
        client_folder_id = self._get_or_create_folder(client_name, self.base_folder_id)
        
        query = f"'{client_folder_id}' in parents and trashed=false"
        results = self.service.files().list(q=query, fields='files(id, name, mimeType, webViewLink, modifiedTime)').execute()
        
        return results.get('files', [])

if __name__ == "__main__":
    # Test
    dm = DriveManager()
    print(f"✅ Drive Manager inicializado. Base folder: {dm.base_folder_id}")
    
    # Crear estructura de prueba
    test_folder = dm.create_client_structure("Test_Cliente")
    print(f"✅ Estructura creada: {test_folder}")
