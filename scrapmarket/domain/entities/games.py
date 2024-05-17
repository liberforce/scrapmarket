from dataclasses import dataclass
from enum import Enum


@dataclass
class GameEntity:
    class Name(Enum):
        MAGIC = "Magic"

    name: Name = Name.MAGIC
