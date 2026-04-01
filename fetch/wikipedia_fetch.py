from algs.seed import get_seed
import requests
import urllib.parse


# ----- \\ -----
TO_FILTER_URL="https://pt.wikipedia.org/w/api.php"
TO_SUMMARY_URL="https://pt.wikipedia.org/api/rest_v1/page/summary"
CATEGORIES = ["Arte", "Biologia", "Ciência", "Filosofia", "Física", "Geografia", "História", "Matemática", "Química"]

HEADERS = {
    'User-Agent': 'CacaPalavra/1.0'
}

MIN_WORDS = 50
MAX_WORDS = 100

# ----- \\ -----
def fetch_wikipedia(category: str) -> list[dict]:
    """ Este método é responsável por buscar o endpoint da Wikipedia, aplicando filtros de categoria. """
    response = requests.get(TO_FILTER_URL, headers=HEADERS, params={
        "action": "query",
        "list": "categorymembers",
        "cmtitle": "Categoria:{}".format(category),
        "format": "json",
    })
    
    try:
        response_json = response.json()
    except requests.exceptions.JSONDecodeError:
        raise Exception(f"❌ ERROR: Wikipedia rejected the request for category '{category}'!")
    
    titles = [item["title"] for item in response_json["query"]["categorymembers"]]
    return titles


def get_valid_article(seed: int, filtered_titles: list) -> dict:
    for offset in range(20):
        # A cada tentativa, calculamos um índice diferente para acessar os títulos, garantindo uma seleção mais variada.
        current_index = (seed + offset) % len(filtered_titles)
        candidate_title = filtered_titles[current_index]
        
        # Requisição
        safe_title = urllib.parse.quote(candidate_title.replace(" ", "_"))
        response = requests.get(f"{TO_SUMMARY_URL}/{safe_title}", headers=HEADERS)
        try:
            summary_data = response.json()
        except requests.exceptions.JSONDecodeError:
            continue
        
        # Validações Gerais
        if summary_data.get("type") != "standard":
            print(f"Skipping {candidate_title}: Not a standard article.")
            continue
        
        extract_text = summary_data.get("extract", "")
        if not extract_text:
            print(f"Skipping {candidate_title}: Empty extract.")
            continue

        word_count = len(extract_text.split())
        if word_count < MIN_WORDS or word_count > MAX_WORDS:
            print(f"Skipping {candidate_title}: Too short ({word_count} words).")
            continue
            
        return summary_data

def get_category(seed: int, _list: list) -> str:
    """ Este método é responsável por selecionar uma categoria aleatória da lista de categorias. """
    return _list[seed % len(_list)]


def get_summary() -> tuple[list[dict], str]:
    """
    Busca o resumo do artigo do Wikipedia para o dia.
    Este método é responsável por buscar o endpoint de resumo, passando o texto, 
    o tema e as palavras-destaque.
    Returns:
        tuple[list[dict], str]: Uma tupla contendo:
            - list[dict]: Lista de dicionários com o resumo do artigo válido
            - str: Categoria do dia selecionada
    """
    seed = get_seed()
    today_category = get_category(seed, CATEGORIES)

    all_filtered_titles = fetch_wikipedia(today_category)
    today_summary = get_valid_article(seed, all_filtered_titles)

    return today_summary, today_category