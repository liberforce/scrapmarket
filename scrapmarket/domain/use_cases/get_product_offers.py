import re
import sys
import time

from bs4 import BeautifulSoup
from scrapmarket.client import Client
from scrapmarket.domain.entities import products

from .common import HEADERS, PAYLOAD, SLEEP_TIME


def _get_product_table(client, url):
    method = "GET"
    result = client.send_request(method, url, headers=HEADERS, params=PAYLOAD)

    if result.status_code != 200:
        raise Exception(f"{result.status_code}: {method} {url}")

    with open("result.html", "w") as f:
        f.write(result.text)

    soup = BeautifulSoup(result.text, features="html.parser")
    soup_rows = soup.find_all(id=re.compile(r"articleRow\d+"))

    rows = []
    for soup_row in soup_rows:
        row = soup_row.get_text(";").split(";")
        rows.append(row)

    return rows


def _interpret_product_row(product_name: str, row: list) -> dict[str, list]:
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


def _interpret_product_table(product_name: str, table: list[list]) -> dict[str, list]:
    product_by_sellers: dict[str, list] = {}
    for row in table:
        product = _interpret_product_row(product_name, row)
        seller = list(product)[0]
        if seller in product_by_sellers:
            product_by_sellers[seller].extend(product[seller])
        else:
            product_by_sellers[seller] = product[seller]

    return product_by_sellers


def get_product_offers_use_case(
    client,
    product: products.ProductEntity,
):
    raw_product_table = _get_product_table(client, product.url)
    product_by_sellers = _interpret_product_table(
        product.name,
        raw_product_table,
    )
    return product_by_sellers


def get_multiproduct_offers_use_case(
    client: Client,
    products: list[products.ProductEntity],
) -> list:
    multiproduct_offers = []

    try:
        for product in products:
            product_offers = get_product_offers_use_case(
                client,
                product,
            )
            multiproduct_offers.append(product_offers)
            time.sleep(SLEEP_TIME)
    except Exception as exc:
        sys.exit(" ".join(exc.args))

    return multiproduct_offers
