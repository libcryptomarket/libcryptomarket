import requests
import datetime

from libcryptomarket.api.coinmarketcap_api import get_ticker


def test_get_ticker(monkeypatch):
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
    result = get_ticker()
    assert len(result) == 2

    # Test getting only bitcoin
    result = get_ticker("bitcoin")
    assert len(result) == 1
    
    result = result[0]
    assert result.r_id == "bitcoin"
    assert result.r_name == "Bitcoin"
    assert result.r_symbol == "BTC"
    assert result.r_rank == 1
    assert result.r_price_usd == 573.137
    assert result.r_price_btc == 1.0
    assert result.r_24h_volume_usd == 72855700.0
    assert result.r_market_cap_usd == 9080883500.0
    assert result.r_available_supply == 15844176.0
    assert result.r_total_supply == 15844176.0
    assert result.r_percent_change_1h == 0.04
    assert result.r_percent_change_24h == -0.3
    assert result.r_percent_change_7d == -0.57
    assert result.r_last_updated == datetime.datetime(2016, 9, 1, 20, 34, 27)