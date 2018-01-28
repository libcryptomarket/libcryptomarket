#!/bin/python
from libcryptomarket.api.exchange_api import ExchangeApi


class BittrexApi(ExchangeApi):
    """Bittrex API.
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
        return "https://bittrex.com/api"

    @classmethod
    def get_public_calls(cls):
        """Get public API calls.
        """
        return {
            'getmarkets': 'GET',
            'getcurrencies': 'GET',
            'getticker': 'GET',
            'getmarketsummaries': 'GET',
            'getmarketsummary': 'GET',
            'getorderbook': 'GET',
            'getmarkethistory': 'GET',
            'getticks': 'GET',
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
        return name.replace("_", "")

    def _request_public(self, name, http_method, **kwargs):
        """Request public API call.

        :param name: Method name.
        :param http_method: HTTP method (POST, GET, DELETE).
        """
        self.log_info("Public request:\n" +
                      "name: {}\n".format(name) +
                      "http_method: {}\n".format(http_method) +
                      "kwargs: {}".format(kwargs))

        if name == 'getticks':
            return self._send_request(
                command="/v2/public/" + name, http_method=http_method,
                public_method=True, params=kwargs)

        return self._send_request(
            command="/v1.1/public/" + name, http_method=http_method,
            public_method=True, params=kwargs)

    def _request_private(self, name, http_method, **kwargs):
        """Request private API call.

        :param name: Method name.
        :param http_method: HTTP method (POST, GET, DELETE).
        """
        raise NotImplementedError("Not support private api at this moment.")
