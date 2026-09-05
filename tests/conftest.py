"""Fresh data for every test, so a mutating solution cannot leak into another."""
import pandas as pd
import pytest

from qfp import data


@pytest.fixture
def prices():
    return data.load_prices()


@pytest.fixture
def trades():
    return data.load_trades()


@pytest.fixture
def quotes():
    return data.load_quotes()


@pytest.fixture
def ref():
    return data.load_ref()


@pytest.fixture
def fx():
    return data.load_fx()


@pytest.fixture
def positions():
    return data.load_positions()


@pytest.fixture
def benchmark():
    return data.load_benchmark()


@pytest.fixture
def risk_wide():
    return data.load_risk_wide()


@pytest.fixture
def calendar():
    """Every trading session in the sample, as a DatetimeIndex."""
    return pd.DatetimeIndex(data.load_benchmark()["date"])
