from sqlmodel import SQLModel, create_engine, Session, select
from models import Usuario, Leccion, PreguntasTest
from seguridad import obtener_hash_password

URL_BASE_DATOS = "sqlite:///./tfg_musica.db"

connect_args = {"check_same_thread": False}
engine = create_engine(URL_BASE_DATOS, echo=True, connect_args=connect_args)

def crear_tablas():
    SQLModel.metadata.create_all(engine)

def poblar_db():
    with Session(engine) as db:
        # 1. Comprobamos si ya hay usuarios
        usuario_existente = db.exec(select(Usuario)).first()
        if not usuario_existente:
            print("👤 Creando usuario de prueba por defecto...")
            usuario_prueba = Usuario(
                nombre="Estudiante",
                email="test@test.com",
                password=obtener_hash_password("123456"),
                exp=0,
                racha_actual=0
            )
            db.add(usuario_prueba)
            db.commit()

        # 2. Comprobamos si ya hay lecciones
        leccion_existente = db.exec(select(Leccion)).first()
        if not leccion_existente:
            print("📚 Creando lecciones teóricas iniciales con Markdown, Pentagramas y Símbolos...")
            
            lecciones = [
                Leccion(
                    titulo="Lección 1: El Pulso",
                    indice_orden=1,
                    contenido_json={
                        "dificultad": "Fácil",
                        "descripcion": "El corazón de la música.",
                        "imagen_url": "https://images.unsplash.com/photo-1506157786151-b8491531f063?q=80&w=800&auto=format&fit=crop",
                        "texto": """### El latido constante
Toda la música tiene un "corazón" que late por debajo, aunque no siempre lo escuches. A este latido constante se le llama **Pulso**.

Imagina el tictac de un reloj o tus pasos cuando caminas a un ritmo constante. ¡Ese es el pulso!
---
### Siente el pulso
Para leer música, siempre debes mantener un pulso mental. En nuestra app, representamos el pulso básico con esta figura:

[RITMO:Negra]

Intenta dar golpes en la mesa sincronizados con el latido de la nota de arriba. ¡Acabas de encontrar el pulso!"""
                    }
                ),
                Leccion(
                    titulo="Lección 2: Las Notas Musicales",
                    indice_orden=2,
                    contenido_json={
                        "dificultad": "Fácil",
                        "descripcion": "El abecedario musical.",
                        "imagen_url": "https://images.unsplash.com/photo-1520523839897-bd0b52f945a0?q=80&w=800&auto=format&fit=crop",
                        "texto": """### El abecedario del sonido
Al igual que usamos letras para formar palabras, en la música usamos **notas** para crear melodías.

Existen 7 notas naturales fundamentales que debes memorizar en este orden:
**Do - Re - Mi - Fa - Sol - La - Si**
---
### La Escala
Cuando tocamos estas notas en orden, creamos lo que se llama una **Escala Musical**. 

Aquí tienes cómo se ven subiendo como una escalera. Fíjate cómo cada nota está un poquito más alta que la anterior:

[PENTAGRAMA:Do, Re, Mi, Fa, Sol, La, Si, Do+]

> **Nota:** Después del "Si", el ciclo vuelve a empezar con un "Do" más agudo."""
                    }
                ),
                Leccion(
                    titulo="Lección 3: El Pentagrama",
                    indice_orden=3,
                    contenido_json={
                        "dificultad": "Fácil",
                        "descripcion": "El lienzo donde se dibuja la música.",
                        "imagen_url": "https://images.unsplash.com/photo-1507838153414-b4b713384a76?q=80&w=800&auto=format&fit=crop",
                        "texto": """### ¿Dónde se escribe la música?
El **pentagrama** (del griego *penta* = cinco y *grama* = línea) es un conjunto de **5 líneas** horizontales y **4 espacios** entre ellas.

Las líneas y los espacios siempre se cuentan **de abajo hacia arriba**.
---
### Líneas y Espacios
Para saber qué nota tocar, el músico mira en qué línea o espacio está dibujada la cabeza de la nota.

Mira estas notas colocadas justo sobre las líneas:
[PENTAGRAMA:Mi, Sol, Si]

Y estas notas colocadas flotando en los espacios:
[PENTAGRAMA:Fa, La, Do+]"""
                    }
                ),
                Leccion(
                    titulo="Lección 4: La Clave de Sol",
                    indice_orden=4,
                    contenido_json={
                        "dificultad": "Fácil",
                        "descripcion": "La llave que da nombre a las notas.",
                        "imagen_url": "https://images.unsplash.com/photo-1558544959-1bc9171ee6a7?q=80&w=800&auto=format&fit=crop",
                        "texto": """### El símbolo principal
El gran símbolo rizado que siempre aparece al principio del pentagrama se llama **Clave de Sol**. 

[SIMBOLO:ClaveDeSol]

Sin ella, el pentagrama sería solo un grupo de líneas sin sentido. La Clave nos dice qué nombre tiene cada línea.
---
### Su secreto
Si te fijas, el dibujo de la Clave de Sol nace haciendo un círculo alrededor de la **segunda línea** (empezando desde abajo). 

Esto es una regla matemática: **Toda nota que se dibuje en esa segunda línea se llamará "Sol".**

[PENTAGRAMA:Sol]

A partir de ahí, deducimos el resto: si el Sol está en la línea 2, el "La" estará en el espacio justo por encima."""
                    }
                ),
                Leccion(
                    titulo="Lección 5: Las Figuras de Nota",
                    indice_orden=5,
                    contenido_json={
                        "dificultad": "Intermedio",
                        "descripcion": "Controlando la duración del sonido.",
                        "imagen_url": "https://images.unsplash.com/photo-1470225620780-dba8ba36b745?q=80&w=800&auto=format&fit=crop",
                        "texto": """### La duración
Ya sabemos leer qué nota tocar en el pentagrama, pero... ¿durante cuánto tiempo? Para eso usamos las **Figuras Rítmicas**.
---
### La Redonda y la Blanca
[RITMO:Redonda]
Dura **4 tiempos** (4 pulsos). Es el sonido más largo que usaremos por ahora.

[RITMO:Blanca]
Dura **2 tiempos**. Dura exactamente la mitad que la redonda.
---
### La Negra
[RITMO:Negra]
Dura **1 tiempo**. Es la figura que hemos usado para marcar nuestro pulso básico."""
                    }
                ),
                Leccion(
                    titulo="Lección 6: Compás y Línea Divisoria",
                    indice_orden=6,
                    contenido_json={
                        "dificultad": "Intermedio",
                        "descripcion": "Organizando el caos musical.",
                        "imagen_url": "https://images.unsplash.com/photo-1514320291840-2e0a9bf2a9ae?q=80&w=800&auto=format&fit=crop",
                        "texto": """### Cajas de música
Para no perdernos leyendo partituras larguísimas, los músicos dividen el pentagrama en pequeños fragmentos o "cajitas" del mismo tamaño. A estas divisiones las llamamos **Compases**.
---
### La línea divisoria
Para separar un compás del siguiente, dibujamos una línea vertical recta que cruza el pentagrama de arriba a abajo. Se llama **Línea Divisoria**.

[SIMBOLO:LineaDivisoria]

> **Regla de oro:** Todos los compases de una partitura deben sumar exactamente la misma cantidad de tiempos."""
                    }
                ),
                Leccion(
                    titulo="Lección 7: La Doble Barra Final",
                    indice_orden=7,
                    contenido_json={
                        "dificultad": "Fácil",
                        "descripcion": "El cartel de 'Fin' en la música.",
                        "imagen_url": "https://images.unsplash.com/photo-1460723237483-7a6dc9d0b212?q=80&w=800&auto=format&fit=crop",
                        "texto": """### El final del camino
Igual que en un libro el punto final te indica que la historia ha terminado, en la música necesitamos avisar a los músicos de que la pieza se ha acabado.
---
### Cómo se dibuja
Para marcar el final, se dibujan **dos líneas verticales juntas** al final del pentagrama. La primera línea es fina, y la segunda es más gruesa.

[SIMBOLO:BarraFinal]

¡Cuando veas la doble barra, es hora de dejar de tocar y esperar los aplausos!"""
                    }
                ),
                Leccion(
                    titulo="Lección 8: Compás de 2/4",
                    indice_orden=8,
                    contenido_json={
                        "dificultad": "Intermedio",
                        "descripcion": "El ritmo de las marchas.",
                        "imagen_url": "https://images.unsplash.com/photo-1533147670608-2a2f9776d3ac?q=80&w=800&auto=format&fit=crop",
                        "texto": """### Las matemáticas del ritmo
Al principio del pentagrama, justo después de la Clave de Sol, suele haber dos números colocados uno encima del otro. Nos dicen cuánto cabe en cada compás.

[SIMBOLO:Compas24]

---
### Dos por Cuatro
El compás de **2/4** significa que en cada "cajita" (compás) caben exactamente **2 pulsos** (dos negras).

Es un ritmo muy marcado y militar. Piensa en el sonido de una marcha o en caminar diciendo: **"Un, Dos. Un, Dos."**"""
                    }
                ),
                Leccion(
                    titulo="Lección 9: Compás de 3/4",
                    indice_orden=9,
                    contenido_json={
                        "dificultad": "Intermedio",
                        "descripcion": "El ritmo del vals.",
                        "imagen_url": "https://images.unsplash.com/photo-1544605417-7407000e0b35?q=80&w=800&auto=format&fit=crop",
                        "texto": """### Tres tiempos por caja
Si el 2/4 nos marcaba 2 tiempos, el **3/4** nos dice que cada compás debe sumar exactamente **3 pulsos**.

[SIMBOLO:Compas34]

---
### A bailar
Este ritmo no es militar, es el ritmo de un Vals. Suena como si el primer tiempo fuera fuerte y los otros dos más suaves.

Cuenta en voz alta marcando el 1: **"UN, dos, tres. UN, dos, tres."** ¡Esa es la magia del 3/4!"""
                    }
                ),
                Leccion(
                    titulo="Lección 10: Los Silencios",
                    indice_orden=10,
                    contenido_json={
                        "dificultad": "Intermedio",
                        "descripcion": "La música también es callar.",
                        "imagen_url": "https://images.unsplash.com/photo-1619983081563-430f63602796?q=80&w=800&auto=format&fit=crop",
                        "texto": """### El sonido de la nada
Mozart decía: *"La música no está en las notas, sino en el silencio entre ellas"*. 

En el pentagrama, no solo escribimos cuándo hay que tocar, sino también cuándo hay que hacer una pausa.
---
### Un silencio para cada figura
Cada figura musical tiene su hermano "silencioso" que dura exactamente el mismo tiempo:
* **Silencio de Negra (𝄽):** 1 tiempo en silencio (¡Shhh!).
* **Silencio de Blanca (𝄻):** 2 tiempos en silencio.
* **Silencio de Redonda (𝄺):** 4 tiempos en silencio absoluto."""
                    }
                ),
                Leccion(
                    titulo="Lección 11: Las Respiraciones",
                    indice_orden=11,
                    contenido_json={
                        "dificultad": "Avanzado",
                        "descripcion": "El aire que da vida a las frases.",
                        "imagen_url": "https://images.unsplash.com/photo-1516280440502-618b08709087?q=80&w=800&auto=format&fit=crop",
                        "texto": """### Tomando aire
Si cantas o tocas un instrumento de viento (como la flauta o el saxofón), no puedes tocar notas infinitamente sin ahogarte. Necesitas respirar.
---
### La coma mágica
Para organizar dónde respiran los músicos sin romper el ritmo, los compositores dibujan una pequeña marca que parece una **coma (, )** o un pequeño apóstrofe por encima del pentagrama.

Cuando ves esa marca, debes "robar" un instante de la nota anterior para coger aire y seguir tocando como si nada. ¡Requiere mucha práctica!"""
                    }
                )
            ]
            
            db.add_all(lecciones)
            db.commit()
            print("✅ Lecciones con Markdown inyectadas con éxito.")

           # 3. Comprobamos si ya hay preguntas
        pregunta_existente = db.exec(select(PreguntasTest)).first()
        if not pregunta_existente:
            print("Creando preguntas de prueba...")
            
            preguntas = [
                PreguntasTest(
                    enunciado="¿Cuántos tiempos dura una nota Blanca?",
                    opciones_json={"opciones": ["1 tiempo", "2 tiempos", "3 tiempos", "4 tiempos"]},
                    indice_correcta=1
                ),
                PreguntasTest(
                    enunciado="¿Qué nota musical está representada en este pentagrama?",
                    etiqueta_visual="[PENTAGRAMA:Sol]",
                    opciones_json={"opciones": ["Mi", "Fa", "Sol", "La"]},
                    indice_correcta=2
                ),
                PreguntasTest(
                    enunciado="¿Qué figura usamos para representar 1 pulso?",
                    etiqueta_visual="[RITMO:Negra]",
                    opciones_json={"opciones": ["Corchea", "Blanca", "Negra", "Redonda"]},
                    indice_correcta=2
                )
            ]
            
            db.add_all(preguntas)
            db.commit()
            print("✅ Preguntas inyectadas con éxito.")

def obtener_sesion():
    with Session(engine) as session:
        yield session