import pytest

from problems.p04_groupby_agg import desk_summary, trader_activity


def test_desk_summary_shape(trades):
    d = desk_summary(trades)
    assert list(d.columns) == ["ticker", "side", "n_trades", "total_qty", "vwap"]
    assert len(d) == 20
    assert list(d.index) == list(range(20))
    assert d["ticker"].is_monotonic_increasing


def test_desk_summary_excludes_unfilled_orders(trades):
    d = desk_summary(trades)
    assert d["n_trades"].sum() == 3028


def test_desk_summary_vwap_is_volume_weighted(trades):
    d = desk_summary(trades)
    row = d[(d["ticker"] == "AAPL") & (d["side"] == "BUY")].iloc[0]
    assert row["n_trades"] == 164
    assert row["total_qty"] == pytest.approx(321891.0)
    assert row["vwap"] == pytest.approx(378.706905, rel=1e-8)


def test_desk_summary_vwap_differs_from_a_plain_mean(trades):
    d = desk_summary(trades)
    filled = trades.dropna(subset=["qty", "price"])
    plain = filled[(filled["ticker"] == "GS") & (filled["side"] == "SELL")]["price"].mean()
    got = d[(d["ticker"] == "GS") & (d["side"] == "SELL")]["vwap"].iloc[0]
    assert got == pytest.approx(488.926122, rel=1e-8)
    assert abs(got - plain) > 1e-6


def test_trader_activity_shape(trades):
    d = trader_activity(trades)
    assert list(d.columns) == ["trader", "n_trades", "n_tickers",
                               "gross_notional", "net_notional"]
    assert len(d) == 5
    assert list(d.index) == [0, 1, 2, 3, 4]
    assert d["trader"].tolist() == ["haddad.y", "kim.r", "novak.p",
                                    "okafor.a", "silva.m"]


def test_trader_activity_values(trades):
    d = trader_activity(trades).set_index("trader")
    assert d.loc["kim.r", "n_trades"] == 637
    assert d.loc["kim.r", "n_tickers"] == 10
    assert d.loc["kim.r", "gross_notional"] == pytest.approx(382537184.9, rel=1e-6)
    assert d.loc["kim.r", "net_notional"] == pytest.approx(663907.7, rel=1e-4)


def test_gross_and_net_are_not_the_same_number(trades):
    d = trader_activity(trades)
    assert (d["gross_notional"] > d["net_notional"].abs()).all()
