"""
Deterministic generator for the synthetic finance datasets used by this practice set.

Everything here is seeded, so re-running reproduces the exact same CSVs.
You should not need to run this -- data/ is already populated. It is committed
so the expected values baked into the tests stay valid.

    python generate_data.py
"""
from __future__ import annotations

import numpy as np
import pandas as pd
from pathlib import Path

OUT = Path(__file__).parent / "data"
SEED = 20240917

# --------------------------------------------------------------------------
# Trading calendar: business days minus real US market holidays.
# (Deliberately NOT equal to pd.bdate_range -- assuming they are equal is a bug.)
# --------------------------------------------------------------------------
US_HOLIDAYS = pd.to_datetime([
    "2023-01-02", "2023-01-16", "2023-02-20", "2023-04-07", "2023-05-29",
    "2023-06-19", "2023-07-04", "2023-09-04", "2023-11-23", "2023-12-25",
    "2024-01-01", "2024-01-15", "2024-02-19", "2024-03-29", "2024-05-27",
    "2024-06-19", "2024-07-04", "2024-09-02", "2024-11-28", "2024-12-25",
])

DE_HOLIDAYS = pd.to_datetime([
    "2023-04-10", "2023-05-01", "2023-10-03", "2023-12-26",
    "2024-04-01", "2024-05-01", "2024-05-09", "2024-10-03", "2024-12-26",
])
GB_HOLIDAYS = pd.to_datetime([
    "2023-04-10", "2023-05-01", "2023-05-08", "2023-08-28", "2023-12-26",
    "2024-04-01", "2024-05-06", "2024-08-26", "2024-12-26",
])
FX_HOLIDAYS = pd.to_datetime([
    "2023-04-10", "2023-12-26", "2024-01-02", "2024-04-01", "2024-05-01",
    "2024-08-15", "2024-12-26",
])

CAL = pd.DatetimeIndex(
    [d for d in pd.bdate_range("2023-01-02", "2024-12-31") if d not in set(US_HOLIDAYS)]
)
N = len(CAL)

# Volatility regimes: calm baseline with two stress windows.
STRESS = [("2023-09-15", "2023-11-10"), ("2024-06-03", "2024-07-15")]

UNIVERSE = [
    # ticker,  sector,        ccy,  beta, idio_vol, ar1_idio, ann_alpha, px0
    ("AAPL",   "Technology",  "USD", 1.15, 0.0110,  0.08, 0.06, 128.0),
    ("MSFT",   "Technology",  "USD", 1.05, 0.0098,  0.06, 0.08, 241.0),
    ("NVDA",   "Technology",  "USD", 1.75, 0.0205,  0.14, 0.35, 147.0),
    ("JPM",    "Financials",  "USD", 1.30, 0.0120,  0.05, 0.04, 134.0),
    ("GS",     "Financials",  "USD", 1.42, 0.0132,  0.11, 0.03, 343.0),
    ("XOM",    "Energy",      "USD", 0.82, 0.0141, -0.09, -0.02, 110.0),
    ("KO",     "Staples",     "USD", 0.50, 0.0072, -0.11, 0.01, 63.5),
    ("PG",     "Staples",     "USD", 0.45, 0.0070,  0.03, 0.02, 151.0),
    ("SAP.DE", "Technology",  "EUR", 1.00, 0.0121,  0.09, 0.05, 98.0),
    ("SHEL.L", "Energy",      "GBP", 0.90, 0.0128, -0.06, 0.03, 23.4),
]
TICKERS = [u[0] for u in UNIVERSE]


def _regime_vol() -> np.ndarray:
    v = np.full(N, 0.0062)
    for lo, hi in STRESS:
        m = (CAL >= lo) & (CAL <= hi)
        v[m] = 0.0215
    # smooth the regime edges a little so vol looks like a process, not a step
    return pd.Series(v).rolling(3, min_periods=1).mean().to_numpy()


def build_prices(rng: np.random.Generator):
    mkt_vol = _regime_vol()
    eps = rng.standard_normal(N)
    mkt = np.zeros(N)
    for t in range(1, N):
        # mild short-horizon reversal in the market factor
        mkt[t] = -0.055 * mkt[t - 1] + mkt_vol[t] * eps[t]
    mkt += 0.07 / 252.0

    frames = []
    for tkr, sector, ccy, beta, ivol, phi, alpha, px0 in UNIVERSE:
        z = rng.standard_normal(N)
        idio = np.zeros(N)
        scale = ivol * np.sqrt(1 - phi ** 2)
        # idio vol also breathes with the regime, but less than the market
        breathe = 1.0 + 1.4 * (mkt_vol / mkt_vol.max())
        for t in range(1, N):
            idio[t] = phi * idio[t - 1] + scale * breathe[t] * z[t]
        ret = alpha / 252.0 + beta * mkt + idio
        ret[0] = 0.0
        close = px0 * np.exp(np.cumsum(ret) - 0.5 * np.cumsum(ret ** 2) * 0.0)

        # volume: base level, weekday effect, |return| link, earnings spikes
        base = {"AAPL": 5.4e7, "MSFT": 2.6e7, "NVDA": 4.1e8, "JPM": 9.4e6,
                "GS": 2.1e6, "XOM": 1.7e7, "KO": 1.3e7, "PG": 6.9e6,
                "SAP.DE": 1.1e6, "SHEL.L": 6.2e6}[tkr]
        dow = np.array([d.weekday() for d in CAL])
        wk = np.where(np.isin(dow, [0, 4]), 0.90, 1.05)
        shock = np.exp(3.1 * np.abs(ret) - 0.02)
        noise = np.exp(rng.normal(0.0, 0.26, N))
        vol = base * wk * shock * noise
        # ~quarterly earnings: heavy volume
        for k in range(4, N, 63):
            vol[k] *= 3.4
        # month-end index rebalance bump
        me = pd.Series(1, index=CAL).groupby([CAL.year, CAL.month]).tail(1).index
        vol[np.isin(CAL, me)] *= 1.35

        frames.append(pd.DataFrame({
            "date": CAL, "ticker": tkr,
            "close": np.round(close, 4),
            "volume": vol.round().astype("int64"),
        }))

    px = pd.concat(frames, ignore_index=True)
    return px, mkt


def inject_anomalies(px: pd.DataFrame, rng: np.random.Generator) -> dict:
    """Plant known data-quality defects. Returns a log of what was planted."""
    log: dict = {}
    px = px.set_index(["ticker", "date"])

    # 1. Stale feed: KO close repeats for 4 consecutive sessions.
    ko_dates = CAL[(CAL >= "2024-03-11") & (CAL <= "2024-03-15")]
    stuck = float(px.loc[("KO", ko_dates[0]), "close"])
    for d in ko_dates:
        px.loc[("KO", d), "close"] = stuck
    log["stale_KO"] = [str(d.date()) for d in ko_dates]

    # 2. Bad tick: single-day 28% spike in NVDA that reverts the next day.
    spike_day = pd.Timestamp("2023-07-19")
    px.loc[("NVDA", spike_day), "close"] = round(
        float(px.loc[("NVDA", spike_day), "close"]) * 1.28, 4)
    log["spike_NVDA"] = str(spike_day.date())

    # 3. Vendor outage: XOM close missing on three sessions (row present, value NaN).
    xom_nan = pd.to_datetime(["2023-05-16", "2024-02-07", "2024-09-19"])
    for d in xom_nan:
        px.loc[("XOM", d), "close"] = np.nan
    log["nan_close_XOM"] = [str(d.date()) for d in xom_nan]

    # 4. Zero-volume sessions scattered across names.
    zero_vol = [("PG", "2023-08-11"), ("KO", "2023-11-24"), ("GS", "2024-05-24"),
                ("SHEL.L", "2024-07-05"), ("MSFT", "2024-11-29")]
    for t, d in zero_vol:
        px.loc[(t, pd.Timestamp(d)), "volume"] = 0
    log["zero_volume"] = zero_vol

    px = px.reset_index()

    # 4b. Trading halt: SHEL.L is suspended for six consecutive sessions, so a
    # blanket forward-fill would carry a two-week-old price.
    halt = CAL[(CAL >= "2024-08-05") & (CAL <= "2024-08-12")]
    drop_halt = px["ticker"].eq("SHEL.L") & px["date"].isin(halt)
    log["halt_SHEL.L"] = [str(d.date()) for d in halt]
    px = px.loc[~drop_halt].copy()

    # 5. Ragged calendars: local holidays simply have no row at all.
    drop_de = px["ticker"].eq("SAP.DE") & px["date"].isin(DE_HOLIDAYS)
    drop_gb = px["ticker"].eq("SHEL.L") & px["date"].isin(GB_HOLIDAYS)
    log["missing_rows_SAP.DE"] = int(drop_de.sum())
    log["missing_rows_SHEL.L"] = int(drop_gb.sum())
    px = px.loc[~(drop_de | drop_gb)].copy()

    return px, log


def build_reference() -> pd.DataFrame:
    """Security master, warts and all."""
    rows = []
    names = {
        "AAPL": "Apple Inc", "MSFT": "Microsoft Corp", "NVDA": "NVIDIA Corp",
        "JPM": "JPMorgan Chase & Co", "GS": "Goldman Sachs Group Inc",
        "XOM": "Exxon Mobil Corp", "KO": "Coca-Cola Co", "PG": "Procter & Gamble Co",
        "SAP.DE": "SAP SE", "SHEL.L": "Shell plc",
    }
    lots = {"SAP.DE": 1, "SHEL.L": 1}
    for tkr, sector, ccy, *_ in UNIVERSE:
        rows.append((tkr, names[tkr], sector, ccy, lots.get(tkr, 1)))
    # Instruments in the master that never appear in prices (inner vs left join matters)
    rows.append(("BAC", "Bank of America Corp", "Financials", "USD", 1))
    rows.append(("TTE.PA", "TotalEnergies SE", "Energy", "EUR", 1))

    ref = pd.DataFrame(rows, columns=["ticker", "name", "sector", "currency", "lot_size"])

    # Vendor artefact: three tickers loaded twice under slightly different names.
    dupes = ref[ref["ticker"].isin(["AAPL", "JPM", "SHEL.L"])].copy()
    dupes["name"] = dupes["name"].str.upper()
    ref = pd.concat([ref, dupes], ignore_index=True)
    return ref.sort_values("ticker", kind="stable").reset_index(drop=True)


def build_fx(rng: np.random.Generator) -> tuple[pd.DataFrame, str]:
    """EUR/GBP rates (USD per 1 unit of local ccy) on their own calendar."""
    fx_cal = pd.DatetimeIndex(
        [d for d in pd.bdate_range("2022-12-27", "2025-01-07")
         if d not in set(US_HOLIDAYS) and d not in set(FX_HOLIDAYS)]
    )
    out = []
    for ccy, mu, sig, kappa, r0 in [("EUR", 1.085, 0.0042, 0.010, 1.066),
                                    ("GBP", 1.262, 0.0039, 0.008, 1.208)]:
        n = len(fx_cal)
        r = np.empty(n)
        r[0] = r0
        e = rng.standard_normal(n)
        for t in range(1, n):
            r[t] = r[t - 1] + kappa * (mu - r[t - 1]) + sig * e[t]
        out.append(pd.DataFrame({"date": fx_cal, "ccy": ccy, "rate": r}))
    fx = pd.concat(out, ignore_index=True)

    # Look-ahead trap: drop one date, then jump the rate on the FOLLOWING day.
    # Carrying the previous rate forward is correct; filling backwards is not.
    gap = pd.Timestamp("2024-04-18")
    nxt = pd.Timestamp("2024-04-19")
    fx.loc[(fx["date"] >= nxt) & (fx["ccy"] == "EUR"), "rate"] += 0.031
    fx.loc[(fx["date"] >= nxt) & (fx["ccy"] == "GBP"), "rate"] -= 0.027
    fx = fx.loc[fx["date"] != gap].copy()

    fx["rate"] = fx["rate"].round(6)
    return fx.sort_values(["date", "ccy"]).reset_index(drop=True), str(gap.date())


def build_benchmark(mkt: np.ndarray) -> pd.DataFrame:
    lvl = 3820.0 * np.exp(np.cumsum(mkt))
    return pd.DataFrame({"date": CAL, "close": np.round(lvl, 4)})


def build_positions(rng: np.random.Generator) -> pd.DataFrame:
    """Three books with slow-moving holdings, rebalanced roughly monthly."""
    books = {
        "ALPHA":  ["AAPL", "MSFT", "NVDA", "KO", "SAP.DE"],
        "DELTA":  ["JPM", "GS", "XOM", "AAPL", "SHEL.L"],
        "MACRO":  ["NVDA", "PG", "XOM", "SAP.DE"],
    }
    rebal = pd.Series(1, index=CAL).groupby([CAL.year, CAL.month]).head(1).index
    rows = []
    for book, tkrs in books.items():
        for tkr in tkrs:
            qty = int(rng.integers(-4000, 9000) // 100 * 100)
            if qty == 0:
                qty = 1500
            cur = qty
            for d in CAL:
                if d in rebal:
                    step = int(rng.normal(0, 2200) // 100 * 100)
                    cur = cur + step
                rows.append((d, book, tkr, cur))
    pos = pd.DataFrame(rows, columns=["date", "book", "ticker", "qty"])
    return pos.sort_values(["date", "book", "ticker"]).reset_index(drop=True)


def build_risk_wide(rng: np.random.Generator) -> pd.DataFrame:
    me = pd.Series(1, index=CAL).groupby([CAL.year, CAL.month]).tail(1).index
    books = ["ALPHA", "DELTA", "MACRO"]
    rows = []
    for d in me:
        for b in books:
            rows.append({
                "date": d, "book": b,
                "MKT": round(float(rng.normal(0.9, 0.25)), 4),
                "SIZE": round(float(rng.normal(-0.2, 0.4)), 4),
                "VALUE": round(float(rng.normal(0.1, 0.35)), 4),
                "MOM": round(float(rng.normal(0.3, 0.3)), 4),
                "QUALITY": round(float(rng.normal(0.0, 0.2)), 4),
            })
    rw = pd.DataFrame(rows)
    # MACRO is not risk-decomposed on the value/quality factors.
    rw.loc[rw["book"].eq("MACRO"), ["VALUE", "QUALITY"]] = np.nan
    # a couple of genuinely missing cells
    rw.loc[4, "MOM"] = np.nan
    rw.loc[31, "SIZE"] = np.nan
    return rw


# --------------------------------------------------------------------------
# Intraday: a minute-level Brownian bridge per (day, ticker) anchored on the
# daily closes, then trades and quotes sampled off that same path so the
# blotter, the quote tape and the daily bars are mutually consistent.
# --------------------------------------------------------------------------
INTRA_DAYS = CAL[-44:]
TRADED = ["AAPL", "MSFT", "NVDA", "JPM", "GS", "XOM", "KO", "PG", "TSLA", "BP.L"]
MINUTES = 390


def _bridge(p0: float, p1: float, sig: float, rng) -> np.ndarray:
    u = np.arange(1, MINUTES + 1) / MINUTES
    w = np.cumsum(rng.standard_normal(MINUTES)) / np.sqrt(MINUTES)
    w = w - u * w[-1]
    return np.exp(np.log(p0) + (np.log(p1) - np.log(p0)) * u + sig * w)


def build_intraday(px: pd.DataFrame, rng: np.random.Generator):
    daily = px.set_index(["ticker", "date"])["close"]
    # standalone paths for the two symbols that exist on the blotter only
    extra = {}
    for tkr, p0, sig in [("TSLA", 248.0, 0.028), ("BP.L", 4.42, 0.014)]:
        r = rng.normal(0.0004, sig, len(INTRA_DAYS))
        extra[tkr] = pd.Series(p0 * np.exp(np.cumsum(r)), index=INTRA_DAYS)

    # U-shaped intraday trade intensity: busy at the open and into the close
    m = np.arange(MINUTES)
    intensity = 1.0 + 3.2 * np.exp(-m / 26.0) + 2.6 * np.exp(-(MINUTES - 1 - m) / 34.0)
    intensity /= intensity.sum()

    traders = ["kim.r", "okafor.a", "silva.m", "novak.p", "haddad.y"]
    venues = ["XNYS", "XNAS", "BATS", "DARK"]

    trades, quotes = [], []
    tid = 700_000
    for tkr in TRADED:
        if tkr in extra:
            path_close = extra[tkr]
            prev_close = path_close.shift(1).fillna(path_close.iloc[0] * 0.998)
            ivol = 0.020
        else:
            s = daily.loc[tkr]
            path_close = s.reindex(INTRA_DAYS)
            prev_close = s.shift(1).reindex(INTRA_DAYS)
            ivol = 0.011
        for d in INTRA_DAYS:
            p1, p0 = path_close.get(d, np.nan), prev_close.get(d, np.nan)
            if not np.isfinite(p0) or not np.isfinite(p1):
                continue
            path = _bridge(float(p0), float(p1), ivol, rng)
            open_ts = pd.Timestamp(d) + pd.Timedelta(hours=9, minutes=30)

            # ---- quotes: ~60/day, spread widest at the open, tight midday
            qm = np.sort(rng.choice(MINUTES, size=60, replace=False))
            half = path[qm] * (0.00018 + 0.00055 * np.exp(-qm / 30.0)
                               + 0.00010 * np.exp(-(MINUTES - 1 - qm) / 45.0))
            quotes.append(pd.DataFrame({
                "timestamp": open_ts + pd.to_timedelta(qm, unit="m"),
                "ticker": tkr,
                "bid": np.round(path[qm] - half, 4),
                "ask": np.round(path[qm] + half, 4),
            }))

            # ---- trades: 5-9 per ticker-day
            k = int(rng.integers(5, 10))
            tm = np.sort(rng.choice(MINUTES, size=k, replace=False, p=intensity))
            mid = path[tm]
            hs = mid * (0.00018 + 0.00055 * np.exp(-tm / 30.0))
            side = rng.choice(["BUY", "SELL"], size=k, p=[0.53, 0.47])
            passive = rng.random(k) < 0.30            # ~30% get price improvement
            sgn = np.where(side == "BUY", 1.0, -1.0)
            fill = mid + np.where(passive, -sgn * hs * 0.9, sgn * hs * 1.05)
            lot = np.where(rng.random(k) < 0.85, 100, 1)
            qty = (rng.integers(1, 45, size=k) * lot).astype("int64")
            trades.append(pd.DataFrame({
                "trade_id": [f"T{tid + i}" for i in range(k)],
                "timestamp": open_ts + pd.to_timedelta(tm, unit="m"),
                "ticker": tkr, "side": side, "qty": qty,
                "price": np.round(fill, 4),
                "trader": rng.choice(traders, size=k),
                "venue": rng.choice(venues, size=k, p=[0.32, 0.34, 0.22, 0.12]),
            }))
            tid += k

    tr = pd.concat(trades, ignore_index=True)
    qt = pd.concat(quotes, ignore_index=True)
    return tr, qt


def dirty_trades(tr: pd.DataFrame, rng: np.random.Generator) -> tuple[pd.DataFrame, dict]:
    log = {}
    n = len(tr)

    # 1. Double bookings: the SAME row keyed in twice, every field identical.
    dup_idx = rng.choice(n, size=26, replace=False)
    doubles = tr.iloc[dup_idx].copy()
    log["exact_duplicate_rows"] = 26

    # 2. Genuine multi-venue fills: one trade_id, several legs, different venue/qty.
    leg_idx = rng.choice(np.setdiff1d(np.arange(n), dup_idx), size=15, replace=False)
    legs = tr.iloc[leg_idx].copy()
    legs["venue"] = "DARK"
    legs["qty"] = (legs["qty"] // 2).clip(lower=1)
    log["multi_venue_legs"] = 15

    tr = pd.concat([tr, doubles, legs], ignore_index=True)

    # 3. Unfilled / partially captured rows.
    m = len(tr)
    nan_px = rng.choice(m, size=38, replace=False)
    tr.loc[tr.index[nan_px], "price"] = np.nan
    nan_qty = rng.choice(np.setdiff1d(np.arange(m), nan_px), size=14, replace=False)
    tr.loc[tr.index[nan_qty], "qty"] = np.nan
    log["nan_price_rows"] = 38
    log["nan_qty_rows"] = 14

    # 4. Venue not reported -- these rows are perfectly good trades.
    rest = np.setdiff1d(np.arange(m), np.concatenate([nan_px, nan_qty]))
    nan_venue = rng.choice(rest, size=21, replace=False)
    tr.loc[tr.index[nan_venue], "venue"] = np.nan
    log["nan_venue_rows"] = 21

    # blotter export arrives in no particular order
    tr = tr.sample(frac=1.0, random_state=7).reset_index(drop=True)
    return tr, log


def main() -> None:
    OUT.mkdir(exist_ok=True)
    rng = np.random.default_rng(SEED)

    px, mkt = build_prices(rng)
    px, plog = inject_anomalies(px, rng)
    bench = build_benchmark(mkt)
    ref = build_reference()
    fx, fx_gap = build_fx(rng)
    pos = build_positions(rng)
    risk = build_risk_wide(rng)
    tr, qt = build_intraday(px, rng)
    tr, tlog = dirty_trades(tr, rng)
    # Quote-tape outage: KO has no quotes before 11:00 on 2024-12-05, so trades
    # in that window have no prevailing quote to attach to.
    outage = (qt["ticker"].eq("KO")
              & qt["timestamp"].dt.normalize().eq(pd.Timestamp("2024-12-05"))
              & (qt["timestamp"].dt.hour < 11))
    tlog["quote_outage_rows_dropped"] = int(outage.sum())
    qt = qt.loc[~outage].copy()
    qt = qt.sample(frac=1.0, random_state=11).reset_index(drop=True)

    # prices arrive grouped by ticker, not sorted by date globally
    px = px.sort_values(["ticker", "date"], kind="stable").reset_index(drop=True)

    px.to_csv(OUT / "prices.csv", index=False)
    bench.to_csv(OUT / "benchmark.csv", index=False)
    ref.to_csv(OUT / "ref.csv", index=False)
    fx.to_csv(OUT / "fx.csv", index=False)
    pos.to_csv(OUT / "positions.csv", index=False)
    risk.to_csv(OUT / "risk_wide.csv", index=False)
    tr.to_csv(OUT / "trades.csv", index=False)
    qt.to_csv(OUT / "quotes.csv", index=False)

    print(f"calendar      : {N} sessions {CAL[0].date()} -> {CAL[-1].date()}")
    print(f"prices.csv    : {len(px):>7,} rows")
    print(f"benchmark.csv : {len(bench):>7,} rows")
    print(f"ref.csv       : {len(ref):>7,} rows")
    print(f"fx.csv        : {len(fx):>7,} rows  (gap planted at {fx_gap})")
    print(f"positions.csv : {len(pos):>7,} rows")
    print(f"risk_wide.csv : {len(risk):>7,} rows")
    print(f"trades.csv    : {len(tr):>7,} rows")
    print(f"quotes.csv    : {len(qt):>7,} rows")
    print("\nplanted in prices :", plog)
    print("planted in trades :", tlog)


if __name__ == "__main__":
    main()
