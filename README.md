# libcryptomarket: Powerful cryptocurrency market analysis toolkit

## Objective

* Support API calls of top cryptocurrency exchanges

* Support trading and analysis tools for cryptocurrency market

The project aims to answer the following two questions:

1. How to get historical data, especially a long period, in a single query?

2. How to send exchange API query in an elegent fashion?

## Prerequisite

Python 3.5+

## Installation

You can install it via pip for static version

```
pip install libcryptomarket
```

or development version

```
pip install git+https://github.com/libcryptomarket/libcryptomarket.git
```

## API Usage

This library is to extend the library [ccxt](https://github.com/ccxt/ccxt) on
more powerful functions. So the supported exchanges are same as ccxt while
a few exchanges are extended with the following features. You just need to
import the exchange from libcryptomarket.

### Candles

```
from datetime import datetime
import libcryptomarket

poloniex = libcryptomarket.poloniex()
candles = libcryptomarket.fetch_candles(
    symbol="ETH/BTC",
    start_time=datetime(2018, 1, 1),
    end_time=datetime(2018, 1, 30),
    frequency="30m")
```

### Latest candles

```
from datetime import datetime
import libcryptomarket

poloniex = libcryptomarket.poloniex()
candles = libcryptomarket.fetch_latest_candles(
    symbols=["ETH/BTC", "LTC/BTC"],
    frequency="30m",
    frequency_count=5)
```

### Supported exchanges

| Exchange | candles | latest_candles |
|---|---|---|
| Poloniex | v | v |
| Bitfinex | v | v |
| GDAX | v | v |


## Console Usage

Console usage is for exporting historical data.

### Request candles

```
request-candles --exchange poloniex --symbols ETH/BTC LTC/BTC --frequency 30m --start-time 2018-01-01 --end-time 2018-01-31 --output test.csv
```

## Contribution

The project is targeting as a core but generic toolkit to query cryptocurrency
market, so we are happy if you join to contribute and make it better. Please
do not hesitate to contact us (gavincyi at gmail dot com).