from pydantic import BaseModel

class EstacionBase(BaseModel):
    nombre: str
    ubicacion: str

class EstacionCreate(EstacionBase):
    pass

class Estacion(EstacionBase):
    id: int
    class Config:
        from_attributes = True

class LecturaBase(BaseModel):
    valor: float
    estacion_id: int

class LecturaCreate(LecturaBase):
    pass

class Lectura(LecturaBase):
    id: int
    class Config:
        from_attributes = True
