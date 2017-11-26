import pandas as pd


def get_order_book(source, symbol, depth=5):
    """Return the order book.

    :param source: Data source name.
    :param symbol: Symbol.
    :param depth: Depth of the order book.
    """
    source = source.lower()

    if source == 'poloniex':
        from libcryptomarket.api.poloniex_api import get_return_order_book

        # Get the raw data
        symbol = symbol.replace("/", "_")
        data = get_return_order_book(currency_pair=symbol, depth=depth)

        # Align the format as symbol="all"
        if symbol == "all":
            # Convert it into a multiindex dataframe with symbol at the first
            # level of the columns
            data = [[pd.DataFrame(
                data[symbol][side],
                columns=pd.MultiIndex.from_product(
                    [[symbol], [side], ['price', 'quantity']]),
                index=range(1, depth + 1)) for side in ['bids', 'asks']]
                for symbol, prices in data.items()]
            data = pd.concat(sum(data, []), axis=1)
        else:
            # Convert it into a dataframe where bid and ask at the columns
            data = [pd.DataFrame(
                data[side],
                columns=pd.MultiIndex.from_product(
                    [[side], ['price', 'quantity']]),
                index=range(1, depth + 1)) for side in ['bids', 'asks']]
            data = pd.concat(data, axis=1)

        return data.astype('float64')
    else:
        raise ValueError("Source ({0}) is not yet implemented.".format(
                         source))
