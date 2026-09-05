import pytest

from problems.p17_pnl import daily_pnl, top_contributors


def test_daily_pnl_shape(positions, prices):
    d = daily_pnl(positions, prices)
    assert list(d.columns) == ["date", "book", "pnl"]
    assert len(d) == 1503
    assert d["date"].nunique() == 501
    assert sorted(d["book"].unique()) == ["ALPHA", "DELTA", "MACRO"]
    assert list(d.index) == list(range(1503))


def test_daily_pnl_drops_the_first_session(positions, prices):
    d = daily_pnl(positions, prices)
    assert d["date"].min() > positions["date"].min()
    assert str(d["date"].min().date()) == "2023-01-04"


def test_daily_pnl_values(positions, prices):
    d = daily_pnl(positions, prices).set_index(["date", "book"])["pnl"]
    assert d.loc[("2024-06-03", "ALPHA")] == pytest.approx(-412924.7, rel=1e-6)
    assert d.sum() == pytest.approx(19412589.1, rel=1e-8)


def test_daily_pnl_uses_the_position_held_into_the_move(positions, prices):
    # Marking today's position against today's move gives a different number.
    d = daily_pnl(positions, prices)
    by_book = d.groupby("book")["pnl"].sum()
    assert by_book["ALPHA"] == pytest.approx(9332076.17, rel=1e-6)
    assert by_book["DELTA"] == pytest.approx(-2982939.74, rel=1e-6)
    assert by_book["MACRO"] == pytest.approx(13063452.67, rel=1e-6)


def test_daily_pnl_survives_missing_prices(positions, prices):
    # Books hold instruments on foreign calendars; a day with no price for one
    # of them must not blank out the rest of the book.
    d = daily_pnl(positions, prices)
    assert d["pnl"].notna().all()
    holiday = d[d["date"] == "2024-05-01"]
    assert len(holiday) == 3
    assert (holiday["pnl"] != 0).all()


def test_top_contributors_shape(positions, prices):
    d = top_contributors(positions, prices, 3)
    assert list(d.columns) == ["month", "book", "ticker", "pnl"]
    assert len(d) == 216
    assert list(d.index) == list(range(216))
    assert d["month"].nunique() == 24


def test_top_contributors_ordering(positions, prices):
    d = top_contributors(positions, prices, 3)
    for _, g in d.groupby(["month", "book"]):
        assert g["pnl"].is_monotonic_decreasing
        assert len(g) <= 3


def test_top_contributors_values(positions, prices):
    d = top_contributors(positions, prices, 3)
    g = d[(d["month"] == "2024-12-31") & (d["book"] == "ALPHA")]
    assert g["ticker"].tolist() == ["KO", "MSFT", "SAP.DE"]
    assert g["pnl"].iloc[0] == pytest.approx(57536.48, rel=1e-6)


def test_top_contributors_of_one_is_the_single_best_name(positions, prices):
    d = top_contributors(positions, prices, 1)
    assert len(d) == 72
    assert (d.groupby(["month", "book"]).size() == 1).all()
