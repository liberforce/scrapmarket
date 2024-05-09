from dataclasses import dataclass

from enum import Enum


@dataclass
class Game:
    class Name(Enum):
        MAGIC = "Magic"

    name: Name = Name.MAGIC
