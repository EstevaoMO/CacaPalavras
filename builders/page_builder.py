from schemas.schemas import WordSearchBase

def highlight_featured_words(text: str, featured_words: list[str]) -> str:
    """Destaca as palavras no texto (em negrito e maiúsculas) apenas na primeira ocorrência. """
    import re
    highlighted_text = text
    highlighted_count = {word.lower(): 0 for word in featured_words}
    
    def replace_first(match):
        word = match.group(0)
        if highlighted_count[word.lower()] == 0:
            highlighted_count[word.lower()] += 1
            return f'<b>{word.upper()}</b>'
        return word
    
    for word in featured_words:
        highlighted_text = re.sub(
            r'\b' + re.escape(word) + r'\b',
            replace_first, 
            highlighted_text,
            flags=re.IGNORECASE
        )
    return highlighted_text


def _create_page(wordsearch: WordSearchBase):
    highlighted_text = highlight_featured_words(wordsearch.raw_text, wordsearch.featured_words)
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(f"""
<!DOCTYPE html>
<html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Caça-Palavras: {wordsearch.theme}</title>
        <link rel="stylesheet" type="text/css" href="style.css">
    </head>
    <body>
        <div class="container">
            <span class="badge">Tema do Dia</span>
            
            <h1>{wordsearch.theme}</h1>
            
            <div class="content-wrapper">
                <img src="{wordsearch.img_url}" alt="{wordsearch.theme}" class="featured-image">
                
                <div class="text-content">
                    <p>{highlighted_text}</p>
                </div>
            </div>
            <a href="{wordsearch.page_url}" class="button" target="_blank">Ler artigo completo</a>
        </div>
    </body>
</html>
        """)