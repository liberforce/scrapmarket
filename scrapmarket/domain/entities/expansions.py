from enum import Enum
from dataclasses import dataclass


class ExpansionId(Enum):
    ONS = "Onslaught"


@dataclass
class Expansion:
    id: ExpansionId

    @property
    def name(self) -> str:
        return self.id.value
