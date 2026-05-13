from scrapmarket.domain.entities import ArticleEntity, ArticleId
from scrapmarket.domain.repositories import ArticlesRepository


class ArticlesInMemoryRepository(ArticlesRepository):
    def __init__(self):
        self._offers = {}

    def get(self, id: ArticleId) -> ArticleEntity | None:
        return self._offers.get(id)

    def get_by_id(self, id: ArticleId) -> ArticleEntity:
        return self._offers[id]

    def set(self, id: ArticleId, value: ArticleEntity) -> None:
        self._offers[id] = value
