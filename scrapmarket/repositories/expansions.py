from scrapmarket.domain.entities import Expansion, ExpansionId
import datetime

EXPANSIONS = [
    {
        "id": ExpansionId.ONS,
        "n_cards": 351,
        "release_date": "2002-10-07",
    }
]


class ExpansionRepository:
    def __init__(self):
        self._expansions = {
            exp["id"]: Expansion(
                id=exp["id"],
                n_cards=exp["n_cards"],
                release_date=datetime.date.fromisoformat(exp["release_date"]),
            )
            for exp in EXPANSIONS
        }

    def get_by_id(self, id: ExpansionId) -> Expansion | None:
        return self._expansions.get(id)

    def insert(self, expansion: Expansion) -> Expansion:
        if expansion.id not in self._expansions:
            self._expansions[expansion.id] = expansion
        return self._expansions

    def delete(self, expansion) -> None:
        del self._expansion[expansion.id]
