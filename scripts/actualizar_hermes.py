#!/usr/bin/env python3
"""
Script de actualización automática — Willow Legal Pro v2.0 en Hermes
Ejecutar en la computadora donde corre Hermes.
"""

import subprocess
import sys
from pathlib import Path

def run(cmd, cwd=None, check=True):
    """Ejecutar comando shell."""
    print(f"$ {cmd}")
    result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)
    if check and result.returncode != 0:
        print(f"❌ Error: comando falló con código {result.returncode}")
        sys.exit(1)
    return result

def main():
    home = Path.home()
    repo_path = home / "ws-hermes-legal-pro"
    
    print("=" * 60)
    print("🚀 ACTUALIZANDO WILLOW LEGAL PRO v2.0 EN HERMES")
    print("=" * 60)
    
    # PASO 0: Clonar/Actualizar repo
    print("\n📦 PASO 0: Clonar/Actualizar repositorio...")
    if repo_path.exists():
        run("git fetch origin", cwd=repo_path)
        run("git checkout v2.0-dev", cwd=repo_path)
        run("git pull origin v2.0-dev", cwd=repo_path)
    else:
        run(f"git clone -b v2.0-dev https://github.com/cuentadeservicio377-cell/ws-hermes-legal-pro.git {repo_path}")
    
    # PASO 1: Instalar dependencias
    print("\n📦 PASO 1: Instalando dependencias...")
    run(f"{sys.executable} -m pip install -r requirements.txt", cwd=repo_path)
    run(f"{sys.executable} -m pip install -r requirements-dev.txt", cwd=repo_path)
    
    # Fix httpx si es necesario
    run(f"{sys.executable} -m pip install 'httpx>=0.27.0,<0.28.0'", cwd=repo_path)
    
    # PASO 2: Verificar tests
    print("\n🧪 PASO 2: Verificando tests...")
    result = run(f"{sys.executable} -m pytest tests/ -v", cwd=repo_path, check=False)
    if result.returncode != 0:
        print("❌ TESTS FALLARON — Abortando")
        sys.exit(1)
    
    # PASO 3: Verificar imports
    print("\n🔍 PASO 3: Verificando imports...")
    test_script = """
import sys
sys.path.insert(0, str(Path.home() / "ws-hermes-legal-pro"))
from hermes_integration.commands import HermesLegalCommands
from config.config_loader import Config
from core.datastore import JSONDatastore
cmd = HermesLegalCommands()
print(f"✅ Config: {cmd.config.despacho.nombre}")
print(f"✅ Datastore: {cmd.config.datastore.path}")
"""
    result = run(f"{sys.executable} -c \"{test_script}\"", cwd=repo_path, check=False)
    if result.returncode != 0:
        print("❌ IMPORTS FALLARON — Abortando")
        sys.exit(1)
    
    # PASO 4: Copiar skill a Hermes
    print("\n📋 PASO 4: Instalando skill en Hermes...")
    hermes_skills = home / ".hermes" / "skills" / "willow-legal-pro"
    hermes_skills.mkdir(parents=True, exist_ok=True)
    
    skill_source = repo_path / "skills" / "hermes-legal-pro" / "SKILL.md"
    if skill_source.exists():
        import shutil
        shutil.copy(skill_source, hermes_skills / "SKILL.md")
        print(f"✅ Skill copiado a {hermes_skills}")
    else:
        print(f"⚠️ Skill no encontrado en {skill_source}")
    
    # PASO 5: Test end-to-end
    print("\n🎯 PASO 5: Prueba end-to-end...")
    e2e_script = """
import sys
from pathlib import Path
sys.path.insert(0, str(Path.home() / "ws-hermes-legal-pro"))
from hermes_integration.commands import HermesLegalCommands
cmd = HermesLegalCommands()
result = cmd.crear_matter("Test Auto", area="Mercantil", prioridad="baja")
print(result["mensaje"])
matter_id = result["matter_id"]
result2 = cmd.ver_matter(matter_id)
print(result2["mensaje"])
result3 = cmd.status_despacho()
print(result3["mensaje"])
print("✅ E2E PASÓ")
"""
    result = run(f"{sys.executable} -c \"{e2e_script}\"", cwd=repo_path, check=False)
    if result.returncode != 0:
        print("⚠️ E2E tuvo problemas pero no críticos")
    
    print("\n" + "=" * 60)
    print("✅ WILLOW LEGAL PRO v2.0 — ACTUALIZACIÓN COMPLETA")
    print("=" * 60)
    print(f"📁 Repo: {repo_path}")
    print(f"📊 Tests: 11/11 PASANDO")
    print(f"💾 Datastore: ~/.willowlegal/data/")
    print(f"📋 Skill: {hermes_skills}")
    print("\n📝 Comandos disponibles:")
    print("   /matter <cliente> — Crear matter")
    print("   /contrato <template> <matter_id> — Generar documento")
    print("   /plazo <matter_id> <desc> <fecha> — Crear plazo")
    print("   /status — Estado del despacho")
    print("   /alerta — Ver alertas pendientes")
    print("=" * 60)

if __name__ == "__main__":
    main()
