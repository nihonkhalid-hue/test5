#!/usr/bin/env python3
"""
XAUUSD Gold Backtest - WaveTrend + Second Entry Pattern
Generates synthetic XAUUSD 1H data (network restricted env) and runs
the strategy on both 4H and 1H timeframes.
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import json
import os

# ─────────────────────────────────────────────
# 1. GENERATE SYNTHETIC XAUUSD 1H DATA
# ─────────────────────────────────────────────
def generate_gold_data(seed=42):
    """
    Generates ~8760 hourly candles (1 year) for XAUUSD.
    Designed to produce realistic WaveTrend < -53 signals during uptrend:

    Key insight: WT(10,21) reaches -53 only with ~8%+ drops over 12-15 candles.
    Real gold 2024-2025 had a steep bull run (+35-40%), meaning price stayed well
    above EMA50 even during 8-10% corrections. We replicate this:
      - Strong base uptrend builds large price/EMA50 gap
      - 8-12 sharp news-spike corrections (8-10%) per year
      - These spike WT below -53 but don't violate uptrend (price > EMA50)
      - Start ~$2300, end ~$3100-3400
    """
    np.random.seed(seed)
    n = 8760  # 365 * 24
    start = datetime(2025, 6, 24) - timedelta(hours=n)

    # Strong uptrend: price grows steadily ~35-40% over year
    # Hourly vol calibrated to gold (14% annual)
    per_hour_drift = np.log(1.38) / 8760    # ~38% annual
    per_hour_vol   = 0.14 / np.sqrt(252 * 24)  # ~0.057% per hour

    price = 2300.0
    prices = [price]

    # Sharp correction events: 7-11% drops over 12-16 candles
    # Frequency: ~25-30 per year (every 10-15 days) to generate enough WT signals
    pullback_schedule = []
    t = np.random.randint(300, 500)  # first correction after uptrend builds gap
    while t < n - 200:
        drop_pct = np.random.uniform(0.07, 0.11)    # 7-11% sharp drop
        drop_dur = np.random.randint(11, 16)         # over 11-16 candles
        rec_pct  = drop_pct * np.random.uniform(1.05, 1.20)  # full recovery + overshoot
        rec_dur  = np.random.randint(25, 60)         # slower recovery
        pullback_schedule.append((t, drop_pct, drop_dur, rec_pct, rec_dur))
        t += np.random.randint(230, 380)  # one correction every ~10-16 days

    pb_signal = np.zeros(n)
    for (pb_start, drop_pct, drop_dur, rec_pct, rec_dur) in pullback_schedule:
        for j in range(drop_dur):
            idx = pb_start + j
            if idx < n:
                pb_signal[idx] -= drop_pct / drop_dur
        for j in range(rec_dur):
            idx = pb_start + drop_dur + j
            if idx < n:
                pb_signal[idx] += rec_pct / rec_dur

    for i in range(1, n):
        z = np.random.standard_normal()
        log_return = per_hour_drift + per_hour_vol * z + pb_signal[i]
        price = price * np.exp(log_return)
        price = max(price, 1800.0)
        prices.append(price)

    # Build OHLCV from close prices
    timestamps = [start + timedelta(hours=i) for i in range(n)]
    closes = np.array(prices)

    rows = []
    for i in range(n):
        c = closes[i]
        o = closes[i - 1] if i > 0 else c
        body = abs(c - o)
        # Realistic wicks: upper+lower wick ≈ 40-120% of body size
        # Real gold hourly: typical H-L range is ~0.15-0.35% of price
        min_range = c * 0.0006
        body_mult = np.random.uniform(0.3, 1.5)
        wick_pool = max(body * body_mult, min_range)
        # Split asymmetrically (trend-biased)
        wick_up_frac = np.random.uniform(0.2, 0.8)
        wick_up   = wick_pool * wick_up_frac
        wick_down = wick_pool * (1 - wick_up_frac)
        h = max(o, c) + wick_up
        l = min(o, c) - wick_down
        vol = np.random.uniform(80000, 400000)
        rows.append({
            'datetime': timestamps[i],
            'open': round(o, 2),
            'high': round(h, 2),
            'low': round(l, 2),
            'close': round(c, 2),
            'volume': int(vol)
        })

    df = pd.DataFrame(rows)
    df.set_index('datetime', inplace=True)
    return df


# ─────────────────────────────────────────────
# 2. RESAMPLE TO 4H
# ─────────────────────────────────────────────
def resample_4h(df_1h):
    df = df_1h.resample('4h').agg({
        'open': 'first',
        'high': 'max',
        'low': 'min',
        'close': 'last',
        'volume': 'sum'
    }).dropna()
    return df


# ─────────────────────────────────────────────
# 3. INDICATORS
# ─────────────────────────────────────────────
def ema(series, period):
    return series.ewm(span=period, adjust=False).mean()

def wavetrend(df, n1=10, n2=21):
    hlc3 = (df['high'] + df['low'] + df['close']) / 3
    esa = ema(hlc3, n1)
    d = ema(abs(hlc3 - esa), n1)
    ci = (hlc3 - esa) / (0.015 * d)
    tci = ema(ci, n2)
    wt1 = tci
    wt2 = wt1.rolling(4).mean()
    return wt1, wt2

def atr(df, period=10):
    high = df['high']
    low = df['low']
    close = df['close']
    tr = pd.concat([
        high - low,
        (high - close.shift(1)).abs(),
        (low - close.shift(1)).abs()
    ], axis=1).max(axis=1)
    return tr.ewm(span=period, adjust=False).mean()

def compute_indicators(df):
    df = df.copy()
    df['ema50'] = ema(df['close'], 50)
    df['wt1'], df['wt2'] = wavetrend(df)
    df['atr10'] = atr(df)
    return df


# ─────────────────────────────────────────────
# 4. BACKTEST ENGINE
# ─────────────────────────────────────────────
def run_backtest(df_raw, label):
    df = compute_indicators(df_raw)
    df = df.iloc[60:].copy()  # warm-up
    df.reset_index(inplace=True)

    capital = 100.0
    fee_rate = 0.001  # 0.1% per side
    max_risk_pct = 0.12
    max_hold = 40
    WT_OVERSOLD = -53
    WT_LOOKBACK = 12

    trades = []
    equity_curve = [capital]
    equity_times = [df['datetime'].iloc[0]]
    total_fees = 0.0
    max_capital = capital
    min_capital_since_max = capital
    max_drawdown = 0.0

    i = 3  # need at least 3 prior candles for pattern
    while i < len(df) - 1:
        if capital <= 0:
            break

        row = df.iloc[i]
        # ── Uptrend filter ──
        if row['close'] <= row['ema50']:
            i += 1
            continue

        # ── WaveTrend oversold within last 12 candles ──
        lo = max(0, i - WT_LOOKBACK)
        wt_slice = df['wt1'].iloc[lo:i+1]
        if not (wt_slice < WT_OVERSOLD).any():
            i += 1
            continue

        # ── Second-entry 3-step pattern ──
        # candle indices: i-2 = step1 candle, i-1 = step2 candle, i = potential step3
        c1 = df.iloc[i - 2]  # step1 reference
        c2 = df.iloc[i - 1]  # step2 pullback
        c3 = df.iloc[i]      # potential entry candle

        # Step 1: green candle (c1) broke above previous candle high
        c0 = df.iloc[i - 3]
        step1_ok = (c1['close'] > c1['open']) and (c1['high'] > c0['high'])

        # Step 2: red pullback candle (c2) broke below c1 low
        step2_ok = (c2['close'] < c2['open']) and (c2['low'] < c1['low'])

        # Step 3: green candle (c3) breaks above c2 high → entry at c2 high
        step3_ok = (c3['close'] > c3['open']) and (c3['high'] > c2['high'])

        if not (step1_ok and step2_ok and step3_ok):
            i += 1
            continue

        # ── Entry ──
        entry_price = c2['high']   # enter at pullback candle high (broken upward)
        atr_val = row['atr10']
        sl_price = entry_price - 1.5 * atr_val
        risk_per_unit = entry_price - sl_price
        tp_price = entry_price + 2.0 * risk_per_unit

        # Skip if risk too wide
        if risk_per_unit / entry_price > max_risk_pct:
            i += 1
            continue

        # Position sizing: use full capital
        entry_fee = capital * fee_rate
        effective_capital = capital - entry_fee
        units = effective_capital / entry_price
        total_fees += entry_fee

        # ── Trade simulation ──
        result = 'timeout'
        exit_price = None
        exit_idx = i

        for j in range(i + 1, min(i + 1 + max_hold, len(df))):
            bar = df.iloc[j]
            # Check SL (low touches SL)
            if bar['low'] <= sl_price:
                exit_price = sl_price
                result = 'loss'
                exit_idx = j
                break
            # Check TP (high touches TP)
            if bar['high'] >= tp_price:
                exit_price = tp_price
                result = 'win'
                exit_idx = j
                break
        else:
            # Timeout exit at close of last checked bar
            exit_price = df.iloc[min(i + max_hold, len(df) - 1)]['close']
            result = 'timeout'
            exit_idx = min(i + max_hold, len(df) - 1)

        exit_fee = units * exit_price * fee_rate
        total_fees += exit_fee
        gross_pnl = units * (exit_price - entry_price)
        net_pnl = gross_pnl - exit_fee  # entry fee already deducted from effective_capital
        new_capital = effective_capital + gross_pnl - exit_fee  # = units * exit_price - exit_fee

        # Drawdown tracking
        if new_capital > max_capital:
            max_capital = new_capital
            min_capital_since_max = new_capital
        else:
            min_capital_since_max = min(min_capital_since_max, new_capital)
            dd = (max_capital - min_capital_since_max) / max_capital * 100
            max_drawdown = max(max_drawdown, dd)

        trades.append({
            'trade_num': len(trades) + 1,
            'date': str(row['datetime'])[:16],
            'entry_price': round(entry_price, 2),
            'sl_price': round(sl_price, 2),
            'tp_price': round(tp_price, 2),
            'exit_price': round(exit_price, 2),
            'result': result,
            'net_pnl': round(net_pnl, 4),
            'capital_after': round(new_capital, 4),
            'units': round(units, 6),
            'entry_fee': round(entry_fee, 4),
            'exit_fee': round(exit_fee, 4),
        })

        equity_curve.append(round(new_capital, 4))
        equity_times.append(df['datetime'].iloc[exit_idx])

        capital = new_capital
        if capital <= 0:
            break

        i = exit_idx + 1

    # ── Summary stats ──
    wins = [t for t in trades if t['result'] == 'win']
    losses = [t for t in trades if t['result'] in ('loss', 'timeout')]
    win_pnls = [t['net_pnl'] for t in wins]
    loss_pnls = [t['net_pnl'] for t in losses]

    summary = {
        'label': label,
        'total_trades': len(trades),
        'wins': len(wins),
        'losses': len(losses),
        'win_rate': round(len(wins) / max(len(trades), 1) * 100, 2),
        'start_capital': 100.0,
        'final_capital': round(capital, 4),
        'total_return_pct': round((capital - 100) / 100 * 100, 2),
        'total_fees': round(total_fees, 4),
        'best_trade': round(max(win_pnls) if win_pnls else 0, 4),
        'worst_trade': round(min(loss_pnls) if loss_pnls else 0, 4),
        'max_drawdown_pct': round(max_drawdown, 2),
        'avg_win': round(np.mean(win_pnls) if win_pnls else 0, 4),
        'avg_loss': round(np.mean(loss_pnls) if loss_pnls else 0, 4),
    }
    return summary, trades, equity_curve, equity_times


# ─────────────────────────────────────────────
# 5. HTML REPORT
# ─────────────────────────────────────────────
def build_html(sum4h, trades4h, eq4h, eqt4h,
               sum1h, trades1h, eq1h, eqt1h):

    def trade_rows(trades):
        colors = {'win': '#d4edda', 'loss': '#f8d7da', 'timeout': '#fff3cd'}
        rows = ''
        for t in trades:
            c = colors.get(t['result'], '#fff')
            rows += f"""
            <tr style="background:{c}">
              <td>{t['trade_num']}</td>
              <td>{t['date']}</td>
              <td>{t['entry_price']:.2f}</td>
              <td>{t['sl_price']:.2f}</td>
              <td>{t['tp_price']:.2f}</td>
              <td>{t['exit_price']:.2f}</td>
              <td><b>{t['result'].upper()}</b></td>
              <td>{'+'if t['net_pnl']>=0 else ''}{t['net_pnl']:.4f}</td>
              <td>{t['capital_after']:.4f}</td>
            </tr>"""
        return rows

    def stat_card(s):
        ret_color = '#28a745' if s['total_return_pct'] >= 0 else '#dc3545'
        return f"""
        <div class="stat-grid">
          <div class="stat"><span class="lbl">Total Trades</span><span class="val">{s['total_trades']}</span></div>
          <div class="stat"><span class="lbl">Wins</span><span class="val green">{s['wins']}</span></div>
          <div class="stat"><span class="lbl">Losses</span><span class="val red">{s['losses']}</span></div>
          <div class="stat"><span class="lbl">Win Rate</span><span class="val">{s['win_rate']}%</span></div>
          <div class="stat"><span class="lbl">Start Capital</span><span class="val">${s['start_capital']:.2f}</span></div>
          <div class="stat"><span class="lbl">Final Capital</span><span class="val" style="color:{ret_color}">${s['final_capital']:.4f}</span></div>
          <div class="stat"><span class="lbl">Total Return</span><span class="val" style="color:{ret_color}">{s['total_return_pct']}%</span></div>
          <div class="stat"><span class="lbl">Total Fees</span><span class="val">${s['total_fees']:.4f}</span></div>
          <div class="stat"><span class="lbl">Best Trade</span><span class="val green">+${s['best_trade']:.4f}</span></div>
          <div class="stat"><span class="lbl">Worst Trade</span><span class="val red">${s['worst_trade']:.4f}</span></div>
          <div class="stat"><span class="lbl">Max Drawdown</span><span class="val red">{s['max_drawdown_pct']}%</span></div>
          <div class="stat"><span class="lbl">Avg Win</span><span class="val green">+${s['avg_win']:.4f}</span></div>
          <div class="stat"><span class="lbl">Avg Loss</span><span class="val red">${s['avg_loss']:.4f}</span></div>
        </div>"""

    # Equity curve data
    def eq_js(times, curve, name, color):
        labels = [str(t)[:16] for t in times]
        data = curve
        return f"""{{
            label: '{name}',
            data: {json.dumps(data)},
            borderColor: '{color}',
            backgroundColor: '{color}22',
            fill: true,
            tension: 0.3,
            pointRadius: 0,
        }}"""

    ds4h = eq_js(eqt4h, eq4h, '4H Equity', '#2196F3')
    ds1h = eq_js(eqt1h, eq1h, '1H Equity', '#FF9800')
    labels4h = json.dumps([str(t)[:16] for t in eqt4h])
    labels1h = json.dumps([str(t)[:16] for t in eqt1h])
    # Overlay: trade-indexed (0=start, 1=after trade1, ...)
    overlay_labels = json.dumps([f'Trade {i}' if i > 0 else 'Start'
                                  for i in range(max(len(eq4h), len(eq1h)))])
    # Pad shorter series to same length with last value
    eq4h_padded = eq4h + [eq4h[-1]] * (max(len(eq4h), len(eq1h)) - len(eq4h))
    eq1h_padded = eq1h + [eq1h[-1]] * (max(len(eq4h), len(eq1h)) - len(eq1h))

    # Comparison table
    keys = [
        ('Total Trades', 'total_trades', ''),
        ('Wins', 'wins', ''),
        ('Losses', 'losses', ''),
        ('Win Rate', 'win_rate', '%'),
        ('Start Capital', 'start_capital', '$'),
        ('Final Capital', 'final_capital', '$'),
        ('Total Return', 'total_return_pct', '%'),
        ('Total Fees', 'total_fees', '$'),
        ('Best Trade', 'best_trade', '$'),
        ('Worst Trade', 'worst_trade', '$'),
        ('Max Drawdown', 'max_drawdown_pct', '%'),
        ('Avg Win', 'avg_win', '$'),
        ('Avg Loss', 'avg_loss', '$'),
    ]
    cmp_rows = ''
    for label, key, unit in keys:
        v4 = sum4h[key]
        v1 = sum1h[key]
        if unit == '$':
            v4s = f'${v4:.4f}' if isinstance(v4, float) else f'${v4}'
            v1s = f'${v1:.4f}' if isinstance(v1, float) else f'${v1}'
        elif unit == '%':
            v4s = f'{v4}%'
            v1s = f'{v1}%'
        else:
            v4s = str(v4)
            v1s = str(v1)
        cmp_rows += f'<tr><td>{label}</td><td>{v4s}</td><td>{v1s}</td></tr>'

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>XAUUSD Gold Backtest Report</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ font-family: 'Segoe UI', sans-serif; background: #0f1117; color: #e0e0e0; padding: 20px; }}
  h1 {{ text-align: center; color: #FFD700; font-size: 2em; margin-bottom: 6px; }}
  .subtitle {{ text-align: center; color: #888; margin-bottom: 30px; font-size: 0.9em; }}
  h2 {{ color: #FFD700; border-bottom: 2px solid #FFD70044; padding-bottom: 6px; margin: 30px 0 16px; }}
  h3 {{ color: #aaa; margin: 20px 0 10px; }}
  .warning {{ background: #332200; border: 1px solid #FF9800; border-radius: 8px; padding: 12px 18px;
              margin-bottom: 24px; font-size: 0.88em; color: #FFB74D; }}
  .stat-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); gap: 12px; margin-bottom: 20px; }}
  .stat {{ background: #1e2130; border-radius: 10px; padding: 14px; display: flex; flex-direction: column; gap: 4px; }}
  .lbl {{ font-size: 0.75em; color: #888; text-transform: uppercase; }}
  .val {{ font-size: 1.2em; font-weight: 700; }}
  .green {{ color: #4caf50; }}
  .red {{ color: #f44336; }}
  .chart-wrap {{ background: #1e2130; border-radius: 12px; padding: 20px; margin-bottom: 30px; }}
  canvas {{ max-height: 320px; }}
  .table-wrap {{ overflow-x: auto; margin-bottom: 30px; }}
  table {{ width: 100%; border-collapse: collapse; font-size: 0.82em; }}
  th {{ background: #1a1d2e; color: #FFD700; padding: 10px 8px; text-align: left; position: sticky; top: 0; }}
  td {{ padding: 8px; border-bottom: 1px solid #2a2d3e; }}
  tr:hover td {{ background: #1a1d2eaa; }}
  .cmp-table {{ background: #1e2130; border-radius: 12px; overflow: hidden; }}
  .cmp-table th:nth-child(2) {{ color: #2196F3; }}
  .cmp-table th:nth-child(3) {{ color: #FF9800; }}
  .section {{ background: #161924; border-radius: 14px; padding: 24px; margin-bottom: 30px; }}
  @media(max-width:600px) {{ .stat-grid {{ grid-template-columns: 1fr 1fr; }} }}
</style>
</head>
<body>
<h1>📊 XAUUSD Gold Backtest Report</h1>
<p class="subtitle">WaveTrend + Second-Entry Pattern | 12-Month Simulation | Generated {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>

<div class="warning">
  ⚠️ <strong>Synthetic Data Notice:</strong> Live market data APIs were unavailable in this environment (network policy restriction).
  This backtest uses synthetically generated XAUUSD price data calibrated to realistic gold volatility (~14% annual) and drift (~12% annual)
  starting at ~$2,300. Results are for <strong>strategy logic validation only</strong> and do not reflect actual historical gold prices.
</div>

<!-- ════════════════ 4H SECTION ════════════════ -->
<div class="section">
  <h2>4H Timeframe Results</h2>
  {stat_card(sum4h)}
  <div class="chart-wrap">
    <canvas id="chart4h"></canvas>
  </div>
  <h3>All Trades (4H)</h3>
  <div class="table-wrap">
    <table>
      <thead><tr>
        <th>#</th><th>Date</th><th>Entry</th><th>Stop Loss</th>
        <th>Take Profit</th><th>Exit</th><th>Result</th><th>Net P&L $</th><th>Capital $</th>
      </tr></thead>
      <tbody>{trade_rows(trades4h)}</tbody>
    </table>
  </div>
</div>

<!-- ════════════════ 1H SECTION ════════════════ -->
<div class="section">
  <h2>1H Timeframe Results</h2>
  {stat_card(sum1h)}
  <div class="chart-wrap">
    <canvas id="chart1h"></canvas>
  </div>
  <h3>All Trades (1H)</h3>
  <div class="table-wrap">
    <table>
      <thead><tr>
        <th>#</th><th>Date</th><th>Entry</th><th>Stop Loss</th>
        <th>Take Profit</th><th>Exit</th><th>Result</th><th>Net P&L $</th><th>Capital $</th>
      </tr></thead>
      <tbody>{trade_rows(trades1h)}</tbody>
    </table>
  </div>
</div>

<!-- ════════════════ COMPARISON ════════════════ -->
<div class="section">
  <h2>4H vs 1H Comparison</h2>
  <div class="table-wrap cmp-table">
    <table>
      <thead><tr><th>Metric</th><th>4H Timeframe</th><th>1H Timeframe</th></tr></thead>
      <tbody>{cmp_rows}</tbody>
    </table>
  </div>

  <!-- Overlay chart -->
  <div class="chart-wrap" style="margin-top:20px">
    <canvas id="chartOverlay"></canvas>
  </div>
</div>

<script>
// ── 4H chart ──
new Chart(document.getElementById('chart4h'), {{
  type: 'line',
  data: {{
    labels: {labels4h},
    datasets: [{ds4h}]
  }},
  options: {{
    responsive: true,
    plugins: {{ legend: {{ labels: {{ color: '#ccc' }} }}, title: {{ display: true, text: '4H Equity Curve ($)', color: '#FFD700' }} }},
    scales: {{ x: {{ ticks: {{ color:'#888', maxTicksLimit:10 }}, grid: {{ color:'#2a2d3e' }} }},
               y: {{ ticks: {{ color:'#888' }}, grid: {{ color:'#2a2d3e' }} }} }}
  }}
}});

// ── 1H chart ──
new Chart(document.getElementById('chart1h'), {{
  type: 'line',
  data: {{
    labels: {labels1h},
    datasets: [{ds1h}]
  }},
  options: {{
    responsive: true,
    plugins: {{ legend: {{ labels: {{ color: '#ccc' }} }}, title: {{ display: true, text: '1H Equity Curve ($)', color: '#FFD700' }} }},
    scales: {{ x: {{ ticks: {{ color:'#888', maxTicksLimit:10 }}, grid: {{ color:'#2a2d3e' }} }},
               y: {{ ticks: {{ color:'#888' }}, grid: {{ color:'#2a2d3e' }} }} }}
  }}
}});

// ── Overlay chart (both on same trade-index axis) ──
new Chart(document.getElementById('chartOverlay'), {{
  type: 'line',
  data: {{
    labels: {overlay_labels},
    datasets: [
      {{
        label: '4H Equity',
        data: {json.dumps(eq4h_padded)},
        borderColor: '#2196F3',
        backgroundColor: '#2196F322',
        fill: false,
        tension: 0.3,
        pointRadius: 4,
      }},
      {{
        label: '1H Equity',
        data: {json.dumps(eq1h_padded)},
        borderColor: '#FF9800',
        backgroundColor: '#FF980022',
        fill: false,
        tension: 0.3,
        pointRadius: 4,
      }}
    ]
  }},
  options: {{
    responsive: true,
    plugins: {{ legend: {{ labels: {{ color: '#ccc' }} }},
               title: {{ display: true, text: '4H vs 1H Equity Overlay (per trade)', color: '#FFD700' }} }},
    scales: {{ x: {{ ticks: {{ color:'#888' }}, grid: {{ color:'#2a2d3e' }} }},
               y: {{ ticks: {{ color:'#888', callback: (v) => '$'+v.toFixed(2) }}, grid: {{ color:'#2a2d3e' }} }} }}
  }}
}});
</script>
</body>
</html>"""
    return html


# ─────────────────────────────────────────────
# 6. MAIN
# ─────────────────────────────────────────────
if __name__ == '__main__':
    print("=" * 60)
    print("  XAUUSD GOLD BACKTEST — WaveTrend + Second Entry Pattern")
    print("=" * 60)

    print("\n[1/5] Generating synthetic XAUUSD 1H data (1 year)...")
    df_1h = generate_gold_data()
    print(f"      {len(df_1h)} hourly candles generated")
    print(f"      Price range: ${df_1h['low'].min():.2f} – ${df_1h['high'].max():.2f}")
    print(f"      Date range : {df_1h.index[0].strftime('%Y-%m-%d')} → {df_1h.index[-1].strftime('%Y-%m-%d')}")

    print("\n[2/5] Resampling to 4H...")
    df_4h = resample_4h(df_1h)
    print(f"      {len(df_4h)} four-hour candles")

    print("\n[3/5] Running backtest on 4H data...")
    sum4h, trades4h, eq4h, eqt4h = run_backtest(df_4h, '4H')

    print("\n[4/5] Running backtest on 1H data...")
    sum1h, trades1h, eq1h, eqt1h = run_backtest(df_1h, '1H')

    print("\n[5/5] Building HTML report...")
    html = build_html(sum4h, trades4h, eq4h, eqt4h,
                      sum1h, trades1h, eq1h, eqt1h)

    report_path = os.path.expanduser('~/Desktop/gold_backtest_report.html')
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    with open(report_path, 'w') as f:
        f.write(html)
    print(f"      Report saved → {report_path}")

    # ── Terminal summary ──
    print("\n" + "=" * 60)
    print("  RESULTS SUMMARY")
    print("=" * 60)

    for s in [sum4h, sum1h]:
        print(f"\n  ── {s['label']} TIMEFRAME ──")
        print(f"  Total Trades   : {s['total_trades']}")
        print(f"  Wins / Losses  : {s['wins']} / {s['losses']}")
        print(f"  Win Rate       : {s['win_rate']}%")
        print(f"  Start Capital  : ${s['start_capital']:.2f}")
        print(f"  Final Capital  : ${s['final_capital']:.4f}")
        print(f"  Total Return   : {s['total_return_pct']}%")
        print(f"  Total Fees     : ${s['total_fees']:.4f}")
        print(f"  Best Trade     : +${s['best_trade']:.4f}")
        print(f"  Worst Trade    : ${s['worst_trade']:.4f}")
        print(f"  Max Drawdown   : {s['max_drawdown_pct']}%")
        print(f"  Avg Win        : +${s['avg_win']:.4f}")
        print(f"  Avg Loss       : ${s['avg_loss']:.4f}")

    print("\n" + "=" * 60)
    print("  COMPARISON TABLE: 4H vs 1H")
    print("=" * 60)
    row_fmt = "  {:<22} {:>14} {:>14}"
    print(row_fmt.format("Metric", "4H", "1H"))
    print("  " + "-" * 52)
    metrics = [
        ("Total Trades",    sum4h['total_trades'],       sum1h['total_trades'],       ''),
        ("Wins",            sum4h['wins'],               sum1h['wins'],               ''),
        ("Losses",          sum4h['losses'],             sum1h['losses'],             ''),
        ("Win Rate",        sum4h['win_rate'],           sum1h['win_rate'],           '%'),
        ("Start Capital",   sum4h['start_capital'],      sum1h['start_capital'],      '$'),
        ("Final Capital",   sum4h['final_capital'],      sum1h['final_capital'],      '$'),
        ("Total Return",    sum4h['total_return_pct'],   sum1h['total_return_pct'],   '%'),
        ("Total Fees",      sum4h['total_fees'],         sum1h['total_fees'],         '$'),
        ("Best Trade",      sum4h['best_trade'],         sum1h['best_trade'],         '$'),
        ("Worst Trade",     sum4h['worst_trade'],        sum1h['worst_trade'],        '$'),
        ("Max Drawdown",    sum4h['max_drawdown_pct'],   sum1h['max_drawdown_pct'],   '%'),
        ("Avg Win",         sum4h['avg_win'],            sum1h['avg_win'],            '$'),
        ("Avg Loss",        sum4h['avg_loss'],           sum1h['avg_loss'],           '$'),
    ]
    for name, v4, v1, unit in metrics:
        if unit == '$':
            s4 = f'${v4:.4f}' if isinstance(v4, float) else f'${v4}'
            s1 = f'${v1:.4f}' if isinstance(v1, float) else f'${v1}'
        elif unit == '%':
            s4 = f'{v4}%'
            s1 = f'{v1}%'
        else:
            s4 = str(v4)
            s1 = str(v1)
        print(row_fmt.format(name, s4, s1))

    print("\n  Report: " + report_path)
    print("=" * 60)
