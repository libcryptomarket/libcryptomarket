import inspect
from time import sleep
from datetime import datetime, timedelta

import pandas as pd
import ccxt

import libcryptomarket.exchange
from libcryptomarket.candle import FREQUENCY_TO_SEC_DICT


def _fetch_candles(self, symbol, start_time, end_time, frequency,
                   **kwargs):
    r"""Return candles of a given period and frequency.

    :param symbol: `str` symbol.
    :param start_time: `datetime` start time.
    :param end_time: `datetime` end time.
    :param frequency: `str` frequency.
    :param \**kwargs:
        See below

    :Keyword Arguments:
        * *quote_currency* (``str``) --
          Quote currency symbol, e.g. BTC.
    """
    self.load_markets()

    # Get the exchange market id
    symbol = self.market_id(symbol)

    # Initialization
    all_data = []
    last_start_time = None

    while (start_time <
           end_time - pd.DateOffset(seconds=FREQUENCY_TO_SEC_DICT[frequency])):
        sleep(self.describe()['rateLimit'] / 1000)
        data = self._fetch_single_candles(
            symbol=symbol, start_time=start_time, end_time=end_time,
            frequency=frequency, **kwargs)

        if len(data) == 0:
            break

        if (last_start_time is not None and
                data["start_time"].iloc[0] >= last_start_time):
            break

        all_data.append(data)

        if data["end_time"].iloc[-1] > start_time:
            start_time = data["end_time"].iloc[-1]
        else:
            break

    if len(all_data) == 0:
        raise ValueError("Start time cannot be after end time.")
    elif len(all_data) == 1:
        return all_data[0]
    else:
        return pd.concat(all_data)


def _fetch_latest_candles(self, symbols, frequency, frequency_count,
                          end_time=None, **kwargs):
    """Return the latest candles based on the frequency and its count.

    :param symbols: `list` list of symbols, or `str` symbol name.
    :param frequency: `int` frequency in seconds.
    :param frequency: `str` frequency.
    :param end_time: `datetime` end time. Default is None which will use
                     current time.
    :param \**kwargs:
        See below

    :Keyword Arguments:
        * *quote_currency* (``str``) --
          Quote currency symbol, e.g. BTC.
    """
    if isinstance(symbols, str):
        symbols = [symbols]

    if end_time is None:
        end_time = datetime.utcnow()

    closest_end_time = pd.Timestamp(end_time).floor(
        timedelta(seconds=FREQUENCY_TO_SEC_DICT[frequency]))
    start_time = closest_end_time - timedelta(
        seconds=FREQUENCY_TO_SEC_DICT[frequency] * frequency_count + 1)

    all_data = []
    for symbol in symbols:
        data = self.fetch_candles(
            symbol=symbol,
            start_time=start_time,
            end_time=closest_end_time,
            frequency=frequency,
            **kwargs)
        data = data[data['end_time'] <= closest_end_time]
        all_data.append(data.set_index(['start_time', 'end_time']))

    if len(all_data) == 1:
        return all_data[0]
    else:
        return pd.concat(all_data, axis=1, keys=symbols)


###############################################################################
# Patch
###############################################################################
for exchange in dir(libcryptomarket.exchange):
    instance = getattr(ccxt, exchange)
    try:
        if inspect.isclass(instance) and issubclass(instance, ccxt.Exchange):
            setattr(instance, 'fetch_candles', _fetch_candles)
            setattr(instance, 'fetch_latest_candles', _fetch_latest_candles)
    except Exception as e:
        raise e


###############################################################################
# Poloniex patching
###############################################################################
def _poloniex_single_candles(
        self, symbol, start_time, end_time, frequency, **kwargs):
    """Poloniex candles.
    """
    data = self.public_get_returnchartdata(params={
        "currencyPair": symbol,
        "start": round(start_time.timestamp()),
        "end": round(end_time.timestamp()) - FREQUENCY_TO_SEC_DICT[frequency],
        "period": self.describe()['timeframes'][frequency]
    })

    data = pd.DataFrame(data).rename(columns={
        'date': 'start_time',
        'quoteVolume': 'quote_volume',
        'weightedAverage': 'weighted_average'
    })

    data.loc[:, 'start_time'] = data['start_time'].apply(
        lambda x: pd.Timestamp.utcfromtimestamp(x))
    data['end_time'] = data['start_time'] + pd.DateOffset(
        seconds=FREQUENCY_TO_SEC_DICT[frequency])

    if 'quote_currency' in kwargs.keys():
        base_currency = symbol.split('_')[1]

        if kwargs['quote_currency'] == base_currency:
            data.loc[:, "open"] = (1 / data.loc[:, "open"]).apply(
                lambda x: round(x, 8))
            data.loc[:, "close"] = (1 / data.loc[:, "close"]).apply(
                lambda x: round(x, 8))
            data.loc[:, "weighted_average"] = (
                (1 / data.loc[:, "weighted_average"]).apply(
                    lambda x: round(x, 8)))
            high_prices = (1 / data.loc[:, "low"]).apply(
                lambda x: round(x, 8))
            low_prices = (1 / data.loc[:, "high"]).apply(
                lambda x: round(x, 8))
            data.loc[:, "high"] = high_prices
            data.loc[:, "low"] = low_prices

    return data


setattr(ccxt.poloniex, '_fetch_single_candles', _poloniex_single_candles)


###############################################################################
# Bitfinex patching
###############################################################################
def _bitfinex_single_candles(self, symbol, start_time, end_time, frequency,
                             **kwargs):
    """Bitfinex candles.
    """
    data = self.request(
        path='candles/trade:{}:{}/hist'.format(
            self.describe()['timeframes'][frequency], symbol),
        params={
            "start": round(start_time.timestamp() * 1000),
            "end": round((end_time.timestamp() -
                          FREQUENCY_TO_SEC_DICT[frequency]) * 1000),
            "sort": 1
        })

    data = pd.DataFrame(data, columns=["start_time", "open", "close", "high",
                                       "low", "volume"])

    data.loc[:, 'start_time'] = data['start_time'].apply(
        lambda x: pd.Timestamp.utcfromtimestamp(x / 1000))
    data['end_time'] = data['start_time'] + pd.DateOffset(
        seconds=FREQUENCY_TO_SEC_DICT[frequency])

    return data


setattr(ccxt.bitfinex, '_fetch_single_candles', _bitfinex_single_candles)


###############################################################################
# GDAX patching
###############################################################################
def _gdax_single_candles(self, symbol, start_time, end_time, frequency,
                         **kwargs):
    """GDAX candles.
    """
    data = self.request(
        path='products/{}/candles'.format(symbol),
        params={
            "granularity": self.describe()['timeframes'][frequency],
            "start": start_time.isoformat(),
            "end": end_time.isoformat(),
        })

    if len(data) == 0:
        return data

    data = pd.DataFrame(data, columns=["start_time", "low", "high", "open",
                                       "close", "volume"])

    data.loc[:, 'start_time'] = data['start_time'].apply(
        lambda x: pd.Timestamp.utcfromtimestamp(x))
    data = data.sort_values(['start_time'])
    data['end_time'] = data['start_time'] + pd.DateOffset(
        seconds=FREQUENCY_TO_SEC_DICT[frequency])

    return data


setattr(ccxt.gdax, '_fetch_single_candles', _gdax_single_candles)
