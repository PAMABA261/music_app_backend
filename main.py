from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="TFG Música API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 👇 NUESTRA BASE DE DATOS EN MEMORIA (El "Truco")
# Almacena el correo como clave y la contraseña como valor.
# Viene con el admin ya creado por defecto.
usuarios_db = {
    "admin@tfg.com": "123456"
}

# --- MOLDES DE DATOS ---
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
    return {"mensaje": "¡El cerebro de FastAPI está vivo y funcionando!"}

@app.post("/register")
def registro_mock(nuevo_usuario: CredencialesRegistro):
    # 1. Comprobamos si el correo ya existe en nuestra base de datos temporal
    if nuevo_usuario.email in usuarios_db:
        raise HTTPException(status_code=400, detail="Este correo ya está en uso")
    
    # 2. Guardamos al nuevo usuario en la memoria
    usuarios_db[nuevo_usuario.email] = nuevo_usuario.password
    
    # Imprimimos en la consola negra para que veas qué está pasando
    print(f"✅ REGISTRO EXITOSO: {nuevo_usuario.nombre}")
    print(f"📂 Base de datos actual: {usuarios_db}")
    
    return {"mensaje": f"Usuario {nuevo_usuario.nombre} registrado con éxito."}

@app.post("/login")
def login_mock(credenciales: CredencialesLogin):
    # 3. Comprobamos si el email existe en la memoria Y si la contraseña es correcta
    if credenciales.email in usuarios_db and usuarios_db[credenciales.email] == credenciales.password:
        return {"token": "token_jwt_simulado_super_seguro", "mensaje": "Login exitoso"}
    else:
        raise HTTPException(status_code=401, detail="Correo o contraseña incorrectos")