from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_dashboard_stats():
    client.post("/estaciones/", json={"nombre": "Estacion Test", "ubicacion": "Amazonas"})
    
    client.post("/lecturas/", json={"valor": 10.5, "estacion_id": 1})
    client.post("/lecturas/", json={"valor": 88.2, "estacion_id": 1})
    
    response = client.get("/estaciones/stats")
    data = response.json()
    
    assert response.status_code == 200
    assert data["total_estaciones"] >= 1
    assert data["total_lecturas"] >= 2
    assert data["punto_critico_maximo"] == 88.2
