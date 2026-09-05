import numpy as np
import pytest

from problems.p10_returns import (add_log_returns, add_simple_returns,
                                  cumulative_return)


def test_simple_returns_preserve_row_order(prices):
    out = add_simple_returns(prices)
    assert list(out.index) == list(prices.index)
    assert out["close"].equals(prices["close"])


def test_simple_returns_do_not_bleed_across_tickers(prices):
    out = add_simple_returns(prices)
    first_rows = out.groupby("ticker", sort=False).head(1)
    assert first_rows["ret"].isna().all()
    assert len(first_rows) == 10


def test_simple_returns_values(prices):
    out = add_simple_returns(prices)
    v = out[(out["ticker"] == "AAPL") & (out["date"] == "2023-01-04")]["ret"].iloc[0]
    assert v == pytest.approx(0.02251563, rel=1e-6)


def test_simple_returns_span_a_missing_session(prices):
    # SAP.DE does not trade on 2024-05-01, so the 05-02 move is against 04-30.
    out = add_simple_returns(prices)
    v = out[(out["ticker"] == "SAP.DE") & (out["date"] == "2024-05-02")]["ret"].iloc[0]
    assert v == pytest.approx(0.00307884, rel=1e-6)


def test_simple_returns_are_missing_where_a_close_is_missing(prices):
    out = add_simple_returns(prices)
    assert int(out["ret"].isna().sum()) == 16
    assert int(out[out["ticker"] == "XOM"]["ret"].isna().sum()) == 7


def test_log_returns(prices):
    out = add_log_returns(prices)
    assert list(out.index) == list(prices.index)
    v = out[(out["ticker"] == "AAPL") & (out["date"] == "2023-01-04")]["log_ret"].iloc[0]
    assert v == pytest.approx(0.02226589, rel=1e-6)
    assert int(out["log_ret"].isna().sum()) == 16


def test_cumulative_return(prices):
    assert cumulative_return(prices, "AAPL", "2024-01-01", "2024-12-31") == \
        pytest.approx(1.16642686, rel=1e-6)
    assert cumulative_return(prices, "KO", "2023-01-01", "2023-12-31") == \
        pytest.approx(-0.07982362, rel=1e-6)


def test_cumulative_return_over_the_whole_sample(prices):
    assert cumulative_return(prices, "NVDA", "2023-01-01", "2024-12-31") == \
        pytest.approx(6.55314966, rel=1e-6)
