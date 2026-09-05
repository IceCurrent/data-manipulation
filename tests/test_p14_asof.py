import pandas as pd
import pytest

from problems.p14_asof import attach_prevailing_quote, slippage_bps

TOL = pd.Timedelta("30min")


def test_attach_quote_shape(trades, quotes):
    d = attach_prevailing_quote(trades, quotes, TOL)
    assert len(d) == 3028
    assert list(d.index) == list(range(3028))
    for c in ["quote_ts", "bid", "ask", "mid"]:
        assert c in d.columns
    assert d["timestamp"].is_monotonic_increasing


def test_attach_quote_never_uses_a_later_quote(trades, quotes):
    d = attach_prevailing_quote(trades, quotes, TOL).dropna(subset=["quote_ts"])
    assert (d["quote_ts"] <= d["timestamp"]).all()


def test_attach_quote_respects_the_tolerance(trades, quotes):
    d = attach_prevailing_quote(trades, quotes, TOL)
    matched = d.dropna(subset=["quote_ts"])
    assert ((matched["timestamp"] - matched["quote_ts"]) <= TOL).all()
    # Without a tolerance every trade matches something, including quotes from
    # the previous afternoon, and the quote outage stays invisible.
    assert int(d["mid"].isna().sum()) == 88


def test_attach_quote_finds_the_tape_outage(trades, quotes):
    d = attach_prevailing_quote(trades, quotes, TOL)
    ko = d[(d["ticker"] == "KO") &
           (d["timestamp"].dt.normalize() == pd.Timestamp("2024-12-05"))]
    assert len(ko) == 10
    assert int(ko["mid"].isna().sum()) == 2


def test_attach_quote_matches_per_ticker(trades, quotes):
    d = attach_prevailing_quote(trades, quotes, TOL).dropna(subset=["mid"])
    assert (d["mid"] == (d["bid"] + d["ask"]) / 2).all()
    # a quote attached to the wrong instrument would be nowhere near the fill
    assert ((d["price"] - d["mid"]).abs() / d["mid"] < 0.05).all()


def test_slippage_shape(trades, quotes):
    s = slippage_bps(trades, quotes, TOL)
    assert isinstance(s, pd.Series)
    assert s.name == "slippage_bps"
    assert len(s) == 10
    assert list(s.index) == sorted(s.index)


def test_slippage_values(trades, quotes):
    s = slippage_bps(trades, quotes, TOL)
    assert s["AAPL"] == pytest.approx(0.511955, rel=1e-4)
    assert s["KO"] == pytest.approx(2.451400, rel=1e-4)
    assert s["NVDA"] == pytest.approx(-0.092071, rel=1e-4)


def test_slippage_is_signed_by_side_not_by_price_level(trades, quotes):
    d = attach_prevailing_quote(trades, quotes, TOL).dropna(subset=["mid"])
    buys = d[(d["side"] == "BUY") & (d["price"] > d["mid"])]
    sells = d[(d["side"] == "SELL") & (d["price"] > d["mid"])]
    assert len(buys) > 0 and len(sells) > 0   # both exist, so sign must depend on side
