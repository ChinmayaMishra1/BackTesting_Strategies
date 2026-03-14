stop_pct = 0.002
rrr = 5

def backtest(df):

    capital = 100000
    risk_percent = 0.01


    brokerage_per_side = 20
    brokerage = brokerage_per_side * 2   # 40 per trade

    position = 0
    direction = 0

    entry = 0
    stop = 0
    target = 0
    qty = 0

    trades = []
    equity = []

    for i in range(len(df)):

        signal = df["signal"].iloc[i]
        price = float(df["Close"].iloc[i])

        risk_amount = capital * risk_percent

        # ENTRY
        if position == 0 and signal != 0:

            entry = price
            direction = signal

            stop_distance = entry * stop_pct

            if stop_distance == 0:
                continue

            qty = max(1, risk_amount / stop_distance)

            if direction == 1:
                stop = entry - stop_distance
                target = entry + (stop_distance * rrr)

            elif direction == -1:
                stop = entry + stop_distance
                target = entry - (stop_distance * rrr)

            position = 1

        # EXIT
        if position == 1:

            exit_trade = False

            if direction == 1:
                if price <= stop or price >= target:
                    exit_trade = True

            elif direction == -1:
                if price >= stop or price <= target:
                    exit_trade = True

            if exit_trade:

                pnl = (price - entry) * qty * direction

                pnl -= brokerage   # ← 40 rupees

                capital += pnl

                trades.append({
                    "date": df.index[i],
                    "entry": entry,
                    "exit": price,
                    "qty": qty,
                    "direction": direction,
                    "pnl": pnl,
                    "capital": capital,
                    "rrr": rrr,
                    "stop_pct": stop_pct
                })

                position = 0

        equity.append({
            "date": df.index[i],
            "capital": capital
        })

    return capital, trades, equity