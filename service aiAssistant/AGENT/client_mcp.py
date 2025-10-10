import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def run_mcp_client():
    """Cliente MCP para interactuar con el servidor"""
    
    # Configuración del servidor
    server_params = StdioServerParameters(
        command="python",
        args=["server_mcp.py"],
        env=None
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Inicializar la sesión
            await session.initialize()
            
            # Listar herramientas disponibles
            tools = await session.list_tools()
            print("\n=== Herramientas disponibles ===")
            for tool in tools.tools:
                print(f"- {tool.name}: {tool.description}")
            
            # Ejemplo: Obtener todas las películas
            print("\n=== Obtener todas las películas ===")
            result = await session.call_tool("get_all_movies", {})
            for content in result.content:
                print(content.text)
            
            # Ejemplo: Buscar películas
            print("\n=== Buscar películas de 'Drama' ===")
            result = await session.call_tool("search_movies", {"query": "Drama"})
            for content in result.content:
                print(content.text)
            
            # Ejemplo: Agregar una película
            print("\n=== Agregar nueva película ===")
            result = await session.call_tool("add_movie", {
                "title": "Interstellar",
                "genre": "Sci-Fi",
                "releaseYear": 2014
            })
            for content in result.content:
                print(content.text)

if __name__ == "__main__":
    asyncio.run(run_mcp_client())