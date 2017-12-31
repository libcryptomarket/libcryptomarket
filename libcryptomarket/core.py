from functools import partial
from datetime import datetime, timedelta
from time import sleep

import pandas as pd


def historical_ticker(source, symbol, period, start_time=None, end_time=None):
    """Return historical ticker.

    :param source: Source, an Exchange API object.
    :param start_time: Start time, datetime object.
    :param end_time: Start time, datetime object.
    """
    # Validation
    if start_time is not None and not isinstance(start_time, datetime):
        raise ValueError("Start time is not a datetime object.")

    if end_time is not None and not isinstance(end_time, datetime):
        raise ValueError("End time is not a datetime object.")

    # Source object name
    source_name = source.__class__.__name__.lower().replace("api", "")

    if source_name == "poloniex":
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

    elif source_name == "gdax":
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

                sleep(0.333)

            if len(data) > 1:
                data = pd.concat(data, axis=0)
            else:
                data = data[0]

        data.columns = ['datetime', 'low', 'high', 'open', 'close', 'volume']
        data['datetime'] = pd.to_datetime(data['datetime'], unit='s')
        data = data.set_index('datetime').sort_index()
        data = data[~data.index.duplicated(keep='first')]

        return data

    else:
        raise ValueError("Source (%s [%s]) does not support historical ticker"
                         % (source, source_name))
