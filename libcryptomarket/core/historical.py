from functools import partial
from datetime import datetime, timedelta
from time import sleep

import pandas as pd


def historical_ticker(source, symbol, period, start_time=None, end_time=None,
                      **kwargs):
    """Return historical ticker.

    :param source: Source, an Exchange API object.
    :param symbol: Symbol, string object.
    :param period: Period or frequency, followed with exchange protocol, string
                   object.
    :param start_time: Start time, datetime object.
    :param end_time: Start time, datetime object.
    :param wait_sec: Seconds to wait between queries, int. Optional.
    """
    # Validation
    if start_time is not None and not isinstance(start_time, datetime):
        raise ValueError("Start time is not a datetime object.")

    if end_time is not None and not isinstance(end_time, datetime):
        raise ValueError("End time is not a datetime object.")

    # Source object name
    source_name = source.__class__.__name__.lower().replace("api", "")

    if source_name == "poloniex":
        return _historical_ticker_poloniex(
            source=source, symbol=symbol, period=period,
            start_time=start_time, end_time=end_time,
            **kwargs)
    elif source_name == "gdax":
        return _historical_ticker_gdax(
            source=source, symbol=symbol, period=period,
            start_time=start_time, end_time=end_time,
            **kwargs)
    elif source_name == "bitfinex":
        return _historical_ticker_bitfinex(
            source=source, symbol=symbol, period=period,
            start_time=start_time, end_time=end_time,
            **kwargs)
    else:
        raise ValueError("Source (%s [%s]) does not support historical ticker"
                         % (source, source_name))


def _historical_ticker_poloniex(source, symbol, period, start_time, end_time,
                                **kwargs):
    """Return historical ticker in Poloniex.

    :param source: Source, an Exchange API object.
    :param symbol: Symbol, string object.
    :param period: Period or frequency, followed with exchange protocol, string
                   object.
    :param start_time: Start time, datetime object.
    :param end_time: Start time, datetime object.
    """
    # Exchange validation
    if start_time is None and end_time is None:
        raise ValueError("Start time and end time cannot be both None.")

    request_func = partial(source.return_chart_data, currencyPair=symbol,
                           period=period)

    if start_time is not None:
        request_func = partial(request_func,
                               start=start_time.timestamp())
    if end_time is not None:
        request_func = partial(request_func,
                               end=end_time.timestamp())
    data = request_func()
    data.raise_for_status()
    data = pd.DataFrame(data.json())
    data['date'] = data['date'].apply(
        lambda x: pd.to_datetime(x, unit='s'))
    data = data.set_index(['date'])
    data.index.name = 'datetime'
    data.columns.name = symbol

    return data


def _historical_ticker_gdax(source, symbol, period, start_time, end_time,
                            **kwargs):
    """Return historical ticker in GDAX.

    :param source: Source, an Exchange API object.
    :param symbol: Symbol, string object.
    :param period: Period or frequency, followed with exchange protocol, string
                   object.
    :param start_time: Start time, datetime object.
    :param end_time: Start time, datetime object.
    :param wait_sec: Seconds to wait between queries, int. Optional.
    """
    # Exchange validation
    if (start_time is None) + (end_time is None) not in [0, 2]:
        # Both start and end time must be provided
        raise ValueError("Start and end time must be both provided")

    request_func = partial(source.products_candles, product_id=symbol,
                           granularity=period)

    if start_time is None and end_time is None:
        # Just get the latest 300 ticks
        data = request_func()
        data.raise_for_status()
        data = pd.DataFrame(data.json())

    else:
        # Safety net
        last_datetime = start_time.timestamp()

        data = []

        while start_time <= end_time:
            tmp_data = request_func(
                start=start_time.isoformat(),
                end=(start_time +
                     timedelta(seconds=period * 200)).isoformat())
            tmp_data.raise_for_status()
            tmp_data = pd.DataFrame(tmp_data.json())

            # Append into data list
            data.append(tmp_data)

            # Check to exit
            if last_datetime >= tmp_data.iloc[0, 0]:
                # Same as the previous query
                break
            else:
                last_datetime = tmp_data.iloc[0, 0]
                start_time = datetime.fromtimestamp(last_datetime)

            sleep(kwargs.get("wait_sec", 0.33))

        if len(data) > 1:
            data = pd.concat(data, axis=0)
        else:
            data = data[0]

    data.columns = ['datetime', 'low', 'high', 'open', 'close', 'volume']
    data['datetime'] = pd.to_datetime(data['datetime'], unit='s')
    data = data.set_index('datetime').sort_index()
    data = data[~data.index.duplicated(keep='first')]

    return data


def _historical_ticker_bitfinex(source, symbol, period, start_time, end_time,
                                **kwargs):
    """Return historical ticker in Bitfinex.

    :param source: Source, an Exchange API object.
    :param symbol: Symbol, string object.
    :param period: Period or frequency, followed with exchange protocol, string
                   object.
    :param start_time: Start time, datetime object.
    :param end_time: Start time, datetime object.
    :param wait_sec: Seconds to wait between queries, int. Optional.
    """
    request_func = partial(source.candles, symbol=symbol, timeframe=period,
                           section="hist", sort=1, limit=1000)

    if start_time is None and end_time is None:
        data = request_func()
        data.raise_for_status()
        data = pd.DataFrame(data.json())
    else:
        # Safety net
        last_datetime = (
            0 if start_time is None else start_time.timestamp() * 1000)

        data = []

        while start_time is None or end_time is None or start_time <= end_time:
            f = request_func

            if start_time is not None:
                f = partial(f, start=round(start_time.timestamp() * 1000))

            if end_time is not None:
                f = partial(f, end=round(end_time.timestamp() * 1000))

            tmp_data = f()
            tmp_data.raise_for_status()
            tmp_data = tmp_data.json()

            if len(tmp_data) == 0:
                break
            elif last_datetime >= tmp_data[-1][0]:
                print(last_datetime)
                print(tmp_data[-1][0])
                break
            else:
                last_datetime = tmp_data[-1][0]
                start_time = datetime.fromtimestamp(
                    round(last_datetime / 1000 + 1))
                data.append(pd.DataFrame(tmp_data))

            sleep(kwargs.get("wait_sec", 1))

        data = pd.concat(data, axis=0)

    data.columns = ["datetime", "open", "close", "high", "low", "volume"]
    data["datetime"] = pd.to_datetime(data["datetime"], unit="ms")
    data = data.set_index("datetime").sort_index()
    data = data[~data.index.duplicated(keep='first')]

    return data
