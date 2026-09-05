import pandas as pd
import pytest

from problems.p15_cross_section import beta_table, return_correlation

FIVE = ["AAPL", "MSFT", "NVDA", "KO", "XOM"]


def test_correlation_shape(prices):
    c = return_correlation(prices, FIVE)
    assert list(c.index) == FIVE
    assert list(c.columns) == FIVE
    assert c.shape == (5, 5)


def test_correlation_is_a_valid_matrix(prices):
    c = return_correlation(prices, FIVE)
    assert c.values.diagonal() == pytest.approx([1.0] * 5)
    assert c.equals(c.T) or (c - c.T).abs().max().max() < 1e-12


def test_correlation_values(prices):
    c = return_correlation(prices, FIVE)
    assert c.loc["AAPL", "MSFT"] == pytest.approx(0.300171, rel=1e-5)
    assert c.loc["NVDA", "XOM"] == pytest.approx(0.216695, rel=1e-5)


def test_correlation_uses_complete_cases_only(prices):
    # SHEL.L misses 15 sessions the others trade. Pairwise deletion gives
    # 0.167512 here; using only dates where all three have a return gives this.
    c = return_correlation(prices, ["AAPL", "SHEL.L", "SAP.DE"])
    assert c.loc["AAPL", "SHEL.L"] == pytest.approx(0.176141, rel=1e-5)


def test_beta_table_shape(prices, benchmark):
    b = beta_table(prices, benchmark)
    assert isinstance(b, pd.Series)
    assert b.name == "beta"
    assert len(b) == 10
    assert list(b.index) == sorted(b.index)


def test_beta_table_values(prices, benchmark):
    b = beta_table(prices, benchmark)
    assert b["NVDA"] == pytest.approx(1.694596, rel=1e-5)
    assert b["PG"] == pytest.approx(0.412545, rel=1e-5)
    assert b["AAPL"] == pytest.approx(1.133277, rel=1e-5)


def test_beta_table_orders_the_names_as_expected(prices, benchmark):
    b = beta_table(prices, benchmark)
    assert b["NVDA"] > b["GS"] > b["AAPL"] > b["XOM"] > b["PG"]
