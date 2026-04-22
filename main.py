from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

# --- MODELOS DE DATOS ---
class Estacion(BaseModel):
    id: int
    nombre: str
    ubicacion: str

class Lectura(BaseModel):
    estacion_id: int
    valor: float

# --- BASES DE DATOS EN MEMORIA ---
db_estaciones = []
db_lecturas = []

# --- ENDPOINTS ---

# 1. Crear Estación
@app.post("/estaciones/", status_code=201)
async def crear_estacion(estacion: Estacion):
    db_estaciones.append(estacion)
    return {"data": estacion}

# 2. Registrar Lectura
@app.post("/lecturas/", status_code=201)
async def registrar_lectura(lectura: Lectura):
    db_lecturas.append(lectura)
    return {"status": "Lectura recibida"}

# 3. Motor de Alertas (Nivel de Riesgo)
@app.get("/estaciones/{id}/riesgo")
async def obtener_riesgo(id: int):
    # Validar existencia
    estacion_existe = any(e.id == id for e in db_estaciones)
    if not estacion_existe:
        raise HTTPException(status_code=404, detail="Estación no encontrada")
    
    # Filtrar lecturas
    lecturas = [l for l in db_lecturas if l.estacion_id == id]
    if not lecturas:
        return {"id": id, "nivel": "SIN DATOS", "valor": 0}
    
    # Evaluar última lectura
    ultima_lectura = lecturas[-1].valor
    if ultima_lectura > 20.0:
        nivel = "PELIGRO"
    elif ultima_lectura > 10.0:
        nivel = "ALERTA"
    else:
        nivel = "NORMAL"
        
    return {"id": id, "valor": ultima_lectura, "nivel": nivel}

# 4. Historial y Promedio (Análisis de Datos)
@app.get("/estaciones/{id}/historial")
async def obtener_historial(id: int):
    # Validar existencia
    estacion_existe = any(e.id == id for e in db_estaciones)
    if not estacion_existe:
        raise HTTPException(status_code=404, detail="Estación no encontrada")
    
    # Filtrar valores de lecturas
    valores = [l.valor for l in db_lecturas if l.estacion_id == id]
    
    conteo = len(valores)
    promedio = sum(valores) / conteo if conteo > 0 else 0.0
    
    return {
        "estacion_id": id,
        "lecturas": valores,
        "conteo": conteo,
        "promedio": promedio
    }

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
import models
from database import engine, get_db

# CRITICAL: CREACIÓN DE LA BASE DE DATOS Y TABLAS
# Crea el archivo 'smat.db' y las tablas si no existen
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="SMAT Persistente")

# Esquemas de validación (Pydantic)
class EstacionCreate(BaseModel):
    id: int
    nombre: str
    ubicacion: str

class LecturaCreate(BaseModel):
    estacion_id: int
    valor: float

# --- ENDPOINTS ---

@app.post("/estaciones/", status_code=201)
def crear_estacion(estacion: EstacionCreate, db: Session = Depends(get_db)):
    # Convertimos el esquema de Pydantic a Modelo de SQLAlchemy
    nueva_estacion = models.EstacionDB(
        id=estacion.id, 
        nombre=estacion.nombre,
        ubicacion=estacion.ubicacion
    )
    db.add(nueva_estacion)
    db.commit()
    db.refresh(nueva_estacion)
    return {"msj": "Estación guardada en DB", "data": nueva_estacion}

@app.post("/lecturas/", status_code=201)
def registrar_lectura(lectura: LecturaCreate, db: Session = Depends(get_db)):
    # Validar si la estación existe en la DB
    estacion = db.query(models.EstacionDB).filter(
        models.EstacionDB.id == lectura.estacion_id
    ).first()
    
    if not estacion:
        raise HTTPException(status_code=404, detail="Estación no existe")
    
    nueva_lectura = models.LecturaDB(
        valor=lectura.valor,
        estacion_id=lectura.estacion_id
    )
    db.add(nueva_lectura)
    db.commit()
    return {"status": "Lectura guardada en DB"}
