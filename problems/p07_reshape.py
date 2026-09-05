"""
P07  Long and wide                                                Med | ~20 min
Concepts: long-to-wide, wide-to-long, reshaping that needs an aggregation
Builds on: P05, P06.

Panels arrive long (one row per date-ticker) and most time series work wants
them wide (one column per ticker). Risk reports arrive wide (one column per
factor) and joining them to anything wants them long. Both directions here.

The middle function differs from the first in one respect, and that difference
decides which reshape can do the job at all. It also re-uses the security
master from P06, with the same caveat.

Run:  python3 -m pytest tests/test_p07_reshape.py
"""
import pandas as pd


def close_panel(prices: pd.DataFrame) -> pd.DataFrame:
    """Closes as a wide panel.

    Returns
    -------
    DataFrame indexed by date ascending (index name 'date'), one column per
    ticker sorted ascending (columns name 'ticker'), values are closes.
    Dates where a ticker did not trade are NaN.
    """
    raise NotImplementedError


def sector_avg_volume(prices: pd.DataFrame, ref: pd.DataFrame) -> pd.DataFrame:
    """Average daily volume per sector, as a wide panel.

    For each date and sector, the mean volume across that sector's tickers
    which traded that day.

    Returns
    -------
    DataFrame indexed by date ascending, one column per sector sorted
    ascending, float values.
    """
    raise NotImplementedError


def melt_risk(risk_wide: pd.DataFrame) -> pd.DataFrame:
    """Turn the month-end factor report into long format.

    data/risk_wide.csv has one column per factor. Some cells are empty because
    that book is not decomposed on that factor; those should not become rows.

    Returns
    -------
    DataFrame with columns exactly ['date', 'book', 'factor', 'exposure'],
    sorted by date, book, factor, with a fresh 0..n-1 index.
    """
    raise NotImplementedError
