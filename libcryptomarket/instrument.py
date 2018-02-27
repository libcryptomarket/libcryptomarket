import pandas as pd


def instruments(source):
    """Return instruments.

    :param source: Source, an Exchange API object.
    """
    # Source object name
    source_name = source.__class__.__name__.lower().replace("api", "")

    if source_name == "coinmarketcap":
        response = source.ticker()
        response.raise_for_status()
        return pd.DataFrame(response.json())
    else:
        raise ValueError("Source (%s [%s]) does not support instruments"
                         % (source, source_name))
