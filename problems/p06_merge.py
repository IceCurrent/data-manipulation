"""
P06  Joining, and what joins do to row counts                     Med | ~25 min
Concepts: join keys, key uniqueness, unmatched rows, multi-column keys
Builds on: P01, P05.

data/ref.csv is the security master, straight off a vendor feed. It is not a
clean lookup table, and the blotter contains instruments it has never heard of.
Before you write anything, look at it:

    from qfp.data import load_ref; print(load_ref())

A left join is supposed to be a lookup: 3080 trades in, 3080 trades out. If
your answer to the first function has more rows than it started with, the join
is telling you something about the right-hand table.

The third function turns on a distinction worth keeping straight: a (date,
ticker) with no row at all in prices is not the same thing as a row whose close
happens to be missing. This one is about the first kind.

Run:  python3 -m pytest tests/test_p06_merge.py
"""
import pandas as pd
# from qfp.data import load_ref

# print(load_ref())

def attach_sector(trades: pd.DataFrame, ref: pd.DataFrame) -> pd.DataFrame:
    """Look up each trade's sector and currency.

    Returns
    -------
    A copy of `trades` with two extra columns, `sector` and `currency`. Exactly
    the same number of rows as `trades`, in the same order. Instruments that
    are not in the master get NaN in both columns.
    """
    master_unique = ref[['ticker', 'sector', 'currency']].drop_duplicates(subset='ticker', keep='first')

    df = pd.merge(trades, master_unique, on='ticker', how='left')
    # df = trades.copy()
    print(df)
    return df


def unmapped_tickers(trades: pd.DataFrame, ref: pd.DataFrame) -> list:
    """Which traded instruments are missing from the security master?

    Returns
    -------
    A plain Python list of ticker strings, sorted ascending.
    """
    ticker_list_trades = trades[['ticker', 'trade_id']]

    ticker_list_ref = ref.drop_duplicates(subset='ticker', keep='first')

    merged = pd.merge(ticker_list_trades, ticker_list_ref, on='ticker', how='left')

    mask = merged['name'].isna()

    ans = merged[mask]['ticker']
    ans = ans.drop_duplicates()
    ans = ans.sort_values()
    print(ans)
    return list(ans)



def positions_without_price(positions: pd.DataFrame, prices: pd.DataFrame) -> pd.DataFrame:
    """(date, ticker) pairs that are held in some book but have no row at all
    in the price file -- the positions you cannot mark.

    Report each pair once, however many books hold it.

    Returns
    -------
    DataFrame with columns exactly ['date', 'ticker'], sorted by date then
    ticker, with a fresh 0..n-1 index.
    """
    # m1 = prices.isna().any(axis=1)

    # p = prices[m1]
    # p = p.set_index(['date', 'ticker'])
    # m2 = p['close'].isna()
    # m2 = ~m2
    # # print(m2)
    # # print(p)
    
    # merged = pd.merge(positions, prices, on=['date', 'ticker'], how='left')

    # # invalid mask, as the mask series and merged do not have the same number of rows (even though they have the same index)
    # # merged = merged[m1] 
    
    # mask = merged[['close', 'volume']].isna().any(axis=1) # axis = 0 collapses the rows, axis=1 collapses the columns
    # mask = mask
    # unlinked_positions = merged[mask]

    # ans = unlinked_positions.drop_duplicates(subset=['date', 'ticker'], keep='first')
    # ans = ans.set_index(['date', 'ticker'])
    # m3 = m2.set_index(ans.index, fill_value=True)
    # print(m3)

    # ans = ans[m3]
    # # ans = ans[m1] also not allowed, because there are a lot of index labels in ans which m1 has never seen

    # ans = ans.sort_values(by=['date', 'ticker'])


    # print(ans)
    # return ans

    ## WE CAN SOLVE THE ABOVE PROBLEM OF FIGURING ALREADY NAN VALUES BY USING INDICATORS IN OUR MERGE FUNCTION
    merged = pd.merge(positions, prices, on=['date', 'ticker'], how='left', indicator=True)

    merged = merged[merged['_merge'] == 'left_only']

    ans = merged[['date', 'ticker']]
    ans = ans.drop_duplicates(subset=['date', 'ticker'])
    ans = ans.sort_values(by=['date', 'ticker'])
    ans = ans.reset_index(drop=True)
    print(ans)

    return ans
