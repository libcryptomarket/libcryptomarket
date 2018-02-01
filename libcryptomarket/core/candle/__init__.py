from datetime import datetime, timedelta
from time import sleep

import pandas as pd
import ccxt

FREQUENCY_TO_SEC_DICT = {
    '1m': 60,
    '5m': 300,
    '15m': 900,
    '30m': 1800,
    '1h': 3600,
    '3h': 10800,
    '6h': 21600,
    '12h': 43200,
    '1d': 86400,
    '1w': 86400 * 7,
    '2w': 86400 * 7 * 2,
    '1M': 86400 * 30,
}

FREQUENCY_TO_SEC_DICT.update(dict(
    [(value, value) for value in FREQUENCY_TO_SEC_DICT.values()]))

from .exchanges import *        # noqa

def candles(source, symbol, start_time, end_time, frequency):
    """Return candles of a given period and frequency.

    :param source: `str` exchange name.
    :param symbol: `str` symbol.
    :param start_time: `datetime` start time.
    :param end_time: `datetime` end time.
    :param frequency: `str` frequency.
    """

    source = source.lower()
    func_name = "%s_candles" % source
    func = globals().get(func_name)

    if source == "bitfinex":
        # Always use version 2 for bitfinex
        source += "2"

    exchange = getattr(ccxt, source.lower())()
    describe = exchange.describe()

    if func is None:
        raise ValueError("Source {} is not implemented".format(
            source.__class__.__name__))

    # Initialization
    all_data = []
    last_start_time = None

    while (start_time <
           end_time - pd.DateOffset(seconds=FREQUENCY_TO_SEC_DICT[frequency])):
        sleep(describe['rateLimit'] / 1000)
        data = func(source=exchange, symbol=symbol, start_time=start_time,
                    end_time=end_time, frequency=frequency)

        if len(data) == 0:
            break

        if (last_start_time is not None and
                data["start_time"].iloc[0] >= last_start_time):
            break

        start_time = data["end_time"].iloc[-1]

        all_data.append(data)

    if len(all_data) == 0:
        raise ValueError("Start time cannot be after end time.")
    elif len(all_data) == 1:
        return all_data[0]
    else:
        return pd.concat(all_data)


def latest_candles(source, symbols, frequency, frequency_count, end_time=None):
    """Return the latest candles based on the frequency and its count.

    :param source: `str` exchange name.
    :param symbols: `list` list of symbols, or `str` symbol name.
    :param frequency: `int` frequency in seconds.
    :param frequency: `str` frequency.
    :param end_time: `datetime` end time. Default is None which will use
                     current time.
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
        data = candles(source=source,
                       symbol=symbol,
                       start_time=start_time,
                       end_time=closest_end_time,
                       frequency=frequency)
        data = data[data['end_time'] <= closest_end_time]
        all_data.append(data.set_index(['start_time', 'end_time']))

    if len(all_data) == 1:
        return all_data[0]
    else:
        return pd.concat(all_data, axis=1, keys=symbols)
