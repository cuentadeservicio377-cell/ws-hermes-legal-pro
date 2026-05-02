#!/usr/bin/env python3
"""
Sheets Manager — Sincronizar datos con Google Sheets maestro.
"""

import gspread
from google.oauth2.credentials import Credentials
from scripts.drive_manager import DriveManager

class SheetsManager:
    def __init__(self):
        self.dm = DriveManager()
        self.gc = gspread.authorize(self.dm.creds)
        self.sheet_id = self._get_or_create_sheet()
    
    def _get_or_create_sheet(self):
        """Obtener o crear Sheet maestro."""
        sheet_name = "WillowLegal_Maestro"
        
        # Buscar en Drive
        query = f"mimeType='application/vnd.google-apps.spreadsheet' and name='{sheet_name}' and trashed=false"
        results = self.dm.service.files().list(q=query, fields='files(id, name)').execute()
        items = results.get('files', [])
        
        if items:
            return items[0]['id']
        
        # Crear nuevo
        spreadsheet = self.gc.create(sheet_name)
        
        # Configurar hojas
        spreadsheet.add_worksheet(title="Matters", rows=1000, cols=20)
        spreadsheet.add_worksheet(title="Finanzas", rows=1000, cols=10)
        spreadsheet.add_worksheet(title="Plazos", rows=1000, cols=10)
        
        # Headers Matters
        matters_ws = spreadsheet.worksheet("Matters")
        matters_ws.append_row(["ID", "Nombre", "Cliente", "Estado", "Área", "Materia", 
                                "Prioridad", "Next Step", "Blocker", "Deadline", "Creado", "Drive Folder"])
        
        # Headers Finanzas
        finanzas_ws = spreadsheet.worksheet("Finanzas")
        finanzas_ws.append_row(["ID", "Matter ID", "Concepto", "Monto", "Tipo", "Estado", "Fecha"])
        
        # Headers Plazos
        plazos_ws = spreadsheet.worksheet("Plazos")
        plazos_ws.append_row(["ID", "Matter ID", "Descripción", "Fecha", "Estado", "Días Restantes"])
        
        return spreadsheet.id
    
    def sync_matter(self, matter):
        """Sincronizar matter a Sheets."""
        spreadsheet = self.gc.open_by_key(self.sheet_id)
        matters_ws = spreadsheet.worksheet("Matters")
        
        # Buscar fila existente
        try:
            cell = matters_ws.find(matter['id'])
        except gspread.exceptions.CellNotFound:
            cell = None
        
        row_data = [
            matter['id'],
            matter.get('nombre', ''),
            matter.get('cliente', ''),
            matter.get('estado', ''),
            matter.get('area', ''),
            matter.get('materia', ''),
            matter.get('prioridad', ''),
            matter.get('next_step', ''),
            matter.get('blocker', ''),
            matter.get('deadline', ''),
            matter.get('creado', ''),
            matter.get('drive_folder_id', '')
        ]
        
        if cell:
            # Actualizar
            matters_ws.update(f'A{cell.row}:L{cell.row}', [row_data])
        else:
            # Insertar
            matters_ws.append_row(row_data)
        
        return {"status": "ok", "mensaje": f"✅ Matter {matter['id']} sincronizado a Sheets"}
    
    def sync_finanza(self, movimiento):
        """Sincronizar movimiento financiero."""
        spreadsheet = self.gc.open_by_key(self.sheet_id)
        finanzas_ws = spreadsheet.worksheet("Finanzas")
        
        finanzas_ws.append_row([
            movimiento['id'],
            movimiento['matter_id'],
            movimiento['concepto'],
            movimiento['monto'],
            movimiento['tipo'],
            movimiento['estado'],
            movimiento['fecha']
        ])
        
        return {"status": "ok"}

if __name__ == "__main__":
    sm = SheetsManager()
    print(f"✅ Sheets Manager inicializado. Sheet ID: {sm.sheet_id}")
