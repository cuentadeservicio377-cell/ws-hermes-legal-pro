#!/usr/bin/env python3
"""
WILLOW STANDALONE — Script Principal
Opera Willow Legal desde terminal sin depender de Onyx ni Docker.

Uso:
    python3 willow_standalone.py --status PRAG-001
    python3 willow_standalone.py --alertas
    python3 willow_standalone.py --generar PRAG-001 prestacion_servicios
    python3 willow_standalone.py --abrir PRAG-001
    python3 willow_standalone.py --listar-templates
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path
from datetime import datetime, date

# ── Paths ─────────────────────────────────────────────────────
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "datos"
MOTOR_DIR = BASE_DIR / "motor_kami"
CLIENTES_DIR = Path("C:/WillowLegal/01_Clientes")

sys.path.insert(0, str(MOTOR_DIR))

# ── Helpers ───────────────────────────────────────────────────
def load_data() -> dict:
    with open(DATA_DIR / "matters.json", "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data: dict):
    with open(DATA_DIR / "matters.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def calcular_dias_restantes(fecha_str: str) -> int:
    try:
        fecha = datetime.strptime(fecha_str, "%Y-%m-%d").date()
        return (fecha - date.today()).days
    except:
        return None

def format_moneda(valor, moneda="MXN"):
    if valor is None:
        return "Por definir"
    return f"${valor:,.0f} {moneda}"

# ── Comandos ──────────────────────────────────────────────────
def cmd_status(matter_id: str):
    data = load_data()
    for m in data.get("matters", []):
        if m["matter_id"] == matter_id:
            print(f"\n{'='*60}")
            print(f"  📋 MATTER: {m['matter_id']}")
            print(f"  🏢 CLIENTE: {m['cliente']['razon_social']}")
            print(f"  👤 REPRESENTANTE: {m['cliente']['representante']}")
            print(f"  📧 EMAIL: {m['cliente']['email']}")
            print(f"  📍 ÁREA: {m['asunto']['area_practica']}")
            print(f"  🚦 STATUS: {m['asunto']['status'].upper()}")
            print(f"  ⚡ PRIORIDAD: {m['asunto']['prioridad'].upper()}")
            print(f"{'='*60}")
            
            print(f"\n  📊 FINANZAS:")
            f = m.get("finanzas", {})
            print(f"     Total Proyecto: {format_moneda(f.get('total_proyecto'))}")
            print(f"     Anticipo: {format_moneda(f.get('anticipo_recibido'))}")
            print(f"     Adeudo: {format_moneda(f.get('adeudo'))}")
            
            print(f"\n  📑 DOCUMENTOS ({len(m.get('documentos', []))}):")
            for d in m.get("documentos", []):
                icon = "⏳" if d["status"] == "pendiente" else "✅"
                print(f"     {icon} {d['nombre']} [{d['status']}]")
            
            print(f"\n  ⏰ PLAZOS:")
            for p in m.get("plazos", []):
                dias = calcular_dias_restantes(p.get("fecha", ""))
                if dias is not None:
                    if dias < 0:
                        status = f"🔴 VENCIDO ({dias} días)"
                    elif dias <= 3:
                        status = f"🔴 URGENTE ({dias} días)"
                    elif dias <= 7:
                        status = f"🟡 PRÓXIMO ({dias} días)"
                    else:
                        status = f"🟢 {dias} días"
                else:
                    status = "N/A"
                print(f"     {status} — {p['descripcion']}")
            
            print(f"\n  ⚠️ PROBLEMAS:")
            for p in m.get("problemas", []):
                icon = "🔴" if p["prioridad"] == "critical" else "🟡" if p["prioridad"] == "high" else "🟢"
                print(f"     {icon} #{p['id']}: {p['descripcion']}")
            
            print(f"\n  🎯 ESTRATEGIA:")
            e = m.get("estrategia", {})
            print(f"     Objetivo: {e.get('objetivo', 'N/A')}")
            print(f"     Próximo paso: {e.get('proximo_paso', 'N/A')}")
            print(f"     Bloqueo: {e.get('bloqueo_actual', 'N/A')}")
            
            print(f"\n  📁 CARPETA: {m.get('carpeta_fisica', 'N/A')}")
            print(f"{'='*60}\n")
            return
    print(f"❌ Matter {matter_id} no encontrado")

def cmd_alertas():
    data = load_data()
    alertas = []
    for m in data.get("matters", []):
        for p in m.get("plazos", []):
            dias = calcular_dias_restantes(p.get("fecha", ""))
            if dias is not None and dias <= 7:
                alertas.append({
                    "matter": m["matter_id"],
                    "cliente": m["cliente"]["razon_social"],
                    "descripcion": p["descripcion"],
                    "dias": dias,
                    "urgencia": p.get("urgencia", "medium")
                })
        for d in m.get("documentos", []):
            if d["status"] == "pendiente":
                dl = calcular_dias_restantes(d.get("fecha_limite", ""))
                if dl is not None and dl <= 14:
                    alertas.append({
                        "matter": m["matter_id"],
                        "cliente": m["cliente"]["razon_social"],
                        "descripcion": f"Doc: {d['nombre']}",
                        "dias": dl,
                        "urgencia": d.get("prioridad", "medium")
                    })
    
    alertas.sort(key=lambda x: x["dias"])
    
    print(f"\n{'='*60}")
    print(f"  🚨 ALERTAS WILLOW LEGAL — {date.today().strftime('%d %b %Y')}")
    print(f"{'='*60}")
    
    if not alertas:
        print("\n  ✅ Sin alertas activas")
    else:
        for a in alertas:
            icon = "🔴" if a["urgencia"] == "critical" else "🟡" if a["urgencia"] == "high" else "🟢"
            dias_text = f"{a['dias']} días" if a['dias'] >= 0 else f"VENCIDO ({abs(a['dias'])} días)"
            print(f"\n  {icon} {a['matter']} — {a['cliente']}")
            print(f"     {a['descripcion']}")
            print(f"     {dias_text}")
    
    print(f"\n{'='*60}\n")

def cmd_generar(matter_id: str, template_key: str, filename: str = None):
    data = load_data()
    matter = None
    for m in data.get("matters", []):
        if m["matter_id"] == matter_id:
            matter = m
            break
    if not matter:
        print(f"❌ Matter {matter_id} no encontrado")
        return
    
    template_path = MOTOR_DIR / "templates" / f"{template_key}.json"
    if not template_path.exists():
        print(f"❌ Template '{template_key}' no encontrado")
        print(f"   Templates disponibles:")
        for t in data.get("templates_disponibles", []):
            print(f"     • {t['key']}: {t['label']}")
        return
    
    # Generar
    output_dir = MOTOR_DIR / "output"
    output_dir.mkdir(exist_ok=True)
    fname = filename or f"{matter_id}_{template_key}_{date.today().strftime('%Y%m%d')}.pdf"
    output_path = output_dir / fname
    
    try:
        from blocks import generar_desde_bloques
        
        # Construir bloques básicos
        blocks = [
            {
                "type": "header_brand",
                "data": {"marca": "We Law S.C.", "titulo": matter["asunto"]["descripcion"], "numero": matter_id}
            },
            {
                "type": "parties_block",
                "data": {
                    "prestador": {"nombre": "We Law S.C.", "rfc": "WLS123456XXX", "domicilio": "Guadalajara", "representante": "Abogado", "email": "hola@welaw.com.mx"},
                    "cliente": {"nombre": matter["cliente"]["razon_social"], "rfc": matter["cliente"].get("rfc", "N/A"), "domicilio": matter["cliente"].get("domicilio_fiscal", "N/A"), "representante": matter["cliente"]["representante"], "email": matter["cliente"]["email"]}
                }
            },
            {
                "type": "clause_section",
                "data": {"numero": "0", "titulo": "Antecedentes", "subclausulas": [matter["asunto"]["descripcion"]]}
            },
            {
                "type": "signature_block",
                "data": {
                    "prestador": {"nombre": "We Law S.C.", "cargo": "Representante Legal"},
                    "cliente": {"nombre": matter["cliente"]["representante"], "cargo": "Representante Legal"}
                }
            }
        ]
        
        pdf_path = generar_desde_bloques(
            blocks,
            str(output_path),
            {"color_primary": "#1a1a18", "color_bg": "#faf8f0"},
            None
        )
        
        pdf_file = Path(pdf_path)
        print(f"\n✅ DOCUMENTO GENERADO")
        print(f"   Matter: {matter_id}")
        print(f"   Template: {template_key}")
        print(f"   Archivo: {pdf_file}")
        print(f"   Tamaño: {round(pdf_file.stat().st_size / 1024, 1)} KB")
        print(f"   HTML Preview: {pdf_file.with_suffix('.html')}")
        print()
    except Exception as e:
        print(f"❌ Error generando documento: {e}")

def cmd_abrir(matter_id: str):
    data = load_data()
    for m in data.get("matters", []):
        if m["matter_id"] == matter_id:
            carpeta = m.get("carpeta_fisica", "")
            if not carpeta:
                safe = "".join(c for c in m["cliente"]["razon_social"] if c.isalnum() or c in " _-").strip()
                carpeta = str(CLIENTES_DIR / safe)
            
            win_path = carpeta.replace("/", "\\")
            print(f"📁 Abriendo carpeta: {win_path}")
            try:
                subprocess.run(["cmd.exe", "/c", "start", "", win_path], check=True)
                print("✅ Carpeta abierta")
            except Exception as e:
                print(f"❌ Error: {e}")
            return
    print(f"❌ Matter {matter_id} no encontrado")

def cmd_listar_templates():
    data = load_data()
    print(f"\n{'='*60}")
    print(f"  📚 TEMPLATES DISPONIBLES — Motor Kami v3")
    print(f"{'='*60}\n")
    
    areas = {}
    for t in data.get("templates_disponibles", []):
        area = t["area"]
        if area not in areas:
            areas[area] = []
        areas[area].append(t)
    
    for area, templates in sorted(areas.items()):
        print(f"  📂 {area}")
        for t in templates:
            print(f"     • {t['key']}: {t['label']}")
        print()
    
    print(f"{'='*60}\n")

def cmd_listar_matters():
    data = load_data()
    print(f"\n{'='*60}")
    print(f"  📋 MATTERS — Willow Legal")
    print(f"{'='*60}\n")
    
    for m in data.get("matters", []):
        docs_pendientes = sum(1 for d in m.get("documentos", []) if d["status"] == "pendiente")
        plazos_vencidos = sum(1 for p in m.get("plazos", []) if calcular_dias_restantes(p.get("fecha", "")) is not None and calcular_dias_restantes(p.get("fecha", "")) < 0)
        
        icon = "🔴" if plazos_vencidos > 0 else "🟡" if docs_pendientes > 0 else "🟢"
        print(f"  {icon} {m['matter_id']} — {m['cliente']['razon_social']}")
        print(f"     Área: {m['asunto']['area_practica']} | Status: {m['asunto']['status']} | Prioridad: {m['asunto']['prioridad']}")
        print(f"     Docs pendientes: {docs_pendientes} | Plazos vencidos: {plazos_vencidos}")
        print()
    
    print(f"{'='*60}\n")

def cmd_crear_matter(razon_social: str, representante: str, email: str, area: str = "Mercantil"):
    data = load_data()
    
    # Generar ID
    existing = [m["matter_id"] for m in data.get("matters", [])]
    max_num = 0
    for e in existing:
        try:
            num = int(e.split("-")[1])
            if num > max_num:
                max_num = num
        except:
            pass
    new_id = f"WIL-{max_num + 1:03d}"
    
    # Crear matter
    new_matter = {
        "matter_id": new_id,
        "cliente": {
            "razon_social": razon_social,
            "representante": representante,
            "email": email,
            "rfc": "",
            "domicilio_fiscal": "",
            "telefono": "",
            "sector": "",
            "tamano": "SME"
        },
        "asunto": {
            "area_practica": area,
            "tipo": "consultoria",
            "descripcion": f"Matter para {razon_social}",
            "status": "active",
            "prioridad": "medium",
            "fecha_apertura": date.today().isoformat(),
            "deadline_principal": ""
        },
        "problemas": [],
        "documentos": [],
        "plazos": [],
        "finanzas": {"total_proyecto": 0, "anticipo_recibido": 0, "adeudo": 0, "honorarios_will": 0, "pagos_recibidos": 0, "total_pendiente": 0, "moneda": "MXN"},
        "estrategia": {"objetivo": "", "proximo_paso": "Intake inicial", "bloqueo_actual": "none", "riesgos": []},
        "historial_sesiones": [],
        "carpeta_fisica": str(CLIENTES_DIR / "".join(c for c in razon_social if c.isalnum() or c in " _-").strip()),
        "agentes_activos": ["Despacho Legal", "Paralegal de Intake"]
    }
    
    data["matters"].append(new_matter)
    save_data(data)
    
    # Crear carpeta física
    safe = "".join(c for c in razon_social if c.isalnum() or c in " _-").strip()
    client_dir = CLIENTES_DIR / safe
    client_dir.mkdir(parents=True, exist_ok=True)
    
    subfolders = [
        "01_Intake", "02_Contratos/Borradores", "02_Contratos/Firmados",
        "02_Contratos/Anexos", "03_Correspondencia/Entrante",
        "03_Correspondencia/Saliente", "04_Litigio/Demandas",
        "04_Litigio/Contestaciones", "04_Litigio/Pruebas",
        "04_Litigio/Audiencias", "05_Facturacion/Cotizaciones",
        "05_Facturacion/Facturas", "05_Facturacion/Pagos",
        "06_Entregables/Documentos_Finales", "06_Entregables/Presentaciones",
        "06_Entregables/Reportes", "07_Archivo/Cerrado"
    ]
    for sf in subfolders:
        (client_dir / sf).mkdir(parents=True, exist_ok=True)
    
    print(f"\n✅ MATTER CREADO")
    print(f"   ID: {new_id}")
    print(f"   Cliente: {razon_social}")
    print(f"   Representante: {representante}")
    print(f"   Email: {email}")
    print(f"   Área: {area}")
    print(f"   Carpeta: {client_dir}")
    print()

# ── Main ──────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="Willow Legal — Standalone CLI")
    parser.add_argument("--status", type=str, help="Ver status de un matter")
    parser.add_argument("--alertas", action="store_true", help="Ver alertas")
    parser.add_argument("--generar", nargs=2, metavar=("MATTER", "TEMPLATE"), help="Generar documento")
    parser.add_argument("--output", type=str, help="Nombre de archivo de salida")
    parser.add_argument("--abrir", type=str, help="Abrir carpeta del matter")
    parser.add_argument("--listar-templates", action="store_true", help="Listar templates")
    parser.add_argument("--listar-matters", action="store_true", help="Listar matters")
    parser.add_argument("--crear-matter", type=str, help="Razón social del nuevo cliente")
    parser.add_argument("--representante", type=str, help="Nombre del representante")
    parser.add_argument("--email", type=str, help="Email del cliente")
    parser.add_argument("--area", type=str, default="Mercantil", help="Área de práctica")
    
    args = parser.parse_args()
    
    if args.status:
        cmd_status(args.status)
    elif args.alertas:
        cmd_alertas()
    elif args.generar:
        cmd_generar(args.generar[0], args.generar[1], args.output)
    elif args.abrir:
        cmd_abrir(args.abrir)
    elif args.listar_templates:
        cmd_listar_templates()
    elif args.listar_matters:
        cmd_listar_matters()
    elif args.crear_matter:
        if not args.representante or not args.email:
            print("❌ Se requiere --representante y --email")
            return
        cmd_crear_matter(args.crear_matter, args.representante, args.email, args.area)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
