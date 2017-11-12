import requests
from datetime import datetime

import pandas as pd
from pandas.util.testing import assert_frame_equal
import pytest

from libcryptomarket.historical import get_historical_prices


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
                        "weightedAverage":0.00430043
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
                "r_weightedaverage":0.00430043
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
        result = get_historical_prices(
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
                return {"error":"Invalid currency pair."}

            @classmethod
            def raise_for_status(cls):
                pass

        return MockReturnClass()

    monkeypatch.setattr(requests, 'get', mockreturn)

    # Test to get historical prices
    with pytest.raises(ValueError):
        result = get_historical_prices(
            source='Poloniex',
            period='4h',
            symbol='BTC/XXX',
            from_time=datetime(2014, 7, 18, 16, 0, 0))
    