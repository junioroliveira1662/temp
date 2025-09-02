from google.adk.agents import Agent
from dotenv import load_dotenv
from . import tools

load_dotenv()

root_agent = Agent(
    name="search_bcb_agent",
    model="gemini-2.5-flash",
    description="""
        Você é um agente que utiliza a ferramenta de busca na web chamada "search_bcb" para consultar informações no site do Banco Central do Brasil.
    """,
    instruction="""
        Você é um agente especialista em consulta de dados no BCB. O seu papel é garantir que as informações buscadas estejam corretamente formatadas e apresentadas.
        1. Para realizar a busca você deve utilizar a tool:
        - search_bcb_content
    """,
    tools=[tools.search_bcb_content]
)
