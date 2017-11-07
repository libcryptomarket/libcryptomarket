import requests
import datetime

import pandas as pd
from pandas.util.testing import assert_frame_equal

from libcryptomarket.instrument import get_instruments


def test_get_instruments_coinmarketcap(monkeypatch):
    def mockreturn(url):
        # The result is from request.get(...).json()
        class MockReturnClass:
            @classmethod
            def json(cls):
                url_split = url.split('/')
                if url_split[-1] == "":
                    # Query all symbols
                    return [
                        {
                            "id": "bitcoin",
                            "name": "Bitcoin",
                            "symbol": "BTC",
                            "rank": "1",
                            "price_usd": "573.137",
                            "price_btc": "1.0",
                            "24h_volume_usd": "72855700.0",
                            "market_cap_usd": "9080883500.0",
                            "available_supply": "15844176.0",
                            "total_supply": "15844176.0",
                            "percent_change_1h": "0.04",
                            "percent_change_24h": "-0.3",
                            "percent_change_7d": "-0.57",
                            "last_updated": "1472762067"
                        },
                        {
                            "id": "ethereum",
                            "name": "Ethereum",
                            "symbol": "ETH",
                            "rank": "2",
                            "price_usd": "12.1844",
                            "price_btc": "0.021262",
                            "24h_volume_usd": "24085900.0",
                            "market_cap_usd": "1018098455.0",
                            "available_supply": "83557537.0",
                            "total_supply": "83557537.0",
                            "percent_change_1h": "-0.58",
                            "percent_change_24h": "6.34",
                            "percent_change_7d": "8.59",
                            "last_updated": "1472762062"
                        }]
                else:
                    # Query the particular symbol. Now only test with bitcoin
                    return [
                        {
                            "id": "bitcoin",
                            "name": "Bitcoin",
                            "symbol": "BTC",
                            "rank": "1",
                            "price_usd": "573.137",
                            "price_btc": "1.0",
                            "24h_volume_usd": "72855700.0",
                            "market_cap_usd": "9080883500.0",
                            "available_supply": "15844176.0",
                            "total_supply": "15844176.0",
                            "percent_change_1h": "0.04",
                            "percent_change_24h": "-0.3",
                            "percent_change_7d": "-0.57",
                            "last_updated": "1472762067"
                        }]

        return MockReturnClass()

    monkeypatch.setattr(requests, 'get', mockreturn)

    # Test getting all coins
    result = get_instruments(source='coinmarketcap')
    expected_result = pd.DataFrame([
        {
            "r_id": "bitcoin",
            "r_name": "Bitcoin",
            "r_symbol": "BTC",
            "r_rank": 1,
            "r_price_usd": 573.137,
            "r_price_btc": 1.0,
            "r_24h_volume_usd": 72855700.0,
            "r_market_cap_usd": 9080883500.0,
            "r_available_supply": 15844176.0,
            "r_total_supply": 15844176.0,
            "r_percent_change_1h": 0.04,
            "r_percent_change_24h": -0.3,
            "r_percent_change_7d": -0.57,
            "r_last_updated": datetime.datetime(2016, 9, 1, 20, 34, 27)
        },
        {
            "r_id": "ethereum",
            "r_name": "Ethereum",
            "r_symbol": "ETH",
            "r_rank": 2,
            "r_price_usd": 12.1844,
            "r_price_btc": 0.021262,
            "r_24h_volume_usd": 24085900.0,
            "r_market_cap_usd": 1018098455.0,
            "r_available_supply": 83557537.0,
            "r_total_supply": 83557537.0,
            "r_percent_change_1h": -0.58,
            "r_percent_change_24h": 6.34,
            "r_percent_change_7d": 8.59,
            "r_last_updated": datetime.datetime(2016, 9, 1, 20, 34, 22)
        }])
    assert_frame_equal(result.set_index(['r_id']).sort_index(),
                       expected_result.set_index(['r_id']).sort_index())

    # Test getting only bitcoin
    result = get_instruments(source='coinmarketcap', coin='bitcoin')
    expected_result = pd.DataFrame([
        {
            "r_id": "bitcoin",
            "r_name": "Bitcoin",
            "r_symbol": "BTC",
            "r_rank": 1,
            "r_price_usd": 573.137,
            "r_price_btc": 1.0,
            "r_24h_volume_usd": 72855700.0,
            "r_market_cap_usd": 9080883500.0,
            "r_available_supply": 15844176.0,
            "r_total_supply": 15844176.0,
            "r_percent_change_1h": 0.04,
            "r_percent_change_24h": -0.3,
            "r_percent_change_7d": -0.57,
            "r_last_updated": datetime.datetime(2016, 9, 1, 20, 34, 27)
        }])
    assert_frame_equal(result.set_index(['r_id']).sort_index(),
                       expected_result.set_index(['r_id']).sort_index())
