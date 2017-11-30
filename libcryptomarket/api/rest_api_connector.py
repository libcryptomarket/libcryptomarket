#!/bin/python
import requests
import urllib
import json
from time import time


class RestApiConnector(object):
    """REST API connector.
    """

    def __init__(self, url, logger=None):
        """Constructor.

        :param url: URL address.
        :param logger: Logger. Default is None.
        """
        self._logger = logger
        self._url = url

    @classmethod
    def _generate_nonce(cls):
        """Generate an increasing unique number.
        """
        return int(round(time() * 1000))

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
        raise NotImplementedError("Not yet implemented.")

    def _generate_auth(self, public_key, private_key):
        """Generate authentication.

        :param public_key: Public key.
        :param private_key: Private key.
        """
        raise NotImplementedError("Not yet implemented.")

    def _format_data(self, data):
        """Format the data to exchange desirable format.

        :param data: Data.
        """
        raise NotImplementedError("Not yet implemented.")

    def _send_request(self, command, http_method, public_key, private_key,
                      params=None, data=None):
        """Send request.

        :param command: API command.
        :param http_method: Http method.
        :param api_key: API key.
        :param params: Input parameters, which will be parsed
                       as "?key1=value1...".
        :param data: Data.
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

        url = urllib.parse.urljoin(self._url, command)
        data = self._format_data(data)
        headers = self._generate_headers(command, http_method, params,
                                         data, public_key, private_key)
        auth = self._generate_auth(public_key, private_key)

        if self._logger is not None:
            self._logger.info(">>> OUT:\n%s" % json.dumps({
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

        if self._logger is not None:
            self._logger.info("<<< IN:\n%s" % json.dumps({
                "Status code": response.status_code,
                "Text": response.text
            }))

        return response
