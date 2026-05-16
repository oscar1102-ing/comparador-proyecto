from pydantic import BaseModel

class FavoritoCrear(BaseModel):
    usuario_id: int
    producto_id: int
