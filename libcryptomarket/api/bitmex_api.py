#!/bin/python
from libcryptomarket.api.exchange_api import ExchangeApi


class BitmexApi(ExchangeApi):
    """BitMEX API connector.
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
        return 'https://www.bitmex.com/api/v1/'

    @classmethod
    def get_public_calls(cls):
        """Get public API calls.
        """
        return {
            "funding": "GET",
            "instrument": "GET",
            "instrument/active": "GET",
            "instrument/activeAndIndices": "GET",
            "instrument/activeIntervals": "GET",
            "instrument/compositeIndex": "GET",
            "instrument/indices": "GET",
            "insurance": "GET",
            "liquidation": "GET",
            "orderbook/l2": "GET",
            "quote": "GET",
            "quote/bucketed": "GET",
            "settlement": "GET",
            "stats": "GET",
            "stats/history": "GET",
            "stats/history/usd": "GET",
            "trade": "GET",
            "trade/bucketed": "GET",
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
        return name.replace("_", "/")

    def _request_public(self, name, http_method, **kwargs):
        """Request public API call.

        :param name: Method name.
        :param http_method: HTTP method (POST, GET, DELETE).
        """
        return self._send_request(
            command=name, http_method=http_method, params=kwargs, data=None)

    def _request_private(self, name, http_method, **kwargs):
        """Request private API call.

        :param name: Method name.
        :param http_method: HTTP method (POST, GET, DELETE).
        """
        # return self._send_request(
        #     command=name, http_method=http_method, params=kwargs,
        #     public_key=self._public_key, private_key=self._private_key)
        raise NotImplementedError("Not support private api at this moment.")
