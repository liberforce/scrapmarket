import time

from scrapmarket.client import Client
from scrapmarket.domain.entities import expansions, products
from scrapmarket.domain.entities.expansions import ExpansionId
from scrapmarket.infrastructure.repositories.expansions import \
    ExpansionRepository

from .common import HEADERS, SLEEP_TIME
from .errors import UnsupportedProductError


def search_product_use_case(
    client: Client,
    unsafe_product_name: str,
    expansion_id: expansions.ExpansionId,
    should_raise=False,
) -> products.ProductEntity | None:
    expansion_repo = ExpansionRepository()
    expansion = expansion_repo.get_by_id(expansion_id)
    product = products.ProductEntity(
        unsafe_name=unsafe_product_name,
        expansion=expansion,
    )
    # FIXME: should be web-agnostic
    method = "HEAD"
    result = client.send_request(method, product.url, headers=HEADERS)

    if result.status_code != 200:
        if should_raise:
            raise Exception(f"{result.status_code}: {method} {product.url}")
        else:
            return None

    return product


def search_card_use_case(
    client: Client,
    unsafe_product_name: str,
    expansion_id: expansions.ExpansionId,
    is_foil: bool = False,
    should_raise=False,
) -> products.ProductEntity | None:
    expansion_repo = ExpansionRepository()
    expansion = expansion_repo.get_by_id(expansion_id)
    product = products.CardEntity(
        unsafe_name=unsafe_product_name,
        expansion=expansion,
        is_foil=is_foil,
    )
    # FIXME: should be web-agnostic
    method = "HEAD"
    result = client.send_request(method, product.url, headers=HEADERS)

    if result.status_code != 200:
        if should_raise:
            raise Exception(f"{result.status_code}: {method} {product.url}")
        else:
            return None

    return product


def search_products_use_case(
    client: Client,
    products: list[dict],
    should_raise=False,
):
    product_entities = []

    for product in products:
        product_type = product.get("type", "card")

        if product_type == "card":
            product_name = product["name"]
            expansion_id = getattr(ExpansionId, product["expansion"])
            is_foil = product.get("foil", False)
            card_entity = search_card_use_case(
                client,
                product_name,
                expansion_id,
                is_foil=is_foil,
                should_raise=should_raise,
            )
        else:
            raise UnsupportedProductError(product_type)

        product_entities.append(card_entity)
        time.sleep(SLEEP_TIME)

    return product_entities
