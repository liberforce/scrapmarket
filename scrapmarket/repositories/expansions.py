from scrapmarket.domain.entities import Expansion, ExpansionId

EXPANSIONS = [
    {
        "id": ExpansionId.ONS,
    }
]


class ExpansionRepository:
    def __init__(self):
        self._expansions = {exp["id"]: Expansion(**exp) for exp in EXPANSIONS}

    def get_by_id(self, id: ExpansionId) -> Expansion | None:
        return self._expansions.get(id)

    def insert(self, expansion: Expansion) -> Expansion:
        if expansion.id not in self._expansions:
            self._expansions[expansion.id] = expansion
        return self._expansions

    def delete(self, expansion) -> None:
        del self._expansion[expansion.id]
