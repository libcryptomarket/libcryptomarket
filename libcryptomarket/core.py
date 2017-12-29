from functools import partial
from datetime import datetime, timedelta

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
    else:
        raise ValueError("Source (%s [%s]) does not support historical ticker"
                         % (source, source_name))