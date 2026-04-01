import random

from algs.word_extractor import extract_valuable_words
from fetch.wikipedia_fetch import get_summary
from builders.page_builder import _create_page
from schemas.schemas import WordSearchBase

# ----- \\ -----
def _construct_base(summary: list[dict], category: str) -> WordSearchBase:
    """ Este método é responsável por construir o objeto WordSearchBase, a partir do resumo obtido da Wikipedia. """
    words = extract_valuable_words(summary.get("extract"))
    return WordSearchBase(
        raw_text=summary.get("extract"),
        html_text=summary.get("extract_html", ""),
        theme=category,
        featured_words=random.sample(words, min(8, len(words))),
        page_url=summary.get("content_urls", {}).get("desktop", {}).get("page", ""),
        img_url=summary.get("thumbnail", {}).get("source")
    )

# PARA FINS DE DEBUG, SALVAR O RESUMO OBTIDO DA WIKIPEDIA
# def _save(today_summary: list[dict]):
#     with open("summary.json", "w", encoding="utf-8") as f:
#         f.write(str(today_summary))

# ----- \\ -----
def main():
    today_summary, category = get_summary()
    # _save(today_summary)

    wordsearch = _construct_base(today_summary, category)
    _create_page(wordsearch)

if __name__ == "__main__":
    main()