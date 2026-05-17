from pydantic import BaseModel
from typing import Optional

class ProductoCrear(BaseModel):
    nombre: str
    descripcion: str
    categoria_id: int
    marca_id: int
    precio: float
    tienda_id: int
    imagen_url: Optional[str] = None

class ProductoActualizar(BaseModel):
    nombre: str
    descripcion: str
    categoria_id: int
    marca_id: int
    imagen_url: Optional[str] = None
