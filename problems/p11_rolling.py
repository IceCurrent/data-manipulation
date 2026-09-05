"""
P11  Rolling windows on a panel                                   Med | ~25 min
Concepts: trailing windows within groups, minimum observations, argmax
Builds on: P10 (returns), P05.

Rolling volatility is the most-asked calculation in this whole set. Two things
make it more than a one-liner here.

First, the panel is stacked, so the window must not run off the end of one
ticker and into the next -- the same hazard as P10, but rolling operations
inside a groupby have a habit of handing back an index you did not ask for.

Second, a window is either full or it is not. A "20-day volatility" computed
off nine observations is not a 20-day volatility, and quietly returning one is
how bad numbers get into reports. Every window here must be complete.

Run:  python3 -m pytest tests/test_p11_rolling.py
"""
import pandas as pd


def add_rolling_vol(prices: pd.DataFrame, window: int,
                    ann_factor: int = 252) -> pd.DataFrame:
    """Add `roll_vol`: annualised trailing volatility of simple daily returns.

    The standard deviation (sample, ddof=1) of the last `window` returns for
    that ticker, multiplied by sqrt(ann_factor). Missing until the ticker has a
    full window of returns available.

    Returns
    -------
    A copy of `prices` with one extra float column -- the four input columns
    plus `roll_vol`, and no intermediate columns. Same rows, same order.
    """
    raise NotImplementedError


def add_rolling_zscore(prices: pd.DataFrame, window: int) -> pd.DataFrame:
    """Add `close_z`: how far the current close sits from its own recent mean,
    in units of its own recent standard deviation.

    Both statistics are over the last `window` closes for that ticker,
    inclusive of the current one, and both require a full window.

    Returns
    -------
    A copy of `prices` with one extra float column. Same rows, same order.
    """
    raise NotImplementedError


def most_volatile_window(prices: pd.DataFrame, window: int,
                         ann_factor: int = 252) -> tuple:
    """Where in the whole panel was trailing volatility highest?

    Returns
    -------
    A tuple (ticker, date) -- a str and a pandas Timestamp -- identifying the
    single row with the largest `roll_vol`.
    """
    raise NotImplementedError
