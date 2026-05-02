#!/usr/bin/env python3
"""
Calendar Manager — Plazos legales en Google Calendar.
"""

from googleapiclient.discovery import build
from scripts.drive_manager import DriveManager
from datetime import datetime, timedelta

class CalendarManager:
    def __init__(self):
        self.dm = DriveManager()
        self.calendar_service = build('calendar', 'v3', credentials=self.dm.creds)
        self.calendar_id = 'primary'  # Calendar principal
    
    def create_deadline(self, matter_id, descripcion, fecha, reminder_days=[3, 1]):
        """Crear evento de deadline en Calendar."""
        
        event = {
            'summary': f'[Willow] {descripcion}',
            'description': f'Matter: {matter_id}\nDescripción: {descripcion}',
            'start': {
                'date': fecha,
                'timeZone': 'America/Mexico_City',
            },
            'end': {
                'date': fecha,
                'timeZone': 'America/Mexico_City',
            },
            'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'email', 'minutes': days * 24 * 60}
                    for days in reminder_days
                ] + [
                    {'method': 'popup', 'minutes': 60}  # 1 hora antes
                ],
            },
            'colorId': '11',  # Rojo para deadlines
        }
        
        event = self.calendar_service.events().insert(calendarId=self.calendar_id, body=event).execute()
        
        return {
            'id': event['id'],
            'link': event.get('htmlLink', ''),
            'mensaje': f"📅 Plazo creado en Calendar: {event.get('htmlLink', '')}"
        }
    
    def list_upcoming(self, days=7):
        """Listar plazos próximos."""
        now = datetime.utcnow().isoformat() + 'Z'
        future = (datetime.utcnow() + timedelta(days=days)).isoformat() + 'Z'
        
        events_result = self.calendar_service.events().list(
            calendarId=self.calendar_id,
            timeMin=now,
            timeMax=future,
            q='[Willow]',
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        
        return events_result.get('items', [])

if __name__ == "__main__":
    cm = CalendarManager()
    print("✅ Calendar Manager inicializado")
