import pandas as pd


def get_instruments(source='coinmarketcap', **kwargs):
    """Return all the instruments.
    """
    if source == 'coinmarketcap':
        # Coinmarketcap
        from libcryptomarket.api.coinmarketcap_api import (
            get_ticker, CoinMarketCapApiTicker)

        result = get_ticker(**kwargs)
        result = [CoinMarketCapApiTicker(**e) for e in result]
    elif source == 'cryptocompare':
        # Cryptocompare
        from libcryptomarket.api.cryptocompare_api import (
            get_coinlist, CryptocompareCoinlist)

        result = get_coinlist(**kwargs)
        result = [CryptocompareCoinlist(**value)
                  for key, value in result['Data'].items()]
    else:
        raise ValueError("No source is called {0}".format(source))

    result = pd.DataFrame([r.__dict__ for r in result])
    return result
