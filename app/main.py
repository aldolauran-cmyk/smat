from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from . import models, schemas, crud
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="SMAT",
    description="Sistema de Monitoreo de Alerta Temprana",
    version="1.0.1"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["Inicio"])
def read_root():
    return {"message": "Servidor Activo"}

@app.post("/estaciones/", tags=["Infraestructura"])
def crear_estacion(estacion: schemas.EstacionCreate, db: Session = Depends(get_db)):
    return crud.crear_estacion(db=db, estacion=estacion)

@app.post("/lecturas/", tags=["Infraestructura"])
def registrar_lectura(lectura: schemas.LecturaCreate, db: Session = Depends(get_db)):
    return crud.crear_lectura(db=db, lectura=lectura)

@app.get("/estaciones/stats", tags=["Auditoria"])
def obtener_estadisticas(db: Session = Depends(get_db)):
    return crud.obtener_stats(db)
