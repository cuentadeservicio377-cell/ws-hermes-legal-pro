#!/usr/bin/env /usr/bin/python3
# -*- coding: utf-8 -*-
"""
MOTOR KAMI — Motor de Documentos Legales con Legal Design
============================================================
Servicio centralizado para generación de documentos legales con diseño Kami.

Usado por:
- Hermes Neo (vía CLI / API local)
- Agentes de Onyx (vía tool LegalDocumentTool)
- Scripts automáticos (cron jobs, triggers)

Regla de oro: Kami maquilla el CONTENEDOR, no el CONTENIDO.
"""

import argparse
import json
import sys
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import Optional, Dict, List, Any
from weasyprint import HTML, CSS

# ============================================================
# CONFIGURACIÓN
# ============================================================
MOTOR_ROOT = Path(__file__).parent
TEMPLATES_DIR = MOTOR_ROOT / "templates"
OUTPUT_DIR = MOTOR_ROOT / "output"
TEMPLATES_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

# ============================================================
# SISTEMA DE DISEÑO KAMI v2 — Editorial Elegante
# ============================================================
KAMI_V2_CSS = """
@page {
    size: A4;
    margin: 28mm 22mm 30mm 22mm;
    background: #faf9f4;
    @bottom-center {
        content: counter(page);
        font-family: "Source Serif 4", "Newsreader", "Charter", Georgia, serif;
        font-size: 9pt;
        color: #9c9b94;
        font-variant-numeric: oldstyle-nums;
    }
    @top-center {
        content: string(doc-title);
        font-family: "Inter", -apple-system, sans-serif;
        font-size: 7.5pt;
        font-weight: 500;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        color: #b8b7b0;
    }
}
@page:first {
    @bottom-center { content: ""; }
    @top-center { content: ""; }
}

* { box-sizing: border-box; margin: 0; padding: 0; }

:root {
    --parchment: #faf9f4;
    --ink-blue: #1B365D;
    --ink-soft: #2a4a7a;
    --near-black: #1a1a18;
    --dark-warm: #3d3d3a;
    --mid: #6b6a63;
    --stone: #9c9b94;
    --border-light: #e8e6dc;
    --border-mid: #d4d2c8;
    --accent: #8B0000;
}

body {
    background: var(--parchment);
    color: var(--near-black);
    font-family: "Source Serif 4", "Newsreader", "Charter", Georgia, serif;
    font-size: 10.8pt;
    line-height: 1.62;
    font-variant-numeric: oldstyle-nums proportional-nums;
}

/* ===== COVER PAGE ===== */
.cover {
    min-height: 234mm;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
    page-break-after: always;
    padding: 20mm;
}
.cover-ornament {
    width: 12mm;
    height: 1.5pt;
    background: var(--ink-blue);
    margin: 0 auto 14mm;
}
.cover-brand {
    font-family: "Inter", sans-serif;
    font-size: 9pt;
    font-weight: 600;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: var(--stone);
    margin-bottom: 10mm;
}
.cover-title {
    font-size: 26pt;
    font-weight: 400;
    color: var(--ink-blue);
    line-height: 1.2;
    margin-bottom: 6mm;
    letter-spacing: -0.01em;
    string-set: doc-title content();
}
.cover-subtitle {
    font-size: 12pt;
    color: var(--mid);
    margin-bottom: 18mm;
    font-style: italic;
    font-weight: 400;
}
.cover-divider {
    width: 40mm;
    height: 0.5pt;
    background: var(--border-mid);
    margin: 0 auto 14mm;
}
.cover-meta {
    font-family: "Inter", sans-serif;
    font-size: 9.5pt;
    color: var(--mid);
    line-height: 2;
    font-weight: 400;
}
.cover-meta strong {
    color: var(--dark-warm);
    font-weight: 500;
}

/* ===== HEADINGS ===== */
h1 {
    font-size: 13pt;
    font-weight: 600;
    color: var(--ink-blue);
    margin-top: 10mm;
    margin-bottom: 4mm;
    page-break-after: avoid;
    letter-spacing: 0.02em;
    border-bottom: 0.5pt solid var(--border-light);
    padding-bottom: 2mm;
}
h2 {
    font-size: 11pt;
    font-weight: 600;
    color: var(--ink-soft);
    margin-top: 5mm;
    margin-bottom: 2.5mm;
    page-break-after: avoid;
}
h3 {
    font-size: 10.5pt;
    font-weight: 600;
    color: var(--dark-warm);
    margin-top: 3.5mm;
    margin-bottom: 2mm;
    page-break-after: avoid;
}

/* ===== BODY TEXT ===== */
p {
    margin-bottom: 3.5mm;
    text-align: justify;
    hyphens: auto;
    orphans: 3;
    widows: 3;
}

/* ===== PARTIES ===== */
.parties-section {
    margin-bottom: 6mm;
}
.parties-label {
    font-weight: 600;
    color: var(--ink-blue);
    margin-top: 4mm;
    margin-bottom: 1.5mm;
    font-size: 10.5pt;
}
.parties-data {
    margin-bottom: 1mm;
    padding-left: 5mm;
    color: var(--dark-warm);
}
.parties-data strong {
    color: var(--near-black);
    font-weight: 600;
}

/* ===== TABLES ===== */
table {
    width: 100%;
    border-collapse: collapse;
    margin: 5mm 0;
    font-size: 10pt;
    page-break-inside: avoid;
}
th {
    background: var(--ink-blue);
    color: #faf9f4;
    font-weight: 500;
    text-align: left;
    padding: 2.5mm 3.5mm;
    font-family: "Inter", sans-serif;
    font-size: 8.5pt;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}
td {
    padding: 2.5mm 3.5mm;
    border-bottom: 0.4pt solid var(--border-light);
    vertical-align: top;
}
tr:nth-child(even) td {
    background: rgba(27, 54, 93, 0.02);
}

/* ===== SIGNATURES ===== */
.sig-section {
    margin-top: 14mm;
    page-break-inside: avoid;
}
.sig-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 12mm 16mm;
    margin-top: 8mm;
}
.sig-box {
    text-align: center;
}
.sig-line {
    border-top: 0.6pt solid var(--near-black);
    margin-top: 18mm;
    padding-top: 2.5mm;
    font-size: 9.5pt;
    line-height: 1.6;
}
.sig-name {
    font-weight: 600;
    color: var(--ink-blue);
    font-size: 10pt;
}

/* ===== ANNEX ===== */
.annex-title {
    font-size: 16pt;
    font-weight: 400;
    color: var(--ink-blue);
    margin-top: 12mm;
    margin-bottom: 5mm;
    page-break-before: always;
    text-align: center;
    letter-spacing: 0.03em;
}
.annex-subtitle {
    text-align: center;
    font-size: 10pt;
    color: var(--mid);
    margin-bottom: 8mm;
    font-style: italic;
}
.annex-note {
    font-size: 9pt;
    color: var(--stone);
    margin-bottom: 5mm;
    font-style: italic;
}

/* ===== MISC ===== */
.small { font-size: 8.5pt; color: var(--stone); }
.center { text-align: center; }
.mt-4 { margin-top: 4mm; }
.mt-8 { margin-top: 8mm; }
.mb-4 { margin-bottom: 4mm; }
.contract-number {
    font-family: "Inter", sans-serif;
    font-size: 9.5pt;
    color: var(--stone);
    text-align: center;
    margin-bottom: 8mm;
    letter-spacing: 0.05em;
}
.disclaimer-footer {
    margin-top: 10mm;
    padding-top: 4mm;
    border-top: 0.3pt solid var(--border-light);
    font-size: 8pt;
    color: var(--stone);
    text-align: center;
    line-height: 1.5;
}

/* ===== CLAUSE NUMBERS INLINE ===== */
.clause-num {
    font-family: "Inter", sans-serif;
    font-size: 9pt;
    font-weight: 600;
    color: var(--ink-blue);
    margin-right: 2mm;
}
"""

# ============================================================
# PLANTILLAS HTML
# ============================================================

def render_contrato(data: dict) -> str:
    """Renderiza un contrato de prestación de servicios."""
    
    partes_prestador = data.get("prestador", {})
    partes_cliente = data.get("cliente", {})
    clausulas = data.get("clausulas", [])
    anexos = data.get("anexos", [])
    
    html = f"""<!DOCTYPE html>
<html lang="es">
<head><meta charset="UTF-8"><title>{data.get('titulo', 'Contrato')}</title></head>
<body>

<!-- COVER -->
<div class="cover">
    <div class="cover-ornament"></div>
    <div class="cover-brand">{data.get('marca', 'Willow Legal')}</div>
    <div class="cover-title">{data.get('titulo', 'Contrato de Prestación de Servicios')}</div>
    <div class="cover-subtitle">{data.get('subtitulo', '')}</div>
    <div class="cover-divider"></div>
    <div class="cover-meta">
        <strong>Contrato No.:</strong> {data.get('numero_contrato', '____-____-____')}<br>
        <strong>Fecha:</strong> {data.get('fecha', '___________________________')}<br><br>
        <strong>Prestador:</strong> {partes_prestador.get('nombre', '___________________________')}<br>
        <strong>Cliente:</strong> {partes_cliente.get('nombre', '___________________________')}
    </div>
</div>

<!-- CUERPO LEGAL -->
<div class="contract-number">{data.get('numero_contrato', '____-____-____')}</div>

<h1>Partes</h1>
<div class="parties-section">
    <div class="parties-label">PRESTADOR:</div>
    <div class="parties-data"><strong>Nombre/Razón social:</strong> {partes_prestador.get('nombre', '___________________________')}</div>
    <div class="parties-data"><strong>RFC:</strong> {partes_prestador.get('rfc', '___________________________')}</div>
    <div class="parties-data"><strong>Domicilio fiscal:</strong> {partes_prestador.get('domicilio', '___________________________')}</div>
    <div class="parties-data"><strong>Representante legal:</strong> {partes_prestador.get('representante', '___________________________')}</div>
    <div class="parties-data"><strong>Correo electrónico:</strong> {partes_prestador.get('email', '___________________________')}</div>
</div>

<div class="parties-section">
    <div class="parties-label">CLIENTE:</div>
    <div class="parties-data"><strong>Nombre/Razón social:</strong> {partes_cliente.get('nombre', '___________________________')}</div>
    <div class="parties-data"><strong>RFC:</strong> {partes_cliente.get('rfc', '___________________________')}</div>
    <div class="parties-data"><strong>Domicilio:</strong> {partes_cliente.get('domicilio', '___________________________')}</div>
    <div class="parties-data"><strong>Representante:</strong> {partes_cliente.get('representante', '___________________________')}</div>
    <div class="parties-data"><strong>Correo electrónico:</strong> {partes_cliente.get('email', '___________________________')}</div>
</div>

<h1>Antecedentes</h1>
<p>{data.get('antecedentes', 'El Cliente requiere servicios profesionales. El Prestador cuenta con la experiencia para brindarlos. Ambas partes acuerdan los términos del presente instrumento.')}</p>
"""
    
    # Renderizar cláusulas
    for i, clausula in enumerate(clausulas, 1):
        html += f"\n<h1>{i}. {clausula.get('titulo', '')}</h1>\n"
        for j, sub in enumerate(clausula.get("subclausulas", []), 1):
            html += f"<h2>{i}.{j}</h2>\n<p>{sub}</p>\n"
        # Tablas dentro de cláusula
        if "tabla" in clausula:
            html += render_tabla(clausula["tabla"])
    
    # Firmas
    html += """
<div class="sig-section">
    <h1>Firmas</h1>
    <div class="sig-grid">
        <div class="sig-box">
            <div class="sig-line">
                <span class="sig-name">""" + partes_prestador.get("nombre", "___________________________") + """</span><br>
                Prestador<br>
                <span class="small">""" + partes_prestador.get("rfc", "RFC: ___________________________") + """</span>
            </div>
        </div>
        <div class="sig-box">
            <div class="sig-line">
                <span class="sig-name">""" + partes_cliente.get("nombre", "___________________________") + """</span><br>
                Cliente / Representante Legal<br>
                <span class="small">""" + partes_cliente.get("rfc", "RFC: ___________________________") + """</span>
            </div>
        </div>
        <div class="sig-box">
            <div class="sig-line">
                <span class="sig-name">Testigo 1</span><br>
                ___________________________<br>
                <span class="small">Identificación: _______________</span>
            </div>
        </div>
        <div class="sig-box">
            <div class="sig-line">
                <span class="sig-name">Testigo 2</span><br>
                ___________________________<br>
                <span class="small">Identificación: _______________</span>
            </div>
        </div>
    </div>
</div>

<div class="disclaimer-footer">
    <p>Lugar y fecha de firma: ___________________________, a ____ de _______________ de 202____</p>
    <p style="margin-top: 2mm;">Documento generado por Willow Legal — Motor Kami v2 — Hermes + Onyx</p>
</div>
"""
    
    # Anexos
    for anexo in anexos:
        html += f"""
<div class="annex-title">Anexo {anexo.get('letra', 'A')} — {anexo.get('titulo', '')}</div>
<div class="annex-subtitle">Este anexo forma parte integral del Contrato {data.get('numero_contrato', '____-____-____')}</div>
"""
        if "tabla" in anexo:
            html += render_tabla(anexo["tabla"])
        if "contenido" in anexo:
            html += f"<p>{anexo['contenido']}</p>\n"
        html += """
<div class="disclaimer-footer">
    <p>Anexo """ + anexo.get('letra', 'A') + """ — Contrato """ + data.get('numero_contrato', '____-____-____') + """</p>
</div>
"""
    
    html += "\n</body>\n</html>"
    return html


def render_tabla(tabla: dict) -> str:
    """Renderiza una tabla de datos."""
    headers = tabla.get("headers", [])
    rows = tabla.get("rows", [])
    
    html = "<table>\n<tr>\n"
    for h in headers:
        html += f"<th>{h}</th>\n"
    html += "</tr>\n"
    
    for row in rows:
        html += "<tr>\n"
        for cell in row:
            html += f"<td>{cell}</td>\n"
        html += "</tr>\n"
    
    html += "</table>\n"
    return html


# ============================================================
# API PÚBLICA
# ============================================================
# API PÚBLICA v4 — Lectura de templates reales
# ============================================================

def generar_documento_real(
    template_key: str,
    matter_data: Dict[str, Any],
    output_path: Path,
    extra_vars: Optional[Dict[str, Any]] = None,
    despacho_data: Optional[Dict[str, str]] = None
) -> Dict[str, Any]:
    """Genera documento usando template real con Motor Kami blocks."""
    from template_engine import Template
    from variable_resolver import VariableResolver
    
    # 1. Cargar template
    try:
        template = Template.load(TEMPLATES_DIR, template_key)
    except FileNotFoundError as e:
        return {"success": False, "error": str(e)}
    
    # 2. Preparar variables
    all_vars = {**(extra_vars or {}), **matter_data}
    if despacho_data:
        all_vars["prestador"] = despacho_data
    
    # 3. Validar
    missing = template.validate_variables(all_vars)
    if missing:
        return {
            "success": False,
            "error": f"Variables faltantes: {', '.join(missing)}",
            "missing_variables": missing
        }
    
    # 4. Resolver variables en template
    resolver = VariableResolver(despacho_data or {}, matter_data)
    doc_data = resolver.resolve_dict(template.document_data_template)
    
    # 5. Generar HTML usando blocks.py
    from blocks import generar_desde_bloques
    
    blocks = []
    for block_type in template.recommended_blocks:
        if block_type == "header_brand":
            blocks.append({
                "type": "header_brand",
                "data": {
                    "marca": doc_data.get("prestador", {}).get("nombre", ""),
                    "numero_doc": doc_data.get("numero_contrato", ""),
                    "fecha": doc_data.get("fecha", "")
                }
            })
        elif block_type == "cover_page":
            blocks.append({
                "type": "cover_page",
                "data": {
                    "titulo": doc_data.get("titulo", "Documento Legal"),
                    "marca": doc_data.get("prestador", {}).get("nombre", ""),
                    "numero": doc_data.get("numero_contrato", "")
                }
            })
        elif block_type == "parties_block":
            blocks.append({
                "type": "parties_block",
                "data": {
                    "prestador": doc_data.get("prestador", {}),
                    "cliente": doc_data.get("cliente", {})
                }
            })
        elif block_type == "clause_section":
            for clausula in doc_data.get("clausulas", []):
                blocks.append({"type": "clause_section", "data": clausula})
        elif block_type == "signature_block":
            blocks.append({
                "type": "signature_block",
                "data": doc_data.get("signature_block", {})
            })
        elif block_type == "footer_block":
            blocks.append({
                "type": "footer_block",
                "data": doc_data.get("footer", {})
            })
    
    # 6. Generar via blocks.py
    try:
        html_path = str(output_path.with_suffix(".html"))
        generar_desde_bloques(
            blocks,
            str(output_path),
            options={"titulo": doc_data.get("titulo", template.label)},
            document_data=doc_data
        )
        return {
            "success": True,
            "file_path": str(output_path),
            "file_size": output_path.stat().st_size,
            "template_used": template_key,
            "template_label": template.label
        }
    except Exception as e:
        return {"success": False, "error": f"Error generando PDF: {str(e)}"}

def generar_documento(data: dict, output_path: Path) -> Path:
    """Genera un documento PDF usando el Motor Kami."""
    
    tipo = data.get("tipo", "contrato")
    
    if tipo == "contrato":
        html_content = render_contrato(data)
    else:
        raise ValueError(f"Tipo de documento no soportado: {tipo}")
    
    html = HTML(string=html_content)
    css = CSS(string=KAMI_V2_CSS)
    html.write_pdf(str(output_path), stylesheets=[css])
    
    return output_path


def main():
    parser = argparse.ArgumentParser(description="Motor Kami — Generador de documentos legales")
    parser.add_argument("--input", "-i", required=True, help="Archivo JSON con datos del documento")
    parser.add_argument("--output", "-o", required=True, help="Ruta de salida del PDF")
    parser.add_argument("--preview-html", action="store_true", help="También guardar preview HTML")
    args = parser.parse_args()
    
    with open(args.input, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    
    result = generar_documento(data, output)
    print(f"✅ PDF generado: {result} ({result.stat().st_size / 1024:.0f} KB)")
    
    # Subir a Drive si está configurado
    try:
        client_name = data.get("cliente", "")
        if client_name:
            from scripts.drive_manager import DriveManager
            dm = DriveManager()
            drive_result = dm.upload_pdf(str(result), client_name)
            print(f"📤 Drive: {drive_result['mensaje']}")
    except Exception as e:
        print(f"⚠️  Drive no configurado: {e}")
    
    if args.preview_html:
        html_path = output.with_suffix(".html")
        tipo = data.get("tipo", "contrato")
        if tipo == "contrato":
            html_content = render_contrato(data)
        html_path.write_text(html_content, encoding="utf-8")
        print(f"📝 Preview HTML: {html_path}")


if __name__ == "__main__":
    main()
