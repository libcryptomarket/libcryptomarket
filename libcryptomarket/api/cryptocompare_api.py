#!/bin/python
import requests

API_URL = "https://www.cryptocompare.com/api/data/"


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


def get_coinlist():
    """Return general info for all coins available.
    """
    url = API_URL + "coinlist"

    return requests.get(url).json()
