#! /bin/env python3
from scrapmarket.domain import use_cases
from pprint import pprint
import dotenv
import logging
from scrapmarket.client import Client
import sys
from scrapmarket.infrastructure.repositories import ExpansionRepository


logging.basicConfig(level=logging.INFO)


def main():
    dotenv.load_dotenv()
    client = Client()
    product_name = "tribal golem"
    repo = ExpansionRepository()

    try:
        product_by_sellers = use_cases.get_product_offers(
            client,
            repo,
            product_name,
        )
    except Exception as exc:
        sys.exit(exc.message)

    pprint(product_by_sellers)


if __name__ == "__main__":
    main()
