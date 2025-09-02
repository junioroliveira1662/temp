import os
from google.adk.agents import Agent
from dotenv import load_dotenv
# from google.adk.tools import google_search
from . import tools
from . import tools_kanbanize
from .util import load_instruction_from_file

load_dotenv()

root_agent = Agent(
    name="full_agent",
    model="gemini-2.5-flash",
    description="""
        Você é um agente que utiliza a ferramenta de busca na web chamada "search_bcb" para consultar informações no site do Banco Central do Brasil.
    """,
    instruction=load_instruction_from_file("instructions/full.txt"),
    tools=[
        tools.search_bcb_content,
        tools_kanbanize.get_boards, 
        tools_kanbanize.get_columns, 
        tools_kanbanize.create_card,
        # google_search
    ]
)