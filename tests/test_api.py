def test_health_check(client):
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["version"] == "2.0.0"

def test_create_matter(client):
    response = client.post("/api/matters", json={
        "cliente": "Test Client",
        "area_practica": "Mercantil",
        "descripcion": "Test",
        "prioridad": "media"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["id"].startswith("WIL-")
    assert data["cliente"] == "Test Client"
    assert data["estado"] == "activo"

def test_create_matter_generates_sequential_ids(client):
    r1 = client.post("/api/matters", json={
        "cliente": "Client A", "area_practica": "Mercantil", "prioridad": "media"
    })
    r2 = client.post("/api/matters", json={
        "cliente": "Client B", "area_practica": "Laboral", "prioridad": "alta"
    })
    assert r1.json()["id"] == "WIL-001"
    assert r2.json()["id"] == "WIL-002"

def test_list_matters(client):
    client.post("/api/matters", json={
        "cliente": "Test", "area_practica": "Mercantil", "prioridad": "media"
    })
    response = client.get("/api/matters")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0

def test_get_matter_404(client):
    response = client.get("/api/matters/WIL-999")
    assert response.status_code == 404

def test_finanzas_flow(client):
    # Create matter first
    r = client.post("/api/matters", json={
        "cliente": "Test Finance",
        "area_practica": "Mercantil",
        "descripcion": "Finance test",
        "prioridad": "media"
    })
    matter_id = r.json()["id"]
    
    # Create finance entry
    response = client.post("/api/finanzas", json={
        "matter_id": matter_id,
        "tipo": "ingreso",
        "monto": 50000,
        "concepto": "Test payment"
    })
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert response.json()["movimiento"]["id"].startswith("FIN-")
    
    # Create expense
    client.post("/api/finanzas", json={
        "matter_id": matter_id,
        "tipo": "egreso",
        "monto": 15000,
        "concepto": "Gasto operativo"
    })
    
    # List finances
    response = client.get("/api/finanzas")
    assert response.status_code == 200
    data = response.json()
    resumen = data["resumen"]
    assert resumen["total_ingresos"] == 50000
    assert resumen["total_egresos"] == 15000
    assert resumen["balance"] == 35000
    assert resumen["count"] == 2

def test_check_plazos(client):
    response = client.post("/api/check-plazos")
    assert response.status_code == 200
    assert "completa" in response.json()["message"]

def test_drive_link(client):
    # Create matter with drive info
    r = client.post("/api/matters", json={
        "cliente": "Test Drive",
        "area_practica": "Mercantil",
        "prioridad": "media"
    })
    matter_id = r.json()["id"]
    
    response = client.get(f"/api/drive-link/{matter_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["matter_id"] == matter_id

def test_dashboard(client):
    response = client.get("/api/dashboard")
    assert response.status_code == 200
    data = response.json()
    assert "kpis" in data
    assert "proximos_plazos" in data

def test_reuniones(client):
    # Create matter
    r = client.post("/api/matters", json={
        "cliente": "Test Reunion",
        "area_practica": "Mercantil",
        "prioridad": "media"
    })
    matter_id = r.json()["id"]
    
    # Create reunion
    response = client.post("/api/reuniones", json={
        "matter_id": matter_id,
        "cliente": "Test Reunion",
        "fecha": "2026-05-04",
        "resumen": "Test reunion"
    })
    assert response.status_code == 200
    assert response.json()["id"].startswith("REU-")

def test_templates(client):
    response = client.get("/api/templates")
    assert response.status_code == 200
    data = response.json()
    assert "templates" in data
    assert data["count"] > 0
