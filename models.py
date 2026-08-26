from datetime import datetime
from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship, Column, JSON

class Usuario(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True) 
    nombre: str 
    email: str = Field(unique=True, index=True) 
    password: str 
    exp: int = Field(default=0)
    racha_actual: int = Field(default=0) 
    ultima_conexion: Optional[datetime] = Field(default=None) 

    progresos: List["ProgresoLeccion"] = Relationship(back_populates="usuario")
    puntuaciones: List["PuntuacionMinijuego"] = Relationship(back_populates="usuario") 

class Leccion(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True) 
    titulo: str
    indice_orden: int 
    contenido_json: dict = Field(default={}, sa_column=Column(JSON)) 

    progresos: List["ProgresoLeccion"] = Relationship(back_populates="leccion") 

class ProgresoLeccion(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True) 
    completada: bool = Field(default=False) 
    estrellas: int = Field(default=0) 
    fecha_completado: Optional[datetime] = Field(default=None) 
    
    id_usuario: int = Field(foreign_key="usuario.id") 
    id_leccion: int = Field(foreign_key="leccion.id") 
    usuario: "Usuario" = Relationship(back_populates="progresos")
    leccion: "Leccion" = Relationship(back_populates="progresos")

class Minijuego(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    titulo: str 
    audio_url: str 
    dificultad: str 
    beatmap_json: dict = Field(default={}, sa_column=Column(JSON)) 

    puntuaciones: List["PuntuacionMinijuego"] = Relationship(back_populates="minijuego") 

class PuntuacionMinijuego(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True) 
    puntuacion_max: int 
    precision: float 
    fecha_completado: datetime = Field(default_factory=datetime.utcnow) 

    id_usuario: int = Field(foreign_key="usuario.id") 
    id_minijuego: int = Field(foreign_key="minijuego.id")

    usuario: "Usuario" = Relationship(back_populates="puntuaciones")
    minijuego: "Minijuego" = Relationship(back_populates="puntuaciones")

class PreguntasTest(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    enunciado: str
    etiqueta_visual : Optional[str] = Field(default=None)
    opciones_json: dict = Field(default={}, sa_column=Column(JSON))
    indice_correcta: int 