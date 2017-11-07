#!/bin/python
import requests
from datetime import datetime


TICKET_URL = "https://api.coinmarketcap.com/v1/ticker/"


class CoinMarketCapApiTicker:
    """Result class of query /ticker
    """

    def __init__(self, **kwargs):
        """Constructor.

        Constructed from the request result like the following
            {
                "id": "bitcoin",
                "name": "Bitcoin",
                "symbol": "BTC",
                "rank": "1",
                "price_usd": "573.137",
                "price_btc": "1.0"
                "24h_volume_usd": "72855700.0",
                "market_cap_usd": "9080883500.0",
                "available_supply": "15844176.0",
                "total_supply": "15844176.0",
                "percent_change_1h": "0.04",
                "percent_change_24h": "-0.3",
                "percent_change_7d": "-0.57",
                "last_updated": "1472762067"
            }
        """
        self.r_id = kwargs["id"]
        self.r_name = kwargs["name"]
        self.r_symbol = kwargs["symbol"]
        self.r_rank = int(kwargs["rank"] or '0')
        self.r_price_usd = float(kwargs["price_usd"] or '0')
        self.r_price_btc = float(kwargs["price_btc"] or '0')
        self.r_24h_volume_usd = float(kwargs["24h_volume_usd"] or '0')
        self.r_market_cap_usd = float(kwargs["market_cap_usd"] or '0')
        self.r_available_supply = float(kwargs["available_supply"] or '0')
        self.r_total_supply = float(kwargs["total_supply"] or '0')
        self.r_percent_change_1h = float(kwargs["percent_change_1h"] or '0')
        self.r_percent_change_24h = float(kwargs["percent_change_24h"] or '0')
        self.r_percent_change_7d = float(kwargs["percent_change_7d"] or '0')
        self.r_last_updated = datetime.fromtimestamp(
            int(kwargs["last_updated"]))


def get_ticker(coin=None):
    """Return the ticker of all coins or the particular coin.

    It returns a list of `CoinMarketCapApiTicker` objects.

    :param coin: Coin id. Default None which means all coins are
                 queued.
    """
    url = TICKET_URL

    if coin is not None:
        url += coin

    return requests.get(url).json()
