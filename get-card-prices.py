#! /bin/env python3
from pprint import pprint
import re
import dotenv
import logging
import sys
from scrapmarket.client import Client
from scrapmarket.entities import products, games, sets

from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO)


def normalize_mtg_set(setname):
    pass


def is_article_row(tag) -> bool:
    return tag.has_attr("id") and tag.get("id").startswith("articleRow")


def get_product_table(client, url):
    method = "GET"
    payload = {"sellerCountry": 12, "language": 2, "minCondition": 2}
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "fr-FR,fr;q=0.8,en-US;q=0.5,en;q=0.3",
        # "Accept-Encoding": "gzip, deflate, br",
        "Accept-Encoding": "text",
        "Referer": "https://www.cardmarket.com/en/Magic/Products/Singles/Onslaught/Tribal-Golem?sellerCountry=12&language=2&minCondition=2",
        "DNT": "1",
        "Connection": "keep-alive",
        "Cookie": "cf_clearance=3GmL3uJX9q2JxTZEOZOwVKm.WqKFJquyd0GbJbGhK98-1713021396-1.0.1.1-Uc33WFLb4B8Wf7l01LpeDCTJy9uvWyqgnHi84PX0Eume9DbXKtAXdAMggjiPC41SBasSb1a5WSrpFpoX6uTGOA; _cfuvid=AGZW3RgNz11Fz6w7jhmoJuXm6Sc_hDQtOAfr0xBjKZg-1715295882066-0.0.1.1-604800000; PHPSESSID=mk12v0lc913ragbsc7rteakde8; __cf_bm=thQ5VwZLoS9psGrWHz7n9V.Dy_AVul_rsmDxq1ZFVus-1715297619-1.0.1.1-Rwdpl7jktiDY1woRThlNfT16TO4CPr7RNhbKLs8rh4x4kDYePYa1OxB03eQUWOrfTRSeCtdHzUmzfXm0vDNPlA",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "TE": "trailers",
    }
    result = client.send_request(method, url, headers=headers, params=payload)

    if result.status_code != 200:
        sys.exit(f"{result.status_code}: {method} {url}")

    with open("result.html", "w") as f:
        f.write(result.text)

    soup = BeautifulSoup(result.text, features="html.parser")
    soup_rows = soup.find_all(id=re.compile(r"articleRow\d+"))

    rows = []
    for soup_row in soup_rows:
        row = soup_row.get_text(";").split(";")
        rows.append(row)

    return rows


def interpret_product_row(product_name: str, row: list) -> dict[str, list]:
    fields = {}
    fields["sales"] = row.pop(0)

    if row[0] == "K":
        fields["powerseller"] = True
        row.pop(0)
    else:
        fields["powerseller"] = False

    fields["seller_name"] = row.pop(0)
    fields["grading"] = row.pop(0)
    assert fields["grading"] in ("MT", "NM", "EX", "GD", "LP", "PL", "PO")
    fields["quantity"] = row.pop(-1)
    assert fields["quantity"].isdigit()
    fields["price"] = row.pop(-1)
    assert "€" in fields["price"]

    seller = {
        "name": fields["seller_name"],
        "sales": fields["sales"],
    }
    offers = [
        {
            "product_name": product_name,
            "grading": fields["grading"],
            "price": fields["price"],
            "quantity": fields["quantity"],
        }
    ]
    return {seller["name"]: offers}


def interpret_product_table(product_name: str, table: list[list]) -> dict[dict, list]:
    product_by_sellers = {}
    for row in table:
        product = interpret_product_row(product_name, row)
        seller = list(product)[0]
        if seller in product_by_sellers:
            product_by_sellers[seller].extend(product[seller])
        else:
            product_by_sellers[seller] = product[seller]

    return product_by_sellers


def normalize_product_name(product_name: str):
    return product_name.title().replace(" ", "-")


def get_product_url(
    product_type: products.ProductType,
    product_name: str,
    set_id: sets.MtgSetId,  # FIXME
    game: games.Game | None = None,
) -> str:
    if game is None:
        game = games.Game()

    if product_type == products.ProductType.CARD:
        return (
            f"https://www.cardmarket.com/en"
            f"/{game.name.value}"
            f"/Products"
            f"/{product_type.value}"
            f"/{set_id.value}"
            f"/{normalize_product_name(product_name)}"
        )

    raise Exception  # TODO: customize exceptions


def main():
    dotenv.load_dotenv()
    client = Client()
    product_name = "tribal golem"
    url = get_product_url(
        products.ProductType.CARD,
        product_name=product_name,  # TODO: use a dataclass with properties to normalize
        set_id=sets.MtgSetId.ONS,
    )
    raw_product_table = get_product_table(client, url)
    product_by_sellers = interpret_product_table(
        normalize_product_name(product_name),
        raw_product_table,
    )
    pprint(product_by_sellers)


if __name__ == "__main__":
    main()
