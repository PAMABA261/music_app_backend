from fastapi import FastAPI, HTTPException, Depends, Security
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel
from sqlmodel import Session, select
from contextlib import asynccontextmanager
from datetime import datetime
from typing import List
from models import Usuario, Leccion, ProgresoLeccion, PreguntasTest

# Importaciones de tus archivos locales
from seguridad import (
    obtener_hash_password, 
    verificar_password, 
    crear_token_acceso, 
    verificar_token  # <--- Asegúrate de tener esta función en seguridad.py
)
from database import crear_tablas, poblar_db, obtener_sesion
from models import Usuario, Leccion, ProgresoLeccion

# Configuración de Seguridad para recibir el Token desde Flutter
security = HTTPBearer()

@asynccontextmanager
async def lifespan(app: FastAPI):
    crear_tablas() # Crea las 5 tablas de tu PDF
    poblar_db()    # Inyecta datos iniciales
    yield

app = FastAPI(title="TFG Música API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- MOLDES DE RECEPCIÓN (Pydantic) ---
class CredencialesLogin(BaseModel):
    email: str
    password: str

class CredencialesRegistro(BaseModel):
    nombre: str
    email: str
    password: str

class ProgresoMinijuego(BaseModel):
    id_minijuego: str
    puntos: int

# --- ENDPOINTS DE USUARIO ---

@app.get("/")
def ruta_raiz():
    return {"mensaje": "API del TFG conectada y funcionando"}

@app.post("/register")
def registro(nuevo_usuario: CredencialesRegistro, db: Session = Depends(obtener_sesion)):
    usuario_existente = db.exec(select(Usuario).where(Usuario.email == nuevo_usuario.email)).first()
    if usuario_existente:
        raise HTTPException(status_code=400, detail="Este correo ya está en uso")

    usuario_db = Usuario(
        nombre=nuevo_usuario.nombre,
        email=nuevo_usuario.email,
        password=obtener_hash_password(nuevo_usuario.password)
    )

    db.add(usuario_db)
    db.commit()
    db.refresh(usuario_db) 

    return {"mensaje": f"Usuario {usuario_db.nombre} registrado con éxito."}

@app.post("/login")
def login(credenciales: CredencialesLogin, db: Session = Depends(obtener_sesion)):
    usuario_db = db.exec(select(Usuario).where(Usuario.email == credenciales.email)).first()
    
    if not usuario_db or not verificar_password(credenciales.password, usuario_db.password):
        raise HTTPException(status_code=401, detail="Correo o contraseña incorrectos")
        
    token_real = crear_token_acceso(data={"sub": usuario_db.email})
    
    return {"token": token_real, "mensaje": f"Bienvenido {usuario_db.nombre}"}

@app.get("/usuarios/me")
def obtener_perfil_usuario(credenciales: HTTPAuthorizationCredentials = Security(security), db: Session = Depends(obtener_sesion)):
    token_data = verificar_token(credenciales.credentials)
    if not token_data:
        raise HTTPException(status_code=401, detail="Token invalido")
    usuario = db.exec(select(Usuario).where(Usuario.email == token_data["sub"])).first()
    if not usuario:
        raise HTTPException(status_code=404, detail='Usuario no encontrado')
    return {
        "nombre": usuario.nombre,
        "exp": usuario.exp,
        "racha_actual": usuario.racha_actual
    }

@app.post("/completar-minijuegos")
def crear_minijuegos(minijuego: ProgresoMinijuego, credenciales: HTTPAuthorizationCredentials = Security(security), db: Session = Depends(obtener_sesion)):
    token_data = verificar_token(credenciales.credentials)
    if not token_data:
        raise HTTPException(status_code=401, detail="Token invalido")
    usuario = db.exec(select(Usuario).where(Usuario.email == token_data["sub"])).first()
    if not usuario:
        raise HTTPException(status_code=404, detail='Usuario no encontrado')
    usuario.exp += minijuego.puntos
    db.add(usuario)
    db.commit()
    return {"mensaje": f"Minijuego {minijuego.id_minijuego} completado, ganaste {minijuego.puntos} puntos de EXP"}

# --- ENDPOINTS DE LECCIONES (NUEVOS) ---

@app.get("/lecciones", response_model=List[Leccion])
def obtener_lecciones(db: Session = Depends(obtener_sesion)):
    """Lista todas las lecciones disponibles"""
    return db.exec(select(Leccion).order_by(Leccion.indice_orden)).all()

@app.post("/completar-leccion/{leccion_id}")
def completar_leccion(
    leccion_id: int, 
    credenciales: HTTPAuthorizationCredentials = Security(security),
    db: Session = Depends(obtener_sesion)
):
    
    """Guarda el progreso del usuario y le da puntos de EXP"""
    # 1. Validamos el Token que viene de Flutter
    token_data = verificar_token(credenciales.credentials)
    if not token_data:
        raise HTTPException(status_code=401, detail="Token inválido")
    
    # 2. Buscamos al usuario en la DB
    email_usuario = token_data["sub"]
    usuario = db.exec(select(Usuario).where(Usuario.email == email_usuario)).first()

    # 3. Miramos si ya la completó antes
    progreso_previo = db.exec(
        select(ProgresoLeccion).where(
            ProgresoLeccion.id_usuario == usuario.id,
            ProgresoLeccion.id_leccion == leccion_id
        )
    ).first()

    if not progreso_previo:
        nuevo_progreso = ProgresoLeccion(
            id_usuario=usuario.id,
            id_leccion=leccion_id,
            completada=True,
            fecha_completado=datetime.now()
        )
        # Sumamos experiencia (Gamificación)
        usuario.exp += 10
        
        db.add(nuevo_progreso)
        db.add(usuario)
        db.commit()
        return {"mensaje": "¡Lección guardada! Ganaste 10 puntos de EXP"}
    
    return {"mensaje": "Lección ya completada anteriormente"}

# --- ENDPOINTS DE PRÁCTICA (NUEVOS) ---

@app.get("/preguntas", response_model=List[PreguntasTest])
def obtener_preguntas(db: Session = Depends(obtener_sesion)):
    """Devuelve la lista de preguntas para el test de práctica"""
    return db.exec(select(PreguntasTest)).all()