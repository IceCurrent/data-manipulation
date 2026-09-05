"""
P19  Data quality report                                Med, composite | ~25 min
Concepts: consecutive-run detection, thresholds on returns, summarising flags
Builds on: P10 (returns), P05 (per-group work), P04 (aggregation).

The last one, and the most interview-shaped: you have been handed a price file
and asked whether it can be trusted. Three defects to find.

A stale feed is the interesting one. Any single unchanged close is unremarkable
-- illiquid names do that. What matters is a RUN of them, and finding runs
means labelling each stretch of consecutive identical closes so you can measure
how long it is. There is a short, standard way to do this with a comparison
against the previous row and a cumulative sum, and it is worth knowing because
the same trick answers a whole family of "consecutive" questions.

A price spike is a move too large to be real. And a zero-volume session on a
liquid name means the feed dropped, not that nobody traded.

Run:  python3 -m pytest tests/test_p19_quality.py
"""
import pandas as pd


def flag_stale(prices: pd.DataFrame, min_run: int) -> pd.DataFrame:
    """Add `stale`: True where this row belongs to a run of at least `min_run`
    consecutive sessions with an identical close for that ticker.

    A run is a maximal stretch of consecutive sessions for one ticker whose
    closes are all equal. Every row in a long enough run is flagged, including
    the first. Rows with a missing close are never flagged.

    Returns
    -------
    A copy of `prices` with one extra boolean column. Same rows, same order.
    """
    raise NotImplementedError


def flag_spikes(prices: pd.DataFrame, threshold: float) -> pd.DataFrame:
    """Add `spike`: True where the simple return against the ticker's previous
    available session exceeds `threshold` in absolute value.

    Rows with no computable return are not flagged.

    Returns
    -------
    A copy of `prices` with one extra boolean column -- the four input columns
    plus `spike`, and no intermediate columns. Same rows, same order.
    """
    raise NotImplementedError


def quality_report(prices: pd.DataFrame, min_run: int,
                   threshold: float) -> pd.DataFrame:
    """One row per ticker counting every defect found.

    n_stale        : rows flagged by flag_stale
    n_spike        : rows flagged by flag_spikes
    n_zero_volume  : sessions with zero volume
    n_nan_close    : rows whose close is missing

    Returns
    -------
    DataFrame with columns exactly ['ticker', 'n_stale', 'n_spike',
    'n_zero_volume', 'n_nan_close'], one row per ticker sorted ascending, with
    a fresh 0..n-1 index. All four counts are integers.
    """
    raise NotImplementedError
