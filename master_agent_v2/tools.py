import requests
from typing import Dict, Any

BCB_BASE_URL = "https://www.bcb.gov.br"

def search_bcb_content(
    querytext: str,
    rowlimit: int = 10,
    startrow: int = 0,
    timeout_seconds: int = 20,
) -> Dict[str, Any]:
    """
    Consulta a API de busca do site do Banco Central do Brasil.

    Parâmetros:
      - querytext: Texto a ser pesquisado (obrigatório).
      - rowlimit: Máximo de resultados retornados (default=10).
      - startrow: Offset inicial/paginação (default=0).
      - timeout_seconds: Timeout da requisição em segundos (default=20).

    Retorno:
      - dict com o JSON da API, incluindo chaves como:
        TotalRows, RowCount, Rows (lista com Url, HitHighlightedSummary, Title, LastModifiedTime, ContentType, RowNumber), ExecutionTime

    Exceções:
      - Levanta Exception com detalhes em caso de erro HTTP ou de conexão.
    """
    if not querytext or not isinstance(querytext, str):
        raise ValueError("querytext é obrigatório e deve ser string.")

    endpoint = f"{BCB_BASE_URL.rstrip('/')}/api/search/sitebcb/buscaconteudo/todos/"
    params = {
        "querytext": querytext,
        "rowlimit": rowlimit,
        "startrow": startrow,
    }

    try:
        resp = requests.get(endpoint, params=params, timeout=timeout_seconds)
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.HTTPError as e:
        # Tenta extrair JSON de erro se existir; senão, texto cru
        try:
            details = resp.json()
        except Exception:
            details = resp.text
        raise Exception(
            f"Erro HTTP {resp.status_code} ao consultar a busca do BCB: {details}"
        ) from e
    except requests.exceptions.RequestException as e:
        raise Exception(f"Erro de conexão ao acessar a API do BCB: {e}") from e