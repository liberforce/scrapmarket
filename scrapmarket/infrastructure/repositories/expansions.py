import datetime

from scrapmarket.domain.entities import ExpansionEntity, ExpansionId

EXPANSIONS = [
    {
        "id": ExpansionId.ONS,
        "n_cards": 351,
        "release_date": "2002-10-07",
    },
    {
        "id": ExpansionId.OTJ,
        "n_cards": 374,
        "release_date": "2024-04-19",
    },
    {
        "id": ExpansionId.ONE,
        "n_cards": 479,
        "release_date": "2023-02-03",
    },
]


class ExpansionRepository:
    def __init__(self):
        self._expansions = {
            exp["id"]: ExpansionEntity(
                id=exp["id"],
                n_cards=exp["n_cards"],
                release_date=datetime.date.fromisoformat(exp["release_date"]),
            )
            for exp in EXPANSIONS
        }

    def get_by_id(self, id: ExpansionId) -> ExpansionEntity | None:
        return self._expansions.get(id)

    def insert(self, expansion: ExpansionEntity) -> ExpansionEntity:
        if expansion.id not in self._expansions:
            self._expansions[expansion.id] = expansion
        return self._expansions

    def delete(self, expansion) -> None:
        del self._expansions[expansion.id]
