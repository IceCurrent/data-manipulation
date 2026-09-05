"""
P04  Aggregating a blotter                                  Easy-Med | ~20 min
Concepts: groupby with several named outputs, weighted averages, nunique
Builds on: P02 (signed quantities), P03 (grouping).

Two desk reports off the same blotter. Throughout this file, ignore any row
where qty or price is missing -- an unfilled order is not a trade.

The volume-weighted average price is the one to think about: a plain mean of
the price column is not it, and there is no `agg` function that takes weights.

Run:  python3 -m pytest tests/test_p04_groupby_agg.py
"""
import pandas as pd
import numpy as np

def desk_summary(trades: pd.DataFrame) -> pd.DataFrame:
    """Per ticker and side: how much traded, and at what average price.

    `vwap` is the volume-weighted average price: total cash traded divided by
    total shares traded.

    Returns
    -------
    DataFrame with columns exactly
        ['ticker', 'side', 'n_trades', 'total_qty', 'vwap']
    sorted by ticker then side, with a fresh 0..n-1 index.
    """

    df = trades[['ticker', 'side', 'qty', 'price']]
    df['volume'] = df['qty']*df['price']
    df = df.dropna(axis=0)

    n_trades = df.groupby(['ticker', 'side'])['volume'].count()
    n_trades.name = 'n_trades'

    total_qty = df.groupby(['ticker', 'side'])['qty'].sum()
    total_qty.name = 'total_qty'

    total_vol = df.groupby(['ticker', 'side'])['volume'].sum()
    total_vol.name = 'total_vol'

    df2 = pd.concat([n_trades, total_qty, total_vol], axis=1)
    df2 = df2.reset_index(drop=False)

    df2['vwap'] = df2['total_vol'] / df2['total_qty']

    
    df2 = df2.drop(columns=['total_vol'])


    # print(df)
    print(df2)

    return df2


def trader_activity(trades: pd.DataFrame) -> pd.DataFrame:
    """Per trader: how busy, how broad, and how directional.

    gross_notional is the sum of the ABSOLUTE signed notional (total cash
    turned over). net_notional is the sum of the signed notional (buys minus
    sells), so a trader who bought and sold equal amounts nets to zero.

    Returns
    -------
    DataFrame with columns exactly
        ['trader', 'n_trades', 'n_tickers', 'gross_notional', 'net_notional']
    sorted by trader, with a fresh 0..n-1 index. `n_tickers` counts distinct
    tickers.
    """
    
    trades['notional'] = trades['qty']*trades['price']
    trades = trades.dropna(subset=['qty', 'price'])

    n_trades = trades.groupby('trader')['notional'].count()
    n_trades.name = 'n_trades'

    n_tickers = trades.groupby('trader')['ticker'].nunique()
    n_tickers.name = 'n_tickers'

    gross_notional = trades.groupby('trader')['notional'].sum()
    gross_notional.name = 'gross_notional'

    trades['notional'] = np.where(trades['side'] == 'SELL', -1*trades['notional'], trades['notional'])
    net_notional = trades.groupby('trader')['notional'].sum()
    net_notional.name = 'net_notional'

    df = pd.concat([n_trades, n_tickers, gross_notional, net_notional], axis=1)
    df = df.dropna(axis=0)

    df = df.reset_index(drop=False)
    
    print(df)

    return df
