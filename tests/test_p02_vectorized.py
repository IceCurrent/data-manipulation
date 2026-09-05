import numpy as np
import pytest

from problems.p02_vectorized import add_notional, add_signed_qty, size_bucket


def test_signed_qty_preserves_the_frame(trades, prices):
    out = add_signed_qty(trades)
    assert len(out) == len(trades)
    assert list(out.index) == list(trades.index)
    assert out["trade_id"].tolist() == trades["trade_id"].tolist()


def test_signed_qty_values(trades):
    out = add_signed_qty(trades)
    assert out["signed_qty"].sum() == pytest.approx(335214.0)
    buys = out["side"] == "BUY"
    assert (out.loc[buys & out["qty"].notna(), "signed_qty"] > 0).all()
    assert (out.loc[~buys & out["qty"].notna(), "signed_qty"] < 0).all()


def test_signed_qty_keeps_missing_quantities_missing(trades):
    assert int(add_signed_qty(trades)["signed_qty"].isna().sum()) == 14


def test_notional_values(trades):
    out = add_notional(trades)
    assert out["notional"].sum() == pytest.approx(131103095.6139, rel=1e-9)


def test_notional_is_missing_not_zero_when_an_input_is_missing(trades):
    out = add_notional(trades)
    assert int(out["notional"].isna().sum()) == 52
    assert not (out.loc[trades["price"].isna(), "notional"] == 0).any()


def test_size_bucket_counts(trades):
    out = size_bucket(trades)
    counts = out["size_bucket"].value_counts(dropna=False).to_dict()
    assert counts.get("small") == 757
    assert counts.get("medium") == 662
    assert counts.get("large") == 1609


def test_size_bucket_boundaries_and_missing(trades):
    out = size_bucket(trades)
    n = out["notional"].abs()
    assert (out.loc[n.notna() & (n < 25_000), "size_bucket"] == "small").all()
    assert (out.loc[n >= 250_000, "size_bucket"] == "large").all()
    assert out.loc[n.isna(), "size_bucket"].isna().all()
