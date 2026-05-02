#!/usr/bin/env python3
"""
check_plazos.py — Alertas automáticas de deadlines y plazos
Hermes Legal Pro v4.0

Uso:
    python3 scripts/check_plazos.py
    python3 scripts/check_plazos.py --test
    python3 scripts/check_plazos.py --notify
"""

import json
import os
import argparse
from pathlib import Path
from datetime import datetime, date, timedelta

try:
    import requests
except ImportError:
    requests = None

# ── Paths ─────────────────────────────────────────────────────
BASE_DIR = Path(__file__).parent.parent
MATTERS_FILE = BASE_DIR / "dashboard" / "datos" / "matters.json"
ALERTAS_FILE = BASE_DIR / "dashboard" / "datos" / "alertas.json"

# ── Config ────────────────────────────────────────────────────
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_HOME_CHAT_ID", "")

# ── Helpers ───────────────────────────────────────────────────
def load_json(path):
    if not path.exists():
        return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def dias_restantes(fecha_str):
    try:
        fecha = datetime.strptime(fecha_str, "%Y-%m-%d").date()
        return (fecha - date.today()).days
    except:
        return None

def nivel_urgencia(dias):
    if dias is None:
        return None
    if dias < 0:
        return "vencido"
    elif dias == 0:
        return "hoy"
    elif dias == 1:
        return "1dia"
    elif dias <= 3:
        return "3dias"
    elif dias <= 7:
        return "7dias"
    return None

def enviar_telegram(mensaje):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("  ⚠️  Telegram no configurado (faltan TELEGRAM_BOT_TOKEN o TELEGRAM_HOME_CHAT_ID)")
        return False
    
    if requests is None:
        print("  ⚠️  requests no instalado. Ejecuta: pip3 install requests")
        return False
    
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": mensaje,
        "parse_mode": "Markdown"
    }
    
    try:
        resp = requests.post(url, json=payload, timeout=10)
        if resp.status_code == 200:
            print("  ✅ Notificación enviada a Telegram")
            return True
        else:
            print(f"  ❌ Error Telegram: {resp.status_code} — {resp.text}")
            return False
    except Exception as e:
        print(f"  ❌ Error enviando a Telegram: {e}")
        return False

# ── Core logic ────────────────────────────────────────────────
def check_plazos(test_mode=False, notify=False):
    print("🔔 Revisando plazos y deadlines...")
    
    matters = load_json(MATTERS_FILE)
    alertas = load_json(ALERTAS_FILE)
    
    nuevas_alertas = []
    alertas_enviadas = 0
    
    for matter in matters:
        if matter.get("estado") != "activo":
            continue
        
        matter_id = matter.get("id", "N/A")
        cliente = matter.get("cliente", "Sin cliente")
        deadline = matter.get("deadline")
        next_step = matter.get("next_step", "Sin descripción")
        
        if not deadline:
            continue
        
        dias = dias_restantes(deadline)
        if dias is None:
            continue
        
        nivel = nivel_urgencia(dias)
        if not nivel:
            continue
        
        # Verificar si ya existe alerta no resuelta para este matter + nivel
        alerta_existente = False
        for a in alertas:
            if (a.get("matter_id") == matter_id and 
                a.get("nivel") == nivel and 
                not a.get("resuelta")):
                alerta_existente = True
                break
        
        if alerta_existente:
            continue
        
        # Crear nueva alerta
        if dias < 0:
            titulo = f"⛔ PLAZO VENCIDO: {matter_id}"
            mensaje = f"El matter *{matter_id}* — *{cliente}* tiene un plazo vencido ({deadline}).\n\n📝 {next_step}"
        elif dias == 0:
            titulo = f"🔴 PLAZO HOY: {matter_id}"
            mensaje = f"El matter *{matter_id}* — *{cliente}* vence *HOY* ({deadline}).\n\n📝 {next_step}"
        elif dias == 1:
            titulo = f"🟠 PLAZO MAÑANA: {matter_id}"
            mensaje = f"El matter *{matter_id}* — *{cliente}* vence *mañana* ({deadline}).\n\n📝 {next_step}"
        elif dias <= 3:
            titulo = f"🟡 PLAZO EN 3 DÍAS: {matter_id}"
            mensaje = f"El matter *{matter_id}* — *{cliente}* vence en *{dias} días* ({deadline}).\n\n📝 {next_step}"
        else:
            titulo = f"🟢 PLAZO PRÓXIMO: {matter_id}"
            mensaje = f"El matter *{matter_id}* — *{cliente}* vence en *{dias} días* ({deadline}).\n\n📝 {next_step}"
        
        alerta = {
            "id": f"ALR-{len(alertas) + len(nuevas_alertas) + 1:04d}",
            "matter_id": matter_id,
            "cliente": cliente,
            "titulo": titulo,
            "mensaje": mensaje,
            "deadline": deadline,
            "dias_restantes": dias,
            "nivel": nivel,
            "fecha_generacion": datetime.now().isoformat(),
            "resuelta": False,
            "canal": "dashboard"
        }
        
        nuevas_alertas.append(alerta)
        print(f"  ⚠️  {titulo} — {cliente} ({dias} días)")
        
        if notify and not test_mode:
            if enviar_telegram(mensaje):
                alerta["canal"] = "dashboard+telegram"
                alertas_enviadas += 1
    
    if test_mode:
        print(f"\n🧪 MODO TEST: {len(nuevas_alertas)} alertas detectadas (NO guardadas)")
        for a in nuevas_alertas:
            print(f"  • {a['titulo']}")
        return nuevas_alertas
    
    if nuevas_alertas:
        alertas.extend(nuevas_alertas)
        save_json(ALERTAS_FILE, alertas)
        print(f"\n✅ {len(nuevas_alertas)} alertas guardadas")
        if notify:
            print(f"  📨 {alertas_enviadas} enviadas por Telegram")
    else:
        print("\n✅ No hay plazos urgentes")
    
    return nuevas_alertas

# ── Test mode ─────────────────────────────────────────────────
def run_test():
    print("🧪 MODO TEST: Generando alertas de prueba...\n")
    
    # Crear matters de prueba con deadlines conocidos
    test_matters = [
        {
            "id": "TEST-001",
            "cliente": "Cliente Vencido",
            "estado": "activo",
            "deadline": (date.today() - timedelta(days=2)).isoformat(),
            "next_step": "Responder demanda"
        },
        {
            "id": "TEST-002",
            "cliente": "Cliente Hoy",
            "estado": "activo",
            "deadline": date.today().isoformat(),
            "next_step": "Audiencia judicial"
        },
        {
            "id": "TEST-003",
            "cliente": "Cliente Mañana",
            "estado": "activo",
            "deadline": (date.today() + timedelta(days=1)).isoformat(),
            "next_step": "Entregar documentos"
        },
        {
            "id": "TEST-004",
            "cliente": "Cliente 3 Días",
            "estado": "activo",
            "deadline": (date.today() + timedelta(days=3)).isoformat(),
            "next_step": "Revisar contrato"
        },
        {
            "id": "TEST-005",
            "cliente": "Cliente Lejano",
            "estado": "activo",
            "deadline": (date.today() + timedelta(days=30)).isoformat(),
            "next_step": "No debería generar alerta"
        }
    ]
    
    # Guardar matters originales
    orig_matters = load_json(MATTERS_FILE)
    save_json(MATTERS_FILE, test_matters)
    
    # Limpiar alertas
    orig_alertas = load_json(ALERTAS_FILE)
    save_json(ALERTAS_FILE, [])
    
    # Ejecutar check
    alertas = check_plazos(test_mode=True)
    
    # Restaurar datos originales
    save_json(MATTERS_FILE, orig_matters)
    save_json(ALERTAS_FILE, orig_alertas)
    
    print("\n🔄 Datos originales restaurados")
    
    assert len(alertas) == 4, f"Esperaba 4 alertas, obtuve {len(alertas)}"
    print("\n✅ TEST PASADO: 4/4 alertas generadas correctamente")
    return alertas

# ── Main ──────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="Check plazos y deadlines")
    parser.add_argument("--test", action="store_true", help="Modo test con datos de prueba")
    parser.add_argument("--notify", action="store_true", help="Enviar notificaciones por Telegram")
    args = parser.parse_args()
    
    if args.test:
        run_test()
    else:
        check_plazos(notify=args.notify)

if __name__ == "__main__":
    main()
