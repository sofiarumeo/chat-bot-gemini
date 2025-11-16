from pydantic import BaseModel
from typing import Optional

class chatRequest(BaseModel):
    mensaje: str
    rol: Optional[str] = None
    reset: bool = False

class chatResponse(BaseModel):
    respuesta: str