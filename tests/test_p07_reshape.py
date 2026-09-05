import pytest

from problems.p07_reshape import close_panel, melt_risk, sector_avg_volume


def test_close_panel_shape(prices):
    d = close_panel(prices)
    assert d.shape == (502, 10)
    assert list(d.columns) == ["AAPL", "GS", "JPM", "KO", "MSFT", "NVDA",
                               "PG", "SAP.DE", "SHEL.L", "XOM"]
    assert d.index.name == "date"
    assert d.index.is_monotonic_increasing


def test_close_panel_values(prices):
    d = close_panel(prices)
    assert d.loc["2024-06-03", "NVDA"] == pytest.approx(535.3414)
    assert d.loc["2023-01-03", "AAPL"] == pytest.approx(128.0)


def test_close_panel_marks_absent_sessions(prices):
    d = close_panel(prices)
    nan = d.isna().sum().to_dict()
    assert nan["AAPL"] == 0
    assert nan["SAP.DE"] == 9
    assert nan["SHEL.L"] == 15
    assert nan["XOM"] == 3


def test_sector_avg_volume_shape(prices, ref):
    d = sector_avg_volume(prices, ref)
    assert d.shape == (502, 4)
    assert list(d.columns) == ["Energy", "Financials", "Staples", "Technology"]
    assert d.index.name == "date"


def test_sector_avg_volume_values(prices, ref):
    d = sector_avg_volume(prices, ref)
    assert d.loc["2024-06-03", "Technology"] == pytest.approx(174321294.75, rel=1e-9)


def test_melt_risk_shape(risk_wide):
    d = melt_risk(risk_wide)
    assert list(d.columns) == ["date", "book", "factor", "exposure"]
    assert len(d) == 310
    assert list(d.index) == list(range(310))


def test_melt_risk_drops_empty_cells(risk_wide):
    d = melt_risk(risk_wide)
    assert d["exposure"].notna().all()
    assert sorted(d["factor"].unique()) == ["MKT", "MOM", "QUALITY", "SIZE", "VALUE"]
    assert not ((d["book"] == "MACRO") & (d["factor"] == "VALUE")).any()


def test_melt_risk_values(risk_wide):
    d = melt_risk(risk_wide).set_index(["date", "book", "factor"])["exposure"]
    assert d.loc[("2023-01-31", "ALPHA", "MKT")] == pytest.approx(1.0197)
