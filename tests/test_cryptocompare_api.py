import requests
from datetime import datetime

import pandas as pd
from pandas.util.testing import assert_frame_equal

from libcryptomarket.instrument import get_instruments
from libcryptomarket.historical import get_historical_prices


def test_get_instruments_cryptocompare(monkeypatch):
    def mockreturn(url, *args, **kwargs):
        # The result is from request.get(...).json()
        class MockReturnClass:
            @classmethod
            def json(cls):
                # Query all symbols
                return {
                    'BaseImageUrl': 'https://www.cryptocompare.com',
                    'BaseLinkUrl': 'https://www.cryptocompare.com',
                    'Data': {
                        'STX': {
                            'Algorithm': 'N/A',
                            'CoinName': 'Stox',
                            'FullName': 'Stox (STX)',
                            'FullyPremined': '0',
                            'Id': '204716',
                            'ImageUrl': '/media/1383946/stx.png',
                            'Name': 'STX',
                            'PreMinedValue': 'N/A',
                            'ProofType': 'N/A',
                            'SortOrder': '1431',
                            'Sponsored': False,
                            'Symbol': 'STX',
                            'TotalCoinSupply': '29600000',
                            'TotalCoinsFreeFloat': 'N/A',
                            'Url': '/coins/stx/overview'},
                        'BCN': {
                            'Algorithm': 'CryptoNight',
                            'CoinName': 'ByteCoin',
                            'FullName': 'ByteCoin (BCN)',
                            'FullyPremined': '0',
                            'Id': '5280',
                            'ImageUrl': '/media/12318404/bcn.png',
                            'Name': 'BCN',
                            'PreMinedValue': 'N/A',
                            'ProofType': 'PoW',
                            'SortOrder': '249',
                            'Sponsored': False,
                            'Symbol': 'BCN',
                            'TotalCoinSupply': '184467440735',
                            'TotalCoinsFreeFloat': 'N/A',
                            'Url': '/coins/bcn/overview'}
                    }
                }

            @classmethod
            def raise_for_status(cls):
                pass

        return MockReturnClass()

    monkeypatch.setattr(requests, 'get', mockreturn)

    # Test getting all coins
    result = get_instruments(source='cryptocompare')

    assert len(result) == 2
    expected_result = pd.DataFrame([
        {
            'r_algorithm': '',
            'r_coinname': 'Stox',
            'r_fullname': 'Stox (STX)',
            'r_fullypremined': 0,
            'r_id': '204716',
            'r_imageurl': '/media/1383946/stx.png',
            'r_name': 'STX',
            'r_preminedvalue': 0.0,
            'r_prooftype': '',
            'r_sortorder': 1431,
            'r_sponsored': False,
            'r_symbol': 'STX',
            'r_url': '/coins/stx/overview'},
        {
            'r_algorithm': 'CryptoNight',
            'r_coinname': 'ByteCoin',
            'r_fullname': 'ByteCoin (BCN)',
            'r_fullypremined': 0,
            'r_id': '5280',
            'r_imageurl': '/media/12318404/bcn.png',
            'r_name': 'BCN',
            'r_preminedvalue': 0.0,
            'r_prooftype': 'PoW',
            'r_sortorder': 249,
            'r_sponsored': False,
            'r_symbol': 'BCN',
            'r_url': '/coins/bcn/overview'}])
    assert_frame_equal(result.set_index(['r_id']).sort_index(),
                       expected_result.set_index(['r_id']).sort_index())


def test_get_historical_prices_cryptocompare(monkeypatch):
    def mockreturn(url, *args, **kwargs):
        # The result is from request.get(...).json()
        class MockReturnClass:
            @classmethod
            def json(cls):
                # Query all symbols
                return {
                    'Aggregated': False,
                    'ConversionType': {
                        'conversionSymbol': '',
                        'type': 'force_direct'},
                    'Data': [
                        {
                            'close': 0.007707,
                            'high': 0.007716,
                            'low': 0.007701,
                            'open': 0.00771,
                            'time': 1510045800,
                            'volumefrom': 289.12,
                            'volumeto': 2.23
                        },
                        {
                            'close': 0.0077,
                            'high': 0.007716,
                            'low': 0.0077,
                            'open': 0.007707,
                            'time': 1510045860,
                            'volumefrom': 33.53,
                            'volumeto': 0.2586

                        }]
                }

            @classmethod
            def raise_for_status(cls):
                pass

        return MockReturnClass()

    monkeypatch.setattr(requests, 'get', mockreturn)

    # Test to get historical prices
    result = get_historical_prices(source='cryptocompare',
                                   period='minute',
                                   exchange='Poloniex',
                                   symbol='LTC/BTC')

    expected_result = pd.DataFrame([
        {
            'r_close': 0.007707,
            'r_high': 0.007716,
            'r_low': 0.007701,
            'r_open': 0.00771,
            'r_time': datetime(2017, 11, 7, 9, 10),
            'r_volumefrom': 289.12,
            'r_volumeto': 2.23
        },
        {
            'r_close': 0.0077,
            'r_high': 0.007716,
            'r_low': 0.0077,
            'r_open': 0.007707,
            'r_time': datetime(2017, 11, 7, 9, 11),
            'r_volumefrom': 33.53,
            'r_volumeto': 0.2586

        }]).set_index(['r_time'])
    expected_result.index.name = 'datetime'

    assert_frame_equal(result, expected_result)
