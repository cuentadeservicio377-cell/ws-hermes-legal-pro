#!/usr/bin/env python3
"""
Tasks Manager — Tareas legales en Google Tasks.
"""

from googleapiclient.discovery import build
from scripts.drive_manager import DriveManager

class TasksManager:
    def __init__(self):
        self.dm = DriveManager()
        self.tasks_service = build('tasks', 'v1', credentials=self.dm.creds)
        self.tasklist_id = self._get_or_create_tasklist()
    
    def _get_or_create_tasklist(self):
        """Obtener o crear lista de tareas."""
        tasklists = self.tasks_service.tasklists().list().execute()
        items = tasklists.get('items', [])
        
        for item in items:
            if item['title'] == 'WillowLegal':
                return item['id']
        
        # Crear nueva
        tasklist = self.tasks_service.tasklists().insert(body={'title': 'WillowLegal'}).execute()
        return tasklist['id']
    
    def create_task(self, matter_id, descripcion, due_date=None, notes=""):
        """Crear tarea en Google Tasks."""
        
        task = {
            'title': f'[{matter_id}] {descripcion}',
            'notes': notes or f'Matter: {matter_id}',
        }
        
        if due_date:
            task['due'] = f"{due_date}T00:00:00.000Z"
        
        result = self.tasks_service.tasks().insert(tasklist=self.tasklist_id, body=task).execute()
        
        return {
            'id': result['id'],
            'mensaje': f"✅ Tarea creada: {result['title']}"
        }
    
    def complete_task(self, task_id):
        """Marcar tarea como completada."""
        self.tasks_service.tasks().update(
            tasklist=self.tasklist_id,
            task=task_id,
            body={'status': 'completed'}
        ).execute()
        
        return {"status": "ok", "mensaje": "✅ Tarea completada"}

if __name__ == "__main__":
    tm = TasksManager()
    print(f"✅ Tasks Manager inicializado. Tasklist: {tm.tasklist_id}")
