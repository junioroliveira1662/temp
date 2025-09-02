from google.adk.agents import Agent
from google.adk.tools import google_search
from dotenv import load_dotenv

load_dotenv()

root_agent = Agent(
    name="search_google_agent",
    model="gemini-2.5-flash",
    description="""
        Você é um agente de pesquisa.
    """,
    instruction="""
        Você é um agente de pesquisa especialista em automação de buscas na web. Sua missão é fornecer 
        informações atualizadas e precisas em tempo real usando a tool:
        - google_search
    """,
    tools=[google_search]   
)
