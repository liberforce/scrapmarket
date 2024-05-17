#! /bin/env python3
import json
import logging
import os.path

import dotenv

from scrapmarket.client import Client
from scrapmarket.domain import use_cases

logging.basicConfig(level=logging.INFO)


def main():
    dotenv.load_dotenv()
    client = Client()

    if not os.path.exists("fastlands-offers.json"):
        with open("fastlands.json") as fp:
            products_data = json.load(fp)

        products = use_cases.search_products(client, products_data, should_raise=True)
        assert all(products), products

        multiproduct_offers = use_cases.get_multiproduct_offers(client, products)

        with open("fastlands-offers.json", "w") as fp:
            json.dump(multiproduct_offers, fp, indent=4, sort_keys=True)
    else:
        with open("fastlands-offers.json") as fp:
            multiproduct_offers = json.load(fp)

    offers_by_seller = {}
    for offer in multiproduct_offers:
        seller_name = offer["seller"]
        seller_offers = offers_by_seller.get(seller_name, list())
        seller_offers.append(offer)
        offers_by_seller[seller_name] = seller_offers

    n_offers_by_seller = {
        seller: len(seller_offers) for seller, seller_offers in offers_by_seller.items()
    }

    sellers_by_n_offers: dict[int, str] = {}
    for seller, n_offers in n_offers_by_seller.items():
        sellers = sellers_by_n_offers.get(n_offers, list())
        sellers.append(seller)
        sellers_by_n_offers[n_offers] = sellers

    print(json.dumps(sellers_by_n_offers, indent=4))


if __name__ == "__main__":
    main()
