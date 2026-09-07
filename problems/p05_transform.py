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
    prices = prices.dropna(subset=['volume'], axis=0)
    d = prices.groupby('ticker') # groupby colors each row of the df into it's block color, to show the association with
    # the block. Each row belongs to a group (or block), and gets a color same as the rest of the rows in the block
    # nothing is copied yet, just the coloring scheme gets stored in memory

    prices['vol_vs_mean'] = prices['volume'] - d['volume'].transform('mean')

    # agg function, collapses the entire block into a row with the aggregated value, so n-row data goes to k-row data
    # where k is the number of distinct groups

    # transform, calculates the aggregated values and assign to each of the colored row of block without collapsing
    # or we can say it's the aggregate method combined with a broadcast, which keeps the row order same

    print(prices)

    return prices



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
    trades['notional'] = trades['qty'] * trades['price']
    d = trades.groupby('ticker')

    trades['total_vol'] = d['notional'].transform('sum')
    trades['share_of_ticker'] = trades['notional'] / trades['total_vol']

    trades = trades.drop(columns=['total_vol'])
    return trades


def add_cross_sectional_zscore(prices: pd.DataFrame) -> pd.DataFrame:
    """Add `vol_z`: the z-score of this ticker's volume among all tickers
    trading on the same date.

    Use the sample standard deviation (ddof=1, pandas' default).

    Returns
    -------
    A copy of `prices` with one extra float column. Same rows, same order.
    """
    d = prices.groupby('date')

    prices['std'] = d['volume'].transform('std')
    prices['mean'] = d['volume'].transform('mean')

    prices['vol_z'] = (prices['volume'] - prices['mean'])/prices['std']

    prices = prices.drop(columns=['std', 'mean'])

    return prices