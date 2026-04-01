import spacy
from spellchecker import SpellChecker

# ----- \\ -----
nlp = spacy.load("pt_core_news_sm")
spell_checker = SpellChecker(language="pt")

MIN_WORD_LENGTH = 4 
MAX_WORD_LENGTH = 8

# ----- \\ -----
def token_validation(token: spacy.tokens.Token) -> bool:
    if token.is_stop or not token.is_alpha:
        return False
    if len(token.text) < MIN_WORD_LENGTH or len(token.text) > MAX_WORD_LENGTH:
        return False
    
    # Verifica se a palavra está no dicionário português
    if token.text.lower() not in spell_checker:
        return False

    # Considera apenas substantivos, adjetivos e verbos no infinitivo
    if token.pos_ in {"NOUN", "PROPN", "ADJ"}:
        return True

    if token.pos_ == "VERB":
        return "Inf" in token.morph.get("VerbForm")

    return False

def extract_valuable_words(text: str) -> list[str]:
    """
    Este método é responsável por extrair as palavras de um texto, utilizando a biblioteca spaCy. 
    Ele aplica uma série de validações para garantir que as palavras extraídas sejam relevantes para o jogo, como:
        - Maior que {MIN_WORD_LENGTH} caracteres e menor que {MAX_WORD_LENGTH} caracteres
        - Não sejam stop words ou pontuações
        - Sejam substantivos, adjetivos ou verbos no infinitivo
    """
    doc = nlp(text)
    return [token.text for token in doc if token_validation(token)]
