#!/bin/python
from libcryptomarket.api.exchange_api import ExchangeApi


class CoinMarketCapApi(ExchangeApi):
    """Coinmarketcap API.
    """

    def __init__(self, logger=None):
        """Constructor.

        :param public_key: Public key.
        :param private_key: Private key.
        :param logger: Logger.
        """
        ExchangeApi.__init__(self, public_key=None, private_key=None,
                             logger=logger)

    @classmethod
    def get_url(cls):
        """Get API url.
        """
        return "https://api.coinmarketcap.com/v1"

    @classmethod
    def get_public_calls(cls):
        """Get public API calls.
        """
        return {
            "ticker": "GET",
            "global": "GET"
        }

    @classmethod
    def get_private_calls(cls):
        """Get private API calls.
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
        name_list = [name]

        if name == "ticker" and "id" in kwargs.keys():
            name_list.append(kwargs["id"])
            del kwargs["id"]

        name_list.append("")

        return self._send_request(
            command='/'.join(name_list), http_method=http_method,
            public_method=True, params=kwargs)

    def _request_private(self, name, http_method, **kwargs):
        """Request private API call.

        :param name: Method name.
        :param http_method: HTTP method (POST, GET, DELETE).
        """
        raise RuntimeError("No private method provided")
