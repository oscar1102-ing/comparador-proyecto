from pydantic import BaseModel

class VerificarMFA(BaseModel):
    usuario_id: int
    codigo: str
