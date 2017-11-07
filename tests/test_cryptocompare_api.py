import requests

import pandas as pd
from pandas.util.testing import assert_frame_equal

from libcryptomarket.instrument import get_instruments


def test_get_instruments_cryptocompare(monkeypatch):
    def mockreturn(url):
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
