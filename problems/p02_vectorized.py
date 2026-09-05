"""
P02  Derived columns without loops                               Easy | ~15 min
Concepts: conditional assignment, NaN propagation, binning
Builds on: P01 (masks).

data/trades.csv is a trade blotter. `side` is 'BUY' or 'SELL' and `qty` is
always positive, so the direction of a trade lives in a different column from
its size. Some orders were never filled, which is why qty and price are floats.

Write these column-by-column, with no Python-level iteration over rows.

Run:  python3 -m pytest tests/test_p02_vectorized.py
"""
import pandas as pd
import numpy as np


def add_signed_qty(trades: pd.DataFrame) -> pd.DataFrame:
    """Add a `signed_qty` column: +qty for a BUY, -qty for a SELL.

    Returns
    -------
    A copy of `trades` with one extra float column. Same rows, same order.
    Where qty is missing, signed_qty is missing too.
    """

    # trades['signed_qty'] = np.where(trades['side'] == 'SELL', -trades['qty'], trades['qty'])
    trades['signed_qty'] = np.select([trades['side'] == 'SELL', trades['side'] == 'BUY'], [-trades['qty'], trades['qty']], default=np.nan)
    return trades


def add_notional(trades: pd.DataFrame) -> pd.DataFrame:
    """Add a `notional` column: signed quantity times price.

    A buy has positive notional, a sell negative.

    Returns
    -------
    A copy of `trades` with one extra float column. Same rows, same order.
    If either qty or price is missing, notional is missing -- not zero.
    """
    trades['notional'] = np.where(trades['side'] == 'SELL', -trades['qty']*trades['price'], trades['qty']*trades['price'])

    return trades


def size_bucket(trades: pd.DataFrame) -> pd.DataFrame:
    """Label each trade by the size of its notional.

    Buckets, on the ABSOLUTE notional:
        'small'   : less than 25,000
        'medium'  : 25,000 up to but not including 250,000
        'large'   : 250,000 or more

    Returns
    -------
    A copy of `trades` with a `notional` column (as in add_notional) and a
    `size_bucket` column of Python strings. Same rows, same order. Where
    notional is missing, size_bucket is NaN.
    """
    trades['notional'] = trades['qty']*trades['price']

    trades['size_bucket'] = np.select([
        trades['notional'] < 25000, 
        (trades['notional'] >= 25000) & (trades['notional'] < 250000),
        trades['notional'] >= 250000
    ], ['small', 'medium', 'large'], default=None)

    

    return trades
