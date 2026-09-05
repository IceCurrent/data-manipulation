import pytest

from problems.p09_duplicates import (drop_double_bookings,
                                     last_trade_price_per_ticker_day)


def test_drop_double_bookings_removes_exactly_the_repeated_rows(trades):
    d = drop_double_bookings(trades)
    assert len(d) == 3054
    assert not d.duplicated().any()


def test_drop_double_bookings_keeps_multi_venue_legs(trades):
    d = drop_double_bookings(trades)
    # deduplicating on trade_id alone would take these out and lose the shares
    assert int(d["trade_id"].duplicated().sum()) == 15


def test_drop_double_bookings_shape(trades):
    d = drop_double_bookings(trades)
    assert list(d.columns) == list(trades.columns)
    assert list(d.index) == list(range(len(d)))


def test_last_trade_price_shape(trades):
    d = last_trade_price_per_ticker_day(trades)
    assert list(d.columns) == ["date", "ticker", "price"]
    assert len(d) == 440
    assert list(d.index) == list(range(440))
    assert d["date"].is_monotonic_increasing


def test_last_trade_price_values(trades):
    d = last_trade_price_per_ticker_day(trades).set_index(["date", "ticker"])["price"]
    assert d.loc[("2024-12-31", "AAPL")] == pytest.approx(404.1421)
    assert d.loc[("2024-10-29", "GS")] == pytest.approx(475.7826)


def test_last_trade_price_really_is_the_last_one(trades):
    d = last_trade_price_per_ticker_day(trades)
    src = trades.dropna(subset=["price"]).copy()
    src["date"] = src["timestamp"].dt.normalize()
    latest = src.loc[src.groupby(["ticker", "date"])["timestamp"].idxmax()]
    merged = d.merge(latest[["date", "ticker", "timestamp"]], on=["date", "ticker"])
    assert len(merged) == 440
