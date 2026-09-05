"""
P16  From blotter to positions                          Med, composite | ~30 min
Concepts: cleaning, signing, cumulative sums, carrying forward across a calendar
Builds on: P02, P09, P08, P10.

Reconstruct the end-of-day share position in each ticker from the trade
blotter. Nothing here is individually hard; the work is doing the steps in an
order that survives the data.

Two traps, both already met earlier in the set. The double-booked rows from P09
are still in this file and each one you leave in overstates a position by a
whole trade. And a ticker's position on a day it did not trade is not zero and
not missing -- it is whatever it was the day before.

Start every ticker flat before its first session, and report every session in
the blotter for every ticker, whether or not it traded that day.

Run:  python3 -m pytest tests/test_p16_positions.py
"""
import pandas as pd


def eod_positions(trades: pd.DataFrame) -> pd.DataFrame:
    """End-of-day share position per ticker per session.

    Sessions are the distinct calendar dates appearing in the blotter. Every
    ticker gets a row for every one of them. Buys add, sells subtract, and
    unfilled orders do not count.

    Returns
    -------
    DataFrame with columns exactly ['date', 'ticker', 'position'], `position`
    a float, sorted by ticker then date, with a fresh 0..n-1 index.
    """
    raise NotImplementedError


def largest_position_day(trades: pd.DataFrame) -> pd.DataFrame:
    """For each ticker, the session on which its position was largest in
    absolute terms, and the position it held.

    Report the signed position, not its absolute value: the largest exposure
    may well be a short.

    Returns
    -------
    DataFrame with columns exactly ['ticker', 'date', 'position'], one row per
    ticker sorted ascending, with a fresh 0..n-1 index.
    """
    raise NotImplementedError
