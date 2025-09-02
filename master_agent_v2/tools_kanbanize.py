import os
import requests
from dotenv import load_dotenv
from typing import Optional, List, Dict, Any

# Variáveis de configuração
BASE_URL = "https://i8solucoes.businessmap.io"
API_KEY = "XgFk8MTf86itLvezTKF0Nnl8ANQwgZiq3lrPbebV"


# Load environment variables
load_dotenv()

# --- Kanbanize API Config ---
KANBANIZE_BASE_URL = os.environ.get("KANBANIZE_BASE_URL")
KANBANIZE_API_KEY = os.environ.get("KANBANIZE_API_KEY")

# Headers com API Key
kanbanize_headers = {
    "apikey": KANBANIZE_API_KEY,
    "accept": "application/json",
    "Content-Type": "application/json"
}

def get_boards():
    """
    Consulta os boards do Kanbanize usando a API v2.
    Retorna a resposta em JSON.
    """
    if not KANBANIZE_API_KEY:
        return {"error": "Kanbanize API Key não configurada no .env."}
    if not KANBANIZE_BASE_URL:
        return {"error": "KANBANIZE_BASE_URL não configurada no .env."}
    
    print("Kanbanize API Key configurada: ", KANBANIZE_API_KEY)
    
    url = f"{KANBANIZE_BASE_URL}/api/v2/boards"

    response = requests.get(url, headers=kanbanize_headers)

    # Tratamento de erros
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(
            f"Erro {response.status_code} ao consultar boards: {response.text}"
        )
        
def get_structure(board_id: int):
    """
    Consulta a estrutura de um board no Kanbanize.
    
    Args:
        board_id (int): ID do board a ser consultado.
    
    Returns:
        list: Lista da estrutura do board em formato JSON.
    """
    if not KANBANIZE_API_KEY:
        return {"error": "Kanbanize API Key não configurada no .env."}
    if not KANBANIZE_BASE_URL:
        return {"error": "KANBANIZE_BASE_URL não configurada no .env."}
    if not board_id:
        return {"error": "Parâmetros obrigatórios ausentes: board_id e title."}
    
    url = f"{KANBANIZE_BASE_URL}/api/v2/boards/{board_id}/currentStructure"
    
    response = requests.get(url, headers=kanbanize_headers)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(
            f"Erro {response.status_code} ao consultar a estrutura do board {board_id}: {response.text}"
        )
        
def get_columns(board_id: int):
    """
    Consulta as colunas de um board no Kanbanize.
    
    Args:
        board_id (int): ID do board a ser consultado.
    
    Returns:
        list: Lista de colunas em formato JSON.
    """
    if not KANBANIZE_API_KEY:
        return {"error": "Kanbanize API Key não configurada no .env."}
    if not KANBANIZE_BASE_URL:
        return {"error": "KANBANIZE_BASE_URL não configurada no .env."}
    if not board_id:
        return {"error": "Parâmetros obrigatórios ausentes: board_id e title."}
    
    url = f"{BASE_URL}/api/v2/boards/{board_id}/columns"
    
    response = requests.get(url, headers=kanbanize_headers)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(
            f"Erro {response.status_code} ao consultar colunas do board {board_id}: {response.text}"
        )
        
def create_card(
    board_id: int,
    title: str,
    description: Optional[str] = None,
    column_id: Optional[int] = None,
    lane_id: Optional[int] = None,
    type_id: Optional[int] = None,
    assignee_user_ids: Optional[List[int]] = None,
    priority: Optional[str] = None,          # "low" | "average" | "high"
    tags: Optional[List[str]] = None,
    custom_fields: Optional[Dict[str, Any]] = None,
    external_link: Optional[str] = None,
    extra: Optional[Dict[str, Any]] = None,  # substitui **kwargs
) -> Dict[str, Any]:
    """
    Cria um card no Kanbanize (API v2).

    Parâmetros:
      - board_id: ID do board (obrigatório)
      - title: Título do card (obrigatório)
      - description: Descrição do card
      - column_id: ID da coluna
      - lane_id: ID da swimlane
      - type_id: Tipo do card
      - assignee_user_ids: IDs dos responsáveis
      - priority: Prioridade do card
      - tags: Lista de tags
      - custom_fields: Campos customizados (dict)
      - external_link: Link externo
      - extra: Dict com campos adicionais suportados pela API (e.g. section_id, template_id, color, deadline)

    Retorno:
      - dict com os dados do card criado ou dict de erro.
    """
    if not KANBANIZE_API_KEY:
        return {"error": "Kanbanize API Key não configurada no .env."}
    if not KANBANIZE_BASE_URL:
        return {"error": "KANBANIZE_BASE_URL não configurada no .env."}
    if not board_id or not title:
        return {"error": "Parâmetros obrigatórios ausentes: board_id e title."}

    api_url = f"{KANBANIZE_BASE_URL}/api/v2/cards"

    payload: Dict[str, Any] = {"board_id": board_id, "title": title}
    if description is not None:
        payload["description"] = description
    if column_id is not None:
        payload["column_id"] = column_id
    if lane_id is not None:
        payload["lane_id"] = lane_id
    if type_id is not None:
        payload["type_id"] = type_id
    if assignee_user_ids:
        payload["assignee_user_ids"] = assignee_user_ids
    if priority is not None:
        payload["priority"] = priority
    if tags:
        payload["tags"] = tags
    if custom_fields:
        payload["custom_fields"] = custom_fields
    if external_link:
        payload["external_link"] = external_link
    if extra:
        payload.update(extra)

    try:
        resp = requests.post(api_url, headers=kanbanize_headers, json=payload, timeout=30)
        resp.raise_for_status()
        raw = resp.json()
        data = raw.get("data") or raw
        return {"created": data}
    except requests.exceptions.HTTPError:
        try:
            details = resp.json()
        except ValueError:
            details = resp.text
        return {"error": "Erro HTTP ao criar card no Kanbanize.", "status_code": resp.status_code, "details": details}
    except requests.exceptions.RequestException as e:
        return {"error": f"Erro de conexão: {e}"}
