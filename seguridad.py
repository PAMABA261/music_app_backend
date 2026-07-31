from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from jose import jwt

# --- 1. CONFIGURACIÓN DE PASSLIB (Bcrypt) ---
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def obtener_hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verificar_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# --- 2. CONFIGURACIÓN DE JWT ---
# IMPORTANTE: En el mundo real, esta clave se esconde en un archivo .env
SECRET_KEY = "tu_clave_super_secreta_para_el_tfg_de_musica_no_compartir"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 # El token será válido durante 1 hora

def crear_token_acceso(data: dict) -> str:
    """Crea un token JWT firmado con los datos del usuario y una fecha de caducidad"""
    to_encode = data.copy()
    
    # Calculamos cuándo caduca el token (ahora + 60 minutos)
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # Añadimos la caducidad ('exp') a los datos
    to_encode.update({"exp": expire})
    
    # Fabricamos y firmamos el token
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt

def verificar_token(token: str) -> dict:
    """
    Recibe el token, lo abre usando la SECRET_KEY y nos devuelve 
    los datos del usuario (el email que guardamos en 'sub').
    """
    try:
        # Intentamos decodificar el token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload  # Si todo está bien, devuelve el diccionario con el email
    except Exception:
        # Si el token es falso, ha caducado o está manipulado, devolvemos None
        return None