import pandas as pd
import pytest

from problems.p11_rolling import (add_rolling_vol, add_rolling_zscore,
                                  most_volatile_window)


def test_rolling_vol_shape(prices):
    out = add_rolling_vol(prices, 20)
    assert list(out.columns) == list(prices.columns) + ["roll_vol"]
    assert list(out.index) == list(prices.index)


def test_rolling_vol_requires_a_complete_window(prices):
    out = add_rolling_vol(prices, 20)
    for _, g in out.groupby("ticker", sort=False):
        assert g["roll_vol"].iloc[:20].isna().all()
        assert g["roll_vol"].notna().any()
    assert int(out["roll_vol"].isna().sum()) == 263


def test_rolling_vol_values(prices):
    out = add_rolling_vol(prices, 20)
    v = out[(out["ticker"] == "AAPL") & (out["date"] == "2024-06-03")]["roll_vol"].iloc[0]
    assert v == pytest.approx(0.35907361, rel=1e-6)


def test_rolling_vol_ranks_the_names_sensibly(prices):
    m = add_rolling_vol(prices, 20).groupby("ticker")["roll_vol"].mean()
    assert m["NVDA"] == pytest.approx(0.5927, abs=5e-4)
    assert m["KO"] == pytest.approx(0.1861, abs=5e-4)
    assert m["NVDA"] > m["AAPL"] > m["KO"]


def test_rolling_vol_scales_with_the_annualisation_factor(prices):
    a = add_rolling_vol(prices, 20, 252)["roll_vol"]
    b = add_rolling_vol(prices, 20, 1)["roll_vol"]
    assert (a / b).dropna().std() < 1e-9


def test_rolling_zscore(prices):
    out = add_rolling_zscore(prices, 20)
    assert list(out.index) == list(prices.index)
    v = out[(out["ticker"] == "NVDA") & (out["date"] == "2024-06-03")]["close_z"].iloc[0]
    assert v == pytest.approx(0.40069576, rel=1e-6)
    for _, g in out.groupby("ticker", sort=False):
        assert g["close_z"].iloc[:19].isna().all()


def test_most_volatile_window(prices):
    got = most_volatile_window(prices, 20)
    assert isinstance(got, tuple) and len(got) == 2
    assert got[0] == "NVDA"
    assert pd.Timestamp(got[1]) == pd.Timestamp("2023-07-20")
