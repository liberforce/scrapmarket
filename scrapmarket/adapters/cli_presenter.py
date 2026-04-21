import enum
import itertools
import json


class PresentationFormat(enum.Enum):
    JSON = "json"


def _take(n, iterable):
    return itertools.islice(iterable, n)


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
    }
    formats.setdefault(format_, _present_sellers_with_most_offers__json)(
        sellers_by_n_offers,
        top,
    )
