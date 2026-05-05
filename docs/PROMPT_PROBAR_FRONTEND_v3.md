# PROMPT EJECUTABLE — Actualizar Willow Legal Pro v3.0 y Ver Frontend

## OBJETIVO
Actualizar el repositorio `ws-hermes-legal-pro` a la última versión del branch `v2.0-dev` (que ahora incluye el frontend v3.0 completamente reescrito), instalar dependencias, verificar que todo funciona, y mostrar una captura de pantalla del nuevo dashboard.

## PASOS A EJECUTAR

### PASO 0: Preparación
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
pip install "httpx>=0.27.0,<0.28.0"
```

### PASO 2: Verificar Tests
```bash
cd ~/ws-hermes-legal-pro
python -m pytest tests/ -v
```
Deben pasar **11/11 tests**. Si fallan, reportar error y NO continuar.

### PASO 3: Iniciar el Backend
```bash
cd ~/ws-hermes-legal-pro/dashboard/backend
python -m uvicorn app:app --host 0.0.0.0 --port 8082 --reload &
```
Esperar 3 segundos y verificar que está corriendo:
```bash
curl http://localhost:8082/api/health
```
Debe responder con `{"status":"ok","version":"2.0.0"}`.

### PASO 4: Abrir el Frontend en Browser y Capturar Pantalla
```bash
# Abrir Chrome/Chromium en el frontend
chromium-browser --headless --screenshot=/tmp/willow-legal-dashboard.png --window-size=375,812 http://localhost:8082/ &
sleep 5
```

O si hay un navegador visual disponible:
```bash
# Intentar abrir en navegador por defecto
xdg-open http://localhost:8082/ || open http://localhost:8082/ || echo "Abre manualmente: http://localhost:8082"
```

### PASO 5: Verificar que el nuevo frontend carga
```bash
# Verificar que los archivos nuevos existen
ls -la ~/ws-hermes-legal-pro/dashboard/frontend/css/kami.css
ls -la ~/ws-hermes-legal-pro/dashboard/frontend/js/dashboard.js
ls -la ~/ws-hermes-legal-pro/dashboard/frontend/js/reuniones.js
ls -la ~/ws-hermes-legal-pro/DESIGN.md
```

### PASO 6: Reportar estado
Responder con:
- ✅ Repo actualizado a v2.0-dev
- ✅ Tests pasando (11/11)
- ✅ Backend corriendo en puerto 8082
- ✅ Frontend v3.0 cargado
- 📸 Screenshot del dashboard (si se pudo capturar)

## MANEJO DE ERRORES

Si algo falla:
1. NO intentar arreglar "a lo bruto"
2. Capturar el error completo (stdout + stderr)
3. Reportar: qué paso falló, qué error dio
4. Esperar instrucciones

## REGLAS
- NO modificar archivos del proyecto sin confirmación
- SIEMPRE verificar tests antes de declarar éxito
- SIEMPRE verificar que el backend responde antes de abrir el frontend
