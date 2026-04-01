from pydantic import BaseModel

class WordSearchBase(BaseModel):
    theme: str
    raw_text: str
    html_text: str
    featured_words: list[str]
    page_url: str
    img_url: str | None = None
