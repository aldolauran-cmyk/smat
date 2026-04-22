from sqlalchemy import Column, Integer, String, Float, ForeignKey
from .database import Base

class Estacion(Base):
    __tablename__ = "estaciones"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    ubicacion = Column(String)

class Lectura(Base):
    __tablename__ = "lecturas"
    id = Column(Integer, primary_key=True, index=True)
    valor = Column(Float)
    estacion_id = Column(Integer, ForeignKey("estaciones.id"))
