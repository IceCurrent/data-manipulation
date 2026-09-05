"""
P09  Duplicates, and which ones are real                          Med | ~20 min
Concepts: duplicate detection across a subset of columns, last-row-per-group
Builds on: P03 (ordering), P08.

The blotter has been double-keyed in places: a handful of rows appear twice,
identical in every column. Those are booking errors and one copy must go.

It also contains trade_ids that appear more than once with a different venue
and quantity. Those are a single order filled in pieces across venues, they are
separate legs of real business, and dropping them loses shares. So "duplicate
trade_id" and "duplicate row" are different tests and only one of them is the
one you want.

The second function is a pattern worth being able to write without thinking:
the last row per group, by some ordering.

Run:  python3 -m pytest tests/test_p09_duplicates.py
"""
import pandas as pd


def drop_double_bookings(trades: pd.DataFrame) -> pd.DataFrame:
    """Remove rows that are identical to an earlier row in every column,
    keeping the first occurrence as it appears in the file.

    Legs that share a trade_id but differ anywhere else must survive.

    Returns
    -------
    DataFrame with the same eight columns as `trades`, in the input order,
    with a fresh 0..n-1 index.
    """
    raise NotImplementedError


def last_trade_price_per_ticker_day(trades: pd.DataFrame) -> pd.DataFrame:
    """The price of the last trade of each session, per ticker.

    "Last" means latest timestamp. Ignore rows with no price. The blotter is
    not exported in time order.

    Returns
    -------
    DataFrame with columns exactly ['date', 'ticker', 'price'], where `date` is
    the trade's calendar date as a datetime64 at midnight. Sorted by date then
    ticker, with a fresh 0..n-1 index.
    """
    raise NotImplementedError
