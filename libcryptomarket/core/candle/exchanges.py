import pandas as pd


def poloniex_candles(source, symbol, start_time, end_time, frequency):
    """Poloniex candles.
    """
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
        lambda x: pd.Timestamp.utcfromtimestamp(x))
    data['end_time'] = data['start_time'].shift(-1)

    return data.iloc[:-1, :]


def bitfinex_candles(source, symbol, start_time, end_time, frequency):
    """Bitfinex candles.
    """
    data = source.request(
        path='candles/trade:{}:{}/hist'.format(frequency, symbol),
        params={
            "start": round(start_time.timestamp() * 1000),
            "end": round(end_time.timestamp() * 1000),
            "sort": 1
        })

    data = pd.DataFrame(data, columns=["start_time", "open", "close", "high",
                                       "low", "volume"])

    data.loc[:, 'start_time'] = data['start_time'].apply(
        lambda x: pd.Timestamp.utcfromtimestamp(x / 1000))
    data['end_time'] = data['start_time'].shift(-1)

    return data.iloc[:-1, :]


def gdax_candles(source, symbol, start_time, end_time, frequency):
    """GDAX candles.
    """
    end_time += pd.DateOffset(seconds=1)

    data = source.request(
        path='products/{}/candles'.format(symbol),
        params={
            "granularity": frequency,
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
    data['end_time'] = data['start_time'].shift(-1)

    return data.iloc[:-1, :]
