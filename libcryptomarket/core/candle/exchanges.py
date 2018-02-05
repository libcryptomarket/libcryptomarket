import pandas as pd

from libcryptomarket.core.candle import FREQUENCY_TO_SEC_DICT


def poloniex_candles(source, symbol, start_time, end_time, frequency,
                     **kwargs):
    """Poloniex candles.
    """
    data = source.public_get_returnchartdata(params={
        "currencyPair": symbol,
        "start": round(start_time.timestamp()),
        "end": round(end_time.timestamp()) - FREQUENCY_TO_SEC_DICT[frequency],
        "period": source.describe()['timeframes'][frequency]
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


def bitfinex_candles(source, symbol, start_time, end_time, frequency,
                     **kwargs):
    """Bitfinex candles.
    """
    data = source.request(
        path='candles/trade:{}:{}/hist'.format(
            source.describe()['timeframes'][frequency], symbol),
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


def gdax_candles(source, symbol, start_time, end_time, frequency,
                 **kwargs):
    """GDAX candles.
    """
    data = source.request(
        path='products/{}/candles'.format(symbol),
        params={
            "granularity": source.describe()['timeframes'][frequency],
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
