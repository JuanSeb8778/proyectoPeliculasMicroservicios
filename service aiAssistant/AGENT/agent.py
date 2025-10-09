import os
import asyncio
from dotenv import load_dotenv
import google.generativeai as genai
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# ==================================================
# 🔧 CONFIGURACIÓN INICIAL
# ==================================================

# Cargar variables de entorno
load_dotenv()

# Obtener y verificar la API Key
api_key = os.getenv('GEMINI_API_KEY')
if not api_key:
    raise ValueError("❌ Error: No se encontró GEMINI_API_KEY en el archivo .env")

# Configurar Gemini
genai.configure(api_key=api_key)
print("✓ API Key de Gemini configurada correctamente")

# 🔹 Forzamos el uso del modelo gratuito
selected_model = "models/gemini-2.0-flash"

print(f"✅ Usando modelo gratuito: {selected_model}")

# ==================================================
# 🤖 CLASE PRINCIPAL DEL AGENTE
# ==================================================

class MovieAgent:
    def __init__(self):
        self.model = genai.GenerativeModel(selected_model)
        self.session = None
        self.mcp_session = None
        self.tools = []
        
    async def initialize_mcp(self):
        """Inicializar conexión con el servidor MCP"""
        server_params = StdioServerParameters(
            command="python",
            args=["server_mcp.py"],
            env=None
        )
        
        self.session = stdio_client(server_params)
        read, write = await self.session.__aenter__()
        
        self.mcp_session = ClientSession(read, write)
        await self.mcp_session.__aenter__()
        await self.mcp_session.initialize()
        
        # Obtener herramientas disponibles
        tools_response = await self.mcp_session.list_tools()
        self.tools = tools_response.tools
        
        print(f"✓ MCP inicializado con {len(self.tools)} herramientas")
    
    async def close_mcp(self):
        """Cerrar conexión MCP"""
        if self.mcp_session:
            await self.mcp_session.__aexit__(None, None, None)
        if self.session:
            await self.session.__aexit__(None, None, None)
    
    def get_tools_description(self):
        """Obtener descripción de herramientas para el prompt"""
        tools_desc = "Herramientas disponibles:\n"
        for tool in self.tools:
            tools_desc += f"- {tool.name}: {tool.description}\n"
            tools_desc += f"  Parámetros: {tool.inputSchema.get('properties', {})}\n"
        return tools_desc
    
    async def execute_tool(self, tool_name: str, arguments: dict):
        """Ejecutar una herramienta MCP"""
        try:
            result = await self.mcp_session.call_tool(tool_name, arguments)
            return result.content[0].text if result.content else "No se obtuvo respuesta"
        except Exception as e:
            return f"Error al ejecutar {tool_name}: {str(e)}"
    
    def parse_tool_call(self, response_text: str):
        """Parsear respuesta del modelo para extraer llamadas a herramientas"""
        import re
        pattern = r'TOOL\[([\w_]+)\]\((.*?)\)'
        matches = re.findall(pattern, response_text)
        
        tools_to_call = []
        for match in matches:
            tool_name = match[0]
            args_str = match[1]
            
            args = {}
            if args_str:
                for arg in args_str.split(','):
                    if '=' in arg:
                        key, value = arg.strip().split('=', 1)
                        value = value.strip().strip('"\'')
                        try:
                            value = int(value)
                        except:
                            pass
                        args[key.strip()] = value
            
            tools_to_call.append((tool_name, args))
        
        return tools_to_call
    
    async def process_query(self, user_query: str):
        """Procesar consulta del usuario"""
        system_prompt = f"""Eres un asistente especializado en gestión de películas.
        
{self.get_tools_description()}

Cuando necesites usar una herramienta, responde con el formato:
TOOL[nombre_herramienta](parametro1=valor1, parametro2=valor2)

Puedes usar múltiples herramientas si es necesario.
Después de recibir los resultados, proporciona una respuesta amigable al usuario.
"""
        
        full_prompt = f"{system_prompt}\n\nUsuario: {user_query}\n\nAsistente:"
        
        try:
            response = self.model.generate_content(full_prompt)
            response_text = response.text
        except Exception as e:
            return f"⚠️ Error al generar respuesta con Gemini: {str(e)}"
        
        print(f"\n🤖 Respuesta inicial: {response_text}\n")
        
        tools_to_call = self.parse_tool_call(response_text)
        
        if tools_to_call:
            tool_results = []
            for tool_name, args in tools_to_call:
                print(f"⚙️  Ejecutando: {tool_name} con {args}")
                result = await self.execute_tool(tool_name, args)
                tool_results.append(f"Resultado de {tool_name}: {result}")
            
            results_text = "\n".join(tool_results)
            final_prompt = f"{full_prompt}\n\nResultados de herramientas:\n{results_text}\n\nPor favor, proporciona una respuesta final clara y concisa:"
            
            try:
                final_response = self.model.generate_content(final_prompt)
                return final_response.text
            except Exception as e:
                return f"⚠️ Error al generar respuesta final: {str(e)}"
        
        return response_text

# ==================================================
# 🚀 FUNCIÓN PRINCIPAL
# ==================================================

async def main():
    """Función principal"""
    agent = MovieAgent()
    
    try:
        await agent.initialize_mcp()
        
        print("\n" + "="*50)
        print("🎬 AGENTE DE IA - GESTIÓN DE PELÍCULAS")
        print("="*50)
        print("\nEjemplos de consultas:")
        print("- Muéstrame todas las películas")
        print("- Busca películas de ciencia ficción")
        print("- Agrega la película Titanic del año 1997 género Drama")
        print("- ¿Qué películas hay del año 1994?")
        print("\nEscribe 'salir' para terminar\n")
        
        while True:
            user_input = input("👤 Tú: ").strip()
            
            if user_input.lower() in ['salir', 'exit', 'quit']:
                print("\n¡Hasta luego! 👋")
                break
            
            if not user_input:
                continue
            
            response = await agent.process_query(user_input)
            print(f"\n🤖 Asistente: {response}\n")
    
    finally:
        await agent.close_mcp()

if __name__ == "__main__":
    asyncio.run(main())
