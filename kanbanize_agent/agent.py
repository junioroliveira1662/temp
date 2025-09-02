from google.adk.agents import Agent
from dotenv import load_dotenv
from . import tools

load_dotenv()

root_agent = Agent(
    name="kanbanize_agent",
    model="gemini-2.5-flash",
    description="""
        Você é um agente que utiliza a ferramenta de administração de tarefas na web chamada "Kanbanize" para gerenciar projetos de software.
    """,
    instruction="""
        Você é um agente especialista em administração de tarefas no Kanbanize. O seu papel é garantir que o trabalho seja organizado e executado eficientemente.
        1. Para realizar consulta de boards você deverá utilizar a tool:
        - get_boards
        2. Para realizar consulta de colunas é necessário informar o board_id, para isso utilize a tool:
        - get_columns
        3. Para criar um novo card utilize a tool:
        - create_card
    """,
    tools=[tools.get_boards, tools.get_columns, tools.create_card]   
)
