#!/usr/bin/env python3
"""
Docs Exporter — Convertir documentos legales a Google Docs editables.
"""

from googleapiclient.discovery import build
from scripts.drive_manager import DriveManager

class DocsExporter:
    def __init__(self):
        self.dm = DriveManager()
        self.docs_service = build('docs', 'v1', credentials=self.dm.creds)
        self.drive_service = self.dm.service
    
    def create_from_template(self, title, content_html, client_folder_id):
        """Crear Google Doc desde contenido HTML."""
        # Crear documento vacío
        doc = self.docs_service.documents().create(body={'title': title}).execute()
        doc_id = doc['documentId']
        
        # Insertar contenido (simplificado)
        requests = [{
            'insertText': {
                'location': {'index': 1},
                'text': content_html
            }
        }]
        
        self.docs_service.documents().batchUpdate(documentId=doc_id, body={'requests': requests}).execute()
        
        # Mover a carpeta del cliente
        self.drive_service.files().update(fileId=doc_id, addParents=client_folder_id).execute()
        
        return {
            'id': doc_id,
            'link': f"https://docs.google.com/document/d/{doc_id}/edit",
            'mensaje': f"📝 Google Doc creado: https://docs.google.com/document/d/{doc_id}/edit"
        }
    
    def convert_pdf_to_doc(self, pdf_path, title, client_name):
        """Convertir PDF existente a Google Doc."""
        client_folder_id = self.dm._get_or_create_folder(client_name, self.dm.base_folder_id)
        
        # Subir como Google Doc (Drive hace conversión)
        from googleapiclient.http import MediaFileUpload
        
        file_metadata = {
            'name': title,
            'mimeType': 'application/vnd.google-apps.document',
            'parents': [client_folder_id]
        }
        media = MediaFileUpload(pdf_path, mimetype='application/pdf')
        file = self.drive_service.files().create(body=file_metadata, media_body=media, fields='id, webViewLink').execute()
        
        return {
            'id': file['id'],
            'link': file['webViewLink'],
            'mensaje': f"📝 PDF convertido a Google Doc: {file['webViewLink']}"
        }

if __name__ == "__main__":
    de = DocsExporter()
    print("✅ Docs Exporter inicializado")
