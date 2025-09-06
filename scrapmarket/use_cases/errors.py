class ProductError(Exception):
    pass


class UnsupportedProductError(ProductError):
    pass


class ExpansionError(Exception):
    pass


class ExpansionNotFoundError(ExpansionError):
    pass
