"""
P01  Selection and filtering                                     Easy | ~15 min
Concepts: label vs positional indexing, boolean masks
Builds on: nothing -- start here.

data/prices.csv holds daily closes and volume for ten tickers in long format:
one row per (date, ticker). Two of the tickers observe local holidays and are
simply absent on those dates; a few rows exist but have a missing close.

Everything below is about getting the rows and columns you asked for, and
nothing else.

Run:  python3 -m pytest tests/test_p01_selection.py
"""
import pandas as pd


def close_series(prices: pd.DataFrame, ticker: str) -> pd.Series:
    """One ticker's close price as a Series.

    Returns
    -------
    Series of float, indexed by date in ascending order.
    Index name 'date', Series name 'close'.
    """
    # approach 1:
    p = prices[prices['ticker'] == ticker] # gives the filtered dataframe
    p = p.set_index('date') # still the same dataframe just indexed by date rather than integers

    s = p['close'].sort_index(ascending=True)
    s.index.name = 'date'
    s.name = 'close' #just naming the series object; becomes the column name during dataframe conversions
    # print(s)

    # # approach 2: 
    # p = prices[prices['ticker'] == ticker] # a pd dataframe
    # date_idx = p['date'] # a pd series
    # close_prices = p['close'] # a pd series

    # # now it's tricky to have a pd series in data and pd series as index, and just expecting that pandas would
    # # line up the two series side by side. It actually searches the labels in data= which correspond to values in index=

    # # this could be fixed if the data= is not a pd series, but just a list


    # s = pd.Series(data=close_prices.to_numpy(), index=date_idx).sort_values(ascending=True)
    # s.name = 'close'
    # print(s)


    return s


def high_volume_days(prices: pd.DataFrame, ticker: str, min_volume: int) -> pd.DataFrame:
    """Sessions where one ticker traded at least `min_volume` shares.

    Returns
    -------
    DataFrame with the same four columns as `prices`, ascending by date,
    with a fresh 0..n-1 index.
    """
    p = prices[(prices['ticker'] == ticker) & (prices['volume'] >= min_volume)]
    p = p.sort_values(by='date', ascending=True)

    p = p.reset_index(drop = True)
    print(p)

    return p


def price_on(prices: pd.DataFrame, ticker: str, date: str) -> float:
    """The close for one ticker on one date.

    `date` is an ISO string such as '2024-06-03'.

    Returns
    -------
    float. If there is no row for that (ticker, date), or the row exists but
    the close is missing, return float('nan').
    """

    p = prices[prices['ticker'] == ticker]

    p = p[p['date'] == date]

    if len(p) == 0:
        return float('nan')
    
    print(p['close'])

    return float(p['close'].iloc[0])




def last_n_sessions(prices: pd.DataFrame, ticker: str, n: int) -> pd.DataFrame:
    """The `n` most recent sessions for one ticker.

    Returns
    -------
    DataFrame with the same four columns as `prices`, ascending by date,
    with a fresh 0..n-1 index.
    """
    p = prices[prices['ticker'] == ticker]
    p = p.sort_values(by='date', ascending=True)

    p = p.tail(n)
    
    p = p.reset_index(drop=True)
    print(p)

    return p
