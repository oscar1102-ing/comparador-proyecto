from pydantic import BaseModel

class TiendaCrear(BaseModel):
    nombre: str
    url: str
    logo: str | None = None
