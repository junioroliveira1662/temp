# ./mcp_agent/agent.py
from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool.mcp_toolset import (
    MCPToolset,
    SseConnectionParams,
)

MCP_URL = "http://127.0.0.1:3000/mcp"

root_agent = LlmAgent(
    model="gemini-2.0-flash",
    name="kanbanize_mcp_agent",
    instruction=(
        "Você é um agente para operar o Kanbanize via MCP. "
        "Sempre que precisar de dados ou ações, use as tools MCP. "
        "Fluxo típico: 1) use get_boards para descobrir o board; "
        "2) use get_columns(board_id) para achar a coluna desejada; "
        "3) use create_card(board_id, column_id, title, description). "
        "Se faltar parâmetro, pergunte ao usuário."
    ),
    tools=[
        MCPToolset(
            connection_params=SseConnectionParams(url=MCP_URL),
            tool_filter=["get_boards", "get_columns", "create_card"],
        )
    ],
)