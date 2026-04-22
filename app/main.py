from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from . import models, schemas, crud
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="SMAT - Sistema de Monitoreo de Alerta Temprana",
    description="API robusta para la gestión y monitoreo de desastres naturales.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/estaciones/", response_model=schemas.Estacion, tags=["Gestión"])
def crear_estacion(estacion: schemas.EstacionCreate, db: Session = Depends(get_db)):
    return crud.crear_estacion(db=db, estacion=estacion)

@app.post("/lecturas/", response_model=schemas.Lectura, tags=["Telemetría"])
def registrar_lectura(lectura: schemas.LecturaCreate, db: Session = Depends(get_db)):
    return crud.crear_lectura(db=db, lectura=lectura)

@app.get("/estaciones/stats", tags=["Auditoría"])
def obtener_estadisticas(db: Session = Depends(get_db)):
    return crud.obtener_stats(db)
