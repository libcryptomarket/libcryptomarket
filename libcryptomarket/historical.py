from functools import partial

import pandas as pd

from libcryptomarket.api.cryptocompare_api import (
    get_histo, CryptocompareHisto
)


def get_historical_prices(source='cryptocompare', symbol=None, exchange=None,
                          period=None, limit=0, from_time=None, to_time=None):
    """Get historical prices.

    :param source: Source of data.
    :param symbol: Symbol. Default is None.
    :param exchange: Exchange. Default is None.
    :param period: Data frequency. Default is None, which follows the source
                   default value.
    :param limit: Limit of records. Default is 0, which follows the source
                  default value.
    :param from_time: From time. Default is None, which follows the source
                      default value.
    :param to_time: To time. Default is None, which follows the source default
                    value.
    """
    if source == 'cryptocompare':
        if period is None:
            raise ValueError("Input parameter period cannot be None.")

        if exchange is None:
            raise ValueError("Input parameter exchange cannot be None.")

        if ((limit > 0) +
                ((from_time is not None) or (to_time is not None)) > 1):
            raise ValueError("Only accept input parameter limit, or from_time"
                             " and to_time pair.")

        if (from_time is None) ^ (to_time is None):
            raise ValueError("Cannot accept either from_time or to_time is "
                             "None")

        # Parse from (first 3) and to (last 3) symbol from the parameter
        # symbol.
        from_sym = symbol[:3]
        to_sym = symbol[3:]

        func = partial(get_histo, period=period, fsym=from_sym, tsym=to_sym,
                       e=exchange)

        data = []
        if limit > 0:
            # Get the data by limit of records
            to_time = 0

            while limit > 0:
                if to_time == 0:
                    response = func(limit=limit)['Data']
                else:
                    response = func(limit=limit, toTs=to_time)['Data']

                if len(response) == 0:
                    # Terminate if no further response
                    break
                else:
                    data += response
                    limit -= len(response)
                    to_time = response[0]['time'] - 1
        elif from_time is not None and to_time is not None:
            # Get the data by time range
            from libcryptomarket.api.cryptocompare_api import MAX_QUERY_LIMIT
            from_time_ts = int(from_time.timestamp())
            to_time_ts = int(to_time.timestamp())

            while from_time_ts < to_time_ts:
                response = func(limit=MAX_QUERY_LIMIT,
                                toTs=to_time_ts)['Data']

                if len(response) == 0:
                    # Terminate if no further response
                    break
                else:
                    data += response
                    to_time_ts = response[0]['time'] - 1

        else:
            data += func()['Data']

        if len(data) == 0:
            return data

        data = pd.DataFrame([CryptocompareHisto(**e).__dict__ for e in data])
        # Filter only valid time range
        if from_time is not None and to_time is not None:
            data = data[(data['r_time'] >= from_time) &
                        (data['r_time'] <= to_time)]

        data = data.set_index(['r_time'])
        data.index.name = 'datetime'

        return data
    else:
        raise ValueError("No source is called {0}".format(source))
