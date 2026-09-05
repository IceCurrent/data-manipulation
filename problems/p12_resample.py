"""
P12  Changing frequency                                           Med | ~25 min
Concepts: downsampling with several aggregations, compounding to a period,
          bucketing timestamps within groups
Builds on: P07 (wide panels), P10 (returns), P04 (aggregation).

Three different frequency changes. The first is a single series to weekly bars.
The second is a whole panel to monthly returns, and returns do not sum -- they
compound, which rules out a plain aggregation. The third moves in the other
direction on the intraday blotter, cutting a continuous timestamp column into
fixed buckets while keeping tickers apart.

Run:  python3 -m pytest tests/test_p12_resample.py
"""
import pandas as pd


def weekly_bars(prices: pd.DataFrame, ticker: str) -> pd.DataFrame:
    """One ticker's daily closes rolled up into weekly bars, weeks ending Friday.

    open   : first close of the week          high : highest close of the week
    low    : lowest close of the week         close: last close of the week
    volume : total volume over the week

    Weeks with no sessions do not appear.

    Returns
    -------
    DataFrame indexed by week-ending date (index name 'date'), with columns
    exactly ['open', 'high', 'low', 'close', 'volume'].
    """
    raise NotImplementedError


def monthly_returns(prices: pd.DataFrame) -> pd.DataFrame:
    """Every ticker's total return within each calendar month.

    Compound that month's simple daily returns. A month's figure is the return
    of holding the ticker from the last session of the previous month to the
    last session of this one.

    Returns
    -------
    DataFrame indexed by calendar month-end date, one column per ticker sorted
    ascending, float values.
    """
    raise NotImplementedError


def intraday_notional(trades: pd.DataFrame, freq: str) -> pd.DataFrame:
    """Cash traded per ticker per time bucket.

    `freq` is a pandas offset string such as '5min'. Sum the ABSOLUTE notional
    of filled trades falling in each bucket. Only report (bucket, ticker) pairs
    that actually have trades.

    Returns
    -------
    DataFrame with columns exactly ['bucket', 'ticker', 'notional'], where
    `bucket` is the timestamp at the start of the interval. Sorted by bucket
    then ticker, with a fresh 0..n-1 index.
    """
    raise NotImplementedError
