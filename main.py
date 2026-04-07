from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlmodel import Session, select
from contextlib import asynccontextmanager
from seguridad import obtener_hash_password, verificar_password, crear_token_acceso

# Importamos lo que acabamos de crear
from database import crear_tablas, poblar_db, obtener_sesion
from models import Usuario

# Este "Lifespan" se ejecuta justo cuando el servidor arranca
@asynccontextmanager
async def lifespan(app: FastAPI):
    crear_tablas() # Crea el archivo .db y las tablas si no existen
    poblar_db()    # Inyecta los usuarios iniciales
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

# --- ENDPOINTS ---
@app.get("/")
def ruta_raiz():
    return {"mensaje": "API conectada a la Base de Datos con SQLModel"}

@app.post("/register")
def registro(nuevo_usuario: CredencialesRegistro, db: Session = Depends(obtener_sesion)):
    usuario_existente = db.exec(select(Usuario).where(Usuario.email == nuevo_usuario.email)).first()
    if usuario_existente:
        raise HTTPException(status_code=400, detail="Este correo ya está en uso")

    # 👇 Creamos el usuario encriptando la contraseña en este preciso instante
    usuario_db = Usuario(
        nombre=nuevo_usuario.nombre,
        email=nuevo_usuario.email,
        password=obtener_hash_password(nuevo_usuario.password) # 🔐 ¡MAGIA AQUÍ!
    )

    db.add(usuario_db)
    db.commit()
    db.refresh(usuario_db) 

    return {"mensaje": f"Usuario {usuario_db.nombre} registrado con éxito con el ID: {usuario_db.id}."}

@app.post("/login")
def login(credenciales: CredencialesLogin, db: Session = Depends(obtener_sesion)):
    usuario_db = db.exec(select(Usuario).where(Usuario.email == credenciales.email)).first()
    
    if not usuario_db or not verificar_password(credenciales.password, usuario_db.password):
        raise HTTPException(status_code=401, detail="Correo o contraseña incorrectos")
        
    # 👇 ¡MAGIA AQUÍ! Fabricamos el token guardando el correo del usuario ('sub' = subject)
    token_real = crear_token_acceso(data={"sub": usuario_db.email})
    
    # Devolvemos el token real a Flutter
    return {"token": token_real, "mensaje": f"Bienvenido {usuario_db.nombre}"}