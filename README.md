# pandas drills for quant interviews

19 problems, LeetCode-Easy to LeetCode-Medium, on synthetic but structurally
realistic finance data. Each one is a file with a problem statement and empty
stubs; pytest tells you pass/fail per case. No solutions are included.

## Running

From this directory:

```bash
python3 -m pytest tests/test_p01_selection.py
```

That command (with the matching filename) is repeated at the top of every
problem file. To run everything:

```bash
python3 -m pytest
```

Output is one line per test case. Add `--tb=line` for terser failures, or
`-x` to stop at the first one.

## Working on a problem

Open `problems/pNN_*.py`, read the module docstring, fill in the stubs, run the
test file. Nothing imports your code except the tests, so you can experiment
freely in a REPL:

```bash
python3 -c "from qfp.data import load_prices; print(load_prices().head(20))"
```

Loaders live in `qfp/data.py` — one per file in `data/`, each documented with
what the columns mean and what is wrong with them. Read that file first; it is
short, and knowing the shape of the data is half of every problem here.

## The problems

Each leans on something introduced earlier. Do them in order.

| #   | File                    | What it drills                                  | Needs      |
|-----|-------------------------|-------------------------------------------------|------------|
| 01  | `p01_selection`         | `.loc` / `.iloc`, boolean masks                  | —          |
| 02  | `p02_vectorized`        | conditional columns, NaN propagation, binning    | 01         |
| 03  | `p03_sorting_topn`      | sorting, top-N per group, ranking within a group | 01, 02     |
| 04  | `p04_groupby_agg`       | multi-output aggregation, weighted averages      | 02, 03     |
| 05  | `p05_transform`         | group statistics broadcast back to every row     | 04         |
| 06  | `p06_merge`             | join keys, key uniqueness, unmatched rows        | 01, 05     |
| 07  | `p07_reshape`           | long ↔ wide, reshapes that need an aggregation   | 05, 06     |
| 08  | `p08_missing`           | targeted `dropna`, reindexing, bounded fills     | 01, 06     |
| 09  | `p09_duplicates`        | duplicate policy, last-row-per-group             | 03, 08     |
| 10  | `p10_returns`           | within-group lags, NaN propagation, compounding  | 05, 08     |
| 11  | `p11_rolling`           | rolling windows inside groups, `min_periods`     | 10, 05     |
| 12  | `p12_resample`          | changing frequency, period compounding, buckets  | 07, 10, 04 |
| 13  | `p13_alignment`         | two calendars, as-of lookups, no look-ahead      | 08, 06     |
| 14  | `p14_asof`              | point-in-time joins, tolerance                   | 13, 09, 06 |
| 15  | `p15_cross_section`     | pairwise vs complete-case alignment, beta        | 07, 10, 13 |
| 16  | `p16_positions`         | blotter → positions (composite)                  | 02, 09, 08 |
| 17  | `p17_pnl`               | mark-to-market P&L, monthly top-N (composite)    | 10, 06, 12 |
| 18  | `p18_signal`            | signal/return alignment, cross-sectional IC      | 07, 10, 15 |
| 19  | `p19_quality`           | consecutive-run detection, thresholds            | 10, 05, 04 |

If you run short on time, the six that repay the most per minute in an
interview are **05, 06, 10, 11, 12, 17**.

## Suggested pace

Roughly 45 minutes a session, most days, over about three weeks.

- **Week 1** — 01–07. The first three are pure syntax and should go quickly;
  slow down at 05 and 06.
- **Week 2** — 08–15. This is the time-series core and the densest stretch.
- **Week 3** — 16–19, then go back and redo earlier problems from a blank file.

That last part is the point. Getting a problem green once means you worked it
out; getting it green a second time from scratch, a week later, is what turns
into fluency you can use under interview pressure. Budget a third of your total
time for re-solving, not for new problems.

## The data

Generated once by `generate_data.py` and committed, so results are stable. It
is not random noise with finance-flavoured column names — the structure is
there to be exploited, and in several problems it is what makes the naive
approach wrong.

| File              | Rows   | Contains                                                        |
|-------------------|--------|-----------------------------------------------------------------|
| `prices.csv`      | 4,996  | Daily closes/volume, 10 tickers, 2023–2024, long format          |
| `benchmark.csv`   | 502    | Index level on the full trading calendar                         |
| `ref.csv`         | 15     | Security master: sector, currency                                |
| `fx.csv`          | 1,006  | EUR/GBP rates, on the FX calendar                                |
| `positions.csv`   | 7,028  | End-of-day positions for three books, long and short             |
| `risk_wide.csv`   | 72     | Month-end factor exposures, one column per factor                |
| `trades.csv`      | 3,080  | Intraday blotter over the last 44 sessions                       |
| `quotes.csv`      | 26,385 | Top-of-book quote tape over the same sessions                    |

Returns carry genuine autocorrelation, both signs; each ticker loads on a
common market factor with a designed beta between 0.41 and 1.69; and volatility
runs at about 10% annualised in calm stretches against 25–40% in two stress
windows. Volume tracks absolute returns and spikes on earnings dates. Two
tickers trade on foreign calendars and one is suspended for six sessions, so
panels do not line up. The blotter has double-booked rows, unfilled orders and
multi-venue fills, and quotes toward instruments the security master has never
heard of. The security master itself lists three tickers twice.

You are not told where the defects are. Finding them is part of several
problems, and `p19` asks for them directly.

## New to pandas entirely

Read the "10 minutes to pandas" page in the official docs once, then start on
`p01` — it is designed to be solvable with only that. Keep the API reference
open throughout; looking up method signatures is normal and is not cheating.
Asking a chatbot for the answer is, and it will cost you the thing you are
trying to build.
