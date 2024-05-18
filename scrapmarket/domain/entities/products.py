from dataclasses import dataclass
from enum import Enum

from .expansions import ExpansionEntity
from .games import GameEntity


class ProductType(Enum):
    CARD = "Singles"
    BOOSTER = "Boosters"


@dataclass
class ProductEntity:
    # FIXME: find out how to declare a product type here so it's defined in child classes
    expansion: ExpansionEntity
    unsafe_name: str = ""
    game = None
    _name = None
    _url: str | None = None

    @property
    def escaped_type(self):
        return self.type_.value

    @property
    def name(self) -> str:
        if self._name is None:
            self._name = ProductEntity.normalize_name(self.unsafe_name)

        return self._name

    @property
    def url(self) -> str:
        if self._url is None:
            self._url = self.guess_url(self.game)

        return self._url

    @staticmethod
    def normalize_name(product_name: str):
        return product_name.title()

    @property
    def escaped_name(self):
        return self.name.replace(" ", "-")

    def guess_url(
        self,
        game: GameEntity | None = None,
    ) -> str:
        raise NotImplementedError


@dataclass
class CardEntity(ProductEntity):
    class CardCondition(Enum):
        MT = "Mint"
        NM = "Near Mint"
        EX = "Excellent"
        GD = "Good"
        LP = "Light Played"
        PL = "Played"
        PO = "Poor"

    condition: CardCondition | None = None
    is_foil: bool = False
    type = ProductType.CARD

    def guess_url(
        self,
        game: GameEntity | None = None,
    ) -> str:
        if game is None:
            game = GameEntity()

        return (
            f"https://www.cardmarket.com/en"
            f"/{game.name.value}"
            f"/Products"
            f"/{self.type.value}"
            f"/{self.expansion.escaped_name}"
            f"/{self.escaped_name}"
        )
