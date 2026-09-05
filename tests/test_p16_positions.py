import pytest

from problems.p16_positions import eod_positions, largest_position_day


def test_eod_positions_shape(trades):
    d = eod_positions(trades)
    assert list(d.columns) == ["date", "ticker", "position"]
    assert d["ticker"].nunique() == 10
    assert d["date"].nunique() == 44
    assert len(d) == 440           # every ticker on every session
    assert list(d.index) == list(range(440))


def test_eod_positions_carries_forward_on_quiet_days(trades):
    d = eod_positions(trades)
    for _, g in d.groupby("ticker"):
        assert g["date"].is_monotonic_increasing
        assert g["position"].notna().all()


def test_eod_positions_excludes_double_bookings(trades):
    # Leaving the repeated rows in inflates AAPL's final position to 84990.
    d = eod_positions(trades)
    final = d.groupby("ticker").tail(1).set_index("ticker")["position"]
    assert final["AAPL"] == pytest.approx(88890.0)
    assert final["MSFT"] == pytest.approx(-49855.0)
    assert final["TSLA"] == pytest.approx(-344.0)


def test_eod_positions_values(trades):
    d = eod_positions(trades).set_index(["ticker", "date"])["position"]
    assert d.loc[("AAPL", "2024-10-29")] == pytest.approx(-629.0)
    assert d.loc[("AAPL", "2024-11-15")] == pytest.approx(34076.0)


def test_largest_position_day_shape(trades):
    d = largest_position_day(trades)
    assert list(d.columns) == ["ticker", "date", "position"]
    assert len(d) == 10
    assert list(d.index) == list(range(10))
    assert d["ticker"].tolist() == sorted(d["ticker"])


def test_largest_position_day_values(trades):
    d = largest_position_day(trades).set_index("ticker")
    assert d.loc["AAPL", "position"] == pytest.approx(88890.0)
    assert str(d.loc["AAPL", "date"].date()) == "2024-12-31"
    assert d.loc["XOM", "position"] == pytest.approx(-41812.0)
    assert str(d.loc["XOM", "date"].date()) == "2024-11-20"


def test_largest_position_day_reports_signed_positions(trades):
    d = largest_position_day(trades)
    assert (d["position"] < 0).any()
