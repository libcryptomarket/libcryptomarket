#!/bin/python
import requests
from datetime import datetime
import logging

API_URL = "https://min-api.cryptocompare.com/data/"
MAX_QUERY_LIMIT = 2000

logger = logging.getLogger(__name__)


class CryptocompareCoinlist:
    """Cryptocompare coinlist.
    """

    def __init__(self, **kwargs):
        """Constructor.
        """
        self.r_algorithm = kwargs['Algorithm'].replace('N/A', '') or ''
        self.r_coinname = kwargs['CoinName'] or ''
        self.r_fullname = kwargs['FullName'] or ''
        self.r_fullypremined = int(kwargs['FullyPremined'].replace('N/A', '')
                                   or 0)
        self.r_id = kwargs['Id'] or ''
        self.r_imageurl = kwargs.get('ImageUrl', '') or ''
        self.r_name = kwargs['Name'] or ''
        self.r_preminedvalue = float(kwargs['PreMinedValue'].replace('N/A', '')
                                     or '0')
        self.r_prooftype = kwargs['ProofType'].replace('N/A', '') or ''
        self.r_sortorder = int(kwargs['SortOrder'].replace('N/A', '') or '0')
        self.r_sponsored = kwargs['Sponsored'] or False
        self.r_symbol = kwargs['Symbol'] or ''
        # TotalCoinSupply and TotalCoinsFreeFloat are not supported due to
        # very dirty data.
        self.r_url = kwargs['Url'] or ''


class CryptocompareHisto:
    """Cryptocompare histo.
    """

    def __init__(self, **kwargs):
        """Constructor.
        """
        self.r_close = float(kwargs['close'])
        self.r_high = float(kwargs['high'])
        self.r_low = float(kwargs['low'])
        self.r_open = float(kwargs['open'])
        self.r_time = datetime.fromtimestamp(int(kwargs['time']))
        self.r_volumefrom = float(kwargs['volumefrom'])
        self.r_volumeto = float(kwargs['volumeto'])


def get_coinlist():
    """Return general info for all coins available.
    """
    url = API_URL + "all/coinlist"

    r = requests.get(url)
    r.raise_for_status()
    return r.json()


def get_histo(period, fsym, tsym, e, limit=None, toTs=None):
    """Return historical prices.

    :param period: Period, one of the values of "minute", "hour" and "day".
    :param fsym: From symbol.
    :param tsym: To symbol.
    :param e: Exchange name.
    :param limit: Limit of return data. Default is None.
    :param toTs: To timestamp. Default is None.
    """
    valid_list = ["minute", "hour", "day"]
    if period not in valid_list:
        raise ValueError("Period must be in {0}".format(', '.join(valid_list)))

    url = API_URL + "histo" + period
    params = {
        "fsym": fsym,
        "tsym": tsym,
        "e": e
    }

    if limit is not None:
        params["limit"] = limit

    if toTs is not None:
        params["toTs"] = toTs

    r = requests.get(url, params=params)

    # Raise html error status
    r.raise_for_status()

    # The api raises a 200 for a warning, but passes a message
    rjson = r.json()
    if rjson.get("Message", None):
        logger.warning(
            'api returned message %r, for url %r',
            rjson["Message"],
            r.url)

    return rjson
