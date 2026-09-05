"""
P10  Returns on a panel                                           Med | ~20 min
Concepts: within-group differencing, missing-value propagation, compounding
Builds on: P05 (per-group operations), P08.

This is the single most common thing anyone does to a price panel, and the
single most common place to get it wrong. prices.csv is stacked ticker by
ticker, so the row above the first AAPL row is the last GS row. Any operation
that looks backwards one row has to be told where one ticker ends and the next
begins.

Second thing: a return computed against a missing close is not a return. Where
either end of the move is missing, so is the answer -- pandas will not do this
for you by default.

Run:  python3 -m pytest tests/test_p10_returns.py
"""
import pandas as pd


def add_simple_returns(prices: pd.DataFrame) -> pd.DataFrame:
    """Add `ret`: the simple return against the ticker's own previous
    available session.

    A ticker's first session has no return. If either close involved in the
    move is missing, the return is missing. Where a ticker skipped sessions,
    the move spans the gap -- previous available, not previous calendar day.

    Returns
    -------
    A copy of `prices` with one extra float column. Same rows, same order.
    """
    raise NotImplementedError


def add_log_returns(prices: pd.DataFrame) -> pd.DataFrame:
    """Add `log_ret`: the natural log return, same conventions as above.

    Returns
    -------
    A copy of `prices` with one extra float column. Same rows, same order.
    """
    raise NotImplementedError


def cumulative_return(prices: pd.DataFrame, ticker: str,
                      start: str, end: str) -> float:
    """The total return of one ticker over a date window, inclusive.

    Compound the simple daily returns whose date falls in [start, end], and
    subtract 1. Missing returns inside the window contribute nothing.

    Returns
    -------
    float. 0.15 means the ticker gained 15% over the window.
    """
    raise NotImplementedError
