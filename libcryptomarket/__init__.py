# -*- coding: utf-8 -*-
# pylint: disable-msg=W0401
# flake8: noqa

"""Top-level package for libcryptomarket."""

from libcryptomarket.exchange import *
from libcryptomarket.instrument import instruments
from libcryptomarket.order_book import order_book
from libcryptomarket.candle import (
    candles, latest_candles, FREQUENCY_TO_SEC_DICT)
import libcryptomarket.candle.inject


__author__ = """Gavin Chan"""
__email__ = 'gavincyi@gmail.com'
