#!/usr/bin/env /usr/bin/python3
# -*- coding: utf-8 -*-
"""
KAMI BLOCKS — Sistema de Bloques de Diseño Legal
=================================================
Motor de composición de documentos legales usando bloques modulares.

El agente elige bloques según el documento y el motor los compone automáticamente.

Tipos de bloque:
- header_brand: Encabezado con logo, marca, número de documento
- cover_page: Portada editorial
- parties_block: Bloque de partes con formato formal
- clause_section: Sección de cláusula con numeralia
- payment_table: Tabla de pagos con estilo robusto
- comparison_table: Cuadro comparativo (2 columnas)
- flow_diagram: Diagrama de flujo SVG
- deliverables_table: Tabla de entregables
- signature_block: Bloque de firmas robusto
- footer_block: Pie con disclaimer y número de página
- annex_section: Sección de anexo
- highlight_rule: Regla visual separadora (no caja de color)
- data_grid: Grid de datos (ej: canales de comunicación)
- checklist_block: Lista con checkboxes
- timeline_block: Línea de tiempo visual
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field


# ============================================================
# VALIDADOR DE SUSTANCIA LEGAL
# ============================================================

METAFORAS_PROHIBIDAS = [
    "como la cfe", "como la CFE", "como la Cfe",
    "metáfora del sastre", "metáfora del traje",
    "mancha de excel", "mancha de Excel",
    "sastre a medida", "traje a medida",
]

ELEMENTOS_OBLIGATORIOS = [
    "partes",
    "antecedentes",
    "objeto",
    "forma_pago",
    "plazo",
    "entregables",
    "propiedad_intelectual",
    "confidencialidad",
    "limitacion_responsabilidad",
    "suspension_terminacion",
    "mediacion_jurisdiccion",
    "disposiciones_generales",
    "firmas",
]


def validar_sustancia(data: dict) -> dict:
    """
    Valida que un documento legal tenga sustancia completa antes de aplicar Kami.
    Retorna: { "valid": bool, "errors": list, "checklist": dict }
    """
    errors = []
    checklist = {k: False for k in ELEMENTOS_OBLIGATORIOS}
    texto_completo = ""
    
    # Acumular todo el texto para análisis de tono
    clausulas = data.get("clausulas", [])
    for c in clausulas:
        for sub in c.get("subclausulas", []):
            texto_completo += " " + sub
    
    # 1. PARTES
    prestador = data.get("prestador", {})
    cliente = data.get("cliente", {})
    partes_ok = bool(
        prestador.get("nombre") and prestador.get("rfc") and
        prestador.get("domicilio") and prestador.get("email") and
        cliente.get("nombre") and cliente.get("rfc") and
        cliente.get("domicilio") and cliente.get("email")
    )
    if not partes_ok:
        errors.append("PARTES incompletas: faltan nombre, RFC, domicilio o email de prestador y/o cliente")
    checklist["partes"] = partes_ok
    
    # 2. ANTECEDENTES
    antecedentes = data.get("antecedentes", "")
    ant_ok = bool(antecedentes and len(antecedentes.strip()) > 20)
    if not ant_ok:
        errors.append("ANTECEDENTES: texto muy corto o vacío")
    checklist["antecedentes"] = ant_ok
    
    # Mapear títulos de cláusulas
    titulos = [c.get("titulo", "").lower() for c in clausulas]
    
    # 3. OBJETO Y ALCANCE
    obj_ok = any("objeto" in t or "alcance" in t for t in titulos)
    if not obj_ok:
        errors.append("OBJETO Y ALCANCE: falta cláusula con 'objeto' o 'alcance'")
    checklist["objeto"] = obj_ok
    
    # 4. FORMA DE PAGO
    pago_ok = any("pago" in t or "pago" in t for t in titulos)
    if not pago_ok:
        errors.append("FORMA DE PAGO: falta cláusula con 'pago'")
    checklist["forma_pago"] = pago_ok
    
    # 5. PLAZO
    plazo_ok = any("plazo" in t for t in titulos)
    if not plazo_ok:
        errors.append("PLAZO: falta cláusula con 'plazo'")
    checklist["plazo"] = plazo_ok
    
    # 6. ENTREGABLES
    ent_ok = any("entregable" in t for t in titulos) or any("anexo" in a.get("titulo", "").lower() for a in data.get("anexos", []))
    if not ent_ok:
        errors.append("ENTREGABLES: falta cláusula o anexo con entregables")
    checklist["entregables"] = ent_ok
    
    # 7. PROPIEDAD INTELECTUAL
    pi_ok = any("propiedad intelectual" in t or "intelectual" in t for t in titulos)
    if not pi_ok:
        errors.append("PROPIEDAD INTELECTUAL: falta cláusula")
    checklist["propiedad_intelectual"] = pi_ok
    
    # 8. CONFIDENCIALIDAD
    conf_ok = any("confidencialidad" in t for t in titulos)
    if not conf_ok:
        errors.append("CONFIDENCIALIDAD: falta cláusula")
    checklist["confidencialidad"] = conf_ok
    
    # 9. LIMITACIÓN DE RESPONSABILIDAD
    lim_ok = any("responsabilidad" in t or "limitación" in t for t in titulos)
    if not lim_ok:
        errors.append("LIMITACIÓN DE RESPONSABILIDAD: falta cláusula")
    checklist["limitacion_responsabilidad"] = lim_ok
    
    # 10. SUSPENSIÓN Y TERMINACIÓN
    susp_ok = any("suspensión" in t or "terminación" in t or "terminacion" in t for t in titulos)
    if not susp_ok:
        errors.append("SUSPENSIÓN Y TERMINACIÓN: falta cláusula")
    checklist["suspension_terminacion"] = susp_ok
    
    # 11. MEDIACIÓN Y JURISDICCIÓN
    med_ok = any("mediación" in t or "jurisdicción" in t or "jurisdiccion" in t for t in titulos)
    if not med_ok:
        errors.append("MEDIACIÓN Y JURISDICCIÓN: falta cláusula")
    checklist["mediacion_jurisdiccion"] = med_ok
    
    # 12. DISPOSICIONES GENERALES
    disp_ok = any("disposiciones" in t or "generales" in t for t in titulos)
    if not disp_ok:
        errors.append("DISPOSICIONES GENERALES: falta cláusula")
    checklist["disposiciones_generales"] = disp_ok
    
    # 13. FIRMAS
    sig = data.get("signature_block", {})
    firmas_ok = bool(sig.get("prestador") and sig.get("cliente"))
    if not firmas_ok:
        errors.append("FIRMAS: faltan datos de prestador y/o cliente en bloque de firmas")
    checklist["firmas"] = firmas_ok
    
    # Tono legal — detectar metáforas prohibidas
    texto_lower = texto_completo.lower()
    for meta in METAFORAS_PROHIBIDAS:
        if meta.lower() in texto_lower:
            errors.append(f"TONO LEGAL: metáfora prohibida detectada → '{meta}'")
    
    # Límite de palabras
    palabras = len(texto_completo.split())
    if palabras > 3000:
        errors.append(f"LÍMITE DE PALABRAS: {palabras} / máximo 3000 para contratos")
    
    valid = len(errors) == 0
    
    return {
        "valid": valid,
        "errors": errors,
        "checklist": checklist,
        "word_count": palabras,
    }


@dataclass
class Block:
    """Un bloque de diseño Kami."""
    type: str
    data: Dict[str, Any] = field(default_factory=dict)
    layout: str = "full"  # full, half, third


# ============================================================
# RENDERIZADORES DE BLOQUES
# ============================================================

def render_header_brand(data: dict) -> str:
    """Encabezado con branding."""
    marca = data.get("marca", "Willow Legal")
    doc_type = data.get("tipo_doc", "Contrato")
    numero = data.get("numero", "____-____-____")
    logo_url = data.get("logo_url", "")
    
    logo_html = f'<img src="{logo_url}" style="height:14mm;" />' if logo_url else f'<div style="font-size:11pt;font-weight:700;letter-spacing:0.15em;text-transform:uppercase;">{marca[:1]}</div>'
    
    return f"""
    <div style="display:flex;justify-content:space-between;align-items:center;border-bottom:2pt solid #1a1a18;padding-bottom:4mm;margin-bottom:6mm;">
        <div style="display:flex;align-items:center;gap:4mm;">
            <div style="width:14mm;height:14mm;background:#1a1a18;color:#faf8f0;display:flex;align-items:center;justify-content:center;font-family:'Playfair Display',Georgia,serif;font-weight:700;">
                {logo_html}
            </div>
            <div>
                <div style="font-family:'Inter',sans-serif;font-size:8pt;font-weight:600;letter-spacing:0.18em;text-transform:uppercase;color:#6b6b68;">{marca}</div>
                <div style="font-family:'Inter',sans-serif;font-size:7pt;letter-spacing:0.1em;text-transform:uppercase;color:#9a9a96;margin-top:1mm;">{doc_type} · {numero}</div>
            </div>
        </div>
        <div style="font-family:'Inter',sans-serif;font-size:7pt;color:#9a9a96;text-align:right;line-height:1.5;">
            Documento generado<br>por Sistema Willow
        </div>
    </div>
    """


def render_cover_page(data: dict) -> str:
    """Portada editorial robusta."""
    marca = data.get("marca", "Willow Legal")
    titulo = data.get("titulo", "Contrato")
    subtitulo = data.get("subtitulo", "")
    numero = data.get("numero", "____-____-____")
    fecha = data.get("fecha", "___________________________")
    prestador = data.get("prestador", "___________________________")
    cliente = data.get("cliente", "___________________________")
    
    return f"""
    <div style="min-height:234mm;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;padding:20mm;page-break-after:always;">
        <div style="font-family:'Inter',sans-serif;font-size:8pt;font-weight:600;letter-spacing:0.25em;text-transform:uppercase;color:#9a9a96;margin-bottom:20mm;">{marca}</div>
        
        <div style="width:20mm;height:3pt;background:#1a1a18;margin-bottom:16mm;"></div>
        
        <div style="font-family:'Playfair Display',Georgia,serif;font-size:30pt;font-weight:700;color:#1a1a18;line-height:1.1;letter-spacing:-0.02em;margin-bottom:6mm;max-width:160mm;">
            {titulo}
        </div>
        
        {f'<div style="font-family:"Playfair Display",Georgia,serif;font-size:14pt;font-style:italic;color:#4a4a46;margin-bottom:16mm;">{subtitulo}</div>' if subtitulo else ''}
        
        <div style="width:40mm;height:0.5pt;background:#c8c6be;margin:0 auto 16mm;"></div>
        
        <div style="font-family:'Inter',sans-serif;font-size:9.5pt;color:#6b6b68;line-height:2;font-weight:400;">
            <div><strong style="color:#1a1a18;">Documento No.</strong> {numero}</div>
            <div><strong style="color:#1a1a18;">Fecha:</strong> {fecha}</div>
            <div style="margin-top:4mm;"><strong style="color:#1a1a18;">Prestador:</strong> {prestador}</div>
            <div><strong style="color:#1a1a18;">Cliente:</strong> {cliente}</div>
        </div>
    </div>
    """


def render_parties_block(data: dict) -> str:
    """Bloque de partes formal con peso visual."""
    prestador = data.get("prestador", {})
    cliente = data.get("cliente", {})
    
    def render_party(label: str, party: dict) -> str:
        return f"""
        <div style="margin-bottom:5mm;">
            <div style="font-family:'Playfair Display',Georgia,serif;font-size:11pt;font-weight:700;color:#1a1a18;margin-bottom:2mm;border-left:3pt solid #1a1a18;padding-left:3mm;">
                {label}
            </div>
            <div style="padding-left:6mm;line-height:1.8;font-size:10pt;color:#3d3d3a;">
                <div><strong style="color:#1a1a18;">Nombre:</strong> {party.get('nombre', '___________________________')}</div>
                <div><strong style="color:#1a1a18;">RFC:</strong> {party.get('rfc', '___________________________')}</div>
                <div><strong style="color:#1a1a18;">Domicilio:</strong> {party.get('domicilio', '___________________________')}</div>
                <div><strong style="color:#1a1a18;">Representante:</strong> {party.get('representante', '___________________________')}</div>
                <div><strong style="color:#1a1a18;">Email:</strong> {party.get('email', '___________________________')}</div>
            </div>
        </div>
        """
    
    return f"""
    <h1 style="font-family:'Playfair Display',Georgia,serif;font-size:16pt;font-weight:700;color:#1a1a18;margin-top:0;margin-bottom:5mm;letter-spacing:-0.01em;border-bottom:1pt solid #1a1a18;padding-bottom:2mm;">
        Partes
    </h1>
    {render_party("PRESTADOR", prestador)}
    {render_party("CLIENTE", cliente)}
    """


def render_clause_section(data: dict) -> str:
    """Sección de cláusula con numeralia editorial."""
    numero = data.get("numero", "1")
    titulo = data.get("titulo", "")
    subclausulas = data.get("subclausulas", [])
    
    subs_html = ""
    for i, sub in enumerate(subclausulas, 1):
        subs_html += f"""
        <div style="margin-bottom:3mm;">
            <span style="font-family:'Inter',sans-serif;font-size:9pt;font-weight:700;color:#1a1a18;">{numero}.{i}</span>
            <span style="margin-left:2mm;">{sub}</span>
        </div>
        """
    
    return f"""
    <div style="margin-top:8mm;margin-bottom:5mm;">
        <div style="font-family:'Playfair Display',Georgia,serif;font-size:13pt;font-weight:700;color:#1a1a18;margin-bottom:3mm;display:flex;align-items:baseline;gap:3mm;">
            <span style="font-family:'Inter',sans-serif;font-size:18pt;font-weight:800;color:#1a1a18;">{numero}</span>
            <span style="border-bottom:1pt solid #1a1a18;padding-bottom:1mm;">{titulo}</span>
        </div>
        <div style="padding-left:8mm;border-left:0.5pt solid #d4d2c8;">
            {subs_html}
        </div>
    </div>
    """


def render_payment_table(data: dict) -> str:
    """Tabla de pagos con estilo editorial robusto."""
    headers = data.get("headers", ["Concepto", "%", "Monto", "Vencimiento"])
    rows = data.get("rows", [])
    
    headers_html = "".join([f'<th style="background:#1a1a18;color:#faf8f0;font-family:Inter,sans-serif;font-size:8.5pt;font-weight:600;text-transform:uppercase;letter-spacing:0.08em;padding:3mm 4mm;text-align:left;border:0.5pt solid #1a1a18;">{h}</th>' for h in headers])
    
    rows_html = ""
    for i, row in enumerate(rows):
        bg = "#f5f3eb" if i % 2 == 0 else "#faf8f0"
        cells = "".join([f'<td style="padding:3mm 4mm;border:0.5pt solid #c8c6be;font-size:10pt;color:#1a1a18;background:{bg};">{c}</td>' for c in row])
        rows_html += f"<tr>{cells}</tr>"
    
    return f"""
    <table style="width:100%;border-collapse:collapse;margin:4mm 0;page-break-inside:avoid;border:1pt solid #1a1a18;">
        <thead><tr>{headers_html}</tr></thead>
        <tbody>{rows_html}</tbody>
    </table>
    """


def render_comparison_table(data: dict) -> str:
    """Cuadro comparativo de 2 columnas."""
    title = data.get("titulo", "Comparativo")
    left_label = data.get("left_label", "Prestador")
    right_label = data.get("right_label", "Cliente")
    items = data.get("items", [])
    
    items_html = ""
    for item in items:
        items_html += f"""
        <tr>
            <td style="padding:2.5mm 3mm;border-bottom:0.5pt solid #d4d2c8;font-size:9.5pt;color:#3d3d3a;background:#f5f3eb;font-weight:600;">{item.get('label', '')}</td>
            <td style="padding:2.5mm 3mm;border-bottom:0.5pt solid #d4d2c8;font-size:9.5pt;color:#1a1a18;">{item.get('left', '')}</td>
            <td style="padding:2.5mm 3mm;border-bottom:0.5pt solid #d4d2c8;font-size:9.5pt;color:#1a1a18;">{item.get('right', '')}</td>
        </tr>
        """
    
    return f"""
    <div style="margin:5mm 0;page-break-inside:avoid;">
        <div style="font-family:'Playfair Display',Georgia,serif;font-size:11pt;font-weight:700;color:#1a1a18;margin-bottom:3mm;text-align:center;">{title}</div>
        <table style="width:100%;border-collapse:collapse;border:1pt solid #1a1a18;">
            <thead>
                <tr style="background:#1a1a18;color:#faf8f0;">
                    <th style="padding:3mm;font-family:Inter,sans-serif;font-size:8.5pt;font-weight:600;text-transform:uppercase;letter-spacing:0.08em;text-align:left;width:35%;">Concepto</th>
                    <th style="padding:3mm;font-family:Inter,sans-serif;font-size:8.5pt;font-weight:600;text-transform:uppercase;letter-spacing:0.08em;text-align:left;width:32.5%;">{left_label}</th>
                    <th style="padding:3mm;font-family:Inter,sans-serif;font-size:8.5pt;font-weight:600;text-transform:uppercase;letter-spacing:0.08em;text-align:left;width:32.5%;">{right_label}</th>
                </tr>
            </thead>
            <tbody>{items_html}</tbody>
        </table>
    </div>
    """


def render_flow_diagram(data: dict) -> str:
    """Diagrama de flujo SVG."""
    steps = data.get("steps", ["Inicio", "Proceso", "Fin"])
    title = data.get("titulo", "Flujo del Proceso")
    
    step_width = 35
    gap = 15
    total_width = len(steps) * step_width + (len(steps) - 1) * gap + 20
    height = 50
    
    steps_svg = ""
    arrows_svg = ""
    x = 10
    
    for i, step in enumerate(steps):
        # Caja
        steps_svg += f'<rect x="{x}" y="15" width="{step_width}" height="20" rx="2" fill="#1a1a18" stroke="#1a1a18" stroke-width="1"/>'
        steps_svg += f'<text x="{x + step_width/2}" y="28.5" text-anchor="middle" fill="#faf8f0" font-family="Inter,sans-serif" font-size="5pt" font-weight="600">{step[:12]}</text>'
        
        # Flecha
        if i < len(steps) - 1:
            arrow_x = x + step_width
            arrows_svg += f'<line x1="{arrow_x}" y1="25" x2="{arrow_x + gap - 3}" y2="25" stroke="#1a1a18" stroke-width="1"/>'
            arrows_svg += f'<polygon points="{arrow_x + gap - 3},22 {arrow_x + gap},25 {arrow_x + gap - 3},28" fill="#1a1a18"/>'
        
        x += step_width + gap
    
    return f"""
    <div style="margin:5mm 0;text-align:center;page-break-inside:avoid;">
        <div style="font-family:'Playfair Display',Georgia,serif;font-size:11pt;font-weight:700;color:#1a1a18;margin-bottom:3mm;">{title}</div>
        <svg viewBox="0 0 {total_width} {height}" style="max-width:100%;height:auto;">
            {arrows_svg}
            {steps_svg}
        </svg>
    </div>
    """


def render_signature_block(data: dict) -> str:
    """Bloque de firmas robusto."""
    prestador = data.get("prestador", {})
    cliente = data.get("cliente", {})
    
    return f"""
    <div style="margin-top:12mm;page-break-inside:avoid;">
        <h1 style="font-family:'Playfair Display',Georgia,serif;font-size:16pt;font-weight:700;color:#1a1a18;margin-bottom:6mm;border-bottom:1pt solid #1a1a18;padding-bottom:2mm;">
            Firmas
        </h1>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:10mm 16mm;margin-top:6mm;">
            <div style="text-align:center;">
                <div style="border:1pt solid #1a1a18;padding:8mm 4mm 4mm;margin-bottom:2mm;">
                    <div style="border-top:1.5pt solid #1a1a18;padding-top:3mm;">
                        <div style="font-family:'Playfair Display',Georgia,serif;font-size:11pt;font-weight:700;color:#1a1a18;">{prestador.get('nombre', '___________________________')}</div>
                        <div style="font-size:9pt;color:#6b6b68;margin-top:1mm;">Prestador</div>
                        <div style="font-size:8pt;color:#9a9a96;margin-top:1mm;">RFC: {prestador.get('rfc', '___________________________')}</div>
                    </div>
                </div>
            </div>
            <div style="text-align:center;">
                <div style="border:1pt solid #1a1a18;padding:8mm 4mm 4mm;margin-bottom:2mm;">
                    <div style="border-top:1.5pt solid #1a1a18;padding-top:3mm;">
                        <div style="font-family:'Playfair Display',Georgia,serif;font-size:11pt;font-weight:700;color:#1a1a18;">{cliente.get('nombre', '___________________________')}</div>
                        <div style="font-size:9pt;color:#6b6b68;margin-top:1mm;">Cliente / Representante Legal</div>
                        <div style="font-size:8pt;color:#9a9a96;margin-top:1mm;">RFC: {cliente.get('rfc', '___________________________')}</div>
                    </div>
                </div>
            </div>
            <div style="text-align:center;">
                <div style="border:1pt solid #c8c6be;padding:8mm 4mm 4mm;">
                    <div style="border-top:1pt solid #9a9a96;padding-top:3mm;">
                        <div style="font-family:'Playfair Display',Georgia,serif;font-size:10pt;font-weight:700;color:#3d3d3a;">Testigo 1</div>
                        <div style="font-size:8pt;color:#9a9a96;margin-top:1mm;">Nombre e identificación</div>
                    </div>
                </div>
            </div>
            <div style="text-align:center;">
                <div style="border:1pt solid #c8c6be;padding:8mm 4mm 4mm;">
                    <div style="border-top:1pt solid #9a9a96;padding-top:3mm;">
                        <div style="font-family:'Playfair Display',Georgia,serif;font-size:10pt;font-weight:700;color:#3d3d3a;">Testigo 2</div>
                        <div style="font-size:8pt;color:#9a9a96;margin-top:1mm;">Nombre e identificación</div>
                    </div>
                </div>
            </div>
        </div>
        <div style="margin-top:6mm;text-align:center;font-size:9pt;color:#6b6b68;">
            Lugar y fecha de firma: <strong style="color:#1a1a18;">___________________________</strong>, a <strong style="color:#1a1a18;">____</strong> de <strong style="color:#1a1a18;">_______________</strong> de 202<strong style="color:#1a1a18;">__</strong>
        </div>
    </div>
    """


def render_footer_block(data: dict) -> str:
    """Pie de página con disclaimer."""
    marca = data.get("marca", "Willow Legal")
    doc_num = data.get("numero", "____-____-____")
    
    return f"""
    <div style="margin-top:10mm;padding-top:4mm;border-top:1pt solid #1a1a18;text-align:center;font-size:7.5pt;color:#9a9a96;line-height:1.6;font-family:'Inter',sans-serif;">
        <div style="font-weight:600;color:#6b6b68;">{marca} · {doc_num}</div>
        <div>Documento generado por Sistema Willow — Motor Kami v3</div>
        <div style="margin-top:1mm;">Este documento es confidencial y está protegido por secreto profesional.</div>
    </div>
    """


def render_annex_section(data: dict) -> str:
    """Sección de anexo."""
    letra = data.get("letra", "A")
    titulo = data.get("titulo", "")
    contenido = data.get("contenido", "")
    
    return f"""
    <div style="page-break-before:always;margin-top:8mm;">
        <div style="text-align:center;margin-bottom:6mm;">
            <div style="font-family:'Inter',sans-serif;font-size:8pt;font-weight:600;letter-spacing:0.2em;text-transform:uppercase;color:#9a9a96;margin-bottom:2mm;">Anexo {letra}</div>
            <div style="font-family:'Playfair Display',Georgia,serif;font-size:18pt;font-weight:700;color:#1a1a18;">{titulo}</div>
            <div style="width:30mm;height:1pt;background:#1a1a18;margin:3mm auto 0;"></div>
        </div>
        <div style="font-size:9.5pt;color:#6b6b68;font-style:italic;margin-bottom:5mm;text-align:center;">
            Este anexo forma parte integral del contrato y tiene el mismo valor jurídico que el cuerpo del mismo.
        </div>
        {contenido}
    </div>
    """


def render_data_grid(data: dict) -> str:
    """Grid de datos (ej: canales de comunicación)."""
    title = data.get("titulo", "")
    headers = data.get("headers", [])
    rows = data.get("rows", [])
    
    headers_html = "".join([f'<th style="background:#2d2d2a;color:#faf8f0;font-family:Inter,sans-serif;font-size:8pt;font-weight:600;text-transform:uppercase;letter-spacing:0.08em;padding:2.5mm 3mm;text-align:left;border:0.5pt solid #1a1a18;">{h}</th>' for h in headers])
    
    rows_html = ""
    for row in rows:
        cells = "".join([f'<td style="padding:2.5mm 3mm;border:0.5pt solid #c8c6be;font-size:9.5pt;color:#1a1a18;">{c}</td>' for c in row])
        rows_html += f"<tr>{cells}</tr>"
    
    return f"""
    <div style="margin:4mm 0;page-break-inside:avoid;">
        <div style="font-family:'Playfair Display',Georgia,serif;font-size:11pt;font-weight:700;color:#1a1a18;margin-bottom:2mm;">{title}</div>
        <table style="width:100%;border-collapse:collapse;border:1pt solid #1a1a18;">
            <thead><tr>{headers_html}</tr></thead>
            <tbody>{rows_html}</tbody>
        </table>
    </div>
    """


def render_highlight_rule(data: dict) -> str:
    """Regla visual separadora (no caja de color)."""
    return f"""
    <div style="margin:6mm 0;display:flex;align-items:center;gap:4mm;">
        <div style="flex:1;height:1pt;background:#1a1a18;"></div>
        <div style="font-family:'Playfair Display',Georgia,serif;font-size:9pt;font-style:italic;color:#6b6b68;white-space:nowrap;">{data.get('texto', '')}</div>
        <div style="flex:1;height:1pt;background:#1a1a18;"></div>
    </div>
    """


# ============================================================
# MOTOR DE COMPOSICIÓN
# ============================================================

BLOCK_RENDERERS = {
    "header_brand": render_header_brand,
    "cover_page": render_cover_page,
    "parties_block": render_parties_block,
    "clause_section": render_clause_section,
    "payment_table": render_payment_table,
    "comparison_table": render_comparison_table,
    "flow_diagram": render_flow_diagram,
    "signature_block": render_signature_block,
    "footer_block": render_footer_block,
    "annex_section": render_annex_section,
    "data_grid": render_data_grid,
    "highlight_rule": render_highlight_rule,
}


def compose_document(blocks: List[Block], options: dict = None) -> str:
    """Compone un documento completo a partir de bloques."""
    options = options or {}
    
    # CSS base
    css = generate_css(options)
    
    # Renderizar bloques
    body_content = ""
    for block in blocks:
        renderer = BLOCK_RENDERERS.get(block.type)
        if renderer:
            body_content += renderer(block.data)
    
    return f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>{options.get('titulo', 'Documento')}</title>
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>{css}</style>
</head>
<body>
    {body_content}
</body>
</html>"""


def generate_css(options: dict) -> str:
    """Genera CSS base para documentos Kami."""
    
    primary = options.get("color_primary", "#1a1a18")
    secondary = options.get("color_secondary", "#3d3d3a")
    accent = options.get("color_accent", "#8B0000")
    bg = options.get("color_bg", "#faf8f0")
    text = options.get("color_text", "#1a1a18")
    
    return f"""
@page {{
    size: A4;
    margin: 25mm 22mm 28mm 22mm;
    background: {bg};
    @bottom-center {{
        content: counter(page);
        font-family: "Playfair Display", Georgia, serif;
        font-size: 9pt;
        color: #9a9a96;
        font-variant-numeric: oldstyle-nums;
    }}
}}
@page:first {{
    @bottom-center {{ content: ""; }}
}}

* {{ box-sizing: border-box; margin: 0; padding: 0; }}

body {{
    background: {bg};
    color: {text};
    font-family: "Playfair Display", Georgia, "Times New Roman", serif;
    font-size: 10.8pt;
    line-height: 1.65;
    font-variant-numeric: oldstyle-nums proportional-nums;
}}

h1 {{
    font-family: "Playfair Display", Georgia, serif;
    font-size: 16pt;
    font-weight: 700;
    color: {primary};
    margin-top: 0;
    margin-bottom: 5mm;
    letter-spacing: -0.01em;
    page-break-after: avoid;
}}

p {{
    margin-bottom: 3.5mm;
    text-align: justify;
    hyphens: auto;
    orphans: 3;
    widows: 3;
}}

ul, ol {{
    margin-left: 8mm;
    margin-bottom: 4mm;
}}

li {{
    margin-bottom: 2mm;
    padding-left: 2mm;
}}

ul li {{
    list-style-type: disc;
}}

ol li {{
    list-style-type: decimal;
}}
"""


# ============================================================
# API PÚBLICA
# ============================================================

def generar_desde_bloques(blocks: List[dict], output_path: str, options: dict = None, document_data: dict = None) -> str:
    """Genera PDF desde una lista de bloques. Valida sustancia si se proporciona document_data."""
    from weasyprint import HTML, CSS
    from pathlib import Path
    
    options = options or {}
    
    # VALIDACIÓN DE SUSTANCIA (si se proporcionan datos)
    if document_data:
        resultado = validar_sustancia(document_data)
        if not resultado["valid"]:
            errores = "\n  • ".join([""] + resultado["errors"])
            raise ValueError(
                f"❌ VALIDACIÓN DE SUSTANCIA FALLIDA ({resultado['word_count']} palabras):\n"
                f"  Errores:{errores}\n\n"
                f"  Checklist:\n"
                + "\n".join([f"    {'✅' if v else '❌'} {k}" for k, v in resultado["checklist"].items()])
            )
        print(f"✅ Sustancia validada ({resultado['word_count']} palabras) — {sum(resultado['checklist'].values())}/13 elementos")
    
    # Convertir dicts a objetos Block
    block_objects = []
    for b in blocks:
        block_objects.append(Block(
            type=b.get("type"),
            data=b.get("data", {}),
            layout=b.get("layout", "full")
        ))
    
    html_content = compose_document(block_objects, options)
    
    # Guardar HTML preview
    html_path = Path(output_path).with_suffix(".html")
    html_path.write_text(html_content, encoding="utf-8")
    
    # Generar PDF
    HTML(string=html_content).write_pdf(output_path)
    
    return output_path


if __name__ == "__main__":
    import json
    import sys
    
    if len(sys.argv) < 3:
        print("Uso: python3 blocks.py <input.json> <output.pdf>")
        sys.exit(1)
    
    with open(sys.argv[1], "r", encoding="utf-8") as f:
        config = json.load(f)
    
    result = generar_desde_bloques(
        config["blocks"],
        sys.argv[2],
        config.get("options", {}),
        config.get("document_data")
    )
    
    print(f"✅ PDF generado: {result}")
