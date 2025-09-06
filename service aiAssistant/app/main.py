from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime

app = FastAPI(
    title="IA Peliculeando",
    description="IA so you can watch and review movies alone with your girlfriend hehe ;-) ;-)",
    version="1.0.0"
)

# -------------------------------
# Usuarios de prueba
# -------------------------------
usuarios = [
    {"id": 1, "nombre": "Samuel", "correo": "samuel@example.com"},
    {"id": 2, "nombre": "Laura", "correo": "laura@example.com"},
]

class Usuario(BaseModel):
    nombre: str
    correo: str

@app.get("/usuarios", summary="Obtener lista de usuarios")
async def obtener_usuarios():
    return {"usuarios": usuarios}

@app.post("/usuarios", summary="Crear un nuevo usuario")
async def crear_usuario(user: Usuario):
    nuevo_id = len(usuarios) + 1
    nuevo_usuario = {"id": nuevo_id, "nombre": user.nombre, "correo": user.correo}
    usuarios.append(nuevo_usuario)
    return {"creado": True, "usuario": nuevo_usuario}


# -------------------------------
# Reseñas de películas con IA
# -------------------------------
reseñas = []

class Reseña(BaseModel):
    usuario_id: int
    pelicula: str
    comentario: str

@app.get("/reviews", summary="Obtener reseñas")
async def obtener_reseñas():
    return {"reseñas": reseñas}

@app.post("/reviews", summary="Crear reseña con IA")
async def crear_reseña(data: Reseña):
    # Buscar usuario
    usuario = next((u for u in usuarios if u["id"] == data.usuario_id), None)
    if not usuario:
        return {"error": "Usuario no encontrado"}

    # Respuesta simulada de la IA
    respuesta_ia = f"La película '{data.pelicula}' suele generar opiniones interesantes. Tu reseña fue: {data.comentario}"

    nueva_reseña = {
        "id": len(reseñas) + 1,
        "usuario": usuario["nombre"],
        "pelicula": data.pelicula,
        "comentario": data.comentario,
        "respuesta_ia": respuesta_ia,
        "fecha": datetime.now().isoformat()
    }
    reseñas.append(nueva_reseña)
    return {"creado": True, "reseña": nueva_reseña}
