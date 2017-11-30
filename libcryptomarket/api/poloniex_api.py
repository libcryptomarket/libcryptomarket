#!/bin/python
import requests
import hmac
import hashlib
import urllib
from functools import partial

from libcryptomarket.api.rest_api_connector import RestApiConnector
API_URL = "https://poloniex.com/public?command="
VALID_PERIODS = [300, 900, 1800, 7200, 14400, 86400]


def get_return_chart_data(currency_pair, period, start, end=None):
    """Return returnChartData.

    :param currency_pair: Currency pair. For example, BTC_XMR.
    :param period: Period. Valid values are 300, 900, 1800, 7200, 14400 and
                   86400.
    :param start: Start time in unix timestamp.
    :param end: End time in unix timestamp. Optional.
    """

    if period not in VALID_PERIODS:
        raise ValueError(
            "Period is not in the valid periods (%s)" % VALID_PERIODS)

    url = (API_URL + "returnChartData" +
           "&currencyPair={0}".format(currency_pair) +
           "&period={0}".format(period) +
           "&start={0}".format(start))

    if end is not None:
        url += "&end={0}".format(end)

    r = requests.get(url)
    r.raise_for_status()
    rjson = r.json()
    if isinstance(rjson, dict) and 'error' in rjson.keys():
        raise ValueError("Query error from Poloniex API ({0})".format(rjson))

    return r.json()


def get_return_order_book(currency_pair, depth=10):
    """Return returnOrderBook.

    :param currency_pair: Currency pair. Specify "all" if requesting for all
                          symbols.
    :param depth: Number of depth. Default is 10.
    """
    if currency_pair is None:
        raise ValueError("Currency pair cannot be None.")

    params = {}
    params["currencyPair"] = currency_pair
    params["depth"] = depth

    url = API_URL + "returnOrderBook"

    r = requests.get(url, params=params)
    r.raise_for_status()
    rjson = r.json()
    if isinstance(rjson, dict) and 'error' in rjson.keys():
        raise ValueError("Query error from Poloniex API ({0})".format(rjson))

    return r.json()


class PoloniexApi(RestApiConnector):
    """Poloniex API.
    """

    URL = 'https://poloniex.com/tradingApi'

    AVAILABLE_TRADING_API = [
        "returnBalances",
        "returnCompleteBalances",
        "returnDepositAddresses",
        "generateNewAddress",
        "returnDepositsWithdrawals",
        "returnOpenOrders",
        "returnTradeHistory",
        "returnOrderTrades",
        "buy",
        "sell",
        "cancelOrder",
        "moveOrder",
        "withdraw",
        "returnFeeInfo",
        "returnAvailableAccountBalances",
        "returnTradableBalances",
        "transferBalance",
        "returnMarginAccountSummary",
        "marginBuy",
        "marginSell",
        "getMarginPosition",
        "closeMarginPosition",
        "createLoanOffer",
        "cancelLoanOffer",
        "returnOpenLoanOffers",
        "returnActiveLoans",
        "returnLendingHistory",
        "toggleAutoRenew",
    ]

    def __init__(self, public_key, private_key, logger=None):
        """Constructor.

        :param public_key: Public key.
        :param private_key: Private key.
        """
        RestApiConnector.__init__(self, url=PoloniexApi.URL, logger=logger)

        self.__public_key = public_key
        self.__private_key = private_key

    def __getattr__(self, name):
        """Get attribute.
        """
        if name in PoloniexApi.AVAILABLE_TRADING_API:
            return partial(self._request, command=name, http_method="POST")
        else:
            raise AttributeError("Trading method ({0}) ".format(name) +
                                 "is not defined.")

    def _request(self, command, **kwargs):
        """Send request.

        :param kwargs: Named arguments.
        """
        kwargs["command"] = command
        kwargs["nonce"] = self._generate_nonce()

        return self._send_request(
            command="",
            http_method="POST",
            public_key=self.__public_key,
            private_key=self.__private_key,
            params=None,
            data=kwargs)

    def _generate_auth(self, public_key, private_key):
        """Generate authentication.

        :param public_key: Public key.
        :param private_key: Private key.
        """
        return None

    def _generate_headers(self, command, http_method, params, data,
                          public_key, private_key):
        """Generate headers.

        :param command: Command.
        :param http_method: HTTP method, for example GET.
        :param params: Parameters.
        :param data: Data.
        :param public_key: Public key.
        :param private_key: Private key.
        """
        signature = hmac.new(private_key.encode(),
                             urllib.parse.urlencode(data).encode(),
                             digestmod=hashlib.sha512).hexdigest()
        header = {
            'Key': public_key,
            'Sign': signature
        }

        return header

    def _format_data(self, data):
        """Format the data to exchange desirable format.

        :param data: Data.
        """
        if data is None:
            return ""
        else:
            return data
