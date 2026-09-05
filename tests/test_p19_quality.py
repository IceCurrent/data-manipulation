import pytest

from problems.p19_quality import flag_spikes, flag_stale, quality_report


def test_flag_stale_shape(prices):
    out = flag_stale(prices, 3)
    assert list(out.columns) == list(prices.columns) + ["stale"]
    assert list(out.index) == list(prices.index)
    assert out["stale"].dtype == bool


def test_flag_stale_finds_the_stuck_feed(prices):
    out = flag_stale(prices, 3)
    hits = out[out["stale"]]
    assert len(hits) == 5
    assert set(hits["ticker"]) == {"KO"}
    assert str(hits["date"].min().date()) == "2024-03-11"
    assert str(hits["date"].max().date()) == "2024-03-15"


def test_flag_stale_flags_the_whole_run_including_its_first_row(prices):
    out = flag_stale(prices, 3)
    ko = out[(out["ticker"] == "KO")].sort_values("date")
    run = ko[ko["stale"]]
    assert run["close"].nunique() == 1
    assert len(run) == 5


def test_flag_stale_respects_min_run(prices):
    assert int(flag_stale(prices, 5)["stale"].sum()) == 5
    assert int(flag_stale(prices, 6)["stale"].sum()) == 0


def test_flag_spikes_shape_and_values(prices):
    out = flag_spikes(prices, 0.20)
    assert list(out.columns) == list(prices.columns) + ["spike"]
    assert list(out.index) == list(prices.index)
    hits = out[out["spike"]]
    assert len(hits) == 2
    assert set(hits["ticker"]) == {"NVDA"}
    assert [str(d.date()) for d in sorted(hits["date"])] == ["2023-07-19", "2023-07-20"]


def test_flag_spikes_threshold(prices):
    assert int(flag_spikes(prices, 0.10)["spike"].sum()) == 17
    assert int(flag_spikes(prices, 0.50)["spike"].sum()) == 0


def test_quality_report_shape(prices):
    d = quality_report(prices, 3, 0.20)
    assert list(d.columns) == ["ticker", "n_stale", "n_spike",
                               "n_zero_volume", "n_nan_close"]
    assert len(d) == 10
    assert list(d.index) == list(range(10))
    assert d["ticker"].is_monotonic_increasing


def test_quality_report_values(prices):
    d = quality_report(prices, 3, 0.20).set_index("ticker")
    assert d.loc["KO"].tolist() == [5, 0, 1, 0]
    assert d.loc["NVDA"].tolist() == [0, 2, 0, 0]
    assert d.loc["XOM"].tolist() == [0, 0, 0, 3]
    assert d.loc["AAPL"].tolist() == [0, 0, 0, 0]
    assert d["n_zero_volume"].sum() == 5
