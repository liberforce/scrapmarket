#! /bin/env python3
import json
import logging

import dotenv

from scrapmarket.client import Client
from scrapmarket.domain import use_cases

logging.basicConfig(level=logging.INFO)


def main():
    dotenv.load_dotenv()
    client = Client()

    with open("fastlands.json") as fp:
        products_data = json.load(fp)

    products = use_cases.search_products(client, products_data)
    assert all(products), products

    multiproduct_offers = use_cases.get_multiproduct_offers(client, products)

    with open("fastlands-offers.json", "w") as fp:
        json.dump(multiproduct_offers, fp)


if __name__ == "__main__":
    main()
