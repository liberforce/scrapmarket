#! /bin/env python3
import json
import logging
import os.path
from itertools import islice

import dotenv

from scrapmarket.client import Client
from scrapmarket.domain import use_cases

logging.basicConfig(level=logging.INFO)


def take(n, iterable):
    return islice(iterable, n)


def main():
    dotenv.load_dotenv()
    client = Client()
    products = []

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

    # Get offers for each product, sorted by best offer
    offers_by_product = {}
    for offer in multiproduct_offers:
        offers_by_product.setdefault(offer["product_name"], list()).append(offer)

    offers_by_product = {
        product_name: sorted(offers, key=lambda x: x["price"])
        for product_name, offers in offers_by_product.items()
    }

    # Get offers for each seller
    offers_by_seller = {}
    for offer in multiproduct_offers:
        offers_by_seller.setdefault(offer["seller"], list()).append(offer)

    # Get the number of offers for each seller
    # FIXME: take into account card quantity
    n_offers_by_seller = {
        seller: len(seller_offers) for seller, seller_offers in offers_by_seller.items()
    }

    # Get the sellers with the most offers
    # FIXME: take into account card quantity
    sellers_by_n_offers = {}
    for seller, n_offers in n_offers_by_seller.items():
        sellers_by_n_offers.setdefault(n_offers, list()).append(seller)

    sellers_by_n_offers = dict(sorted(sellers_by_n_offers.items(), reverse=True))

    top = 5
    print(f"# Top {top} Sellers with the most offers:")
    print(json.dumps(dict(take(top, sellers_by_n_offers.items())), indent=4))

    sellers_by_n_offers: dict[int, str] = {}
    for seller, n_offers in n_offers_by_seller.items():
        sellers_by_n_offers.setdefault(n_offers, list()).append(seller)

    # print(json.dumps(sellers_by_n_offers, indent=4))


if __name__ == "__main__":
    main()
