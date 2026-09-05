"""
P08  Missing data is a decision                                   Med | ~25 min
Concepts: targeted dropna, reindexing onto a calendar, bounded forward-fill
Builds on: P01, P06.

Data goes missing in two different ways in this dataset and they need different
treatment:

  * the row is absent entirely -- the instrument did not trade that session
  * the row is there but the close is empty -- the vendor dropped a value

`prices` alone cannot tell you about the first kind, because you cannot see a
row that is not there. You need a calendar to compare against, which is what
data/benchmark.csv is for: it has a row for every trading session in the sample.

The second function is where the judgement is. Carrying the last price forward
across a one-day local holiday is normal practice. This dataset also contains a
six-session suspension, and carrying a price across that is how a book ends up
marked on a two-week-old price. So the fill is bounded.

Run:  python3 -m pytest tests/test_p08_missing.py
"""
import pandas as pd


def filled_trades(trades: pd.DataFrame) -> pd.DataFrame:
    """Keep only rows that represent an actual fill.

    A fill needs a quantity and a price. Other fields may legitimately be
    empty -- some venues are not reported, and those trades still happened.

    Returns
    -------
    DataFrame with the same eight columns as `trades`, in the input order,
    with a fresh 0..n-1 index.
    """
    raise NotImplementedError


def reindexed_close(prices: pd.DataFrame, ticker: str,
                    calendar: pd.DatetimeIndex, max_gap: int) -> pd.Series:
    """One ticker's close, placed on `calendar` and carried forward across
    short gaps only.

    Every date in `calendar` gets an entry. Where the ticker has no close, the
    most recent earlier close is carried forward for at most `max_gap`
    consecutive sessions; beyond that the value stays missing.

    Returns
    -------
    Series of float indexed by `calendar`, Series name 'close'.
    """
    raise NotImplementedError


def missing_close_report(prices: pd.DataFrame,
                         calendar: pd.DatetimeIndex) -> pd.DataFrame:
    """Per ticker, count the two kinds of missing data.

    n_missing_rows : dates in `calendar` with no row for this ticker
    n_nan_close    : rows that exist for this ticker but have no close

    Returns
    -------
    DataFrame with columns exactly ['ticker', 'n_missing_rows', 'n_nan_close'],
    one row per ticker sorted ascending, with a fresh 0..n-1 index.
    Both counts are integers.
    """
    raise NotImplementedError
