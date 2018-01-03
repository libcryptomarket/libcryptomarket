import pandas as pd


def order_book(source, symbol, depth=5):
    """Return the order book.

    :param source: Source, an Exchange API object.
    :param symbol: Symbol.
    :param depth: Depth of the order book.
    """
    source_name = source.__class__.__name__.lower().replace("api", "")

    if source_name == "poloniex":
        return _order_book_poloniex(source, symbol, depth)
    else:
        raise ValueError("Source (%s [%s]) does not support order book"
                         % (source, source_name))


def _order_book_poloniex(source, symbol, depth=5):
    """Return the order book from Poloniex

    :param source: Source, an Exchange API object.
    :param symbol: Symbol.
    :param depth: Depth of the order book.
    """
    if symbol == "all":
        raise ValueError("Currently not support all symbol order book query.")

    response = source.return_order_book(currencyPair=symbol, depth=depth)
    response.raise_for_status()
    data = response.json()
    data = [pd.DataFrame(
        data[side],
        columns=pd.MultiIndex.from_product(
            [[side], ['price', 'quantity']]),
        index=range(1, depth + 1)) for side in ['bids', 'asks']]
    data = pd.concat(data, axis=1).astype('float64')

    return data
