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

## Exchanges supported

| Exchange | Public API | Private API |
|---|---|---|
| [Bitfinex](https://docs.bitfinex.com/v2/docs/ws-general) | v | x |
| [BitMEX](https://www.bitmex.com/api/explorer/) | v | x |
| [Bittrex](https://bittrex.com/home/api) | v | x |
| [CoinMarketCap](https://coinmarketcap.com/api/) | v | x |
| [GDAX](https://docs.gdax.com/#api) | v | x |
| [Poloniex](https://poloniex.com/support/api/) | v | v |

## Basic Usage

### Generic API

You can just make a simple call to query the same function from different
exchanges. For example, if you want to get the historical data from GDAX and
Bitfinex in a 5 minute timeframe, just call

```
In [1]: from libcryptomarket.api import GdaxApi, BitfinexApi

In [2]: from libcryptomarket.core import historical_ticker

In [3]: from datetime import datetime

In [4]: ticker1 = historical_ticker(source=GdaxApi(), symbol="BTC-USD", period=300, start_time=datetime(2017, 12, 30, 12, 0, 0), end_time=datetime(2017, 12, 31, 12, 0, 0))

In [5]: ticker2 = historical_ticker(source=BitfinexApi(), symbol="tBTCUSD", period="5m", start_time=datetime(2017, 12, 30, 12, 0, 0), end_time=datetime(2017, 12, 31, 12, 0, 0))
```

The historical data query automatically rolls over if the exchange response 
chunk a long period data. It can guarantee that you do not need to write your
own logic to get a long period of data.


### Exchange API

You can easily initialize an exchange API client and call any method stated
in the exchange API official documentation. The return value is always
the native response from library `requests`.


For example, to get GDAX order book information,

```
In [1]: from libcryptomarket.api import GdaxApi

In [2]: exchange = GdaxApi()

In [3]: exchange.products_book(product_id="BTC-USD").json()
Out[3]:
{'asks': [['14903.01', '22.60310282', 18]],
 'bids': [['14903', '3.4933731', 2]],
 'sequence': 4757644393}
```

Also, to buy order in Poloniex,

```
In [1]: from libcryptomarket.api import PoloniexApi

In [2]: exchange = PoloniexApi(public_key="<your public key>", private_key="<your private key>")

In [3]: exchange.buy(currencyPair="BTC_LTC", rate=0.001, amount=0.1, postOnly=1)
```

The exchange API methods are always delimited by underscore.

| Exchange | Method | libcryptomarket | URL |
|---|---|---|---|
| [Bitfinex](https://docs.bitfinex.com/v2/docs/ws-general) | [candles](https://docs.bitfinex.com/v2/reference#rest-public-candles) | `BitfinexApi().candles(timeframe="1m", symbol="tBTCUSD", session="hist")` | https://api.bitfinex.com/v2/candles/trade:1m:tBTCUSD/hist |
| [BitMEX](https://www.bitmex.com/api/explorer/) | [trades/bucketed](https://www.bitmex.com/api/explorer/#!/Trade/Trade_getBucketed) | `BitmexApi().trade_bucketed(binSize="1m", symbol="XBTUSD")` | https://www.bitmex.com/api/v1/trade/bucketed?binSize=1m&symbol=XBTUSD |
| [Bittrex](https://bittrex.com/home/api) | [/public/getorderbook](https://bittrex.com/home/api) | `BittrexApi().get_order_book(market="BTC-LTC", type="both")` | https://bittrex.com/api/v1.1/public/getorderbook?market=BTC-LTC&type=both |
| [CoinMarketCap](https://coinmarketcap.com/api/) | [ticket/<id>/](https://coinmarketcap.com/api/) | `CoinMarketCapApi().ticker(id="bitcoin", convert="EUR")` | https://api.coinmarketcap.com/v1/ticker/bitcoin/?convert=EUR |
| [GDAX](https://docs.gdax.com/#api) | [/products/<product-id>/candles](https://docs.gdax.com/#get-historic-rates) | `GdaxApi().products_candles(product_id="BTC-USD")` | https://api.gdax.com/products/BTC-USD/candles |
| [Poloniex](https://poloniex.com/support/api/) | [returnOrderBook](https://poloniex.com/support/api/#returnOrderBook) | `PoloniexApi().return_order_book(currencyPair="BTC_NXT", depth=10)` | https://poloniex.com/public?command=returnOrderBook&currencyPair=BTC_NXT&depth=10 |

## Contribution

The project is targeting as a core but generic toolkit to query cryptocurrency
market, so we are happy if you join to contribute and make it better. Please
do not hesitate to contact us (gavincyi at gmail dot com).