from sqlalchemy.orm import Session
from sqlalchemy import func
from . import models, schemas

def crear_estacion(db: Session, estacion: schemas.EstacionCreate):
    db_estacion = models.Estacion(nombre=estacion.nombre, ubicacion=estacion.ubicacion)
    db.add(db_estacion)
    db.commit()
    db.refresh(db_estacion)
    return db_estacion

def crear_lectura(db: Session, lectura: schemas.LecturaCreate):
    db_lectura = models.Lectura(valor=lectura.valor, estacion_id=lectura.estacion_id)
    db.add(db_lectura)
    db.commit()
    db.refresh(db_lectura)
    return db_lectura

def obtener_stats(db: Session):
    total_est = db.query(models.Estacion).count()
    total_lec = db.query(models.Lectura).count()
    max_val = db.query(func.max(models.Lectura.valor)).scalar()
    return {
        "total_estaciones": total_est,
        "total_lecturas": total_lec,
        "valor_maximo": max_val or 0.0
    }
