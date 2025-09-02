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
        tools_kanbanize.get_structure,
        tools_kanbanize.create_card
    ],
    output_key="kanbanize_result"
)

sub_agent_search_google = LlmAgent(
    name="search_google_agent",
    model="gemini-2.5-flash",
    instruction=load_instruction_from_file("instructions/search_google.txt"),
    tools=[
        google_search
    ],
    output_key="search_google_result"
)

sub_agent_search_bcb = LlmAgent(
    name="search_bcb_agent",
    model="gemini-2.5-flash",
    instruction=load_instruction_from_file("instructions/search_bcb.txt"),
    tools=[
        tools.search_bcb_content
    ],
    output_key="search_bcb_result"
)

agent_master = LlmAgent(
    name="user_story_agent",
    model="gemini-2.5-flash",
    instruction=load_instruction_from_file("instructions/user_story.txt"),
    tools=[
        AgentTool(sub_agent_search_google),
        AgentTool(sub_agent_search_bcb),
        AgentTool(sub_agent_kanbanize)
    ]
)

root_agent = agent_master
