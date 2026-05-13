#! /bin/env python3
import argparse
import json
import logging
from pathlib import Path

import dotenv
from xdg_base_dirs import xdg_cache_home

from scrapmarket import use_cases
from scrapmarket.adapters.cli_presenter import (
    PresentationFormat,
    present_sellers_with_most_offers,
)
from scrapmarket.client import Client

logging.basicConfig(level=logging.INFO)


def get_cmdline_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "wishlist",
        help="The file containing the wished products",
    )
    parser.add_argument(
        "--force",
        "-f",
        help="Force refreshing the offers cache",
        default=False,
        dest="refresh",
        action="store_true",
    )
    parser.add_argument(
        "--output",
        "-o",
        help="Output format",
        default="table",
        dest="output_format",
        choices=list(i.value for i in PresentationFormat),
    )
    return parser.parse_args()


def get_multiproduct_offers(client, offers_file, wishlist) -> list:
    if not offers_file.exists():
        products = use_cases.search_products(client, wishlist, should_raise=True)
        assert all(products), products

        multiproduct_offers = use_cases.get_multiproduct_offers(client, products)

        with offers_file.open("w") as fp:
            json.dump(multiproduct_offers, fp, indent=4, sort_keys=True)
    else:
        with offers_file.open("r") as fp:
            multiproduct_offers = json.load(fp)

    return multiproduct_offers


def main():
    dotenv.load_dotenv()
    client = Client()
    args = get_cmdline_args()

    wishlist_file = Path(args.wishlist)

    with wishlist_file.open() as fp:
        wishlist = json.load(fp)

    offers_dir = Path(xdg_cache_home(), "scrapmarket", "offers")
    offers_dir.mkdir(parents=True, exist_ok=True)
    offers_file = offers_dir.joinpath(wishlist_file.name)

    if args.refresh:
        offers_file.unlink(missing_ok=True)

    multiproduct_offers = get_multiproduct_offers(client, offers_file, wishlist)

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

    sellers_by_n_offers = {}
    for seller, n_offers in n_offers_by_seller.items():
        sellers_by_n_offers.setdefault(n_offers, list()).append(seller)

    present_sellers_with_most_offers(
        sellers_by_n_offers,
        top,
        PresentationFormat(args.output_format),
    )


if __name__ == "__main__":
    main()
