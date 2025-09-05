from dataclasses import dataclass

from .products import ProductEntity


@dataclass
class OrderEntity:
    seller: str
    seller_country: str
    is_tracked: bool
    products: ProductEntity


@dataclass
class OrdersBatchEntity:
    orders: list[OrderEntity]
