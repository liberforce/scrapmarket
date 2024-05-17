import datetime
from dataclasses import dataclass
from enum import Enum


class ExpansionId(Enum):
    ONS = "Onslaught"
    OTJ = "Outlaws of Thunder Junction"
    ONE = "Phyrexia: All Will Be One"


@dataclass
class ExpansionEntity:
    # Id of the expansion set
    id: ExpansionId

    # Full name of the expansion set
    @property
    def name(self) -> str:
        return self.id.value

    # Full name suitable for urls
    @property
    def escaped_name(self) -> str:
        translation_table = str.maketrans(
            {
                " ": "-",
                ":": "-",
            }
        )
        return self.name.translate(translation_table).replace("--", "-")

    # Number of cards
    n_cards: int

    # Original release date
    release_date: datetime.date
