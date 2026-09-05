import pytest

from problems.p12_resample import (intraday_notional, monthly_returns,
                                   weekly_bars)


def test_weekly_bars_shape(prices):
    d = weekly_bars(prices, "AAPL")
    assert list(d.columns) == ["open", "high", "low", "close", "volume"]
    assert len(d) == 105
    assert d.index.name == "date"
    assert d.index.is_monotonic_increasing


def test_weekly_bars_values(prices):
    d = weekly_bars(prices, "AAPL")
    row = d.loc["2024-06-07"]
    assert row["open"] == pytest.approx(264.7558)
    assert row["high"] == pytest.approx(273.9053)
    assert row["low"] == pytest.approx(263.9087)
    assert row["close"] == pytest.approx(273.3813)
    assert row["volume"] == pytest.approx(306467656)


def test_weekly_bars_are_internally_consistent(prices):
    d = weekly_bars(prices, "NVDA")
    assert (d["high"] >= d["low"]).all()
    assert (d["high"] >= d[["open", "close"]].max(axis=1)).all()
    assert d["volume"].sum() == prices[prices["ticker"] == "NVDA"]["volume"].sum()


def test_monthly_returns_shape(prices):
    d = monthly_returns(prices)
    assert d.shape == (24, 10)
    assert list(d.columns) == sorted(prices["ticker"].unique())
    assert str(d.index[0].date()) == "2023-01-31"


def test_monthly_returns_compound_rather_than_sum(prices):
    d = monthly_returns(prices)
    assert d.loc["2024-06-30", "NVDA"] == pytest.approx(0.07967707, rel=1e-6)
    assert d.loc["2023-01-31", "AAPL"] == pytest.approx(0.01766953, rel=1e-6)


def test_intraday_notional_shape(trades):
    d = intraday_notional(trades, "5min")
    assert list(d.columns) == ["bucket", "ticker", "notional"]
    assert len(d) == 2880
    assert list(d.index) == list(range(2880))
    assert d["bucket"].is_monotonic_increasing


def test_intraday_notional_conserves_cash(trades):
    d = intraday_notional(trades, "5min")
    assert d["notional"].sum() == pytest.approx(1798309978.8419, rel=1e-9)


def test_intraday_notional_buckets_are_aligned_to_the_frequency(trades):
    d = intraday_notional(trades, "5min")
    assert (d["bucket"].dt.minute % 5 == 0).all()
    assert (d["bucket"].dt.second == 0).all()
    coarse = intraday_notional(trades, "30min")
    assert len(coarse) < len(d)
    assert coarse["notional"].sum() == pytest.approx(d["notional"].sum(), rel=1e-9)
