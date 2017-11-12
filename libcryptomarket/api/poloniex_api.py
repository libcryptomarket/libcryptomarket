#!/bin/python
import requests
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

    assert period in VALID_PERIODS, (
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
