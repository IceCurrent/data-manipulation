import pytest

from problems.p06_merge import (attach_sector, positions_without_price,
                                unmapped_tickers)


def test_attach_sector_does_not_multiply_rows(trades, ref):
    out = attach_sector(trades, ref)
    assert len(out) == len(trades) == 3080


def test_attach_sector_preserves_order(trades, ref):
    out = attach_sector(trades, ref)
    assert out["trade_id"].tolist() == trades["trade_id"].tolist()
    assert "sector" in out.columns and "currency" in out.columns


def test_attach_sector_values(trades, ref):
    out = attach_sector(trades, ref)
    counts = out["sector"].value_counts(dropna=False).to_dict()
    assert counts["Technology"] == 933
    assert counts["Financials"] == 598
    assert counts["Staples"] == 614
    assert counts["Energy"] == 312
    assert (out.loc[out["ticker"] == "SAP.DE", "currency"] == "EUR").all()


def test_attach_sector_leaves_unknown_instruments_null(trades, ref):
    out = attach_sector(trades, ref)
    assert int(out["sector"].isna().sum()) == 623
    assert out.loc[out["ticker"] == "TSLA", "sector"].isna().all()


def test_unmapped_tickers(trades, ref):
    got = unmapped_tickers(trades, ref)
    assert isinstance(got, list)
    assert got == ["BP.L", "TSLA"]


def test_positions_without_price_shape(positions, prices):
    d = positions_without_price(positions, prices)
    assert list(d.columns) == ["date", "ticker"]
    assert len(d) == 24
    assert list(d.index) == list(range(24))
    assert not d.duplicated().any()


def test_positions_without_price_values(positions, prices):
    d = positions_without_price(positions, prices)
    assert sorted(d["ticker"].unique()) == ["SAP.DE", "SHEL.L"]
    assert str(d["date"].iloc[0].date()) == "2023-04-10"
    assert d["date"].is_monotonic_increasing


def test_positions_without_price_ignores_rows_that_merely_lack_a_close(positions, prices):
    # XOM has rows on every session; three of them have an empty close. Those
    # are a different defect and do not belong in this answer.
    d = positions_without_price(positions, prices)
    assert "XOM" not in set(d["ticker"])
