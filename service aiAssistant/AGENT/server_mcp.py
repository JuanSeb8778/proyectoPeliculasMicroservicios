import asyncio
import logging
from mcp.server import Server
from mcp.types import Tool, TextContent
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("mcp-server")

# Configuración de la base de datos PostgreSQL
DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': os.getenv('DB_NAME', 'PeliculasIA'),
    'user': 'postgres',
    'password': os.getenv('DB_PASSWORD', 'samu05'),
    'options': '-c client_encoding=UTF8'
}

def get_db_connection():
    """Crear conexión a la base de datos"""
    return psycopg2.connect(**DB_CONFIG, cursor_factory=RealDictCursor)

# Crear servidor MCP
app = Server("movies-mcp-server")

@app.list_tools()
async def list_tools() -> list[Tool]:
    """Lista todas las herramientas disponibles"""
    return [
        Tool(
            name="get_all_movies",
            description="Obtiene todas las películas de la base de datos",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        Tool(
            name="get_movie_by_id",
            description="Obtiene una película por su ID",
            inputSchema={
                "type": "object",
                "properties": {
                    "id": {
                        "type": "integer",
                        "description": "ID de la película"
                    }
                },
                "required": ["id"]
            }
        ),
        Tool(
            name="search_movies",
            description="Busca películas por título o género",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Texto a buscar en título o género"
                    }
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="add_movie",
            description="Agrega una nueva película a la base de datos",
            inputSchema={
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "Título de la película"
                    },
                    "genre": {
                        "type": "string",
                        "description": "Género de la película"
                    },
                    "releaseYear": {
                        "type": "integer",
                        "description": "Año de lanzamiento"
                    }
                },
                "required": ["title", "genre", "releaseYear"]
            }
        ),
        Tool(
            name="update_movie",
            description="Actualiza una película existente",
            inputSchema={
                "type": "object",
                "properties": {
                    "id": {
                        "type": "integer",
                        "description": "ID de la película"
                    },
                    "title": {
                        "type": "string",
                        "description": "Nuevo título"
                    },
                    "genre": {
                        "type": "string",
                        "description": "Nuevo género"
                    },
                    "releaseYear": {
                        "type": "integer",
                        "description": "Nuevo año de lanzamiento"
                    }
                },
                "required": ["id"]
            }
        ),
        Tool(
            name="delete_movie",
            description="Elimina una película por su ID",
            inputSchema={
                "type": "object",
                "properties": {
                    "id": {
                        "type": "integer",
                        "description": "ID de la película a eliminar"
                    }
                },
                "required": ["id"]
            }
        ),
        Tool(
            name="get_movies_by_year",
            description="Obtiene películas filtradas por año de lanzamiento",
            inputSchema={
                "type": "object",
                "properties": {
                    "year": {
                        "type": "integer",
                        "description": "Año de lanzamiento"
                    }
                },
                "required": ["year"]
            }
        ),
        Tool(
            name="get_movies_by_genre",
            description="Obtiene películas filtradas por género",
            inputSchema={
                "type": "object",
                "properties": {
                    "genre": {
                        "type": "string",
                        "description": "Género de la película"
                    }
                },
                "required": ["genre"]
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Ejecuta una herramienta específica"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        if name == "get_all_movies":
            cursor.execute("SELECT * FROM movies ORDER BY releaseYear DESC")
            movies = cursor.fetchall()
            return [TextContent(
                type="text",
                text=f"Películas encontradas: {len(movies)}\n\n" + 
                     "\n".join([f"ID: {m['id']} - {m['title']} ({m['releaseyear']}) - {m['genre']}" 
                               for m in movies])
            )]
        
        elif name == "get_movie_by_id":
            movie_id = arguments["id"]
            cursor.execute("SELECT * FROM movies WHERE id = %s", (movie_id,))
            movie = cursor.fetchone()
            if movie:
                return [TextContent(
                    type="text",
                    text=f"Película encontrada:\nID: {movie['id']}\nTítulo: {movie['title']}\n"
                         f"Género: {movie['genre']}\nAño: {movie['releaseyear']}"
                )]
            return [TextContent(type="text", text=f"No se encontró película con ID {movie_id}")]
        
        elif name == "search_movies":
            query = arguments["query"].lower()
            cursor.execute(
                "SELECT * FROM movies WHERE LOWER(title) LIKE %s OR LOWER(genre) LIKE %s",
                (f"%{query}%", f"%{query}%")
            )
            movies = cursor.fetchall()
            if movies:
                return [TextContent(
                    type="text",
                    text=f"Se encontraron {len(movies)} películas:\n\n" +
                         "\n".join([f"ID: {m['id']} - {m['title']} ({m['releaseyear']}) - {m['genre']}"
                                   for m in movies])
                )]
            return [TextContent(type="text", text=f"No se encontraron películas con: {query}")]
        
        elif name == "add_movie":
            title = arguments["title"]
            genre = arguments["genre"]
            year = arguments["releaseYear"]
            
            cursor.execute(
                "INSERT INTO movies (title, genre, releaseYear) VALUES (%s, %s, %s) RETURNING id",
                (title, genre, year)
            )
            new_id = cursor.fetchone()['id']
            conn.commit()
            
            return [TextContent(
                type="text",
                text=f"Película agregada exitosamente con ID: {new_id}\n"
                     f"Título: {title}\nGénero: {genre}\nAño: {year}"
            )]
        
        elif name == "update_movie":
            movie_id = arguments["id"]
            updates = []
            params = []
            
            if "title" in arguments:
                updates.append("title = %s")
                params.append(arguments["title"])
            if "genre" in arguments:
                updates.append("genre = %s")
                params.append(arguments["genre"])
            if "releaseYear" in arguments:
                updates.append("releaseYear = %s")
                params.append(arguments["releaseYear"])
            
            if updates:
                params.append(movie_id)
                cursor.execute(
                    f"UPDATE movies SET {', '.join(updates)} WHERE id = %s",
                    params
                )
                conn.commit()
                return [TextContent(
                    type="text",
                    text=f"Película con ID {movie_id} actualizada exitosamente"
                )]
            return [TextContent(type="text", text="No se proporcionaron campos para actualizar")]
        
        elif name == "delete_movie":
            movie_id = arguments["id"]
            cursor.execute("DELETE FROM movies WHERE id = %s", (movie_id,))
            conn.commit()
            
            if cursor.rowcount > 0:
                return [TextContent(
                    type="text",
                    text=f"Película con ID {movie_id} eliminada exitosamente"
                )]
            return [TextContent(type="text", text=f"No se encontró película con ID {movie_id}")]
        
        elif name == "get_movies_by_year":
            year = arguments["year"]
            cursor.execute("SELECT * FROM movies WHERE releaseYear = %s", (year,))
            movies = cursor.fetchall()
            if movies:
                return [TextContent(
                    type="text",
                    text=f"Películas del año {year}:\n\n" +
                         "\n".join([f"ID: {m['id']} - {m['title']} - {m['genre']}"
                                   for m in movies])
                )]
            return [TextContent(type="text", text=f"No se encontraron películas del año {year}")]
        
        elif name == "get_movies_by_genre":
            genre = arguments["genre"]
            cursor.execute("SELECT * FROM movies WHERE LOWER(genre) = LOWER(%s)", (genre,))
            movies = cursor.fetchall()
            if movies:
                return [TextContent(
                    type="text",
                    text=f"Películas de género {genre}:\n\n" +
                         "\n".join([f"ID: {m['id']} - {m['title']} ({m['releaseyear']})"
                                   for m in movies])
                )]
            return [TextContent(type="text", text=f"No se encontraron películas del género {genre}")]
        
    except Exception as e:
        logger.error(f"Error en {name}: {str(e)}")
        return [TextContent(type="text", text=f"Error: {str(e)}")]
    
    finally:
        cursor.close()
        conn.close()

async def main():
    """Iniciar el servidor MCP"""
    from mcp.server.stdio import stdio_server
    
    logger.info("Iniciando servidor MCP para películas...")
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())

if __name__ == "__main__":
    asyncio.run(main())