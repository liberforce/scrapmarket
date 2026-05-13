from dataclasses import dataclass


ArticleId = int

@dataclass
class ArticleEntity:
    name: str
    price: float
    currency: str
    condition: str
    is_foil: bool = False
