# ============================================================
# XAUUSD GOLD BACKTEST — Google Colab Version
# Strategy: WaveTrend + Second-Entry Pattern
# ============================================================
# USAGE: Copy each cell block into a separate Colab cell,
#        then run them top to bottom.
# ============================================================


# ─────────────────────────────────────────────────────────────
# CELL 1 — Install dependencies
# ─────────────────────────────────────────────────────────────
# !pip install yfinance pandas numpy plotly -q


# ─────────────────────────────────────────────────────────────
# CELL 2 — Imports
# ─────────────────────────────────────────────────────────────
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from IPython.display import display, HTML
import warnings
warnings.filterwarnings("ignore")


# ─────────────────────────────────────────────────────────────
# CELL 3 — Download XAUUSD (Gold Futures) 1H data — 1 Year
# ─────────────────────────────────────────────────────────────
print("Downloading XAUUSD 1H data (1 year)...")
raw = yf.download("GC=F", period="1y", interval="1h", progress=True, auto_adjust=True)

# Flatten multi-index columns if present
if isinstance(raw.columns, pd.MultiIndex):
    raw.columns = raw.columns.get_level_values(0)

raw = raw[["Open", "High", "Low", "Close", "Volume"]].copy()
raw.columns = ["open", "high", "low", "close", "volume"]
raw.dropna(inplace=True)
raw.index = pd.to_datetime(raw.index)
if raw.index.tz is not None:
    raw.index = raw.index.tz_localize(None)

print(f"✅ Downloaded {len(raw):,} hourly candles")
print(f"   Range : {raw.index[0].strftime('%Y-%m-%d')} → {raw.index[-1].strftime('%Y-%m-%d')}")
print(f"   Price : ${raw['close'].min():.2f} – ${raw['close'].max():.2f}")
raw.tail(3)


# ─────────────────────────────────────────────────────────────
# CELL 4 — Resample to 4H
# ─────────────────────────────────────────────────────────────
def resample_4h(df):
    return df.resample("4h").agg({
        "open":   "first",
        "high":   "max",
        "low":    "min",
        "close":  "last",
        "volume": "sum"
    }).dropna()

df_1h = raw.copy()
df_4h = resample_4h(df_1h)
print(f"1H candles : {len(df_1h):,}")
print(f"4H candles : {len(df_4h):,}")


# ─────────────────────────────────────────────────────────────
# CELL 5 — Indicator Functions
# ─────────────────────────────────────────────────────────────
def calc_ema(series, period):
    return series.ewm(span=period, adjust=False).mean()


def calc_wavetrend(df, n1=10, n2=21):
    """WaveTrend oscillator calculated from HLC3."""
    hlc3 = (df["high"] + df["low"] + df["close"]) / 3
    esa  = calc_ema(hlc3, n1)
    d    = calc_ema((hlc3 - esa).abs(), n1)
    ci   = (hlc3 - esa) / (0.015 * d.replace(0, np.nan))
    wt1  = calc_ema(ci.fillna(0), n2)
    wt2  = wt1.rolling(4).mean()
    return wt1, wt2


def calc_atr(df, period=10):
    hi, lo, pc = df["high"], df["low"], df["close"].shift(1)
    tr = pd.concat([hi - lo, (hi - pc).abs(), (lo - pc).abs()], axis=1).max(axis=1)
    return tr.ewm(span=period, adjust=False).mean()


def add_indicators(df):
    df = df.copy()
    df["ema20"]  = calc_ema(df["close"], 20)
    df["wt1"], df["wt2"] = calc_wavetrend(df)
    df["atr10"]  = calc_atr(df)
    return df


# ─────────────────────────────────────────────────────────────
# CELL 6 — Backtest Engine
# ─────────────────────────────────────────────────────────────
def run_backtest(df_raw, label):
    """
    Strategy rules:
      Entry conditions (ALL must be true):
        1. close > EMA(20)                        — uptrend filter
        2. WaveTrend(10,21) < -30 within last 20 candles
        3. Three-step second-entry pattern:
             c1 = green candle, high > prev high  (breakout)
             c2 = red candle,   low  < prev low   (pullback)
             c3 = green candle, high > c2 high    → ENTRY at c2 high

      Trade management:
        Stop loss  = entry − 1.5 × ATR(10)
        Take profit = entry + 2 × risk  (1:2 RR)
        Skip trade if risk > 8% of entry price
        Timeout exit after 40 candles at close

      Capital:
        Start $100, 0.1% fee per side, full reinvestment
    """
    df = add_indicators(df_raw)
    df = df.iloc[50:].copy()          # warm-up period
    df = df.reset_index()

    # ── Constants ──
    CAPITAL_START  = 100.0
    FEE_RATE       = 0.001            # 0.1% per side
    MAX_RISK_PCT   = 0.08             # 8% of entry price
    MAX_HOLD       = 40               # candles
    WT_THRESH      = -30
    WT_LOOKBACK    = 20

    capital        = CAPITAL_START
    total_fees     = 0.0
    peak_capital   = capital
    trough_capital = capital
    max_drawdown   = 0.0

    trades         = []
    equity_times   = [df["datetime"].iloc[0]]
    equity_curve   = [capital]

    i = 3
    while i < len(df) - 1:
        if capital <= 0:
            break

        row = df.iloc[i]

        # ── Filter 1: uptrend ──
        if row["close"] <= row["ema20"]:
            i += 1
            continue

        # ── Filter 2: WaveTrend oversold within last 20 candles ──
        lo = max(0, i - WT_LOOKBACK)
        if not (df["wt1"].iloc[lo : i + 1] < WT_THRESH).any():
            i += 1
            continue

        # ── Filter 3: three-step entry pattern ──
        c0 = df.iloc[i - 3]
        c1 = df.iloc[i - 2]   # step-1 candle
        c2 = df.iloc[i - 1]   # step-2 pullback candle
        c3 = df.iloc[i]       # step-3 entry candle

        step1 = (c1["close"] > c1["open"]) and (c1["high"] > c0["high"])
        step2 = (c2["close"] < c2["open"]) and (c2["low"]  < c1["low"])
        step3 = (c3["close"] > c3["open"]) and (c3["high"] > c2["high"])

        if not (step1 and step2 and step3):
            i += 1
            continue

        # ── Entry ──
        entry_price  = c2["high"]                     # break of pullback high
        atr_val      = row["atr10"]
        sl_price     = entry_price - 1.5 * atr_val
        risk_per_unit = entry_price - sl_price
        tp_price     = entry_price + 2.0 * risk_per_unit

        if risk_per_unit / entry_price > MAX_RISK_PCT:
            i += 1
            continue

        # Fees & position sizing
        entry_fee        = capital * FEE_RATE
        effective_capital = capital - entry_fee
        units            = effective_capital / entry_price
        total_fees      += entry_fee

        # ── Simulate trade ──
        result     = "timeout"
        exit_price = None
        exit_idx   = i

        end = min(i + 1 + MAX_HOLD, len(df))
        for j in range(i + 1, end):
            bar = df.iloc[j]
            if bar["low"] <= sl_price:
                exit_price = sl_price
                result     = "loss"
                exit_idx   = j
                break
            if bar["high"] >= tp_price:
                exit_price = tp_price
                result     = "win"
                exit_idx   = j
                break
        else:
            exit_idx   = min(i + MAX_HOLD, len(df) - 1)
            exit_price = df.iloc[exit_idx]["close"]
            result     = "timeout"

        exit_fee   = units * exit_price * FEE_RATE
        total_fees += exit_fee
        gross_pnl  = units * (exit_price - entry_price)
        net_pnl    = gross_pnl - exit_fee
        new_capital = effective_capital + gross_pnl - exit_fee

        # ── Drawdown tracking ──
        if new_capital >= peak_capital:
            peak_capital   = new_capital
            trough_capital = new_capital
        else:
            trough_capital = min(trough_capital, new_capital)
            dd = (peak_capital - trough_capital) / peak_capital * 100
            max_drawdown = max(max_drawdown, dd)

        trades.append({
            "trade_num"    : len(trades) + 1,
            "date"         : str(row["datetime"])[:16],
            "entry_price"  : round(entry_price,  2),
            "sl_price"     : round(sl_price,     2),
            "tp_price"     : round(tp_price,     2),
            "exit_price"   : round(exit_price,   2),
            "result"       : result,
            "net_pnl"      : round(net_pnl,      4),
            "capital_after": round(new_capital,  4),
        })

        equity_times.append(df["datetime"].iloc[exit_idx])
        equity_curve.append(round(new_capital, 4))

        capital = new_capital
        i       = exit_idx + 1

    # ── Summary ──
    wins      = [t for t in trades if t["result"] == "win"]
    losses    = [t for t in trades if t["result"] in ("loss", "timeout")]
    win_pnls  = [t["net_pnl"] for t in wins]
    loss_pnls = [t["net_pnl"] for t in losses]

    n = max(len(trades), 1)
    summary = {
        "label"           : label,
        "total_trades"    : len(trades),
        "wins"            : len(wins),
        "losses"          : len(losses),
        "win_rate"        : round(len(wins) / n * 100, 2),
        "start_capital"   : CAPITAL_START,
        "final_capital"   : round(capital, 4),
        "total_return_pct": round((capital - CAPITAL_START) / CAPITAL_START * 100, 2),
        "total_fees"      : round(total_fees, 4),
        "best_trade"      : round(max(win_pnls,  default=0), 4),
        "worst_trade"     : round(min(loss_pnls, default=0), 4),
        "max_drawdown_pct": round(max_drawdown, 2),
        "avg_win"         : round(np.mean(win_pnls)  if win_pnls  else 0, 4),
        "avg_loss"        : round(np.mean(loss_pnls) if loss_pnls else 0, 4),
    }
    return summary, trades, equity_curve, equity_times


# ─────────────────────────────────────────────────────────────
# CELL 7 — Run Both Backtests
# ─────────────────────────────────────────────────────────────
print("Running 4H backtest...")
sum4h, trades4h, eq4h, eqt4h = run_backtest(df_4h, "4H")
print(f"  → {sum4h['total_trades']} trades found")

print("Running 1H backtest...")
sum1h, trades1h, eq1h, eqt1h = run_backtest(df_1h, "1H")
print(f"  → {sum1h['total_trades']} trades found")


# ─────────────────────────────────────────────────────────────
# CELL 8 — Print Terminal Summary
# ─────────────────────────────────────────────────────────────
SEP  = "=" * 62
sep2 = "-" * 62
FMT  = "  {:<26} {:>16} {:>16}"

print(f"\n{SEP}")
print("  XAUUSD GOLD BACKTEST — RESULTS SUMMARY")
print(SEP)

for s in [sum4h, sum1h]:
    ret_sign = "+" if s["total_return_pct"] >= 0 else ""
    print(f"\n  ── {s['label']} TIMEFRAME ──")
    print(f"  Total Trades     : {s['total_trades']}")
    print(f"  Wins / Losses    : {s['wins']} / {s['losses']}")
    print(f"  Win Rate         : {s['win_rate']}%")
    print(f"  Start Capital    : ${s['start_capital']:.2f}")
    print(f"  Final Capital    : ${s['final_capital']:.4f}")
    print(f"  Total Return     : {ret_sign}{s['total_return_pct']}%")
    print(f"  Total Fees Paid  : ${s['total_fees']:.4f}")
    print(f"  Best Trade       : +${s['best_trade']:.4f}")
    print(f"  Worst Trade      : ${s['worst_trade']:.4f}")
    print(f"  Max Drawdown     : {s['max_drawdown_pct']}%")
    print(f"  Avg Win          : +${s['avg_win']:.4f}")
    print(f"  Avg Loss         : ${s['avg_loss']:.4f}")

print(f"\n{SEP}")
print("  4H vs 1H COMPARISON")
print(SEP)
print(FMT.format("Metric", "4H", "1H"))
print("  " + sep2)

rows = [
    ("Total Trades",   str(sum4h["total_trades"]),                   str(sum1h["total_trades"])),
    ("Wins",           str(sum4h["wins"]),                           str(sum1h["wins"])),
    ("Losses",         str(sum4h["losses"]),                         str(sum1h["losses"])),
    ("Win Rate",       f"{sum4h['win_rate']}%",                      f"{sum1h['win_rate']}%"),
    ("Start Capital",  f"${sum4h['start_capital']:.2f}",             f"${sum1h['start_capital']:.2f}"),
    ("Final Capital",  f"${sum4h['final_capital']:.4f}",             f"${sum1h['final_capital']:.4f}"),
    ("Total Return",   f"{sum4h['total_return_pct']}%",              f"{sum1h['total_return_pct']}%"),
    ("Total Fees",     f"${sum4h['total_fees']:.4f}",                f"${sum1h['total_fees']:.4f}"),
    ("Best Trade",     f"+${sum4h['best_trade']:.4f}",               f"+${sum1h['best_trade']:.4f}"),
    ("Worst Trade",    f"${sum4h['worst_trade']:.4f}",               f"${sum1h['worst_trade']:.4f}"),
    ("Max Drawdown",   f"{sum4h['max_drawdown_pct']}%",              f"{sum1h['max_drawdown_pct']}%"),
    ("Avg Win",        f"+${sum4h['avg_win']:.4f}",                  f"+${sum1h['avg_win']:.4f}"),
    ("Avg Loss",       f"${sum4h['avg_loss']:.4f}",                  f"${sum1h['avg_loss']:.4f}"),
]
for name, v4, v1 in rows:
    print(FMT.format(name, v4, v1))
print(SEP)


# ─────────────────────────────────────────────────────────────
# CELL 9 — Trade Tables
# ─────────────────────────────────────────────────────────────
def print_trade_table(trades, label):
    if not trades:
        print(f"\n  No trades found for {label}.")
        return
    hdr = f"{'#':>3}  {'Date':<17} {'Entry':>8} {'SL':>8} {'TP':>8} {'Exit':>8}  {'Result':<8} {'P&L':>9}  {'Capital':>10}"
    print(f"\n{'─'*84}")
    print(f"  ALL TRADES — {label}")
    print(f"{'─'*84}")
    print("  " + hdr)
    print("  " + "─" * 82)
    for t in trades:
        pnl_str = f"+${t['net_pnl']:.4f}" if t["net_pnl"] >= 0 else f"-${abs(t['net_pnl']):.4f}"
        marker  = "✅" if t["result"] == "win" else ("❌" if t["result"] == "loss" else "⏱")
        print(f"  {t['trade_num']:>3}  {t['date']:<17} {t['entry_price']:>8.2f} "
              f"{t['sl_price']:>8.2f} {t['tp_price']:>8.2f} {t['exit_price']:>8.2f}  "
              f"{marker} {t['result']:<6}  {pnl_str:>9}  ${t['capital_after']:>9.4f}")

print_trade_table(trades4h, "4H")
print_trade_table(trades1h, "1H")


# ─────────────────────────────────────────────────────────────
# CELL 10 — Build HTML Report
# ─────────────────────────────────────────────────────────────
import json
from datetime import datetime

def build_html_report(sum4h, trades4h, eq4h, eqt4h,
                      sum1h, trades1h, eq1h, eqt1h):

    def trade_rows_html(trades):
        if not trades:
            return '<tr><td colspan="9" style="text-align:center;color:#888">No trades</td></tr>'
        palette = {"win": "#1a3a1a", "loss": "#3a1a1a", "timeout": "#2a2a0a"}
        icons   = {"win": "✅", "loss": "❌", "timeout": "⏱"}
        out = ""
        for t in trades:
            bg  = palette.get(t["result"], "#1e2130")
            ico = icons.get(t["result"], "")
            pnl_color = "#4caf50" if t["net_pnl"] >= 0 else "#f44336"
            pnl_str   = f'+${t["net_pnl"]:.4f}' if t["net_pnl"] >= 0 else f'-${abs(t["net_pnl"]):.4f}'
            out += f"""<tr style="background:{bg}">
              <td>{t['trade_num']}</td>
              <td>{t['date']}</td>
              <td>${t['entry_price']:.2f}</td>
              <td>${t['sl_price']:.2f}</td>
              <td>${t['tp_price']:.2f}</td>
              <td>${t['exit_price']:.2f}</td>
              <td><b>{ico} {t['result'].upper()}</b></td>
              <td style="color:{pnl_color};font-weight:700">{pnl_str}</td>
              <td>${t['capital_after']:.4f}</td>
            </tr>"""
        return out

    def stat_cards(s):
        ret_col = "#4caf50" if s["total_return_pct"] >= 0 else "#f44336"
        ret_sign = "+" if s["total_return_pct"] >= 0 else ""
        items = [
            ("Total Trades",  str(s["total_trades"]),                    "#e0e0e0"),
            ("Wins",          str(s["wins"]),                            "#4caf50"),
            ("Losses",        str(s["losses"]),                          "#f44336"),
            ("Win Rate",      f"{s['win_rate']}%",                       "#e0e0e0"),
            ("Start Capital", f"${s['start_capital']:.2f}",              "#e0e0e0"),
            ("Final Capital", f"${s['final_capital']:.4f}",              ret_col),
            ("Total Return",  f"{ret_sign}{s['total_return_pct']}%",     ret_col),
            ("Total Fees",    f"${s['total_fees']:.4f}",                 "#FF9800"),
            ("Best Trade",    f"+${s['best_trade']:.4f}",                "#4caf50"),
            ("Worst Trade",   f"${s['worst_trade']:.4f}",                "#f44336"),
            ("Max Drawdown",  f"{s['max_drawdown_pct']}%",               "#f44336"),
            ("Avg Win",       f"+${s['avg_win']:.4f}",                   "#4caf50"),
            ("Avg Loss",      f"${s['avg_loss']:.4f}",                   "#f44336"),
        ]
        cards = ""
        for lbl, val, col in items:
            cards += f"""<div class="card">
              <div class="clbl">{lbl}</div>
              <div class="cval" style="color:{col}">{val}</div>
            </div>"""
        return cards

    # Equity curve JSON
    eq4h_labels = json.dumps([str(t)[:16] for t in eqt4h])
    eq1h_labels = json.dumps([str(t)[:16] for t in eqt1h])
    eq4h_data   = json.dumps(eq4h)
    eq1h_data   = json.dumps(eq1h)

    # Overlay: trade-indexed
    max_len = max(len(eq4h), len(eq1h))
    eq4h_pad = eq4h + [eq4h[-1]] * (max_len - len(eq4h))
    eq1h_pad = eq1h + [eq1h[-1]] * (max_len - len(eq1h))
    ov_labels = json.dumps([f"T{i}" if i > 0 else "Start" for i in range(max_len)])

    # Comparison rows
    cmp_rows = ""
    metrics = [
        ("Total Trades",  str(sum4h["total_trades"]),           str(sum1h["total_trades"])),
        ("Wins",          str(sum4h["wins"]),                   str(sum1h["wins"])),
        ("Losses",        str(sum4h["losses"]),                 str(sum1h["losses"])),
        ("Win Rate",      f"{sum4h['win_rate']}%",              f"{sum1h['win_rate']}%"),
        ("Start Capital", f"${sum4h['start_capital']:.2f}",     f"${sum1h['start_capital']:.2f}"),
        ("Final Capital", f"${sum4h['final_capital']:.4f}",     f"${sum1h['final_capital']:.4f}"),
        ("Total Return",  f"{sum4h['total_return_pct']}%",      f"{sum1h['total_return_pct']}%"),
        ("Total Fees",    f"${sum4h['total_fees']:.4f}",        f"${sum1h['total_fees']:.4f}"),
        ("Best Trade",    f"+${sum4h['best_trade']:.4f}",       f"+${sum1h['best_trade']:.4f}"),
        ("Worst Trade",   f"${sum4h['worst_trade']:.4f}",       f"${sum1h['worst_trade']:.4f}"),
        ("Max Drawdown",  f"{sum4h['max_drawdown_pct']}%",      f"{sum1h['max_drawdown_pct']}%"),
        ("Avg Win",       f"+${sum4h['avg_win']:.4f}",          f"+${sum1h['avg_win']:.4f}"),
        ("Avg Loss",      f"${sum4h['avg_loss']:.4f}",          f"${sum1h['avg_loss']:.4f}"),
    ]
    for name, v4, v1 in metrics:
        cmp_rows += f"<tr><td>{name}</td><td>{v4}</td><td>{v1}</td></tr>"

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>XAUUSD Gold Backtest Report</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
<style>
  *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
  :root {{
    --bg:      #0d0f16;
    --surface: #161923;
    --card:    #1e2235;
    --border:  #2a2d3e;
    --gold:    #FFD700;
    --blue:    #2196F3;
    --orange:  #FF9800;
    --green:   #4caf50;
    --red:     #f44336;
    --text:    #e0e0e0;
    --muted:   #888;
  }}
  body {{ font-family: 'Segoe UI', system-ui, sans-serif; background: var(--bg); color: var(--text);
          padding: 24px; line-height: 1.5; }}
  h1   {{ text-align: center; color: var(--gold); font-size: 2rem; margin-bottom: 4px; }}
  .sub {{ text-align: center; color: var(--muted); margin-bottom: 32px; font-size: 0.9rem; }}
  h2   {{ color: var(--gold); font-size: 1.25rem; border-bottom: 2px solid #FFD70033;
          padding-bottom: 8px; margin: 32px 0 16px; }}
  h3   {{ color: var(--muted); font-size: 1rem; margin: 20px 0 10px; }}

  /* Stat cards */
  .cards {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(155px, 1fr)); gap: 12px; margin-bottom: 24px; }}
  .card  {{ background: var(--card); border: 1px solid var(--border); border-radius: 10px;
            padding: 14px; display: flex; flex-direction: column; gap: 5px; }}
  .clbl  {{ font-size: 0.72rem; color: var(--muted); text-transform: uppercase; letter-spacing: .05em; }}
  .cval  {{ font-size: 1.18rem; font-weight: 700; }}

  /* Chart wrapper */
  .chart-box {{ background: var(--surface); border: 1px solid var(--border); border-radius: 12px;
                padding: 20px; margin-bottom: 28px; }}
  canvas {{ max-height: 300px; }}

  /* Tables */
  .tbl-wrap {{ overflow-x: auto; margin-bottom: 28px; border-radius: 10px;
               border: 1px solid var(--border); }}
  table  {{ width: 100%; border-collapse: collapse; font-size: 0.82rem; min-width: 680px; }}
  thead th {{ background: #12141f; color: var(--gold); padding: 11px 10px; text-align: left;
              position: sticky; top: 0; white-space: nowrap; }}
  tbody td {{ padding: 9px 10px; border-bottom: 1px solid var(--border); white-space: nowrap; }}
  tbody tr:hover td {{ filter: brightness(1.15); }}

  /* Comparison table */
  .cmp thead th:nth-child(2) {{ color: var(--blue); }}
  .cmp thead th:nth-child(3) {{ color: var(--orange); }}

  /* Section wrapper */
  .section {{ background: var(--surface); border: 1px solid var(--border); border-radius: 14px;
              padding: 24px; margin-bottom: 30px; }}

  /* Badge */
  .badge {{ display: inline-block; padding: 3px 10px; border-radius: 20px; font-size: 0.78rem;
            font-weight: 700; }}
  .badge-4h {{ background: #2196F322; color: var(--blue); border: 1px solid #2196F366; }}
  .badge-1h {{ background: #FF980022; color: var(--orange); border: 1px solid #FF980066; }}

  @media (max-width: 640px) {{ .cards {{ grid-template-columns: 1fr 1fr; }} }}
</style>
</head>
<body>

<h1>📊 XAUUSD Gold Backtest</h1>
<p class="sub">
  WaveTrend(10,21) + Second-Entry Pattern &nbsp;|&nbsp;
  Real GC=F Data (yfinance) &nbsp;|&nbsp;
  Generated {datetime.now().strftime("%Y-%m-%d %H:%M UTC")}
</p>

<!-- ══════════════════ 4H ══════════════════ -->
<div class="section">
  <h2><span class="badge badge-4h">4H</span> &nbsp;Timeframe Results</h2>
  <div class="cards">{stat_cards(sum4h)}</div>

  <div class="chart-box">
    <canvas id="chart4h"></canvas>
  </div>

  <h3>All Trades — 4H</h3>
  <div class="tbl-wrap">
    <table>
      <thead><tr>
        <th>#</th><th>Date</th><th>Entry $</th><th>Stop Loss $</th>
        <th>Take Profit $</th><th>Exit $</th><th>Result</th>
        <th>Net P&amp;L $</th><th>Capital After $</th>
      </tr></thead>
      <tbody>{trade_rows_html(trades4h)}</tbody>
    </table>
  </div>
</div>

<!-- ══════════════════ 1H ══════════════════ -->
<div class="section">
  <h2><span class="badge badge-1h">1H</span> &nbsp;Timeframe Results</h2>
  <div class="cards">{stat_cards(sum1h)}</div>

  <div class="chart-box">
    <canvas id="chart1h"></canvas>
  </div>

  <h3>All Trades — 1H</h3>
  <div class="tbl-wrap">
    <table>
      <thead><tr>
        <th>#</th><th>Date</th><th>Entry $</th><th>Stop Loss $</th>
        <th>Take Profit $</th><th>Exit $</th><th>Result</th>
        <th>Net P&amp;L $</th><th>Capital After $</th>
      </tr></thead>
      <tbody>{trade_rows_html(trades1h)}</tbody>
    </table>
  </div>
</div>

<!-- ══════════════════ COMPARISON ══════════════════ -->
<div class="section">
  <h2>📋 4H vs 1H Comparison</h2>
  <div class="tbl-wrap cmp">
    <table>
      <thead><tr>
        <th>Metric</th>
        <th><span class="badge badge-4h">4H</span></th>
        <th><span class="badge badge-1h">1H</span></th>
      </tr></thead>
      <tbody>{cmp_rows}</tbody>
    </table>
  </div>

  <h3>Equity Curves — Side by Side (per trade)</h3>
  <div class="chart-box">
    <canvas id="chartOverlay"></canvas>
  </div>
</div>

<script>
const chartDefaults = {{
  responsive: true,
  interaction: {{ mode: 'index', intersect: false }},
  plugins: {{
    legend: {{ labels: {{ color: '#ccc', padding: 16 }} }},
    tooltip: {{ callbacks: {{ label: ctx => ' $' + ctx.parsed.y.toFixed(4) }} }}
  }},
  scales: {{
    x: {{ ticks: {{ color: '#888', maxTicksLimit: 10 }}, grid: {{ color: '#1e2235' }} }},
    y: {{ ticks: {{ color: '#888', callback: v => '$' + v.toFixed(2) }},
          grid: {{ color: '#1e2235' }} }}
  }}
}};

// ── 4H chart ──
new Chart(document.getElementById('chart4h'), {{
  type: 'line',
  data: {{
    labels: {eq4h_labels},
    datasets: [{{
      label: '4H Equity ($)',
      data: {eq4h_data},
      borderColor: '#2196F3',
      backgroundColor: 'rgba(33,150,243,0.08)',
      fill: true, tension: 0.35, pointRadius: 3, pointHoverRadius: 6,
      borderWidth: 2,
    }}]
  }},
  options: {{ ...chartDefaults,
    plugins: {{ ...chartDefaults.plugins,
      title: {{ display: true, text: '4H Equity Curve', color: '#FFD700', font: {{ size: 14 }} }}
    }}
  }}
}});

// ── 1H chart ──
new Chart(document.getElementById('chart1h'), {{
  type: 'line',
  data: {{
    labels: {eq1h_labels},
    datasets: [{{
      label: '1H Equity ($)',
      data: {eq1h_data},
      borderColor: '#FF9800',
      backgroundColor: 'rgba(255,152,0,0.08)',
      fill: true, tension: 0.35, pointRadius: 3, pointHoverRadius: 6,
      borderWidth: 2,
    }}]
  }},
  options: {{ ...chartDefaults,
    plugins: {{ ...chartDefaults.plugins,
      title: {{ display: true, text: '1H Equity Curve', color: '#FFD700', font: {{ size: 14 }} }}
    }}
  }}
}});

// ── Overlay chart (trade-indexed) ──
new Chart(document.getElementById('chartOverlay'), {{
  type: 'line',
  data: {{
    labels: {ov_labels},
    datasets: [
      {{
        label: '4H Equity ($)',
        data: {json.dumps(eq4h_pad)},
        borderColor: '#2196F3', backgroundColor: 'rgba(33,150,243,0.06)',
        fill: false, tension: 0.35, pointRadius: 4, pointHoverRadius: 7,
        borderWidth: 2.5,
      }},
      {{
        label: '1H Equity ($)',
        data: {json.dumps(eq1h_pad)},
        borderColor: '#FF9800', backgroundColor: 'rgba(255,152,0,0.06)',
        fill: false, tension: 0.35, pointRadius: 4, pointHoverRadius: 7,
        borderWidth: 2.5,
      }}
    ]
  }},
  options: {{ ...chartDefaults,
    plugins: {{ ...chartDefaults.plugins,
      title: {{ display: true, text: '4H vs 1H Equity — Per Trade Comparison',
               color: '#FFD700', font: {{ size: 14 }} }}
    }}
  }}
}});
</script>
</body>
</html>"""
    return html


html_report = build_html_report(
    sum4h, trades4h, eq4h, eqt4h,
    sum1h, trades1h, eq1h, eqt1h
)


# ─────────────────────────────────────────────────────────────
# CELL 11 — Save HTML Report
# ─────────────────────────────────────────────────────────────
import os

# Colab saves to /content/ by default; also try Google Drive if mounted
REPORT_PATH = "/content/gold_backtest_report.html"

with open(REPORT_PATH, "w", encoding="utf-8") as f:
    f.write(html_report)

print(f"✅ HTML report saved → {REPORT_PATH}")

# Auto-download in Colab
try:
    from google.colab import files
    files.download(REPORT_PATH)
    print("📥 Download started automatically.")
except Exception:
    print("   (Not in Colab — open the file manually.)")


# ─────────────────────────────────────────────────────────────
# CELL 12 — Display Equity Chart Inline (Colab)
# ─────────────────────────────────────────────────────────────
import plotly.graph_objects as go
from plotly.subplots import make_subplots

fig = make_subplots(
    rows=2, cols=2,
    subplot_titles=(
        "4H Equity Curve",
        "1H Equity Curve",
        "4H vs 1H Overlay (per trade)",
        "Equity Drawdown Comparison",
    ),
    vertical_spacing=0.14,
    horizontal_spacing=0.08,
)

# 4H equity
fig.add_trace(go.Scatter(
    x=[str(t)[:16] for t in eqt4h], y=eq4h,
    mode="lines+markers", name="4H Equity",
    line=dict(color="#2196F3", width=2.5),
    marker=dict(size=5),
    fill="tozeroy", fillcolor="rgba(33,150,243,0.07)",
), row=1, col=1)

# 1H equity
fig.add_trace(go.Scatter(
    x=[str(t)[:16] for t in eqt1h], y=eq1h,
    mode="lines+markers", name="1H Equity",
    line=dict(color="#FF9800", width=2.5),
    marker=dict(size=5),
    fill="tozeroy", fillcolor="rgba(255,152,0,0.07)",
), row=1, col=2)

# Overlay
max_len = max(len(eq4h), len(eq1h))
trade_idx = list(range(max_len))
eq4h_pad = eq4h + [eq4h[-1]] * (max_len - len(eq4h))
eq1h_pad = eq1h + [eq1h[-1]] * (max_len - len(eq1h))

fig.add_trace(go.Scatter(
    x=trade_idx, y=eq4h_pad,
    mode="lines+markers", name="4H (overlay)",
    line=dict(color="#2196F3", width=2),
    marker=dict(size=6, symbol="circle"),
    showlegend=False,
), row=2, col=1)
fig.add_trace(go.Scatter(
    x=trade_idx, y=eq1h_pad,
    mode="lines+markers", name="1H (overlay)",
    line=dict(color="#FF9800", width=2),
    marker=dict(size=6, symbol="diamond"),
    showlegend=False,
), row=2, col=1)

# Drawdown comparison (bar chart)
fig.add_trace(go.Bar(
    x=["4H", "1H"],
    y=[sum4h["max_drawdown_pct"], sum1h["max_drawdown_pct"]],
    marker_color=["#2196F3", "#FF9800"],
    name="Max Drawdown %",
    text=[f"{sum4h['max_drawdown_pct']}%", f"{sum1h['max_drawdown_pct']}%"],
    textposition="outside",
    showlegend=False,
), row=2, col=2)

fig.update_layout(
    height=700,
    title=dict(text="XAUUSD Gold Backtest — Equity Curves", font=dict(size=18, color="#FFD700")),
    paper_bgcolor="#0d0f16",
    plot_bgcolor="#161923",
    font=dict(color="#e0e0e0"),
    legend=dict(bgcolor="#1e2235", bordercolor="#2a2d3e", borderwidth=1),
    margin=dict(t=80, b=40, l=50, r=30),
)
fig.update_xaxes(gridcolor="#1e2235", linecolor="#2a2d3e")
fig.update_yaxes(gridcolor="#1e2235", linecolor="#2a2d3e",
                 tickprefix="$", row=1, col=1)
fig.update_yaxes(gridcolor="#1e2235", linecolor="#2a2d3e",
                 tickprefix="$", row=1, col=2)
fig.update_yaxes(gridcolor="#1e2235", linecolor="#2a2d3e",
                 tickprefix="$", row=2, col=1)
fig.update_yaxes(gridcolor="#1e2235", linecolor="#2a2d3e",
                 ticksuffix="%", row=2, col=2)

fig.show()


# ─────────────────────────────────────────────────────────────
# CELL 13 — Display summary inline as styled HTML (Colab)
# ─────────────────────────────────────────────────────────────
def summary_html(s):
    ret_col = "green" if s["total_return_pct"] >= 0 else "red"
    ret_sign = "+" if s["total_return_pct"] >= 0 else ""
    return f"""
    <div style="display:inline-block;background:#1e2235;border:1px solid #2a2d3e;
                border-radius:12px;padding:20px 28px;margin:10px;min-width:280px;
                font-family:monospace;color:#e0e0e0">
      <div style="color:#FFD700;font-size:1.1em;font-weight:bold;margin-bottom:12px">
        {s['label']} Timeframe
      </div>
      <table style="border-collapse:collapse;width:100%">
        <tr><td style="color:#888;padding:3px 0">Total Trades</td>
            <td style="text-align:right;font-weight:bold">{s['total_trades']}</td></tr>
        <tr><td style="color:#888;padding:3px 0">Wins / Losses</td>
            <td style="text-align:right"><span style="color:green">{s['wins']}</span> /
            <span style="color:red">{s['losses']}</span></td></tr>
        <tr><td style="color:#888;padding:3px 0">Win Rate</td>
            <td style="text-align:right;font-weight:bold">{s['win_rate']}%</td></tr>
        <tr><td style="color:#888;padding:3px 0">Final Capital</td>
            <td style="text-align:right;color:{ret_col};font-weight:bold">${s['final_capital']:.4f}</td></tr>
        <tr><td style="color:#888;padding:3px 0">Total Return</td>
            <td style="text-align:right;color:{ret_col};font-weight:bold">{ret_sign}{s['total_return_pct']}%</td></tr>
        <tr><td style="color:#888;padding:3px 0">Total Fees</td>
            <td style="text-align:right;color:orange">${s['total_fees']:.4f}</td></tr>
        <tr><td style="color:#888;padding:3px 0">Best Trade</td>
            <td style="text-align:right;color:green">+${s['best_trade']:.4f}</td></tr>
        <tr><td style="color:#888;padding:3px 0">Worst Trade</td>
            <td style="text-align:right;color:red">${s['worst_trade']:.4f}</td></tr>
        <tr><td style="color:#888;padding:3px 0">Max Drawdown</td>
            <td style="text-align:right;color:red">{s['max_drawdown_pct']}%</td></tr>
        <tr><td style="color:#888;padding:3px 0">Avg Win</td>
            <td style="text-align:right;color:green">+${s['avg_win']:.4f}</td></tr>
        <tr><td style="color:#888;padding:3px 0">Avg Loss</td>
            <td style="text-align:right;color:red">${s['avg_loss']:.4f}</td></tr>
      </table>
    </div>"""

display(HTML(
    '<div style="background:#0d0f16;padding:20px;border-radius:14px">'
    '<div style="color:#FFD700;font-size:1.3em;font-weight:bold;text-align:center;'
    'margin-bottom:16px">XAUUSD Backtest Summary</div>'
    + summary_html(sum4h) + summary_html(sum1h) +
    '</div>'
))
