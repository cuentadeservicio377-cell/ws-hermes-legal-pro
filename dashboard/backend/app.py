#!/usr/bin/env python3
"""
HERMES LEGAL PRO — Backend API v2.0
Dashboard visual + Motor Kami v3 integrado
FastAPI + JSON local + Motor Kami v3 + WeasyPrint
"""

import json
import os
import sys
import subprocess
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
MOTOR_DIR = BASE_DIR / "motor_kami"
CLIENTES_DIR = Path.home() / "WillowLegal" / "01_Clientes"
PLANTILLAS_DIR = Path.home() / "WillowLegal" / "02_Administracion" / "Plantillas"

# Añadir motor al path para importar
sys.path.insert(0, str(MOTOR_DIR))

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
    description="API para dashboard visual de abogados con Motor Kami v3",
    version="2.0.0"
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

class GenerarDocumentoRequest(BaseModel):
    template_key: str
    output_filename: Optional[str] = None
    datos_extra: Optional[Dict[str, Any]] = {}

# ── Endpoints ───────────────────────────────────────────────

@app.get("/api/health")
def health():
    motor_ok = (MOTOR_DIR / "motor_kami.py").exists()
    templates_count = len(list((MOTOR_DIR / "templates").glob("*.json"))) if (MOTOR_DIR / "templates").exists() else 0
    return {
        "status": "ok",
        "producto": "Hermes Legal Pro",
        "version": "2.0.0",
        "motor_kami": "ok" if motor_ok else "no_encontrado",
        "templates_disponibles": templates_count
    }

# ── Dashboard ───────────────────────────────────────────────
@app.get("/api/dashboard")
def dashboard():
    """KPIs y resumen para el dashboard principal"""
    matters = load_json(MATTERS_FILE)
    reuniones = load_json(REUNIONES_FILE)
    alertas = load_json(ALERTAS_FILE)
    documentos = load_json(DOCUMENTOS_FILE)
    
    hoy = date.today().isoformat()
    
    matters_activos = [m for m in matters if m.get("estado") == "activo"]
    matters_urgentes = [m for m in matters_activos if m.get("prioridad") == "alta"]
    reuniones_hoy = [r for r in reuniones if r.get("fecha") == hoy]
    docs_pendientes = [d for d in documentos if d.get("estado") == "borrador"]
    alertas_activas = [a for a in alertas if not a.get("resuelta")]
    
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
    
    crear_carpeta_cliente(data.cliente)
    
    return matter

@app.get("/api/matters/{matter_id}")
def get_matter(matter_id: str):
    matters = load_json(MATTERS_FILE)
    for m in matters:
        if m.get("id") == matter_id:
            return m
    raise HTTPException(status_code=404, detail="Matter no encontrado")

@app.put("/api/matters/{matter_id}")
def update_matter(matter_id: str, data: MatterInput):
    matters = load_json(MATTERS_FILE)
    for m in matters:
        if m.get("id") == matter_id:
            m["cliente"] = data.cliente
            m["area_practica"] = data.area_practica
            m["descripcion"] = data.descripcion
            m["deadline"] = data.deadline
            m["prioridad"] = data.prioridad
            if hasattr(data, 'estado') and data.estado:
                m["estado"] = data.estado
            save_json(MATTERS_FILE, matters)
            return m
    raise HTTPException(status_code=404, detail="Matter no encontrado")

@app.delete("/api/matters/{matter_id}")
def delete_matter(matter_id: str):
    matters = load_json(MATTERS_FILE)
    original_len = len(matters)
    matters = [m for m in matters if m.get("id") != matter_id]
    if len(matters) == original_len:
        raise HTTPException(status_code=404, detail="Matter no encontrado")
    save_json(MATTERS_FILE, matters)
    return {"success": True, "message": f"Matter {matter_id} eliminado"}

# ── Reuniones ─────────────────────────────────────────────
@app.get("/api/reuniones")
def list_reuniones(matter_id: Optional[str] = None):
    reuniones = load_json(REUNIONES_FILE)
    if matter_id:
        reuniones = [r for r in reuniones if r.get("matter_id") == matter_id]
    return reuniones[::-1]

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

# ── Motor Kami Integration ──────────────────────────────────

@app.get("/api/templates")
def list_templates():
    """Lista los templates legales disponibles desde Motor Kami"""
    templates_dir = MOTOR_DIR / "templates"
    if not templates_dir.exists():
        return {"templates": [], "count": 0}
    
    templates = []
    index_path = templates_dir / "index.json"
    if index_path.exists():
        with open(index_path, "r", encoding="utf-8") as f:
            index = json.load(f)
        templates = index.get("templates", [])
    else:
        # Fallback: leer archivos JSON directamente
        for t in sorted(templates_dir.glob("*.json")):
            if t.name == "index.json":
                continue
            with open(t, "r", encoding="utf-8") as f:
                data = json.load(f)
            templates.append({
                "key": t.stem,
                "label": data.get("titulo", t.stem),
                "area": data.get("area", "General"),
                "materia": data.get("materia", "General")
            })
    
    return {"templates": templates, "count": len(templates)}

@app.get("/api/templates/{key}")
def get_template(key: str):
    template_path = MOTOR_DIR / "templates" / f"{key}.json"
    if not template_path.exists():
        raise HTTPException(status_code=404, detail=f"Template '{key}' no encontrado")
    with open(template_path, "r", encoding="utf-8") as f:
        return json.load(f)

@app.post("/api/matter/{matter_id}/generar-documento")
def generar_documento(matter_id: str, req: GenerarDocumentoRequest):
    """Genera un documento PDF usando Motor Kami v3"""
    matters = load_json(MATTERS_FILE)
    matter = None
    for m in matters:
        if m.get("id") == matter_id:
            matter = m
            break
    
    if not matter:
        raise HTTPException(status_code=404, detail="Matter no encontrado")
    
    template_path = MOTOR_DIR / "templates" / f"{req.template_key}.json"
    if not template_path.exists():
        raise HTTPException(status_code=404, detail=f"Template '{req.template_key}' no encontrado")
    
    # Preparar output
    output_dir = MOTOR_DIR / "output"
    output_dir.mkdir(exist_ok=True)
    filename = req.output_filename or f"{matter_id}_{req.template_key}_{date.today().strftime('%Y%m%d')}.pdf"
    output_path = output_dir / filename
    
    # Construir bloques para Kami
    blocks = construir_bloques_desde_matter(matter, req.template_key, req.datos_extra)
    
    # Generar via Motor Kami CLI
    try:
        json_input = json.dumps({"blocks": blocks, "options": {"titulo": f"Documento {req.template_key}"}})
        result = subprocess.run(
            [sys.executable, str(MOTOR_DIR / "motor_kami.py"), "--input", "-", "--output", str(output_path)],
            input=json_input,
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if result.returncode != 0:
            raise HTTPException(status_code=500, detail=f"Error Motor Kami: {result.stderr}")
        
        # Actualizar documentos del matter
        documentos = load_json(DOCUMENTOS_FILE)
        doc = {
            "id": f"DOC-{len(documentos)+1:04d}",
            "matter_id": matter_id,
            "template_key": req.template_key,
            "estado": "generado",
            "fecha_creacion": datetime.now().isoformat(),
            "ruta_pdf": str(output_path),
            "ruta_editable": str(output_path.with_suffix(".html"))
        }
        documentos.append(doc)
        save_json(DOCUMENTOS_FILE, documentos)
        
        return {
            "success": True,
            "file_path": str(output_path),
            "file_size_kb": round(output_path.stat().st_size / 1024, 1),
            "documento_id": doc["id"]
        }
        
    except subprocess.TimeoutExpired:
        raise HTTPException(status_code=500, detail="Timeout generando documento")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generando PDF: {str(e)}")

@app.post("/api/kami/validate")
def validate_document(data: Dict[str, Any]):
    """Valida sustancia legal de un documento"""
    try:
        from blocks import validar_sustancia
        resultado = validar_sustancia(data)
        return resultado
    except ImportError:
        raise HTTPException(status_code=500, detail="Motor Kami no disponible")

# ── Carpetas / Explorador ─────────────────────────────────
@app.get("/api/carpetas/{matter_id}")
def list_carpeta(matter_id: str):
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
    return "".join(c for c in nombre if c.isalnum() or c in " _-").strip()

def crear_carpeta_cliente(cliente: str):
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

def construir_bloques_desde_matter(matter: Dict, template_key: str, datos_extra: Dict) -> List[Dict]:
    """Construye bloques para Motor Kami desde un matter"""
    blocks = []
    
    # Cover page
    blocks.append({
        "type": "cover_page",
        "data": {
            "titulo": f"{template_key.replace('_', ' ').title()}",
            "cliente": matter.get("cliente", ""),
            "matter_id": matter.get("id", ""),
            "fecha": date.today().strftime("%d de %B de %Y")
        }
    })
    
    # Parties block
    blocks.append({
        "type": "parties_block",
        "data": {
            "prestador": {
                "nombre": "We Law S.C.",
                "rfc": "WEL123456ABC",
                "domicilio": "Ciudad de México"
            },
            "cliente": {
                "nombre": matter.get("cliente", ""),
                "rfc": datos_extra.get("rfc_cliente", "[PENDIENTE]"),
                "domicilio": datos_extra.get("domicilio_cliente", "[PENDIENTE]")
            }
        }
    })
    
    # Cláusulas básicas
    blocks.append({
        "type": "clause_section",
        "data": {
            "numero": "1",
            "titulo": "Objeto",
            "subclausulas": [matter.get("descripcion", "Servicios legales profesionales")]
        }
    })
    
    # Signature block
    blocks.append({
        "type": "signature_block",
        "data": {
            "prestador": {"nombre": "We Law S.C.", "puesto": "Representante Legal"},
            "cliente": {"nombre": matter.get("cliente", ""), "puesto": "Representante Legal"}
        }
    })
    
    return blocks

# ── Mount SPA ─────────────────────────────────────────────
FRONTEND_DIR = BASE_DIR / "frontend"
if FRONTEND_DIR.exists():
    app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")

# ── Run ───────────────────────────────────────────────────
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8082)
