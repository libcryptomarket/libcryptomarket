#!/bin/python
import requests
import hmac
import hashlib
import urllib
# from functools import partial

from libcryptomarket.api.exchange_api import ExchangeApi
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


class PoloniexApi(ExchangeApi):
    """Poloniex API.
    """

    def __init__(self, public_key=None, private_key=None, logger=None):
        """Constructor.

        :param public_key: Public key.
        :param private_key: Private key.
        :param logger: Logger.
        """
        ExchangeApi.__init__(self, public_key, private_key, logger)

    @classmethod
    def get_url(cls):
        """Get API url.
        """
        return None

    @classmethod
    def get_public_url(cls):
        """Get public API url.
        """
        return 'https://poloniex.com/public'

    @classmethod
    def get_private_url(cls):
        """Get private API url.
        """
        return 'https://poloniex.com/tradingApi'

    @classmethod
    def get_public_calls(cls):
        """Get public API calls.
        """
        return {
            "returnTicker": "GET",
            "return24Volume": "GET",
            "returnOrderBook": "GET",
            "returnTradeHistory": "GET",
            "returnChartData": "GET",
            "returnCurrencies": "GET",
            "returnTicker": "GET",
            "returnLoanOrders": "GET",
        }

    @classmethod
    def get_private_calls(cls):
        """Get public API calls.
        """
        return {
            "returnBalances": "POST",
            "returnCompleteBalances": "POST",
            "returnDepositAddresses": "POST",
            "generateNewAddress": "POST",
            "returnDepositsWithdrawals": "POST",
            "returnOpenOrders": "POST",
            "returnTradeHistory": "POST",
            "returnOrderTrades": "POST",
            "buy": "POST",
            "sell": "POST",
            "cancelOrder": "POST",
            "moveOrder": "POST",
            "withdraw": "POST",
            "returnFeeInfo": "POST",
            "returnAvailableAccountBalances": "POST",
            "returnTradableBalances": "POST",
            "transferBalance": "POST",
            "returnMarginAccountSummary": "POST",
            "marginBuy": "POST",
            "marginSell": "POST",
            "getMarginPosition": "POST",
            "closeMarginPosition": "POST",
            "createLoanOffer": "POST",
            "cancelLoanOffer": "POST",
            "returnOpenLoanOffers": "POST",
            "returnActiveLoans": "POST",
            "returnLendingHistory": "POST",
            "toggleAutoRenew": "POST"
        }

    @classmethod
    def translate_call_name(cls, name):
        """Translate API call name.

        The class method name is always underscored (aligned with Python
        standard.) This method is to translate underscored name to exchange
        API call name.

        :param name: Method name (underscored).
        """
        splitted_names = name.split('_')
        if len(splitted_names) > 1:
            splitted_names = ([splitted_names[0]] +
                              [n.title() for n in splitted_names[1:]])

        return ''.join(splitted_names)

    def _request_public(self, name, http_method, **kwargs):
        """Request public API call.

        :param name: Method name.
        :param http_method: HTTP method (POST, GET, DELETE).
        """
        kwargs['command'] = name

        return self._send_request(
            command=None, http_method=http_method, params=kwargs,
            public_method=True)

    def _request_private(self, name, http_method, **kwargs):
        """Request private API call.

        :param name: Method name.
        :param http_method: HTTP method (POST, GET, DELETE).
        """
        kwargs['command'] = name
        kwargs['nonce'] = self._generate_nonce()

        return self._send_request(
            command=None, http_method=http_method, params=None, data=kwargs)

    @classmethod
    def _generate_auth(cls, public_key, private_key):
        """Generate authentication.

        :param public_key: Public key.
        :param private_key: Private key.
        """
        return None

    @classmethod
    def _generate_headers(cls, command, http_method, params, data,
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

    @classmethod
    def _format_data(cls, data):
        """Format the data to exchange desirable format.

        :param data: Data.
        """
        return data
