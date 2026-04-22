from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from . import models, schemas, crud
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="SMAT Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/estaciones/", response_model=schemas.Estacion)
def crear_estacion(estacion: schemas.EstacionCreate, db: Session = Depends(get_db)):
    return crud.crear_estacion(db=db, estacion=estacion)

@app.post("/lecturas/", response_model=schemas.Lectura)
def registrar_lectura(lectura: schemas.LecturaCreate, db: Session = Depends(get_db)):
    return crud.crear_lectura(db=db, lectura=lectura)

@app.get("/estaciones/stats")
def obtener_estadisticas(db: Session = Depends(get_db)):
    return crud.obtener_stats(db)
