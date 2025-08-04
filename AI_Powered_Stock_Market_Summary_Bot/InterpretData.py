import pandas as pd
import numpy as np
import json

bars_by_symbol = items[0]['json']['bars']
stocks = []

for symbol, bars in bars_by_symbol.items():
    closes = [float(bar['c']) for bar in bars if 'c' in bar]
    if len(closes) < 30:
        continue

    df = pd.DataFrame({'close': closes})

    # RSI(14)
    delta = df['close'].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(14).mean()
    avg_loss = loss.rolling(14).mean()
    rs = avg_gain / avg_loss
    df['rsi'] = 100 - (100 / (1 + rs))

    # MACD (12,26,9)
    ema12 = df['close'].ewm(span=12, adjust=False).mean()
    ema26 = df['close'].ewm(span=26, adjust=False).mean()
    df['macd'] = ema12 - ema26
    df['signal'] = df['macd'].ewm(span=9, adjust=False).mean()

    # 移動平均線（短中長）
    df['ma5'] = df['close'].rolling(5).mean()
    df['ma10'] = df['close'].rolling(10).mean()
    df['ma20'] = df['close'].rolling(20).mean()

    # 跳過還沒收斂的資料
    if df[['rsi', 'macd', 'signal', 'ma5', 'ma10', 'ma20']].isnull().iloc[-1].any():
        continue

    latest = df.iloc[-1]
    rsi = float(latest['rsi'])
    macd = float(latest['macd'])
    signal = float(latest['signal'])
    ma5 = float(latest['ma5'])
    ma10 = float(latest['ma10'])
    ma20 = float(latest['ma20'])
    price = float(latest['close'])

    # 均線糾結判斷（三條均線差距接近）
    ma_list = [ma5, ma10, ma20]
    ma_spread = max(ma_list) - min(ma_list)
    ma_spread_pct = ma_spread / price
    is_entangled = bool(ma_spread_pct < 0.002)  # 差距 < 0.2% 視為糾結

    # RSI 區間說明
    if rsi < 30:
        rsi_zone = "Oversold"
    elif rsi > 70:
        rsi_zone = "Overbought"
    else:
        rsi_zone = "Neutral"

    # 技術分析狀態判斷
    status = "Hold"
    if rsi < 30 and macd > signal:
        status = "Buy"
    elif rsi > 70 and macd < signal:
        status = "Sell"

    stocks.append({
        "ticker": symbol,
        "rsi": round(rsi, 5),
        "rsi_zone": rsi_zone,
        "macd": round(macd, 5),
        "signal": round(signal, 5),
        "ma5": round(ma5, 5),
        "ma10": round(ma10, 5),
        "ma20": round(ma20, 5),
        "ma_spread_pct": round(ma_spread_pct, 5),
        "entangled": is_entangled,
        "status": status
    })

return [{
    "json": {
        "summary": json.dumps({
            "stocks": stocks
        }, separators=(',', ':')),
        "stocks": stocks
    }
}]
