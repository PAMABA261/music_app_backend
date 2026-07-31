from datetime import datetime
from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship, Column, JSON

# --- 1. TABLA USUARIO ---
class Usuario(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True) # [cite: 1, 4]
    nombre: str # [cite: 2, 5]
    email: str = Field(unique=True, index=True) # [cite: 6, 7]
    password: str # [cite: 8, 9]
    exp: int = Field(default=0) # [cite: 10, 11]
    racha_actual: int = Field(default=0) # [cite: 12]
    ultima_conexion: Optional[datetime] = Field(default=None) # [cite: 13]

    # Relaciones para acceder a los datos fácilmente
    progresos: List["ProgresoLeccion"] = Relationship(back_populates="usuario") # [cite: 14]
    puntuaciones: List["PuntuacionMinijuego"] = Relationship(back_populates="usuario") # [cite: 29]

# --- 2. TABLA LECCIÓN (Teoría) ---
class Leccion(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True) # [cite: 54, 55]
    titulo: str # [cite: 56, 57]
    indice_orden: int # [cite: 58]
    # Usamos sa_column para que SQLite/PostgreSQL entiendan el formato JSON de tu PDF
    contenido_json: dict = Field(default={}, sa_column=Column(JSON)) # [cite: 59]

    progresos: List["ProgresoLeccion"] = Relationship(back_populates="leccion") # [cite: 45]

# --- 3. TABLA PROGRESO LECCIÓN (Relación Usuario-Lección) ---
class ProgresoLeccion(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True) # [cite: 41, 42]
    completada: bool = Field(default=False) # [cite: 43, 44]
    estrellas: int = Field(default=0) # [cite: 46, 47]
    fecha_completado: Optional[datetime] = Field(default=None) # [cite: 48]
    
    # Claves Foráneas (FK) del diagrama
    id_usuario: int = Field(foreign_key="usuario.id") # [cite: 49, 50]
    id_leccion: int = Field(foreign_key="leccion.id") # [cite: 51, 52]

    usuario: "Usuario" = Relationship(back_populates="progresos")
    leccion: "Leccion" = Relationship(back_populates="progresos")

# --- 4. TABLA MINIJUEGO (Práctica) ---
class Minijuego(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True) # [cite: 32, 33]
    titulo: str # [cite: 34, 35]
    audio_url: str # [cite: 36, 37]
    dificultad: str # [cite: 38, 39]
    beatmap_json: dict = Field(default={}, sa_column=Column(JSON)) # [cite: 40]

    puntuaciones: List["PuntuacionMinijuego"] = Relationship(back_populates="minijuego") # [cite: 30]

# --- 5. TABLA PUNTUACIÓN MINIJUEGO (Relación Usuario-Minijuego) ---
class PuntuacionMinijuego(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True) # [cite: 17, 18]
    puntuacion_max: int # [cite: 19, 20]
    precision: float # [cite: 21, 22]
    fecha_completado: datetime = Field(default_factory=datetime.utcnow) # [cite: 23, 24]

    # Claves Foráneas (FK) del diagrama
    id_usuario: int = Field(foreign_key="usuario.id") # [cite: 25, 26]
    id_minijuego: int = Field(foreign_key="minijuego.id") # [cite: 27, 28]

    usuario: "Usuario" = Relationship(back_populates="puntuaciones")
    minijuego: "Minijuego" = Relationship(back_populates="puntuaciones")

# --- 6. TABLA PREGUNTAS TEST ---
class PreguntasTest(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    enunciado: str
    etiqueta_visual : Optional[str] = Field(default=None)
    opciones_json: dict = Field(default={}, sa_column=Column(JSON))
    indice_correcta: int 