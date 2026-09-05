"""
P15  Comparing series that do not line up                         Med | ~20 min
Concepts: pairwise vs complete-case alignment, covariance and beta
Builds on: P07 (wide panels), P10 (returns), P13 (alignment).

Both of these are covariance calculations, and in both of them the arithmetic
is the easy part. The question is which dates go into the sample.

`.corr()` on a DataFrame defaults to using every date where a given PAIR both
have data, so different cells of the matrix are computed over different
samples. That is often not what you want -- a covariance matrix built that way
is not guaranteed to be internally consistent. This dataset has two tickers on
foreign calendars and a six-session suspension, so the two conventions give
visibly different answers. The first function asks for the complete-case one.

Run:  python3 -m pytest tests/test_p15_cross_section.py
"""
import pandas as pd


def return_correlation(prices: pd.DataFrame, tickers: list) -> pd.DataFrame:
    """Correlation matrix of simple daily returns for `tickers`.

    Use only the dates on which EVERY ticker in `tickers` has a return, so that
    every cell of the matrix is computed over the same sample.

    Returns
    -------
    DataFrame of float, index and columns both equal to `tickers` in the order
    given.
    """
    raise NotImplementedError


def beta_table(prices: pd.DataFrame, benchmark: pd.DataFrame) -> pd.Series:
    """Each ticker's beta to the benchmark.

    Beta is the covariance of the ticker's simple daily returns with the
    benchmark's, divided by the variance of the benchmark's, measured over the
    dates where both have a return.

    Returns
    -------
    Series of float indexed by ticker ascending, Series name 'beta'.
    """
    raise NotImplementedError
