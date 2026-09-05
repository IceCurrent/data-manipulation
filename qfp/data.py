"""
Loaders for the synthetic datasets in data/.

Every loader re-reads the CSV and hands back a fresh object, so you can mutate
whatever you get without affecting anything else. Loaders parse dtypes and
nothing more -- in particular they do NOT sort, deduplicate or clean. The files
are meant to arrive the way real exports arrive.

    from qfp.data import load_prices, load_trades
    px = load_prices()
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd

DATA = Path(__file__).resolve().parent.parent / "data"


def load_prices() -> pd.DataFrame:
    """Daily closes and volume, long format.

    Columns: date (datetime64), ticker (str), close (float), volume (int).
    Ten tickers, 2023-01-03 to 2024-12-31. Two tickers observe local holidays
    and are simply absent on those dates. Some rows are present but have a
    missing close.
    """
    return pd.read_csv(DATA / "prices.csv", parse_dates=["date"])


def load_benchmark() -> pd.DataFrame:
    """Daily index level on the full US trading calendar.

    Columns: date (datetime64), close (float). This is the canonical session
    list -- it has a row for every trading day in the sample.
    """
    return pd.read_csv(DATA / "benchmark.csv", parse_dates=["date"])


def load_ref() -> pd.DataFrame:
    """Security master.

    Columns: ticker, name, sector, currency (str), lot_size (int).
    Sourced from a vendor feed, with the imperfections that implies.
    """
    return pd.read_csv(DATA / "ref.csv")


def load_fx() -> pd.DataFrame:
    """Daily FX rates, long format.

    Columns: date (datetime64), ccy (str), rate (float).
    `rate` is USD per 1 unit of `ccy`. Only EUR and GBP are quoted. The FX
    calendar is not the equity calendar.
    """
    return pd.read_csv(DATA / "fx.csv", parse_dates=["date"])


def load_positions() -> pd.DataFrame:
    """End-of-day share positions per book.

    Columns: date (datetime64), book (str), ticker (str), qty (int).
    Positions may be long or short.
    """
    return pd.read_csv(DATA / "positions.csv", parse_dates=["date"])


def load_risk_wide() -> pd.DataFrame:
    """Month-end factor exposures per book, one column per factor.

    Columns: date (datetime64), book (str), MKT, SIZE, VALUE, MOM, QUALITY (float).
    """
    return pd.read_csv(DATA / "risk_wide.csv", parse_dates=["date"])


def load_trades() -> pd.DataFrame:
    """Trade blotter for the last ~44 sessions of the sample.

    Columns: trade_id (str), timestamp (datetime64), ticker (str),
    side ('BUY'/'SELL'), qty (float), price (float), trader (str), venue (str).

    Exported in no particular order. qty and price are floats because some
    orders were never filled.
    """
    return pd.read_csv(DATA / "trades.csv", parse_dates=["timestamp"])


def load_quotes() -> pd.DataFrame:
    """Top-of-book quote tape over the same sessions as the blotter.

    Columns: timestamp (datetime64), ticker (str), bid (float), ask (float).
    Irregularly spaced, and exported in no particular order.
    """
    return pd.read_csv(DATA / "quotes.csv", parse_dates=["timestamp"])
