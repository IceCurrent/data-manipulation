import pandas as pd
import pytest

from problems.p13_alignment import add_usd_close, fx_rate_on


def test_fx_rate_on_shape(fx, calendar):
    s = fx_rate_on(fx, "EUR", calendar)
    assert len(s) == len(calendar)
    assert s.index.equals(calendar)
    assert s.name == "rate"
    assert s.notna().all()


def test_fx_rate_on_uses_a_quoted_rate_when_there_is_one(fx):
    idx = pd.DatetimeIndex(["2024-04-17", "2024-04-19"])
    s = fx_rate_on(fx, "EUR", idx)
    assert s.loc["2024-04-17"] == pytest.approx(1.066152)
    assert s.loc["2024-04-19"] == pytest.approx(1.099991)


def test_fx_rate_on_does_not_look_ahead(fx):
    # 2024-04-18 has no quote, and the next one is three cents higher.
    idx = pd.DatetimeIndex(["2024-04-17", "2024-04-18", "2024-04-19"])
    s = fx_rate_on(fx, "EUR", idx)
    assert s.loc["2024-04-18"] == pytest.approx(1.066152)
    assert s.loc["2024-04-18"] != pytest.approx(1.099991)


def test_add_usd_close_shape(prices, ref, fx):
    out = add_usd_close(prices, ref, fx)
    assert list(out.columns) == list(prices.columns) + ["close_usd"]
    assert len(out) == len(prices)
    assert list(out.index) == list(prices.index)


def test_add_usd_close_leaves_usd_instruments_alone(prices, ref, fx):
    out = add_usd_close(prices, ref, fx)
    usd = out[out["ticker"].isin(["AAPL", "JPM", "KO"])]
    assert (usd["close_usd"] == usd["close"]).all()


def test_add_usd_close_converts_foreign_instruments(prices, ref, fx):
    out = add_usd_close(prices, ref, fx)
    row = out[(out["ticker"] == "SAP.DE") & (out["date"] == "2024-04-18")]
    assert float(row["close_usd"].iloc[0]) == pytest.approx(101.928822, rel=1e-7)
    row = out[(out["ticker"] == "SHEL.L") & (out["date"] == "2024-12-31")]
    assert float(row["close_usd"].iloc[0]) == pytest.approx(27.028968, rel=1e-7)


def test_add_usd_close_propagates_missing_closes(prices, ref, fx):
    out = add_usd_close(prices, ref, fx)
    assert int(out["close_usd"].isna().sum()) == 3
