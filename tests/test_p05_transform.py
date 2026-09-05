import pytest

from problems.p05_transform import (add_cross_sectional_zscore,
                                    add_share_of_ticker_notional,
                                    add_volume_vs_ticker_mean)


def test_volume_vs_mean_preserves_row_order(prices):
    out = add_volume_vs_ticker_mean(prices)
    assert list(out.index) == list(prices.index)
    assert out["ticker"].tolist() == prices["ticker"].tolist()
    assert out["volume"].tolist() == prices["volume"].tolist()


def test_volume_vs_mean_values(prices):
    out = add_volume_vs_ticker_mean(prices)
    row = out[(out["ticker"] == "AAPL") & (out["date"] == "2023-01-03")]
    assert float(row["vol_vs_mean"].iloc[0]) == pytest.approx(5842901.3825, rel=1e-8)


def test_volume_vs_mean_sums_to_zero_within_each_ticker(prices):
    out = add_volume_vs_ticker_mean(prices)
    resid = out.groupby("ticker")["vol_vs_mean"].sum().abs()
    scale = out.groupby("ticker")["volume"].mean()
    assert (resid / scale).max() < 1e-9


def test_share_of_ticker_preserves_row_order(trades):
    out = add_share_of_ticker_notional(trades)
    assert list(out.index) == list(trades.index)
    assert out["trade_id"].tolist() == trades["trade_id"].tolist()


def test_share_of_ticker_sums_to_one_per_ticker(trades):
    out = add_share_of_ticker_notional(trades)
    s = out.groupby("ticker")["share_of_ticker"].sum()
    assert len(s) == 10
    assert s.sub(1.0).abs().max() < 1e-9


def test_share_of_ticker_is_missing_where_notional_is(trades):
    out = add_share_of_ticker_notional(trades)
    assert int(out["share_of_ticker"].isna().sum()) == 52


def test_zscore_preserves_row_order(prices):
    out = add_cross_sectional_zscore(prices)
    assert list(out.index) == list(prices.index)
    assert out["volume"].tolist() == prices["volume"].tolist()


def test_zscore_is_centred_within_each_date(prices):
    out = add_cross_sectional_zscore(prices)
    assert out.groupby("date")["vol_z"].mean().abs().max() < 1e-9


def test_zscore_values(prices):
    out = add_cross_sectional_zscore(prices)
    row = out[(out["ticker"] == "NVDA") & (out["date"] == "2024-06-03")]
    assert float(row["vol_z"].iloc[0]) == pytest.approx(2.786967, rel=1e-5)
