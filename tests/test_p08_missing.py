import pytest

from problems.p08_missing import (filled_trades, missing_close_report,
                                  reindexed_close)


def test_filled_trades_keeps_rows_whose_only_gap_is_the_venue(trades):
    d = filled_trades(trades)
    assert len(d) == 3028          # a blanket dropna() would leave 3007
    assert int(d["venue"].isna().sum()) == 21


def test_filled_trades_shape(trades):
    d = filled_trades(trades)
    assert list(d.columns) == list(trades.columns)
    assert list(d.index) == list(range(len(d)))
    assert d["qty"].notna().all() and d["price"].notna().all()


def test_reindexed_close_covers_the_whole_calendar(prices, calendar):
    s = reindexed_close(prices, "SAP.DE", calendar, 5)
    assert len(s) == 502
    assert s.index.equals(calendar)
    assert s.name == "close"


def test_reindexed_close_fills_a_one_day_holiday(prices, calendar):
    s = reindexed_close(prices, "SAP.DE", calendar, 5)
    assert s.loc["2024-05-01"] == pytest.approx(s.loc["2024-04-30"])
    assert int(s.isna().sum()) == 0


def test_reindexed_close_stops_filling_at_max_gap(prices, calendar):
    # SHEL.L is suspended for six consecutive sessions.
    assert int(reindexed_close(prices, "SHEL.L", calendar, 1).isna().sum()) == 5
    assert int(reindexed_close(prices, "SHEL.L", calendar, 2).isna().sum()) == 4
    assert int(reindexed_close(prices, "SHEL.L", calendar, 5).isna().sum()) == 1
    assert int(reindexed_close(prices, "SHEL.L", calendar, 6).isna().sum()) == 0


def test_missing_close_report_shape(prices, calendar):
    d = missing_close_report(prices, calendar)
    assert list(d.columns) == ["ticker", "n_missing_rows", "n_nan_close"]
    assert len(d) == 10
    assert list(d.index) == list(range(10))
    assert d["ticker"].is_monotonic_increasing


def test_missing_close_report_separates_the_two_kinds_of_gap(prices, calendar):
    d = missing_close_report(prices, calendar).set_index("ticker")
    assert d.loc["SAP.DE", "n_missing_rows"] == 9
    assert d.loc["SAP.DE", "n_nan_close"] == 0
    assert d.loc["SHEL.L", "n_missing_rows"] == 15
    assert d.loc["XOM", "n_missing_rows"] == 0
    assert d.loc["XOM", "n_nan_close"] == 3
    assert d.loc["AAPL", "n_missing_rows"] == 0
    assert d.loc["AAPL", "n_nan_close"] == 0
