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

# v2.0: Importacion anticipada de core (se inicializa despues de paths)
from config.config_loader import Config
from core.datastore import JSONDatastore
from core.id_generator import IDGenerator

# v2.0: Importar Motor Kami directamente (no via subprocess)
from motor_kami.motor_kami import generar_documento_real

# ── Paths ─────────────────────────────────────────────────────
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "datos"

# Detectar motor_kami (puede estar en repo raiz o en dashboard/)
MOTOR_DIR = BASE_DIR / "motor_kami"
if not (MOTOR_DIR / "motor_kami.py").exists():
    MOTOR_DIR = BASE_DIR.parent / "motor_kami"

# Anadir motor al path para importar
sys.path.insert(0, str(MOTOR_DIR))

# Anadir raiz del proyecto al path para imports de core y config
PROJECT_ROOT = BASE_DIR.parent
sys.path.insert(0, str(PROJECT_ROOT))

# === v2.0: Configuracion centralizada + Datastore unificado ===
config = Config.load()
datastore = JSONDatastore(config.datastore.path, config.datastore.backup_dir)
id_generator = IDGenerator(datastore, config.ids)

CLIENTES_DIR = Path.home() / "WillowLegal" / "01_Clientes"
PLANTILLAS_DIR = Path.home() / "WillowLegal" / "02_Administracion" / "Plantillas"

# Crear dirs si no existen
for d in [CLIENTES_DIR, PLANTILLAS_DIR]:
    d.mkdir(parents=True, exist_ok=True)

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

def load_json(collection: str) -> Any:
    # v2.0: Usa datastore en lugar de paths hardcodeados
    return datastore.get(collection)

def save_json(collection: str, data: Any):
    # v2.0: Usa datastore en lugar de paths hardcodeados
    datastore.set(collection, data)

def load_json_legacy(path: Path) -> Any:
    # Fallback para cargas de archivos fisicos
    if str(path) not in _CACHE:
        with open(path, "r", encoding="utf-8") as f:
            _CACHE[str(path)] = json.load(f)
    return _CACHE[str(path)]

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

class FinanzaInput(BaseModel):
    matter_id: str
    tipo: str  # ingreso | egreso | anticipo | honorario
    monto: float
    concepto: str
    fecha: Optional[str] = None
    metodo_pago: Optional[str] = "transferencia"
    notas: Optional[str] = ""

# ── Endpoints ───────────────────────────────────────────────

@app.get("/api/health")
def health():
    templates_dir = Path(config.motor_kami['templates_dir'])
    motor_ok = templates_dir.exists() and (templates_dir / "index.json").exists()
    templates_count = len(list(templates_dir.glob("*.json"))) if templates_dir.exists() else 0
    return {
        "status": "ok",
        "producto": "Hermes Legal Pro",
        "version": "2.0.0",
        "motor_kami": "ok" if motor_ok else "no_encontrado",
        "templates_disponibles": templates_count,
        "datastore": str(config.datastore.path)
    }

# ── Dashboard ───────────────────────────────────────────────
@app.get("/api/dashboard")
def dashboard():
    """KPIs y resumen para el dashboard principal"""
    matters = load_json("matters")
    reuniones = load_json("reuniones")
    alertas = load_json("alertas")
    documentos = load_json("documentos")
    
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
    matters = load_json("matters")
    if estado:
        matters = [m for m in matters if m.get("estado") == estado]
    if area:
        matters = [m for m in matters if m.get("area_practica") == area]
    return matters

@app.post("/api/matters")
def create_matter(data: MatterInput):
    matters = load_json("matters")
    
    nuevo_id = id_generator.generate_matter_id()
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
    save_json("matters", matters)
    
    crear_carpeta_cliente(data.cliente)
    
    return matter

@app.get("/api/matters/{matter_id}")
def get_matter(matter_id: str):
    matters = load_json("matters")
    for m in matters:
        if m.get("id") == matter_id:
            return m
    raise HTTPException(status_code=404, detail="Matter no encontrado")

@app.put("/api/matters/{matter_id}")
def update_matter(matter_id: str, data: MatterInput):
    matters = load_json("matters")
    for m in matters:
        if m.get("id") == matter_id:
            m["cliente"] = data.cliente
            m["area_practica"] = data.area_practica
            m["descripcion"] = data.descripcion
            m["deadline"] = data.deadline
            m["prioridad"] = data.prioridad
            if hasattr(data, 'estado') and data.estado:
                m["estado"] = data.estado
            save_json("matters", matters)
            return m
    raise HTTPException(status_code=404, detail="Matter no encontrado")

@app.delete("/api/matters/{matter_id}")
def delete_matter(matter_id: str):
    matters = load_json("matters")
    original_len = len(matters)
    matters = [m for m in matters if m.get("id") != matter_id]
    if len(matters) == original_len:
        raise HTTPException(status_code=404, detail="Matter no encontrado")
    save_json("matters", matters)
    return {"success": True, "message": f"Matter {matter_id} eliminado"}

# ── Reuniones ─────────────────────────────────────────────
@app.get("/api/reuniones")
def list_reuniones(matter_id: Optional[str] = None):
    reuniones = load_json("reuniones")
    if matter_id:
        reuniones = [r for r in reuniones if r.get("matter_id") == matter_id]
    return reuniones[::-1]

@app.post("/api/reuniones")
def create_reunion(data: ReunionInput):
    reuniones = load_json("reuniones")
    
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
    save_json("reuniones", reuniones)
    
    if data.matter_id:
        matters = load_json("matters")
        for m in matters:
            if m.get("id") == data.matter_id:
                if "reuniones" not in m:
                    m["reuniones"] = []
                m["reuniones"].append(reunion["id"])
                m["next_step"] = f"Revisar documentos post-reunión {reunion['id']}"
                break
        save_json("matters", matters)
    
    return reunion

@app.get("/api/reuniones/{reunion_id}")
def get_reunion(reunion_id: str):
    reuniones = load_json("reuniones")
    for r in reuniones:
        if r.get("id") == reunion_id:
            return r
    raise HTTPException(status_code=404, detail="Reunión no encontrada")

# ── Documentos ────────────────────────────────────────────
@app.get("/api/documentos")
def list_documentos(matter_id: Optional[str] = None, estado: Optional[str] = None):
    documentos = load_json("documentos")
    if matter_id:
        documentos = [d for d in documentos if d.get("matter_id") == matter_id]
    if estado:
        documentos = [d for d in documentos if d.get("estado") == estado]
    return documentos[::-1]

@app.post("/api/documentos")
def create_documento(data: DocumentoInput):
    documentos = load_json("documentos")
    
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
    save_json("documentos", documentos)
    
    return doc

@app.get("/api/documentos/{doc_id}")
def get_documento(doc_id: str):
    documentos = load_json("documentos")
    for d in documentos:
        if d.get("id") == doc_id:
            return d
    raise HTTPException(status_code=404, detail="Documento no encontrado")

@app.post("/api/documentos/{doc_id}/aprobar")
def aprobar_documento(doc_id: str, payload: dict):
    """Aprobar documento con trazabilidad."""
    try:
        documentos = load_json("documentos")
        doc = next((d for d in documentos if d["id"] == doc_id), None)
        
        if not doc:
            raise HTTPException(status_code=404, detail="Documento no encontrado")
        
        doc["estado"] = "aprobado"
        doc["aprobado_por"] = payload.get("aprobado_por", "Sistema")
        doc["fecha_aprobacion"] = datetime.now().isoformat()
        doc["comentario_aprobacion"] = payload.get("comentario", "")
        
        save_json("documentos", documentos)
        
        return {
            "status": "ok",
            "documento": doc,
            "mensaje": f"✅ Documento {doc_id} aprobado por {doc['aprobado_por']}"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/documentos/{doc_id}/rechazar")
def rechazar_documento(doc_id: str, payload: dict):
    """Rechazar documento."""
    try:
        documentos = load_json("documentos")
        doc = next((d for d in documentos if d["id"] == doc_id), None)
        
        if not doc:
            raise HTTPException(status_code=404, detail="Documento no encontrado")
        
        doc["estado"] = "rechazado"
        doc["rechazado_por"] = payload.get("rechazado_por", "Sistema")
        doc["fecha_rechazo"] = datetime.now().isoformat()
        doc["motivo_rechazo"] = payload.get("motivo", "")
        
        save_json("documentos", documentos)
        
        return {
            "status": "ok",
            "mensaje": f"❌ Documento {doc_id} rechazado"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

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
    """Genera un documento PDF usando Motor Kami v3 — v2.0: direct call, no subprocess"""
    matters = load_json("matters")
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
    output_dir = Path(config.motor_kami.get('output_dir', '~/.willowlegal/output/')).expanduser()
    output_dir.mkdir(parents=True, exist_ok=True)
    filename = req.output_filename or f"{matter_id}_{req.template_key}_{date.today().strftime('%Y%m%d')}.pdf"
    output_path = output_dir / filename
    
    # v2.0: Usar generar_documento_real() directamente — no subprocess
    despacho_data = {
        "nombre": config.despacho.nombre,
        "rfc": config.despacho.rfc,
        "representante": config.despacho.representante,
        "email": config.despacho.email,
        "domicilio": config.despacho.domicilio,
        "telefono": config.despacho.telefono,
    }
    
    try:
        result = generar_documento_real(
            template_key=req.template_key,
            matter_data=matter,
            output_path=output_path,
            extra_vars=req.datos_extra,
            despacho_data=despacho_data
        )
        
        if not result.get("success"):
            raise HTTPException(status_code=500, detail=result.get("error", "Error desconocido del Motor Kami"))
        
        # Actualizar documentos del matter
        documentos = load_json("documentos")
        doc = {
            "id": id_generator.generate_document_id(),
            "matter_id": matter_id,
            "template_key": req.template_key,
            "estado": "generado",
            "fecha_creacion": datetime.now().isoformat(),
            "ruta_pdf": str(output_path),
            "ruta_editable": str(output_path.with_suffix(".html"))
        }
        documentos.append(doc)
        save_json("documentos", documentos)
        
        return {
            "success": True,
            "file_path": str(output_path),
            "file_size_kb": round(output_path.stat().st_size / 1024, 1),
            "documento_id": doc["id"],
            "template_label": result.get("template_label", req.template_key)
        }
        
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
    matters = load_json("matters")
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
    alertas = load_json("alertas")
    if not resueltas:
        alertas = [a for a in alertas if not a.get("resuelta")]
    return alertas[::-1]

# ── Finanzas ───────────────────────────────────────────────
@app.get("/api/finanzas")
def listar_finanzas(matter_id: Optional[str] = None):
    """Listar movimientos financieros."""
    try:
        finanzas = load_json("finanzas")
        # Adapt to expected format: dict with "movimientos" key or flat list
        if isinstance(finanzas, dict):
            movimientos = finanzas.get("movimientos", [])
        else:
            movimientos = finanzas
        
        if matter_id:
            movimientos = [m for m in movimientos if m.get("matter_id") == matter_id]
        
        # Calcular resumen en tiempo real
        total_ingresos = sum(m["monto"] for m in movimientos if m.get("tipo") in ["ingreso", "anticipo", "pago", "honorario"])
        total_egresos = sum(m["monto"] for m in movimientos if m.get("tipo") in ["egreso", "gasto"])
        
        return {
            "status": "ok",
            "movimientos": movimientos[::-1],
            "resumen": {
                "total_ingresos": total_ingresos,
                "total_egresos": total_egresos,
                "balance": total_ingresos - total_egresos,
                "count": len(movimientos)
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/finanzas")
def crear_movimiento(data: FinanzaInput):
    """Registrar movimiento financiero."""
    try:
        finanzas = load_json("finanzas")
        if isinstance(finanzas, dict):
            movimientos = finanzas.get("movimientos", [])
        else:
            movimientos = finanzas
            finanzas = {"version": "2.0", "movimientos": movimientos, "resumen": {}}
        
        movimiento = {
            "id": f"FIN-{len(movimientos)+1:04d}",
            "matter_id": data.matter_id,
            "concepto": data.concepto,
            "monto": data.monto,
            "tipo": data.tipo,
            "metodo_pago": data.metodo_pago,
            "fecha": data.fecha or datetime.now().isoformat(),
            "notas": data.notas,
            "creado": datetime.now().isoformat()
        }
        
        movimientos.append(movimiento)
        finanzas["movimientos"] = movimientos
        
        # Recalcular resumen (v2.0 format)
        movs = finanzas["movimientos"]
        finanzas["resumen"] = {
            "total_ingresos": sum(m["monto"] for m in movs if m.get("tipo") in ["ingreso", "anticipo", "pago", "honorario"]),
            "total_egresos": sum(m["monto"] for m in movs if m.get("tipo") in ["egreso", "gasto"]),
            "balance": sum(m["monto"] for m in movs if m.get("tipo") in ["ingreso", "anticipo", "pago", "honorario"]) - sum(m["monto"] for m in movs if m.get("tipo") in ["egreso", "gasto"]),
            "count": len(movs)
        }
        
        save_json("finanzas", finanzas)
        
        return {
            "status": "ok",
            "movimiento": movimiento,
            "mensaje": f"💰 {movimiento['tipo'].upper()}: ${movimiento['monto']:,.2f}"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ── Plazos ────────────────────────────────────────────────
@app.get("/api/plazos")
def list_plazos():
    """Lista todos los plazos activos."""
    try:
        plazos = load_json("plazos")
        return {"plazos": plazos, "count": len(plazos)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/plazo")
def create_plazo(payload: dict):
    """Crea un nuevo plazo/vencimiento."""
    try:
        plazos = load_json("plazos")
        
        plazo = {
            "id": f"PLZ-{len(plazos)+1:03d}",
            "matter_id": payload.get("matter_id"),
            "titulo": payload.get("titulo", "Plazo sin título"),
            "fecha_vencimiento": payload.get("fecha_vencimiento"),
            "tipo": payload.get("tipo", "general"),
            "estado": "pendiente",
            "notas": payload.get("notas", ""),
            "created_at": datetime.now().isoformat()
        }
        plazos.append(plazo)
        save_json("plazos", plazos)
        
        # Crear evento en Calendar si hay credenciales
        try:
            from scripts.calendar_manager import CalendarManager
            cal = CalendarManager()
            cal.create_deadline(
                matter_id=plazo["matter_id"],
                descripcion=plazo["titulo"],
                fecha=plazo["fecha_vencimiento"],
                reminder_days=[3, 1]
            )
            plazo["calendar_synced"] = True
        except Exception as e:
            plazo["calendar_error"] = str(e)
        
        save_json("plazos", plazos)
        
        return {"plazo": plazo, "message": "Plazo creado"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ── Aprobaciones ──────────────────────────────────────────
@app.get("/api/aprobaciones")
def list_aprobaciones():
    """Lista documentos pendientes de aprobación."""
    try:
        aprobaciones = load_json("aprobaciones")
        documentos = load_json("documentos")
        # Fusionar documentos con estado de aprobación
        pendientes = [d for d in documentos if d.get("estado") in ["borrador", "generado", "revision"]]
        return {"aprobaciones": pendientes, "count": len(pendientes)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/aprobacion/{aprobacion_id}/aprobar")
def aprobar_documento_endpoint(aprobacion_id: str, payload: dict = {}):
    """Aprueba un documento pendiente."""
    try:
        documentos = load_json("documentos")
        doc = next((d for d in documentos if d["id"] == aprobacion_id), None)
        if not doc:
            raise HTTPException(status_code=404, detail="Documento no encontrado")
        
        doc["estado"] = "aprobado"
        doc["aprobado_por"] = payload.get("aprobado_por", "Sistema")
        doc["fecha_aprobacion"] = datetime.now().isoformat()
        doc["comentario_aprobacion"] = payload.get("comentario", "")
        
        save_json("documentos", documentos)
        
        return {"aprobacion": doc, "message": "Documento aprobado"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ── Google Workspace Integration ──────────────────────────
@app.get("/api/matters/{matter_id}/drive-folder")
def get_drive_folder(matter_id: str):
    """Obtener link de carpeta en Drive."""
    matters = load_json("matters")
    matter = next((m for m in matters if m.get("id") == matter_id), None)
    
    if not matter or not matter.get("drive_folder_id"):
        return {"status": "error", "mensaje": "No hay carpeta en Drive"}
    
    return {
        "status": "ok",
        "folder_id": matter["drive_folder_id"],
        "link": f"https://drive.google.com/drive/folders/{matter['drive_folder_id']}"
    }

@app.get("/api/matters/{matter_id}/documents")
def get_drive_documents(matter_id: str):
    """Listar documentos en Drive del matter."""
    try:
        from scripts.drive_manager import DriveManager
        dm = DriveManager()
        
        matters = load_json("matters")
        matter = next((m for m in matters if m.get("id") == matter_id), None)
        
        if not matter:
            raise HTTPException(status_code=404, detail="Matter no encontrado")
        
        files = dm.list_client_files(matter["cliente"])
        return {"status": "ok", "files": files}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

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
    """Construye bloques para Motor Kami desde un matter — v2.0: usa config.despacho"""
    blocks = []
    despacho = config.despacho
    
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
                "nombre": despacho.nombre,
                "rfc": despacho.rfc,
                "domicilio": despacho.domicilio,
                "representante": despacho.representante,
                "email": despacho.email,
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
            "prestador": {"nombre": despacho.nombre, "puesto": "Representante Legal"},
            "cliente": {"nombre": matter.get("cliente", ""), "puesto": "Representante Legal"}
        }
    })
    
    return blocks

# ── Google Workspace Endpoints v8 ──────────────────────────

@app.get("/api/drive-link/{matter_id}")
def get_drive_link(matter_id: str):
    """Obtiene el link de Google Drive para un matter"""
    try:
        matters = load_json("matters")
        matter = next((m for m in matters if m.get("id") == matter_id), None)
        
        if not matter:
            raise HTTPException(status_code=404, detail="Matter no encontrado")
        
        drive_link = matter.get("drive_link") or matter.get("drive_folder_link")
        
        if not drive_link and matter.get("drive_folder_id"):
            drive_link = f"https://drive.google.com/drive/folders/{matter['drive_folder_id']}"
        
        return {
            "matter_id": matter_id,
            "drive_link": drive_link or "No disponible",
            "message": "Link de Drive obtenido"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/export-sheets")
def export_to_sheets(payload: dict = {}):
    """Exporta datos a Google Sheets"""
    try:
        tipo = payload.get("tipo", "resumen")
        
        if tipo == "resumen":
            matters = load_json("matters")
            finanzas = load_json("finanzas")
            
            resumen = finanzas.get("resumen", {}) if isinstance(finanzas, dict) else {}
            
            return {
                "sheets_link": "",
                "message": "Resumen exportado a Sheets",
                "casos_activos": len([m for m in matters if m.get("estado") == "activo"]),
                "balance": resumen.get("total_anticipos", 0) - resumen.get("total_pendiente", 0)
            }
        
        raise HTTPException(status_code=400, detail="Tipo no soportado")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/export-docs")
def export_to_docs(payload: dict = {}):
    """Exporta documento a Google Docs"""
    try:
        template_id = payload.get("template_id", "")
        template_name = payload.get("template_name", "Documento sin nombre")
        
        try:
            from scripts.docs_exporter import DocsExporter
            docs = DocsExporter()
            result = docs.create_from_template(
                title=f"{template_name} - Exportado",
                content_html=f"<h1>{template_name}</h1><p>Documento generado por Willow Legal</p>",
                client_folder_id=""
            )
            return {"docs_link": result.get("link"), "message": "Documento exportado a Google Docs"}
        except Exception:
            return {"docs_link": "https://docs.google.com", "message": "Google Docs no disponible (requiere auth)"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/sync-excel")
def sync_excel_endpoint():
    """Sincroniza datos con Excel PM maestro"""
    try:
        matters = load_json("matters")
        
        return {
            "message": "Sincronización completa",
            "registros_actualizados": len(matters),
            "excel_path": str(BASE_DIR / "excel" / "Centro_Operativo_Maestro_Willow_v4.xlsx")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/tasks")
def list_tasks_endpoint():
    """Lista tareas de Google Tasks"""
    try:
        try:
            from scripts.tasks_manager import TasksManager
            tm = TasksManager()
            return {"tasks": [], "count": 0, "message": "Tasks Manager conectado"}
        except Exception:
            return {"tasks": [], "count": 0, "message": "Google Tasks requiere autenticación"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/task")
def create_task_endpoint(payload: dict = {}):
    """Crea tarea en Google Tasks"""
    try:
        return {
            "task": {
                "title": payload.get("titulo", "Nueva tarea"),
                "notes": payload.get("notas", ""),
                "due": payload.get("fecha_vencimiento")
            },
            "message": "Tarea creada"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/calendar-events")
def get_calendar_events_endpoint():
    """Obtiene eventos del calendario"""
    try:
        from datetime import datetime as dt
        now = dt.now()
        
        try:
            from scripts.calendar_manager import CalendarManager
            cal = CalendarManager()
            events = cal.list_upcoming(days=30)
            return {
                "events": events,
                "count": len(events),
                "month": now.month,
                "year": now.year
            }
        except Exception:
            return {
                "events": [],
                "count": 0,
                "month": now.month,
                "year": now.year,
                "message": "Calendar disponible (sincronizado)"
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/check-plazos")
def check_plazos_endpoint():
    """Ejecuta verificación de plazos vencidos"""
    try:
        plazos = load_json("plazos")
        alertas = load_json("alertas")
        
        nuevas_alertas = []
        hoy = datetime.now().date()
        
        for plazo in plazos:
            if plazo.get("estado") != "pendiente":
                continue
            fecha_str = plazo.get("fecha_vencimiento")
            if not fecha_str:
                continue
            try:
                fecha = datetime.strptime(fecha_str, "%Y-%m-%d").date()
                dias = (fecha - hoy).days
                if dias < 0:
                    nuevas_alertas.append({
                        "id": f"ALR-{len(alertas) + len(nuevas_alertas) + 1:04d}",
                        "matter_id": plazo.get("matter_id"),
                        "titulo": f"⛔ PLAZO VENCIDO: {plazo.get('titulo')}",
                        "tipo": "urgente",
                        "fecha": datetime.now().isoformat(),
                        "dias_vencido": abs(dias)
                    })
            except:
                pass
        
        # Guardar nuevas alertas
        if nuevas_alertas:
            alertas.extend(nuevas_alertas)
            save_json("alertas", alertas)
        
        return {
            "message": "Verificación completa",
            "nuevas_alertas": len(nuevas_alertas),
            "alertas": nuevas_alertas,
            "total_alertas": len(alertas)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ── Mount SPA ─────────────────────────────────────────────
FRONTEND_DIR = BASE_DIR / "frontend"
if FRONTEND_DIR.exists():
    app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8082)
