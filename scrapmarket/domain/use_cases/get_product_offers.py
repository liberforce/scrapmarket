import re
import sys
import time

from bs4 import BeautifulSoup
from scrapmarket.client import Client
from scrapmarket.domain.entities import products

from .common import HEADERS, PAYLOAD, SLEEP_TIME


def _get_product_offers_table(client: Client, text: str):
    soup = BeautifulSoup(text, features="html.parser")
    soup_rows = soup.find_all(id=re.compile(r"articleRow\d+"))

    rows = []
    for soup_row in soup_rows:
        row = soup_row.get_text(";").split(";")
        rows.append(row)

    return rows


def _interpret_product_offers_row(product_name: str, row: list) -> dict:
    fields = {}
    fields["sales"] = row.pop(0)

    if row[0] == "K":
        fields["powerseller"] = True
        row.pop(0)
    else:
        fields["powerseller"] = False

    fields["seller_name"] = row.pop(0)
    fields["grading"] = row.pop(0)
    assert fields["grading"] in [cc.name for cc in products.CardEntity.CardCondition]
    fields["quantity"] = int(row.pop(-1))
    price, currency = row.pop(-1).split(" ")
    fields["price"] = float(price.replace(",", "."))
    assert "€" in currency
    fields["currency"] = currency

    offer = {
        "seller": fields["seller_name"],
        "product_name": product_name,
        "grading": fields["grading"],
        "price": fields["price"],
        "currency": fields["currency"],
        "quantity": fields["quantity"],
    }

    return offer


def _interpret_product_offers_table(product_name: str, table: list[list]) -> list:
    offers: list = []
    for row in table:
        offer = _interpret_product_offers_row(product_name, row)
        offers.append(offer)

    return offers


def get_product_offers_use_case(
    client,
    product: products.ProductEntity,
):
    method = "GET"
    params = PAYLOAD.copy()
    # FIXME: foilness is only for card product types
    params["isFoil"] = "Y" if product.is_foil else "N"
    response = client.send_request(method, product.url, headers=HEADERS, params=params)

    if response.status_code != 200:
        raise Exception(f"{response.status_code}: {method} {product.url}")

    raw_product_offers_table = _get_product_offers_table(client, response.text)
    offers = _interpret_product_offers_table(
        product.name,
        raw_product_offers_table,
    )
    return offers


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
            multiproduct_offers.extend(product_offers)
            time.sleep(SLEEP_TIME)
    except Exception as exc:
        sys.exit(" ".join(exc.args))

    return multiproduct_offers
