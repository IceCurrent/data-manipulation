"""
P18  Does the signal predict anything?                  Med, composite | ~30 min
Concepts: lead/lag alignment, cross-sectional ranking, correlation by date
Builds on: P07 (wide panels), P10 (returns), P05 (cross-sectional work), P15.

The standard first test of any alpha signal: on each day, rank the names by the
signal, rank them by what they went on to do, and correlate the two rankings.
Average that over every day and you have the information coefficient. Real ICs
are small -- something in the low hundredths is a real signal, not a bug.

The whole exercise is an exercise in alignment. The signal at date t may only
use prices up to and including t. The return it is judged against is the one
from t to t+1, which nobody knows at t. Line these up off by one in either
direction and you will either measure nothing or measure something impossibly
good.

Ranks are computed only among the tickers that have both a signal and a forward
return that day, so that both rankings cover the same names.

Run:  python3 -m pytest tests/test_p18_signal.py
"""
import pandas as pd


def momentum_signal(prices: pd.DataFrame, lookback: int) -> pd.DataFrame:
    """Trailing `lookback`-session return of each ticker, as a wide panel.

    The value at date t is the return from the close `lookback` sessions
    earlier to the close at t -- information available at t. Missing where
    the ticker has no close at either end.

    Returns
    -------
    DataFrame indexed by date ascending, one column per ticker sorted
    ascending, float values.
    """
    raise NotImplementedError


def information_coefficient(prices: pd.DataFrame, lookback: int) -> pd.Series:
    """The daily cross-sectional rank correlation between signal and next-day
    return.

    For each date, take the tickers that have both a signal and a next-session
    return, rank them on each, and correlate the ranks (Spearman). Dates with
    fewer than three such tickers are excluded, as are dates where the
    correlation is undefined.

    Returns
    -------
    Series of float indexed by date ascending (index name 'date'), Series name
    'ic'.
    """
    raise NotImplementedError


def mean_ic(prices: pd.DataFrame, lookback: int) -> float:
    """The average of the daily information coefficients.

    Returns
    -------
    float.
    """
    raise NotImplementedError
