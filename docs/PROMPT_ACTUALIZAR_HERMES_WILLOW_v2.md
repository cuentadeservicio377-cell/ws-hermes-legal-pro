# PROMPT EJECUTABLE — Actualizar Willow Legal Pro v2.0 en Instancia Hermes

## OBJETIVO
Tomar el repositorio `ws-hermes-legal-pro` (branch `v2.0-dev`) y actualizar la instancia de Hermes que corre en esta computadora para que use el nuevo sistema Willow Legal Pro v2.0.

## CONTEXTO DE LA INSTANCIA HERMES ACTUAL
- Hermes corre como servicio en esta máquina (Linux/WSL)
- Config principal: `~/.hermes/config.yaml`
- El agente Hermes tiene acceso a herramientas: terminal, file, web, browser, skills
- El agente puede ejecutar código Python y comandos shell
- El agente tiene memoria persistente entre sesiones

## PASOS A EJECUTAR

### PASO 0: Preparación
1. Verificar que `git` está instalado y configurado
2. Verificar que `gh` CLI está autenticado (OAuth activo en `~/.config/gh/hosts.yml`)
3. Clonar o actualizar el repo:
   ```bash
   cd ~
   if [ -d "ws-hermes-legal-pro" ]; then
     cd ws-hermes-legal-pro
     git fetch origin
     git checkout v2.0-dev
     git pull origin v2.0-dev
   else
     git clone -b v2.0-dev https://github.com/cuentadeservicio377-cell/ws-hermes-legal-pro.git
     cd ws-hermes-legal-pro
   fi
   ```

### PASO 1: Instalar Dependencias
```bash
cd ~/ws-hermes-legal-pro
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

**IMPORTANTE**: Si hay conflictos de versiones con `httpx`, usar:
```bash
pip install "httpx>=0.27.0,<0.28.0"
```

### PASO 2: Verificar Tests
```bash
cd ~/ws-hermes-legal-pro
python -m pytest tests/ -v
```
Deben pasar **11/11 tests**. Si fallan, NO continuar — reportar el error.

### PASO 3: Configurar el Sistema Willow Legal
1. Verificar que `config/config.yaml` existe y tiene la configuración correcta
2. La primera ejecución creará automáticamente:
   - `~/.willowlegal/data/` — base de datos JSON
   - `~/.willowlegal/backups/` — backups automáticos
   - `~/.willowlegal/output/` — documentos generados

### PASO 4: Integrar con Hermes (CRÍTICO)

El objetivo es que el agente Hermes que corre en esta máquina pueda usar los comandos legales.

#### Opción A: Skill de Hermes (Recomendada)
1. Copiar el skill a la carpeta de skills de Hermes:
   ```bash
   mkdir -p ~/.hermes/skills/willow-legal-pro
   cp ~/ws-hermes-legal-pro/skills/hermes-legal-pro/SKILL.md ~/.hermes/skills/willow-legal-pro/
   ```

2. Verificar que el skill se detecta:
   ```bash
   hermes skills list | grep -i willow
   ```

3. Si no aparece, recargar skills:
   ```bash
   hermes skills reload
   ```

#### Opción B: Script de Inicialización (Fallback)
Si el skill no funciona, crear un script de inicialización:

```bash
cat > ~/.hermes/scripts/willow-legal-init.py << 'EOF'
#!/usr/bin/env python3
"""Inicializa Willow Legal Pro en la sesión de Hermes."""
import sys
from pathlib import Path

# Añadir el repo al path
REPO_PATH = Path.home() / "ws-hermes-legal-pro"
if str(REPO_PATH) not in sys.path:
    sys.path.insert(0, str(REPO_PATH))

from hermes_integration.commands import HermesLegalCommands

# Instancia global
willow = HermesLegalCommands()

print(f"✅ Willow Legal Pro v2.0 inicializado")
print(f"   Despacho: {willow.config.despacho.nombre}")
print(f"   Datastore: {willow.config.datastore.path}")
EOF
chmod +x ~/.hermes/scripts/willow-legal-init.py
```

### PASO 5: Verificar Funcionamiento End-to-End

Ejecutar estas pruebas manuales:

```python
# Test 1: Crear un matter de prueba
from hermes_integration.commands import HermesLegalCommands
cmd = HermesLegalCommands()
result = cmd.crear_matter("Cliente de Prueba", area="Mercantil", prioridad="media")
print(result["mensaje"])
matter_id = result["matter_id"]

# Test 2: Listar matters
result = cmd.listar_matters()
print(result["mensaje"])

# Test 3: Ver estado del despacho
result = cmd.status_despacho()
print(result["mensaje"])

# Test 4: Generar un documento (si hay templates)
result = cmd.listar_templates()
print(result["mensaje"])
```

### PASO 6: Documentar en Memoria de Hermes

Guardar en la memoria del agente:
- "Willow Legal Pro v2.0 está activo en esta máquina"
- "Repo en: ~/ws-hermes-legal-pro (branch v2.0-dev)"
- "Comandos disponibles: /matter, /contrato, /plazo, /status, /alerta"
- "Datastore en: ~/.willowlegal/data/"
- "Tests: 11/11 pasando"

## VERIFICACIÓN FINAL

Antes de reportar éxito, confirmar:
- [ ] Repo clonado/actualizado en `~/ws-hermes-legal-pro`
- [ ] Branch `v2.0-dev` activo
- [ ] `pip install` completado sin errores
- [ ] `pytest tests/` → 11/11 PASSED
- [ ] `config/config.yaml` existe y es válido
- [ ] `~/.willowlegal/data/` creado
- [ ] Skill copiado a `~/.hermes/skills/willow-legal-pro/`
- [ ] Comandos de prueba ejecutados exitosamente
- [ ] Memoria actualizada

## REPORTE DE ÉXITO

Si todo funciona, responder con:
```
✅ WILLOW LEGAL PRO v2.0 — ACTIVADO EN HERMES

- Repo: ~/ws-hermes-legal-pro (v2.0-dev)
- Tests: 11/11 PASANDO
- Datastore: ~/.willowlegal/data/
- Skill: willow-legal-pro cargado
- Comandos listos: /matter, /contrato, /plazo, /status, /alerta
```

## MANEJO DE ERRORES

Si algo falla:
1. NO intentar "arreglarlo rápido"
2. Capturar el error completo (stdout + stderr)
3. Reportar: qué paso falló, qué error dio, qué se intentó
4. Esperar instrucciones antes de continuar

## REGLAS
- NO modificar `~/.hermes/config.yaml` sin confirmación
- NO borrar datos existentes de Willow Legal
- SIEMPRE hacer backup antes de cambios destructivos
- SIEMPRE verificar tests antes de declarar éxito
