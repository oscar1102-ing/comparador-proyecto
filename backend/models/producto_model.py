from pydantic import BaseModel

class ProductoCrear(BaseModel):
    nombre: str
    descripcion: str
    categoria_id: int
    marca_id: int
    precio: float
    tienda_id: int

class ProductoActualizar(BaseModel):
    nombre: str
    descripcion: str
    categoria_id: int
    marca_id: int
