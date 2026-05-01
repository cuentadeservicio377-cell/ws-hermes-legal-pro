#!/usr/bin/env python3
"""
HERMES LEGAL PRO — Backend API v1.0
Dashboard visual para abogados: Meet, documentos, matters, calendario, admin
"""

import json
import os
import sys
from pathlib import Path
from datetime import datetime, date, timedelta
from typing import Optional, List, Dict, Any

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

# ── Paths ─────────────────────────────────────────────────────
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "datos"
CLIENTES_DIR = Path.home() / "WillowLegal" / "01_Clientes"
PLANTILLAS_DIR = Path.home() / "WillowLegal" / "02_Administracion" / "Plantillas"

# Crear dirs si no existen
for d in [DATA_DIR, CLIENTES_DIR, PLANTILLAS_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# Archivos JSON
MATTERS_FILE = DATA_DIR / "matters.json"
REUNIONES_FILE = DATA_DIR / "reuniones.json"
ALERTAS_FILE = DATA_DIR / "alertas.json"
DOCUMENTOS_FILE = DATA_DIR / "documentos.json"

# Inicializar JSON si no existen
for f in [MATTERS_FILE, REUNIONES_FILE, ALERTAS_FILE, DOCUMENTOS_FILE]:
    if not f.exists():
        with open(f, "w", encoding="utf-8") as fh:
            json.dump([], fh)

app = FastAPI(
    title="Hermes Legal Pro — Dashboard API",
    description="API para dashboard visual de abogados",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Cache ─────────────────────────────────────────────────────
_CACHE: Dict[str, Any] = {}

def load_json(path: Path) -> Any:
    if str(path) not in _CACHE:
        with open(path, "r", encoding="utf-8") as f:
            _CACHE[str(path)] = json.load(f)
    return _CACHE[str(path)]

def save_json(path: Path, data: Any):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    _CACHE[str(path)] = data

def invalidate(path: Path):
    _CACHE.pop(str(path), None)

# ── Pydantic Models ─────────────────────────────────────────
class ReunionInput(BaseModel):
    matter_id: Optional[str] = None
    cliente: str
    fecha: str
    meet_url: Optional[str] = None
    transcript: Optional[str] = None
    resumen: Optional[str] = None
    acuerdos: Optional[List[str]] = []
    documentos_necesarios: Optional[List[str]] = []
    plazos: Optional[List[Dict]] = []

class DocumentoInput(BaseModel):
    matter_id: str
    template_key: str
    datos: Optional[Dict[str, Any]] = {}
    estado: str = "borrador"

class MatterInput(BaseModel):
    cliente: str
    area_practica: str = "Mercantil"
    descripcion: Optional[str] = ""
    deadline: Optional[str] = None
    prioridad: str = "media"

# ── Endpoints ───────────────────────────────────────────────

@app.get("/api/health")
def health():
    return {"status": "ok", "producto": "Hermes Legal Pro", "version": "1.0.0"}

# ── Dashboard ───────────────────────────────────────────────
@app.get("/api/dashboard")
def dashboard():
    """KPIs y resumen para el dashboard principal"""
    matters = load_json(MATTERS_FILE)
    reuniones = load_json(REUNIONES_FILE)
    alertas = load_json(ALERTAS_FILE)
    documentos = load_json(DOCUMENTOS_FILE)
    
    hoy = date.today().isoformat()
    
    # Métricas
    matters_activos = [m for m in matters if m.get("estado") == "activo"]
    matters_urgentes = [m for m in matters_activos if m.get("prioridad") == "alta"]
    
    reuniones_hoy = [r for r in reuniones if r.get("fecha") == hoy]
    
    docs_pendientes = [d for d in documentos if d.get("estado") == "borrador"]
    
    alertas_activas = [a for a in alertas if not a.get("resuelta")]
    
    # Próximos plazos (próximos 7 días)
    proximos_plazos = []
    for m in matters_activos:
        if m.get("deadline"):
            dias = calcular_dias_restantes(m["deadline"])
            if dias is not None and dias <= 7:
                proximos_plazos.append({
                    "matter_id": m.get("id"),
                    "cliente": m.get("cliente"),
                    "deadline": m["deadline"],
                    "dias_restantes": dias,
                    "descripcion": m.get("next_step", "Sin descripción")
                })
    proximos_plazos.sort(key=lambda x: x["dias_restantes"])
    
    return {
        "kpis": {
            "matters_activos": len(matters_activos),
            "matters_urgentes": len(matters_urgentes),
            "reuniones_hoy": len(reuniones_hoy),
            "documentos_pendientes": len(docs_pendientes),
            "alertas_activas": len(alertas_activas)
        },
        "proximos_plazos": proximos_plazos[:5],
        "reuniones_recientes": reuniones[-5:][::-1],
        "alertas": alertas_activas[:5]
    }

# ── Matters ───────────────────────────────────────────────
@app.get("/api/matters")
def list_matters(estado: Optional[str] = None, area: Optional[str] = None):
    matters = load_json(MATTERS_FILE)
    if estado:
        matters = [m for m in matters if m.get("estado") == estado]
    if area:
        matters = [m for m in matters if m.get("area_practica") == area]
    return matters

@app.post("/api/matters")
def create_matter(data: MatterInput):
    matters = load_json(MATTERS_FILE)
    
    nuevo_id = f"LEG-{len(matters)+1:03d}"
    matter = {
        "id": nuevo_id,
        "cliente": data.cliente,
        "area_practica": data.area_practica,
        "descripcion": data.descripcion,
        "deadline": data.deadline,
        "prioridad": data.prioridad,
        "estado": "activo",
        "fecha_creacion": date.today().isoformat(),
        "next_step": "Intake inicial pendiente",
        "reuniones": [],
        "documentos": [],
        "tareas": [],
        "carpeta": str(CLIENTES_DIR / safe_filename(data.cliente))
    }
    matters.append(matter)
    save_json(MATTERS_FILE, matters)
    
    # Crear carpeta física
    crear_carpeta_cliente(data.cliente)
    
    return matter

@app.get("/api/matters/{matter_id}")
def get_matter(matter_id: str):
    matters = load_json(MATTERS_FILE)
    for m in matters:
        if m.get("id") == matter_id:
            return m
    raise HTTPException(status_code=404, detail="Matter no encontrado")

# ── Reuniones ─────────────────────────────────────────────
@app.get("/api/reuniones")
def list_reuniones(matter_id: Optional[str] = None):
    reuniones = load_json(REUNIONES_FILE)
    if matter_id:
        reuniones = [r for r in reuniones if r.get("matter_id") == matter_id]
    return reuniones[::-1]  # Más recientes primero

@app.post("/api/reuniones")
def create_reunion(data: ReunionInput):
    reuniones = load_json(REUNIONES_FILE)
    
    reunion = {
        "id": f"REU-{len(reuniones)+1:04d}",
        "matter_id": data.matter_id,
        "cliente": data.cliente,
        "fecha": data.fecha,
        "meet_url": data.meet_url,
        "transcript": data.transcript,
        "resumen": data.resumen,
        "acuerdos": data.acuerdos,
        "documentos_necesarios": data.documentos_necesarios,
        "plazos": data.plazos,
        "estado": "procesada",
        "fecha_registro": datetime.now().isoformat()
    }
    reuniones.append(reunion)
    save_json(REUNIONES_FILE, reuniones)
    
    # Si hay matter_id, actualizar el matter
    if data.matter_id:
        matters = load_json(MATTERS_FILE)
        for m in matters:
            if m.get("id") == data.matter_id:
                if "reuniones" not in m:
                    m["reuniones"] = []
                m["reuniones"].append(reunion["id"])
                m["next_step"] = f"Revisar documentos post-reunión {reunion['id']}"
                break
        save_json(MATTERS_FILE, matters)
    
    return reunion

@app.get("/api/reuniones/{reunion_id}")
def get_reunion(reunion_id: str):
    reuniones = load_json(REUNIONES_FILE)
    for r in reuniones:
        if r.get("id") == reunion_id:
            return r
    raise HTTPException(status_code=404, detail="Reunión no encontrada")

# ── Documentos ────────────────────────────────────────────
@app.get("/api/documentos")
def list_documentos(matter_id: Optional[str] = None, estado: Optional[str] = None):
    documentos = load_json(DOCUMENTOS_FILE)
    if matter_id:
        documentos = [d for d in documentos if d.get("matter_id") == matter_id]
    if estado:
        documentos = [d for d in documentos if d.get("estado") == estado]
    return documentos[::-1]

@app.post("/api/documentos")
def create_documento(data: DocumentoInput):
    documentos = load_json(DOCUMENTOS_FILE)
    
    doc = {
        "id": f"DOC-{len(documentos)+1:04d}",
        "matter_id": data.matter_id,
        "template_key": data.template_key,
        "datos": data.datos,
        "estado": data.estado,
        "fecha_creacion": datetime.now().isoformat(),
        "ruta_pdf": None,
        "ruta_editable": None
    }
    documentos.append(doc)
    save_json(DOCUMENTOS_FILE, documentos)
    
    return doc

@app.get("/api/documentos/{doc_id}")
def get_documento(doc_id: str):
    documentos = load_json(DOCUMENTOS_FILE)
    for d in documentos:
        if d.get("id") == doc_id:
            return d
    raise HTTPException(status_code=404, detail="Documento no encontrado")

# ── Templates ─────────────────────────────────────────────
@app.get("/api/templates")
def list_templates():
    """Lista los 23 templates legales disponibles"""
    return [
        {"key": "prestacion_servicios", "nombre": "Contrato de Prestación de Servicios", "categoria": "Contratos"},
        {"key": "confidencialidad", "nombre": "Acuerdo de Confidencialidad (NDA)", "categoria": "Contratos"},
        {"key": "nda", "nombre": "NDA Corporativo", "categoria": "Contratos"},
        {"key": "trabajo", "nombre": "Contrato de Trabajo", "categoria": "Laboral"},
        {"key": "arrendamiento", "nombre": "Contrato de Arrendamiento", "categoria": "Inmobiliario"},
        {"key": "pagaré", "nombre": "Pagaré", "categoria": "Cobranza"},
        {"key": "carta_cobranza", "nombre": "Carta de Cobranza", "categoria": "Cobranza"},
        {"key": "convenio_pagos", "nombre": "Convenio de Pagos", "categoria": "Cobranza"},
        {"key": "acta_asamblea", "nombre": "Acta de Asamblea", "categoria": "Corporativo"},
        {"key": "poder_notarial", "nombre": "Poder Notarial", "categoria": "Corporativo"},
        {"key": "estatutos", "nombre": "Estatutos Sociales", "categoria": "Corporativo"},
        {"key": "convenio_accionistas", "nombre": "Convenio de Accionistas", "categoria": "Corporativo"},
        {"key": "reglamento_interior", "nombre": "Reglamento Interior", "categoria": "Laboral"},
        {"key": "finiquito", "nombre": "Finiquito", "categoria": "Laboral"},
        {"key": "nda_laboral", "nombre": "NDA Laboral", "categoria": "Laboral"},
        {"key": "garantia", "nombre": "Garantía", "categoria": "Civil"},
        {"key": "calendario_cobranza", "nombre": "Calendario de Cobranza", "categoria": "Cobranza"},
        {"key": "bitacora", "nombre": "Bitácora de Entregas", "categoria": "Corporativo"},
        {"key": "expediente_sat", "nombre": "Expediente de Materialidad", "categoria": "Fiscal"},
        {"key": "carta_sat", "nombre": "Carta SAT", "categoria": "Fiscal"},
        {"key": "aviso_privacidad", "nombre": "Aviso de Privacidad", "categoria": "Privacidad"},
        {"key": "formato_arco", "nombre": "Formato ARCO", "categoria": "Privacidad"},
        {"key": "terminos_condiciones", "nombre": "Términos y Condiciones", "categoria": "Corporativo"}
    ]

# ── Carpetas / Explorador ─────────────────────────────────
@app.get("/api/carpetas/{matter_id}")
def list_carpeta(matter_id: str):
    """Lista archivos en la carpeta del cliente"""
    matters = load_json(MATTERS_FILE)
    matter = None
    for m in matters:
        if m.get("id") == matter_id:
            matter = m
            break
    
    if not matter:
        raise HTTPException(status_code=404, detail="Matter no encontrado")
    
    carpeta = Path(matter.get("carpeta", CLIENTES_DIR / safe_filename(matter["cliente"])))
    
    if not carpeta.exists():
        return {"carpeta": str(carpeta), "archivos": [], "existe": False}
    
    archivos = []
    for f in carpeta.rglob("*"):
        if f.is_file():
            archivos.append({
                "nombre": f.name,
                "ruta": str(f.relative_to(carpeta)),
                "tamaño": f.stat().st_size,
                "modificado": datetime.fromtimestamp(f.stat().st_mtime).isoformat()
            })
    
    return {"carpeta": str(carpeta), "archivos": archivos, "existe": True}

# ── Alertas ────────────────────────────────────────────────
@app.get("/api/alertas")
def list_alertas(resueltas: bool = False):
    alertas = load_json(ALERTAS_FILE)
    if not resueltas:
        alertas = [a for a in alertas if not a.get("resuelta")]
    return alertas[::-1]

# ── Helpers ───────────────────────────────────────────────
def calcular_dias_restantes(fecha_str: str) -> Optional[int]:
    try:
        fecha = datetime.strptime(fecha_str, "%Y-%m-%d").date()
        hoy = date.today()
        return (fecha - hoy).days
    except:
        return None

def safe_filename(nombre: str) -> str:
    """Convierte nombre de cliente a nombre de carpeta seguro"""
    return "".join(c for c in nombre if c.isalnum() or c in " _-").strip()

def crear_carpeta_cliente(cliente: str):
    """Crea estructura de carpetas para un cliente nuevo"""
    safe = safe_filename(cliente)
    base = CLIENTES_DIR / safe
    
    subcarpetas = [
        "01_Intake",
        "02_Contratos/Borradores",
        "02_Contratos/Firmados",
        "02_Contratos/Anexos",
        "03_Correspondencia/Entrante",
        "03_Correspondencia/Saliente",
        "04_Litigio/Demandas",
        "04_Litigio/Contestaciones",
        "04_Litigio/Pruebas",
        "04_Litigio/Audiencias",
        "05_Facturacion/Cotizaciones",
        "05_Facturacion/Facturas",
        "05_Facturacion/Pagos",
        "06_Entregables/Documentos_Finales",
        "06_Entregables/Presentaciones",
        "06_Entregables/Reportes",
        "07_Archivo/Cerrado"
    ]
    
    for sub in subcarpetas:
        (base / sub).mkdir(parents=True, exist_ok=True)
    
    return base

# ── Mount SPA ─────────────────────────────────────────────
FRONTEND_DIR = BASE_DIR / "frontend"
if FRONTEND_DIR.exists():
    app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")

# ── Run ───────────────────────────────────────────────────
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8082)
