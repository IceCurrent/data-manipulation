import pytest

from problems.p18_signal import (information_coefficient, mean_ic,
                                 momentum_signal)


def test_momentum_signal_shape(prices):
    d = momentum_signal(prices, 20)
    assert d.shape == (502, 10)
    assert list(d.columns) == sorted(prices["ticker"].unique())
    assert d.index.is_monotonic_increasing


def test_momentum_signal_uses_only_past_prices(prices):
    d = momentum_signal(prices, 20)
    assert d.iloc[:20].isna().all().all()
    assert d.loc["2024-06-03", "NVDA"] == pytest.approx(0.0539229, rel=1e-5)


def test_momentum_signal_lookback_changes_the_answer(prices):
    a = momentum_signal(prices, 5)
    b = momentum_signal(prices, 20)
    assert not a.equals(b)
    assert a.iloc[:5].isna().all().all()
    assert a.iloc[6].notna().any()


def test_ic_shape(prices):
    ic = information_coefficient(prices, 20)
    assert ic.name == "ic"
    assert ic.index.name == "date"
    assert len(ic) == 481
    assert ic.index.is_monotonic_increasing
    assert ic.notna().all()


def test_ic_is_bounded(prices):
    ic = information_coefficient(prices, 20)
    assert ic.min() >= -1.0 and ic.max() <= 1.0


def test_ic_values(prices):
    assert mean_ic(prices, 20) == pytest.approx(0.01454671, rel=1e-5)
    assert mean_ic(prices, 5) == pytest.approx(0.01473607, rel=1e-5)


def test_ic_is_not_accidentally_measuring_the_present(prices):
    # Correlating the signal with the CURRENT day's return instead of the next
    # one produces a large number rather than a plausible one.
    assert abs(mean_ic(prices, 20)) < 0.1


def test_ic_starts_after_the_signal_warms_up(prices):
    ic = information_coefficient(prices, 20)
    assert str(ic.index[0].date()) == "2023-02-01"
