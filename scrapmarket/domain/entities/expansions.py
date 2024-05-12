from enum import Enum
from dataclasses import dataclass
import datetime


class ExpansionId(Enum):
    ONS = "Onslaught"


@dataclass
class Expansion:
    # Id of the expansion set
    id: ExpansionId

    # Full name of the expansion set
    @property
    def name(self) -> str:
        return self.id.value

    # Number of cards
    n_cards: int

    # Original release date
    release_date: datetime.date
