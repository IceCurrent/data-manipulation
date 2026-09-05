import pytest

from problems.p03_sorting_topn import (busiest_sessions,
                                       top_volume_days_per_ticker,
                                       volume_rank_within_date)


def test_busiest_sessions(prices):
    d = busiest_sessions(prices, 5)
    assert len(d) == 5
    assert list(d.index) == [0, 1, 2, 3, 4]
    assert list(d.columns) == list(prices.columns)
    assert d["volume"].tolist() == [3199011314, 2167976019, 1755055843,
                                    1729687729, 1632716340]


def test_top_volume_days_per_ticker_covers_every_ticker(prices):
    d = top_volume_days_per_ticker(prices, 3)
    assert len(d) == 30
    assert d.groupby("ticker").size().nunique() == 1
    assert list(d.index) == list(range(30))


def test_top_volume_days_per_ticker_ordering_and_values(prices):
    d = top_volume_days_per_ticker(prices, 3)
    assert d["ticker"].tolist()[:3] == ["AAPL", "AAPL", "AAPL"]
    assert d["volume"].tolist()[:3] == [285131428, 274414516, 260895120]
    for _, g in d.groupby("ticker"):
        assert g["volume"].is_monotonic_decreasing


def test_volume_rank_preserves_the_frame(prices):
    out = volume_rank_within_date(prices)
    assert list(out.index) == list(prices.index)
    assert out["volume"].tolist() == prices["volume"].tolist()


def test_volume_rank_values(prices):
    out = volume_rank_within_date(prices)
    row = out[(out["ticker"] == "NVDA") & (out["date"] == "2024-06-03")]
    assert float(row["volume_rank"].iloc[0]) == pytest.approx(1.0)
    assert out["volume_rank"].min() == pytest.approx(1.0)
    assert out["volume_rank"].max() == pytest.approx(10.0)


def test_volume_rank_adapts_to_days_with_fewer_tickers(prices):
    out = volume_rank_within_date(prices)
    day = out[out["date"] == "2024-05-01"]
    assert len(day) == 9
    assert sorted(day["volume_rank"].tolist()) == [float(i) for i in range(1, 10)]
