#! /bin/env python3
from scrapmarket.domain import use_cases
from pprint import pprint
import dotenv
import logging
from scrapmarket.client import Client
import sys
from scrapmarket.infrastructure.repositories import ExpansionRepository
from scrapmarket.domain.entities.expansions import ExpansionId


logging.basicConfig(level=logging.INFO)


def main():
    dotenv.load_dotenv()
    client = Client()
    product_name = "blooming marsh"
    expansion_id = ExpansionId.OTJ

    try:
        product = use_cases.search_product(
            client,
            product_name,
            expansion_id,
            should_raise=True,
        )
        offers = use_cases.get_product_offers(
            client,
            product,
        )
    except Exception as exc:
        sys.exit(exc.message)

    pprint(offers)


if __name__ == "__main__":
    main()
