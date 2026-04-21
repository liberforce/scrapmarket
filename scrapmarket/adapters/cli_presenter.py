import enum
import itertools
import json

import tabulate


class PresentationFormat(enum.Enum):
    JSON = "json"
    TABLE = "table"


def _take(n, iterable):
    return itertools.islice(iterable, n)


def _present_sellers_with_most_offers__table(
    sellers_by_n_offers: dict[int, str],
    top: int,
) -> None:
    print("# Sellers with the most offers:")
    data = dict(_take(top, sellers_by_n_offers.items()))
    table_data = [
        [n_offers, seller] for n_offers, sellers in data.items() for seller in sellers
    ]
    table = tabulate.tabulate(
        table_data,
        headers=("n_offers", "seller"),
        tablefmt="fancy_grid",
        stralign="center",
        colalign=("center", "left"),
    )
    print(table)


def _present_sellers_with_most_offers__json(
    sellers_by_n_offers: dict[int, str],
    top: int,
) -> None:
    print(f"# Top {top} Sellers with the most offers:")
    print(json.dumps(dict(_take(top, sellers_by_n_offers.items())), indent=4))


def present_sellers_with_most_offers(
    sellers_by_n_offers: dict[int, str],
    top: int,
    format_: PresentationFormat,
) -> None:
    formats = {
        PresentationFormat.JSON: _present_sellers_with_most_offers__json,
        PresentationFormat.TABLE: _present_sellers_with_most_offers__table,
    }
    formats.setdefault(format_, _present_sellers_with_most_offers__json)(
        sellers_by_n_offers,
        top,
    )
