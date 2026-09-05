"""
P13  Two calendars                                                Med | ~25 min
Concepts: aligning series that do not share dates, as-of lookups, look-ahead
Builds on: P08 (reindexing and filling), P06 (lookups).

Two of the tickers are quoted in EUR and GBP and the book reports in USD, so
their closes need converting. data/fx.csv does not run on the equity calendar:
it starts earlier, ends later, and is missing days the equity market traded --
including 2024-04-18, right before the EUR rate jumps by three cents.

That date is the whole point of this problem. When a rate is missing you may
carry the last known rate forward, because on the day itself that is all anyone
knew. You may not reach for the next available rate. Filling backwards is
free money in a backtest and a rewrite in production, and here the two answers
differ by 3%.

Run:  python3 -m pytest tests/test_p13_alignment.py
"""
import pandas as pd


def fx_rate_on(fx: pd.DataFrame, ccy: str, dates: pd.DatetimeIndex) -> pd.Series:
    """The rate that applied to `ccy` on each date in `dates`.

    The rate quoted on that date if there is one, otherwise the most recent
    rate quoted before it. Never a rate quoted after it.

    Returns
    -------
    Series of float indexed by `dates`, Series name 'rate'.
    """
    raise NotImplementedError


def add_usd_close(prices: pd.DataFrame, ref: pd.DataFrame,
                  fx: pd.DataFrame) -> pd.DataFrame:
    """Add `close_usd`: every close restated in USD.

    `rate` in fx.csv is USD per one unit of the quoted currency. Instruments
    already quoted in USD are unchanged and have no row in fx.csv. Currencies
    are in the security master -- which has the same defect it had in P06.

    Returns
    -------
    A copy of `prices` with one extra float column -- the four input columns
    plus `close_usd`, and no intermediate columns. Same rows, same order.
    Where the close is missing, close_usd is missing.
    """
    raise NotImplementedError
