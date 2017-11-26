import requests
from datetime import datetime

import pandas as pd
from pandas.util.testing import assert_frame_equal
import pytest

from libcryptomarket.historical import get_historical_prices
from libcryptomarket.price import get_order_book


def test_get_historical_prices_poloniex(monkeypatch):
    def mockreturn(url, *args, **kwargs):
        # The result is from request.get(...).json()
        class MockReturnClass:
            @classmethod
            def json(cls):
                # Query all symbols
                return [
                    {
                        "date": 1405699200,
                        "high": 0.0045388,
                        "low": 0.00403001,
                        "open": 0.00404545,
                        "close": 0.00435873,
                        "volume": 44.34555992,
                        "quoteVolume": 10311.88079097,
                        "weightedAverage": 0.00430043
                    },
                    {
                        "date": 1405713600,
                        "high": 0.00435,
                        "low": 0.00412,
                        "open": 0.00428012,
                        "close": 0.00412,
                        "volume": 19.12271662,
                        "quoteVolume": 4531.85801066,
                        "weightedAverage": 0.00421961
                    }]

            @classmethod
            def raise_for_status(cls):
                pass

        return MockReturnClass()

    monkeypatch.setattr(requests, 'get', mockreturn)

    # Test to get historical prices
    result = get_historical_prices(source='Poloniex',
                                   period='4h',
                                   symbol='BTC/XMR',
                                   from_time=datetime(2014, 7, 18, 16, 0, 0))

    expected_result = pd.DataFrame([
        {
            "r_date": datetime(2014, 7, 18, 16, 0, 0),
            "r_high": 0.0045388,
            "r_low": 0.00403001,
            "r_open": 0.00404545,
            "r_close": 0.00435873,
            "r_volume": 44.34555992,
            "r_quotevolume": 10311.88079097,
            "r_weightedaverage": 0.00430043
        },
        {
            "r_date": datetime(2014, 7, 18, 20, 0, 0),
            "r_high": 0.00435,
            "r_low": 0.00412,
            "r_open": 0.00428012,
            "r_close": 0.00412,
            "r_volume": 19.12271662,
            "r_quotevolume": 4531.85801066,
            "r_weightedaverage": 0.00421961
        }
    ]).set_index(['r_date'])
    expected_result.index.name = 'datetime'

    assert_frame_equal(result, expected_result)


def test_get_historical_prices_poloniex_invalid_period(monkeypatch):
    with pytest.raises(ValueError):
        get_historical_prices(
            source='Poloniex',
            period='29m',
            symbol='BTC/XMR',
            from_time=datetime(2014, 7, 18, 16, 0, 0))


def test_get_historical_prices_poloniex_invalid_instrument(monkeypatch):
    def mockreturn(url, *args, **kwargs):
        # The result is from request.get(...).json()
        class MockReturnClass:
            @classmethod
            def json(cls):
                # Query all symbols
                return {"error": "Invalid currency pair."}

            @classmethod
            def raise_for_status(cls):
                pass

        return MockReturnClass()

    monkeypatch.setattr(requests, 'get', mockreturn)

    # Test to get historical prices
    with pytest.raises(ValueError):
        get_historical_prices(
            source='Poloniex',
            period='4h',
            symbol='BTC/XXX',
            from_time=datetime(2014, 7, 18, 16, 0, 0))


def test_get_order_book_poloniex_all_symbols(monkeypatch):
    def mockreturn(url, *args, **kwargs):
        # The result is from request.get(...).json()
        class MockReturnClass:
            @classmethod
            def json(cls):
                # Query all symbols
                import json
                return json.loads(
                    """
{"BTC_AMP": {"asks": [["0.00002755", 16.03393139],
   ["0.00002756", 20.24556409]],
  "bids": [["0.00002739", 20.23199043], ["0.00002723", 20.30358806]],
  "isFrozen": "0",
  "seq": 44422443},
 "BTC_ARDR": {"asks": [["0.00003331", 62.49465571], ["0.00003332", 6567.629]],
  "bids": [["0.00003285", 25], ["0.00003277", 44.83974499]],
  "isFrozen": "0",
  "seq": 27008837}}
"""
                )

            @classmethod
            def raise_for_status(cls):
                pass

        return MockReturnClass()

    monkeypatch.setattr(requests, 'get', mockreturn)

    expected_df = pd.DataFrame([
        [0.00002739, 20.231990, 0.00002755, 16.033931,
            0.00003285, 25.000000, 0.00003331, 62.494656],
        [0.00002723, 20.303588, 0.00002756, 20.245564,
            0.00003277, 44.839745, 0.00003332, 6567.629000]],
        columns=pd.MultiIndex.from_product(
            [['BTC_AMP', 'BTC_ARDR'],
             ['bids', 'asks'],
             ['price', 'quantity']]),
        index=[1, 2])

    df = get_order_book(source="Poloniex", symbol="all", depth=2)
    assert_frame_equal(expected_df.sort_index(axis=1),
                       df.sort_index(axis=1))


def test_get_order_book_poloniex_one_symbol(monkeypatch):
    def mockreturn(url, *args, **kwargs):
        # The result is from request.get(...).json()
        class MockReturnClass:
            @classmethod
            def json(cls):
                # Query all symbols
                import json
                return json.loads(
                    """
{"asks": [["0.00002755", 16.03393139],
   ["0.00002756", 20.24556409]],
  "bids": [["0.00002739", 20.23199043], ["0.00002723", 20.30358806]]}
"""
                )

            @classmethod
            def raise_for_status(cls):
                pass

        return MockReturnClass()

    monkeypatch.setattr(requests, 'get', mockreturn)

    expected_df = pd.DataFrame([
        [0.00002739, 20.231990, 0.00002755, 16.033931],
        [0.00002723, 20.303588, 0.00002756, 20.245564]],
        columns=pd.MultiIndex.from_product([['bids', 'asks'],
                                            ['price', 'quantity']]),
        index=[1, 2])

    df = get_order_book(source="Poloniex", symbol="BTC_AMP", depth=2)
    assert_frame_equal(expected_df,
                       df)
