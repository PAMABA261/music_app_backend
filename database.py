from sqlmodel import SQLModel, create_engine, Session, select
from models import Usuario
from seguridad import obtener_hash_password

# El día que uses PostgreSQL, solo cambiarás esta línea por algo como:
# URL_BASE_DATOS = "postgresql://usuario:contraseña@localhost/tfg_musica"
URL_BASE_DATOS = "sqlite:///./tfg_musica.db"

# Configuramos el motor (echo=True hará que veas las consultas SQL en la terminal)
connect_args = {"check_same_thread": False}
engine = create_engine(URL_BASE_DATOS, echo=True, connect_args=connect_args)

def crear_tablas():
    SQLModel.metadata.create_all(engine)

def poblar_db():
    with Session(engine) as session:
        admin_existente = session.exec(select(Usuario).where(Usuario.email == "admin@tfg.com")).first()
        
        if not admin_existente:
            print("🌱 Poblando base de datos con usuarios seguros...")
            
            # 👇 Encriptamos las contraseñas antes de guardarlas en la base de datos
            usuario_admin = Usuario(
                nombre="Administrador", 
                email="admin@tfg.com", 
                password=obtener_hash_password("123456")
            )
            usuario_prueba = Usuario(
                nombre="Alumno Prueba", 
                email="alumno@tfg.com", 
                password=obtener_hash_password("password")
            )
            
            session.add(usuario_admin)
            session.add(usuario_prueba)
            session.commit()
            print("✅ Base de datos segura poblada con éxito.")

# Esta función se usará en FastAPI para abrir y cerrar la conexión en cada petición
def obtener_sesion():
    with Session(engine) as session:
        yield session