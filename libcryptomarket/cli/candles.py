import argparse
import logging

import pandas as pd

# pylint: disable-msg=W0401
from libcryptomarket.exchange import *  # flake8: noqa

LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

FREQUENCIES = ['1m', '5m', '15m', '30m', '1h', '3h', '6h', '12h', '1d',
               '1w', '2w', '1M', ]


def get_args():
    """Get input arguments.
    """
    parser = argparse.ArgumentParser(description=(
        'Query historical candles to files.'))
    parser.add_argument('--exchange', action='store', dest='exchange',
                        help='Exchange name.', required=True)
    parser.add_argument('--symbols', action='store', dest='symbols',
                        help='List of symbols',
                        type=str, nargs='+', required=True)
    parser.add_argument('--frequency', action='store', dest='frequency',
                        help='Frequency.',
                        choices=list(FREQUENCIES),
                        required=True)
    parser.add_argument('--start-time', action='store', dest='start_time',
                        help='Start time in format of \'YYYY-MM-DD\'',
                        required=True)
    parser.add_argument('--end-time', action='store', dest='end_time',
                        help='End time in format of \'YYYY-MM-DD\'',
                        required=True)
    parser.add_argument('--output', action='store', dest='output',
                        help='Output filename', required=True)

    return parser.parse_args()


def main():
    """Main.
    """
    args = get_args()
    logging.basicConfig(format=LOG_FORMAT, level=logging.INFO)

    start_time = pd.Timestamp(args.start_time)
    logging.info('Start time: %s', start_time)

    end_time = pd.Timestamp(args.end_time)
    logging.info('End time: %s', end_time)

    logging.info('Starting querying to exchange %s with frequency %s...',
                 args.exchange, args.frequency)

    all_data = {}

    exchange = globals()[args.exchange.lower()]

    for symbol in args.symbols:
        logging.info('Querying symbol %s...', symbol)
        data = exchange().fetch_candles(
            symbol=symbol,
            start_time=start_time,
            end_time=end_time,
            frequency=args.frequency)
        all_data[symbol] = data.set_index(['start_time'], ['end_time'])

    logging.info('Cleaning the data...')

    all_data = pd.concat(all_data, axis=1, names=['symbol', 'value'])
    all_data = all_data.stack(level=0)

    logging.info('Exporting to path (%s)...', args.output)
    all_data.to_csv(args.output)

    logging.info('Exported all the historical prices')


if __name__ == '__main__':
    main()
