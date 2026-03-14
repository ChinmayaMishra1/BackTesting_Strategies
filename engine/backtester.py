stop_pct = 0.002
rrr = 5


def backtest(df):

    capital = 100000
    risk_percent = 0.0025

    brokerage_per_side = 20
    brokerage = brokerage_per_side * 2

    # NIFTY LIMITS 2026
    lot_size = 65
    max_lots = 27
    max_qty = 1800

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

        # =====================
        # ENTRY
        # =====================

        if position == 0 and signal != 0:

            risk_amount = capital * risk_percent

            entry = price
            direction = signal

            stop_distance = entry * stop_pct

            if stop_distance <= 0:
                continue

            raw_qty = risk_amount / stop_distance

            # convert to lots
            lots = int(raw_qty / lot_size)

            if lots < 1:
                lots = 1

            # limit lots per order
            lots = min(lots, max_lots)

            qty = lots * lot_size

            # limit max quantity per order
            if qty > max_qty:
                qty = max_qty

            if direction == 1:
                stop = entry - stop_distance
                target = entry + stop_distance * rrr

            elif direction == -1:
                stop = entry + stop_distance
                target = entry - stop_distance * rrr

            position = 1

        # =====================
        # EXIT
        # =====================

        if position == 1:

            exit_trade = False

            if direction == 1:
                if price <= stop or price >= target:
                    exit_trade = True

            elif direction == -1:
                if price >= stop or price <= target:
                    exit_trade = True

            if exit_trade:

                if direction == 1:
                    exit_price = stop if price <= stop else target
                else:
                    exit_price = stop if price >= stop else target

                pnl = (exit_price - entry) * qty * direction
                pnl -= brokerage

                capital += pnl

                trades.append({
                    "date": df.index[i],
                    "entry": entry,
                    "exit": exit_price,
                    "qty": qty,
                    "direction": direction,
                    "pnl": pnl,
                    "capital": capital
                })

                position = 0

                if capital <= 0:
                    break

        equity.append({
            "date": df.index[i],
            "capital": capital
        })

    return capital, trades, equity