import abc

from scrapmarket.domain.entities import ArticleEntity, ArticleId


class ArticlesRepository(abc.ABC):
    @abc.abstractmethod
    def get(self, id: ArticleId) -> ArticleEntity | None: ...

    @abc.abstractmethod
    def get_by_id(self, id) -> ArticleEntity: ...

    @abc.abstractmethod
    def set(self, id, value: ArticleEntity) -> None: ...
