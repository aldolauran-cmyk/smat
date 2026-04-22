from pydantic import BaseModel
from typing import List, Optional

class EstacionCreate(BaseModel):
    nombre: str
    ubicacion: str

class Estacion(EstacionCreate):
    id: int
    class Config:
        from_attributes = True

class LecturaCreate(BaseModel):
    valor: float
    estacion_id: int

class Lectura(LecturaCreate):
    id: int
    class Config:
        from_attributes = True
