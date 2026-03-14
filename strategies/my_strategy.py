import pandas as pd

LOOKBACK = 12
COOLDOWN = 4


def strategy(df):

    df["signal"] = 0

    df["ema50"] = df["Close"].ewm(span=50).mean()

    df["atr"] = (
        (df["High"] - df["Low"])
        .rolling(14)
        .mean()
    )

    cooldown = 0

    for i in range(60, len(df) - 1):

        if cooldown > 0:
            cooldown -= 1
            continue

        time = df.index[i].time()

        # session filter
        if not (
            time >= pd.to_datetime("09:20").time()
            and time <= pd.to_datetime("14:30").time()
        ):
            continue

        atr = df["atr"].iloc[i]

        if pd.isna(atr):
            continue

        entry = df["Close"].iloc[i]

        stop_distance = entry * 0.002

        # light volatility filter
        if atr < stop_distance * 0.4:
            continue

        body = abs(
            df["Close"].iloc[i]
            - df["Open"].iloc[i]
        )

        if body < atr * 0.15:
            continue

        # trend filter
        uptrend = entry > df["ema50"].iloc[i]
        downtrend = entry < df["ema50"].iloc[i]

        # ===== BUY =====

        last_low = df["Low"].iloc[i-LOOKBACK:i].min()

        if (
            uptrend
            and df["Low"].iloc[i] < last_low
        ):

            df.loc[df.index[i], "signal"] = 1
            cooldown = COOLDOWN
            continue

        # ===== SELL =====

        last_high = df["High"].iloc[i-LOOKBACK:i].max()

        if (
            downtrend
            and df["High"].iloc[i] > last_high
        ):

            df.loc[df.index[i], "signal"] = -1
            cooldown = COOLDOWN
            continue

    return df