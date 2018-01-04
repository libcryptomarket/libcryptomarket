#!/bin/python
# import requests
# import hmac
# import hashlib
# import urllib
# from functools import partial

from libcryptomarket.api.exchange_api import ExchangeApi


class BitfinexApi(ExchangeApi):
    """Bitfinex API.
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
        return "https://api.bitfinex.com/v2"

    @classmethod
    def get_public_calls(cls):
        """Get public API calls.
        """
        return {
            'tickers': 'GET',
            'ticker': 'GET',
            'trades': 'GET',
            'book': 'GET',
            'stat1': 'GET',
            'candles': 'GET'
        }

    @classmethod
    def get_private_calls(cls):
        """Get public API calls.
        """
        return {}

    @classmethod
    def translate_call_name(cls, name):
        """Translate API call name.

        The class method name is always underscored (aligned with Python
        standard.) This method is to translate underscored name to exchange
        API call name.

        :param name: Method name (underscored).
        """
        return name

    def _request_public(self, name, http_method, **kwargs):
        """Request public API call.

        :param name: Method name.
        :param http_method: HTTP method (POST, GET, DELETE).
        """
        if name == "ticker":
            symbol = kwargs["symbol"]
            del kwargs["symbol"]
            name = '/'.join([name, symbol])
        elif name == "trades":
            symbol = kwargs["symbol"]
            del kwargs["symbol"]
            name = '/'.join([name, symbol, "hist"])
        elif name == "book":
            symbol = kwargs["symbol"]
            precision = kwargs["precision"]
            del kwargs["symbol"]
            del kwargs["precision"]
            name = "/".join([name, symbol, precision])
        elif name == "stat1":
            key = kwargs["key"]
            size = kwargs["size"]
            symbol = kwargs["symbol"]
            section = kwargs["section"]
            del kwargs["key"]
            del kwargs["size"]
            del kwargs["symbol"]
            del kwargs["section"]
            name = "/".join([name,
                             "{}:{}:{}".format(key, size, symbol),
                             section])
        elif name == "candles":
            timeframe = kwargs["timeframe"]
            symbol = kwargs["symbol"]
            section = kwargs["section"]
            del kwargs["timeframe"]
            del kwargs["symbol"]
            del kwargs["section"]
            name = "/".join([name,
                             "trade:{}:{}".format(timeframe, symbol),
                             section])

        self.log_info("Public request:\n" +
                      "name: {}\n".format(name) +
                      "http_method: {}\n".format(http_method) +
                      "kwargs: {}".format(kwargs))

        return self._send_request(
            command=name, http_method=http_method,
            public_method=True, params=kwargs)

    def _request_private(self, name, http_method, **kwargs):
        """Request private API call.

        :param name: Method name.
        :param http_method: HTTP method (POST, GET, DELETE).
        """
        raise NotImplementedError("Not support private api at this moment.")

    # @classmethod
    # def _generate_auth(cls, public_key, private_key):
    #     """Generate authentication.

    #     :param public_key: Public key.
    #     :param private_key: Private key.
    #     """
    #     return None

    # @classmethod
    # def _generate_headers(cls, command, http_method, params, data,
    #                       public_key, private_key):
    #     """Generate headers.

    #     :param command: Command.
    #     :param http_method: HTTP method, for example GET.
    #     :param params: Parameters.
    #     :param data: Data.
    #     :param public_key: Public key.
    #     :param private_key: Private key.
    #     """
    #     signature = hmac.new(private_key.encode(),
    #                          urllib.parse.urlencode(data).encode(),
    #                          digestmod=hashlib.sha512).hexdigest()
    #     header = {
    #         'Key': public_key,
    #         'Sign': signature
    #     }

    #     return header

    # @classmethod
    # def _format_data(cls, data):
    #     """Format the data to exchange desirable format.

    #     :param data: Data.
    #     """
    #     return data
