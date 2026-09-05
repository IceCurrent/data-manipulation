"""
P03  Ordering and top-N                                          Easy | ~15 min
Concepts: sorting, per-group top-N, ranking within a group
Builds on: P01, P02.

The busiest sessions in the whole panel all belong to one very heavily traded
name, which is exactly why "top N overall" and "top N per ticker" are different
questions. The third function asks the cross-sectional version: on each day,
where does each ticker sit relative to the others?

Run:  python3 -m pytest tests/test_p03_sorting_topn.py
"""
import pandas as pd


def busiest_sessions(prices: pd.DataFrame, n: int) -> pd.DataFrame:
    """The `n` highest-volume (date, ticker) rows in the whole panel.

    Returns
    -------
    DataFrame with the same four columns as `prices`, ordered by volume
    descending, with a fresh 0..n-1 index.
    """
    prices = prices.sort_values('volume', ascending=False).head(n)
    prices = prices.reset_index(drop=True)
    # print(prices)

    return prices


def top_volume_days_per_ticker(prices: pd.DataFrame, n: int) -> pd.DataFrame:
    """Each ticker's own `n` highest-volume sessions.

    Returns
    -------
    DataFrame with the same four columns as `prices`, sorted by ticker
    ascending then volume descending, with a fresh 0..n-1 index.
    """

    p = prices.sort_values(['ticker', 'volume'], ascending=[True, False])
    p = p.groupby('ticker').head(n) # .groupby gives a DataFrameGroupBy object which converts to a dataframe upon applying
    # certain functions, like head(n), mean(), max(), etc. 

    p = p.reset_index(drop=True) # drop=True is necessary otherwise reset index makes the older index a new column in the DF
    # print(p)

    return p


def volume_rank_within_date(prices: pd.DataFrame) -> pd.DataFrame:
    """Add a `volume_rank` column: how a ticker's volume ranks that day.

    Rank 1 is the highest volume traded on that date. Use the 'min' method for
    ties. Note that not every ticker trades on every date, so the number of
    ranks varies by day.

    Returns
    -------
    A copy of `prices` with one extra float column. Same rows, same order.
    """
    p = prices.groupby('date')['volume'].rank(ascending=False, method='min')

    prices['volume_rank'] = p

    return prices
