import ccxt


def order_book(source, symbol, depth=None, params=None):
    """Return the order book.

    :param source: Source, an Exchange API object.
    :param symbol: Symbol.
    :param depth: Depth of the order book.
    """
    exchange = getattr(ccxt, source.lower())()

    if depth is not None:
        raise ValueError("Sorry that currently depth is not supported.")

    return exchange.fetch_order_book(symbol=symbol, params=params or {})
