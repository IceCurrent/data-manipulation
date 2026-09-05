"""
P05  Group-relative values                                        Med | ~25 min
Concepts: comparing each row against its own group's statistic
Builds on: P04 (grouping and aggregation).

P04 collapsed groups down to one row each. These three want the opposite: a
value computed per group, then lined back up against every original row. There
are at least three ways to do that in pandas and they differ in how much they
disturb the row order -- all three functions here must return the rows exactly
as they came in.

The last one is the cross-sectional version, grouping by date rather than by
ticker: on each day, how unusual was this ticker's volume compared with the
other tickers trading that day?

Run:  python3 -m pytest tests/test_p05_transform.py
"""
import pandas as pd


def add_volume_vs_ticker_mean(prices: pd.DataFrame) -> pd.DataFrame:
    """Add `vol_vs_mean`: this session's volume minus the ticker's own average
    volume across the whole sample.

    Returns
    -------
    A copy of `prices` with one extra float column. Same rows, same order.
    """
    raise NotImplementedError


def add_share_of_ticker_notional(trades: pd.DataFrame) -> pd.DataFrame:
    """Add `share_of_ticker`: what fraction of all the cash traded in this
    ticker went through this trade.

    Use absolute notional, so buys and sells do not cancel. Rows with a missing
    notional get a missing share and are left out of the denominator, so the
    shares within each ticker sum to 1.

    Returns
    -------
    A copy of `trades` with a `notional` column (as in P02) and a
    `share_of_ticker` float column. Same rows, same order.
    """
    raise NotImplementedError


def add_cross_sectional_zscore(prices: pd.DataFrame) -> pd.DataFrame:
    """Add `vol_z`: the z-score of this ticker's volume among all tickers
    trading on the same date.

    Use the sample standard deviation (ddof=1, pandas' default).

    Returns
    -------
    A copy of `prices` with one extra float column. Same rows, same order.
    """
    raise NotImplementedError
