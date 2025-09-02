import os
from google.adk.agents import Agent
from google.adk.agents import LlmAgent
from dotenv import load_dotenv
from google.adk.tools import google_search
from google.adk.tools.agent_tool import AgentTool
from . import tools
from . import tools_kanbanize
from .util import load_instruction_from_file

load_dotenv()

sub_agent_kanbanize = LlmAgent(
    name="kanbanize_agent",
    model="gemini-2.5-flash",
    instruction=load_instruction_from_file("instructions/kanbanize.txt"),
    tools=[
        tools_kanbanize.get_boards,
        tools_kanbanize.get_columns,
        tools_kanbanize.create_card
    ],
    output_key="kanbanize_result"
)

sub_agent_search_google = LlmAgent(
    name="search_google_agent",
    model="gemini-2.5-flash",
    instruction="""
        Você é um agente de pesquisa especialista em automação de buscas na web. Sua missão é fornecer 
        informações atualizadas e precisas em tempo real usando a tool:
        - google_search
    """,
    tools=[
        google_search
    ],
    output_key="search_google_result"
)

sub_agent_search_bcb = LlmAgent(
    name="search_bcb_agent",
    model="gemini-2.5-flash",
    instruction="""
        Você é um agente especialista em consulta de dados no BCB. O seu papel é garantir que as informações buscadas estejam corretamente formatadas e apresentadas.
        1. Para realizar a busca você deve utilizar a tool:
        - search_bcb_content
    """,
    tools=[
        tools.search_bcb_content
    ],
    output_key="search_bcb_result"
)

sub_agent_user_story = LlmAgent(
    name="user_story_agent",
    model="gemini-2.5-flash",
    instruction=load_instruction_from_file("instructions/user_story.txt"),
    tools=[
        AgentTool(sub_agent_search_google),
        AgentTool(sub_agent_search_bcb),
        AgentTool(sub_agent_kanbanize)
    ],
    output_key="user_story_result"
)

agent_master = LlmAgent(
    name="master_agent_v2",
    model="gemini-2.0-flash-001",
    instruction=load_instruction_from_file("instructions/master.txt"),
    tools=[
        AgentTool(sub_agent_user_story)
    ],
)

root_agent = agent_master
