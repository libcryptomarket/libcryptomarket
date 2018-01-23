from datetime import datetime, timedelta

import pandas as pd
import ccxt


def candles(source, symbol, start_time, end_time, frequency):
    """Return candles of a given period and frequency.

    :param source: `str` exchange name.
    :param symbol: `str` symbol.
    :param start_time: `datetime` start time.
    :param end_time: `datetime` end time.
    :param frequency: `int` frequency in seconds.
    """

    if source.lower() == 'poloniex':
        source = getattr(ccxt, source.lower())()

        data = source.public_get_returnchartdata(params={
            "currencyPair": symbol,
            "start": round(start_time.timestamp()),
            "end": round(end_time.timestamp()),
            "period": frequency
        })

        data = pd.DataFrame(data).rename(columns={
            'date': 'start_time',
            'quoteVolume': 'quote_volume',
            'weightedAverage': 'weighted_average'
        })

        data.loc[:, 'start_time'] = data['start_time'].apply(
            lambda x : pd.Timestamp.fromtimestamp(x).tz_localize('UTC'))
        data['end_time'] = data['start_time'] + pd.DateOffset(
            seconds=frequency)

        return data
    else:
        raise ValueError("Source {} is not implemented".format(
            source.__class__.__name__))


def latest_candles(source, symbols, frequency, frequency_count, end_time=None):
    """Return the latest candles based on the frequency and its count.

    :param source: `str` exchange name.
    :param symbols: `list` list of symbols, or `str` symbol name.
    :param frequency: `int` frequency in seconds.
    :param frequency: `int` frequency count.
    :param end_time: `datetime` end time. Default is None which will use
                     current time.
    """
    if isinstance(symbols, str):
        symbols = [symbols]

    if end_time is None:
        end_time = datetime.utcnow()

    closest_end_time = pd.Timestamp(end_time).floor(
        timedelta(seconds=frequency))
    start_time = closest_end_time - timedelta(
        seconds=frequency * frequency_count)

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
