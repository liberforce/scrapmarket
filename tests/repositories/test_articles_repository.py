from scrapmarket.domain.entities import ArticleEntity
from scrapmarket.infrastructure.repositories import (
    ArticlesInMemoryRepository as ArticlesRepository,
)


def test_create():
    repo = ArticlesRepository()
    article = ArticleEntity(
        name="Questing Beast",
        price=1,
        currency="EUR",
        condition="NM",
        is_foil=False,
    )
    repo.set(1, article)
    assert repo.get_by_id(1) == article
