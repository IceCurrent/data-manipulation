"""
P17  Mark-to-market P&L                                 Med, composite | ~30 min
Concepts: lagging within groups, multi-key joins, aggregation, per-group top-N
Builds on: P10 (lags), P06 (multi-key joins), P12 (monthly periods), P03 (top-N).

The daily P&L of a book is the position it was holding, multiplied by the price
move that happened to it. Which is one line of arithmetic and one decision:
which position.

Today's position already includes today's trades, so multiplying it by today's
price move credits the book for a move it was not in the whole time. The
position that earned today's move is yesterday's. Getting this backwards is the
classic error in P&L attribution and it is the thing being tested here.

Missing prices show up again -- some holdings are on foreign calendars and have
no price on some days. A day with no price move contributes nothing rather
than making the whole book's P&L disappear.

Run:  python3 -m pytest tests/test_p17_pnl.py
"""
import pandas as pd


def daily_pnl(positions: pd.DataFrame, prices: pd.DataFrame) -> pd.DataFrame:
    """Mark-to-market P&L per book per day.

    For each (date, book), sum across tickers of

        position held at the previous close  x  (close today - close before)

    where "the close before" is the ticker's own previous available close. A
    ticker contributes zero on days where either piece is unavailable.

    The earliest date in `positions` has no previous position and is excluded
    from the result entirely.

    Returns
    -------
    DataFrame with columns exactly ['date', 'book', 'pnl'], sorted by date then
    book, with a fresh 0..n-1 index.
    """
    raise NotImplementedError


def top_contributors(positions: pd.DataFrame, prices: pd.DataFrame,
                     n: int) -> pd.DataFrame:
    """The `n` biggest P&L contributors in each book in each calendar month.

    Rank by that ticker's total P&L contribution over the month, largest first.
    Same P&L convention as above. Books holding fewer than `n` tickers in a
    month contribute however many they have.

    Returns
    -------
    DataFrame with columns exactly ['month', 'book', 'ticker', 'pnl'], where
    `month` is the calendar month-end date as a Timestamp. Sorted by month,
    then book, then pnl descending, with a fresh 0..n-1 index.
    """
    raise NotImplementedError
