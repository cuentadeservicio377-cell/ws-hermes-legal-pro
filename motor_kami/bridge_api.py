#!/usr/bin/env /usr/bin/python3
# -*- coding: utf-8 -*-
"""
KAMI BRIDGE API
===============
Bridge entre Onyx y Motor Kami.

Endpoints:
- POST /api/kami/generate   → Genera PDF desde bloques
- POST /api/kami/validate   → Valida sustancia legal
- GET  /api/kami/templates  → Lista plantillas disponibles
- GET  /api/kami/templates/{key} → Obtiene plantilla específica
- GET  /health              → Health check

Uso:
    python3 bridge_api.py
    # o
    uvicorn bridge_api:app --host 0.0.0.0 --port 8080
"""

import sys
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import json

# Añadir directorio del motor al path
sys.path.insert(0, str(Path(__file__).parent))
from blocks import generar_desde_bloques, validar_sustancia, BLOCK_RENDERERS

app = FastAPI(
    title="Kami Bridge API",
    description="Bridge entre Onyx y Motor Kami para generación de documentos legales",
    version="3.1.0"
)

# CORS para Onyx
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

TEMPLATES_DIR = Path(__file__).parent / "templates"


# ============================================================
# MODELOS Pydantic
# ============================================================

class BlockInput(BaseModel):
    type: str
    data: Dict[str, Any] = {}
    layout: str = "full"


class GenerateRequest(BaseModel):
    blocks: List[BlockInput]
    options: Optional[Dict[str, Any]] = {}
    document_data: Optional[Dict[str, Any]] = None
    output_filename: Optional[str] = "documento.pdf"


class ValidateRequest(BaseModel):
    document_data: Dict[str, Any]


class ValidateResponse(BaseModel):
    valid: bool
    errors: List[str]
    checklist: Dict[str, bool]
    word_count: int


class TemplateInfo(BaseModel):
    key: str
    label: str
    area: str
    materia: str


class TemplateListResponse(BaseModel):
    templates: List[TemplateInfo]
    count: int


class GenerateResponse(BaseModel):
    success: bool
    file_path: str
    file_size_kb: float
    html_preview_path: str
    validation: Optional[ValidateResponse] = None


# ============================================================
# ENDPOINTS
# ============================================================

@app.get("/health")
def health():
    return {"status": "ok", "version": "3.1.0", "blocks_available": len(BLOCK_RENDERERS)}


@app.get("/api/kami/templates", response_model=TemplateListResponse)
def list_templates():
    """Lista todas las plantillas disponibles."""
    index_path = TEMPLATES_DIR / "index.json"
    if not index_path.exists():
        raise HTTPException(status_code=500, detail="Index de plantillas no encontrado")
    
    with open(index_path, "r", encoding="utf-8") as f:
        index = json.load(f)
    
    templates = [TemplateInfo(**t) for t in index.get("templates", [])]
    return TemplateListResponse(templates=templates, count=len(templates))


@app.get("/api/kami/templates/{key}")
def get_template(key: str):
    """Obtiene una plantilla específica por key."""
    template_path = TEMPLATES_DIR / f"{key}.json"
    if not template_path.exists():
        raise HTTPException(status_code=404, detail=f"Plantilla '{key}' no encontrada")
    
    with open(template_path, "r", encoding="utf-8") as f:
        return json.load(f)


@app.post("/api/kami/validate", response_model=ValidateResponse)
def validate_document(data: ValidateRequest):
    """Valida la sustancia legal de un documento sin generar PDF."""
    resultado = validar_sustancia(data.document_data)
    return ValidateResponse(**resultado)


@app.post("/api/kami/generate", response_model=GenerateResponse)
def generate_document(req: GenerateRequest):
    """Genera un documento PDF con Kami. Valida sustancia si se proporciona document_data."""
    
    # Validación previa (si hay document_data)
    validation_result = None
    if req.document_data:
        resultado = validar_sustancia(req.document_data)
        validation_result = ValidateResponse(**resultado)
        if not resultado["valid"]:
            raise HTTPException(
                status_code=400,
                detail={
                    "message": "Validación de sustancia fallida",
                    "errors": resultado["errors"],
                    "checklist": resultado["checklist"],
                    "word_count": resultado["word_count"]
                }
            )
    
    # Preparar output
    output_dir = Path(__file__).parent / "output"
    output_dir.mkdir(exist_ok=True)
    output_path = output_dir / req.output_filename
    
    # Convertir bloques a dicts planos
    blocks_plain = [b.dict() for b in req.blocks]
    
    try:
        pdf_path = generar_desde_bloques(
            blocks_plain,
            str(output_path),
            req.options or {},
            req.document_data
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generando PDF: {str(e)}")
    
    pdf_file = Path(pdf_path)
    html_file = pdf_file.with_suffix(".html")
    
    return GenerateResponse(
        success=True,
        file_path=str(pdf_file),
        file_size_kb=round(pdf_file.stat().st_size / 1024, 1),
        html_preview_path=str(html_file),
        validation=validation_result
    )


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
