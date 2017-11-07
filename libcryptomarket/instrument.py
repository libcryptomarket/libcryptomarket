import pandas as pd

from libcryptomarket.api.coinmarketcap_api import get_ticker


def get_instruments():
    """Return all the instruments.
    """
    result = get_ticker()
    result = pd.DataFrame([r.__dict__ for r in result])
    
    return result