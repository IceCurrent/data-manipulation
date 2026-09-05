import numpy as np
import pandas as pd
import pytest

from problems.p01_selection import (close_series, high_volume_days,
                                    last_n_sessions, price_on)


def test_close_series_shape_and_labels(prices):
    s = close_series(prices, "AAPL")
    assert isinstance(s, pd.Series)
    assert len(s) == 502
    assert s.index.name == "date" and s.name == "close"


def test_close_series_is_sorted_and_correct(prices):
    s = close_series(prices, "AAPL")
    assert s.index.is_monotonic_increasing
    assert s.iloc[0] == pytest.approx(128.0)
    assert s.iloc[-1] == pytest.approx(403.3772)


def test_close_series_respects_a_short_calendar(prices):
    assert len(close_series(prices, "SAP.DE")) == 493


def test_high_volume_days(prices):
    d = high_volume_days(prices, "NVDA", 1_500_000_000)
    assert len(d) == 7
    assert list(d.columns) == list(prices.columns)
    assert list(d.index) == list(range(7))
    assert d["date"].is_monotonic_increasing
    assert str(d["date"].iloc[0].date()) == "2023-01-09"
    assert (d["volume"] >= 1_500_000_000).all()


def test_price_on_returns_a_float(prices):
    assert price_on(prices, "AAPL", "2024-06-03") == pytest.approx(264.7558)


def test_price_on_missing_row_is_nan(prices):
    assert np.isnan(price_on(prices, "SAP.DE", "2024-05-01"))


def test_price_on_missing_value_is_nan(prices):
    assert np.isnan(price_on(prices, "XOM", "2024-02-07"))


def test_last_n_sessions(prices):
    d = last_n_sessions(prices, "KO", 5)
    assert len(d) == 5
    assert list(d.index) == [0, 1, 2, 3, 4]
    assert [str(x.date()) for x in d["date"]] == [
        "2024-12-24", "2024-12-26", "2024-12-27", "2024-12-30", "2024-12-31"]
    assert d["close"].iloc[-1] == pytest.approx(69.7828)
