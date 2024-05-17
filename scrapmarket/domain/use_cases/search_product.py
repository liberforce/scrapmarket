from scrapmarket.domain.entities import products, expansions
from scrapmarket.infrastructure.repositories.expansions import ExpansionRepository
from .common import HEADERS


def search_product_use_case(
    client,
    unsafe_product_name: str,
    expansion_repo: ExpansionRepository,
    expansion_id: expansions.ExpansionId = None,
    should_raise=False,
) -> products.ProductEntity | None:
    expansion = expansion_repo.get_by_id(expansion_id)
    product = products.ProductEntity(
        type=products.ProductType.CARD,
        unsafe_name=unsafe_product_name,
        expansion=expansion,
    )
    method = "HEAD"
    result = client.send_request(method, product.url, headers=HEADERS)

    if result.status_code != 200:
        if should_raise:
            raise Exception(f"{result.status_code}: {method} {product.url}")
        else:
            return None

    return product
