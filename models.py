from typing import Optional
from sqlmodel import Field, SQLModel

# Al poner table=True, SQLModel sabe que esto debe ser una tabla en la base de datos
class Usuario(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    email: str = Field(unique=True, index=True) # unique=True evita correos duplicados
    password: str # En el próximo sprint la encriptaremos