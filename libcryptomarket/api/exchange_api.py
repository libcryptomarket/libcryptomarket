#!/bin/python
import requests
# import hmac
# import hashlib
# import urllib
import json
from functools import partial
from time import time


class ExchangeApi:
    """Exchange API connector.
    """

    def __init__(self, public_key, private_key, logger=None):
        """Constructor.

        :param public_key: Public key.
        :param private_key: Private key.
        :param logger: Logger.
        """
        self._public_key = public_key
        self._private_key = private_key
        self._logger = logger

    @classmethod
    def get_url(cls):
        """Get API url.
        """
        raise NotImplementedError("Url getter not implemented")

    @classmethod
    def get_public_url(cls):
        """Get public API url.
        """
        raise NotImplementedError("Public url getter not implemented")

    @classmethod
    def get_private_url(cls):
        """Get private API url.
        """
        raise NotImplementedError("Private url getter not implemented")

    @classmethod
    def get_public_calls(cls):
        """Get public API calls.
        """
        return {}

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

    def __getattr__(self, name):
        """Get attribute.
        """
        name = self.translate_call_name(name)

        if name in self.get_public_calls().keys():
            return partial(self._request_public, name=name,
                           http_method=self.get_public_calls()[name])
        elif name in self.get_private_calls().keys():
            return partial(self._request_private, name=name,
                           http_method=self.get_private_calls()[name])
        else:
            raise AttributeError("Trading method ({0}) ".format(name) +
                                 "is not defined.")

    def _request_public(self, name, http_method, **kwargs):
        """Request public API call.

        :param name: Method name.
        :param http_method: HTTP method (POST, GET, DELETE).
        """
        raise NotImplementedError("Public API request not implemented")

    def _request_private(self, name, http_method, *kwargs):
        """Request private API call.

        :param name: Method name.
        :param http_method: HTTP method (POST, GET, DELETE).
        """
        raise NotImplementedError("Private API request not implemented")

    # ======================================================================
    # Requests
    # ======================================================================

    @classmethod
    def _generate_nonce(cls):
        """Generate an increasing unique number.
        """
        return int(round(time() * 1000))

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
        raise NotImplementedError("Not yet implemented.")

    @classmethod
    def _generate_auth(cls, public_key, private_key):
        """Generate authentication.

        :param public_key: Public key.
        :param private_key: Private key.
        """
        raise NotImplementedError("Not yet implemented.")

    @classmethod
    def _generate_data(cls, data):
        """Generate data.

        :param data: Dict containing data information.
        """
        raise NotImplementedError("Not yet implemented.")

    def log_info(self, msg, *args):
        """Log in INFO.
        """
        if self._logger is not None:
            self._logger.info(msg, *args)

    def log_debug(self, msg, *args):
        """Log in DEBUG.
        """
        if self._logger is not None:
            self._logger.debug(msg, *args)

    def _send_request(self, command, http_method, params=None, data=None,
                      public_method=False):
        """Send request.

        :param command: API command.
        :param http_method: Http method.
        :param api_key: API key.
        :param params: Input parameters, which will be parsed
                       as "?key1=value1...".
        :param data: Data.
        :param public_method: Indicate if the request is a public method.
        :return: JSON object.
        """
        http_method = http_method.upper()
        if http_method == "DELETE":
            R = requests.delete
        elif http_method == "GET":
            R = requests.get
        elif http_method == "POST":
            R = requests.post
        else:
            raise ValueError("Http method must be either DELETE, GET or "
                             "POST.")

        # Get url
        url = self.get_url()

        if url is None:
            if public_method:
                url = self.get_public_url()
            else:
                url = self.get_private_url()

        if url is None:
            raise NotImplementedError("Url cannot be None.")

        if command is not None or command == "":
            url = '/'.join([url, command])

        # Get data
        if data is not None:
            data = self._format_data(data)
        else:
            data = ""

        # Get headers and auth
        if (self._public_key is not None and self._private_key is not None and
                not public_method):
            headers = self._generate_headers(command, http_method, params,
                                             data, self._public_key,
                                             self._private_key)
            auth = self._generate_auth(self._public_key, self._private_key)
        else:
            headers = None
            auth = None

        self.log_debug(">>> OUT:\n%s" % json.dumps({
            "Method": http_method,
            "Url": url,
            "Params": params,
            "Data": data,
            "Headers": headers
        }))

        if auth is None:
            response = R(url, params=params, data=data, headers=headers)
        else:
            response = R(url, params=params, data=data, headers=headers,
                         auth=auth)

        self.log_debug("<<< IN:\n%s" % json.dumps({
            "Status code": response.status_code,
            "Text": response.text
        }))

        return response
