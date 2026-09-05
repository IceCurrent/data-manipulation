"""
P06  Joining, and what joins do to row counts                     Med | ~25 min
Concepts: join keys, key uniqueness, unmatched rows, multi-column keys
Builds on: P01, P05.

data/ref.csv is the security master, straight off a vendor feed. It is not a
clean lookup table, and the blotter contains instruments it has never heard of.
Before you write anything, look at it:

    from qfp.data import load_ref; print(load_ref())

A left join is supposed to be a lookup: 3080 trades in, 3080 trades out. If
your answer to the first function has more rows than it started with, the join
is telling you something about the right-hand table.

The third function turns on a distinction worth keeping straight: a (date,
ticker) with no row at all in prices is not the same thing as a row whose close
happens to be missing. This one is about the first kind.

Run:  python3 -m pytest tests/test_p06_merge.py
"""
import pandas as pd


def attach_sector(trades: pd.DataFrame, ref: pd.DataFrame) -> pd.DataFrame:
    """Look up each trade's sector and currency.

    Returns
    -------
    A copy of `trades` with two extra columns, `sector` and `currency`. Exactly
    the same number of rows as `trades`, in the same order. Instruments that
    are not in the master get NaN in both columns.
    """
    raise NotImplementedError


def unmapped_tickers(trades: pd.DataFrame, ref: pd.DataFrame) -> list:
    """Which traded instruments are missing from the security master?

    Returns
    -------
    A plain Python list of ticker strings, sorted ascending.
    """
    raise NotImplementedError


def positions_without_price(positions: pd.DataFrame, prices: pd.DataFrame) -> pd.DataFrame:
    """(date, ticker) pairs that are held in some book but have no row at all
    in the price file -- the positions you cannot mark.

    Report each pair once, however many books hold it.

    Returns
    -------
    DataFrame with columns exactly ['date', 'ticker'], sorted by date then
    ticker, with a fresh 0..n-1 index.
    """
    raise NotImplementedError
