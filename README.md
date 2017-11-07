# libcryptomarket: Powerful cryptocurrency market analysis toolkit

-------------------

## Objective

The library is for researchers to analysis cryptocurrency in a fast and
flexible way. Currently there are different source of API to get the 
cryptocurrency market information. The sources are from websites which provides
a general comparative information among the currencies and from exchanges.


## Prerequisite

Python 3.x and pip.

## Installation

To install the library, please run the command to install via pip


```
pip install git+https://github.com/libcryptomarket/libcryptomarket.git
```

## Usage

All the query result are converted into pandas Series or DataFrame.

### Instrument

To get a list of available currencies, run

```
from libcryptomarket.instrument import get_instruments

instruments = get_instruments()
```

## Contribution

The project is targeting as a core but generic toolkit to query cryptocurrency
market, so we are happy if you join to contribute and make it better. Please 
do not hesitate to contact us (gavincyi at gmail dot com).