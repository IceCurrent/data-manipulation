"""
P14  Point-in-time joins                                          Med | ~25 min
Concepts: joining on nearest-earlier key, per-group as-of matching, tolerance
Builds on: P13 (as-of lookups), P09 (ordering), P06 (joins).

Every trade needs the market it was executed into: the top-of-book quote that
was standing at the moment it printed. The keys do not match -- a trade at
10:47:13 has no quote at 10:47:13 -- so this is a join on "most recent at or
before", per ticker.

Both files are exported unordered, and this kind of join will refuse to run
until you fix that.

The `tolerance` argument is not decoration. Without a limit, a trade at 09:41
will happily match a quote from the previous afternoon and you will get a full
result set with no missing values and no indication that anything is wrong. The
quote tape has an outage in it. With a tolerance, you find it.

Run:  python3 -m pytest tests/test_p14_asof.py
"""
import pandas as pd


def attach_prevailing_quote(trades: pd.DataFrame, quotes: pd.DataFrame,
                            tolerance: pd.Timedelta) -> pd.DataFrame:
    """Attach the quote that was standing when each filled trade printed.

    For each filled trade, take that ticker's most recent quote at or before
    the trade timestamp, provided it is no more than `tolerance` old. Where
    there is no such quote, the quote fields are missing.

    Returns
    -------
    DataFrame with the eight trade columns plus ['quote_ts', 'bid', 'ask',
    'mid'], where mid is the midpoint of bid and ask. One row per filled trade,
    sorted by timestamp then trade_id, with a fresh 0..n-1 index.
    """
    raise NotImplementedError


def slippage_bps(trades: pd.DataFrame, quotes: pd.DataFrame,
                 tolerance: pd.Timedelta) -> pd.Series:
    """Average execution slippage against the prevailing mid, per ticker.

    Slippage is positive when the trade was worse than the mid: a buy filled
    above it, or a sell filled below it. Express it in basis points of the mid,
    so (price - mid) / mid * 10000 for a buy, and the negative of that for a
    sell. Then average over each ticker's trades.

    Trades with no quote inside the tolerance are excluded.

    Returns
    -------
    Series of float indexed by ticker ascending, Series name 'slippage_bps'.
    """
    raise NotImplementedError
