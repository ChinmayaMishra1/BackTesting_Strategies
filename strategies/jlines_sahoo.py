import pandas as pd


def ema(series, length):
    return series.ewm(span=length, adjust=False).mean()


def strategy(df):

    sl = 72
    hl = 89

    max_candle_size = 30

    # =========================
    # EMA (same timeframe)
    # =========================

    df["ema72"] = ema(df["Close"], sl)
    df["ema89"] = ema(df["Close"], hl)

    # =========================
    # Daily Open (higher TF)
    # =========================

    df["date_only"] = df.index.date

    df["dailyOpen"] = (
        df.groupby("date_only")["Open"]
        .transform("first")
    )

    # =========================
    # Candle size filter
    # =========================

    df["candleSize"] = df["High"] - df["Low"]
    df["validCandle"] = df["candleSize"] <= max_candle_size

    # =========================
    # Candle direction
    # =========================

    df["bullish"] = df["Close"] > df["Open"]
    df["bearish"] = df["Close"] < df["Open"]

    # =========================
    # Trend
    # =========================

    df["trendUp"] = df["ema72"] > df["ema89"]
    df["trendDown"] = df["ema72"] < df["ema89"]

    # =========================
    # 5 minute check
    # =========================
    # In pandas we assume data already 5m
    # so always True

    df["isFiveMinute"] = True

    # =========================
    # SIGNALS
    # =========================

    df["signal"] = 0

    buy_cond = (
        df["isFiveMinute"]
        & df["validCandle"]
        & (df["Close"] > df["dailyOpen"])
        & df["bullish"]
        & df["trendUp"]
    )

    sell_cond = (
        df["isFiveMinute"]
        & df["validCandle"]
        & (df["Close"] < df["dailyOpen"])
        & df["bearish"]
        & df["trendDown"]
    )

    df.loc[buy_cond, "signal"] = 1
    df.loc[sell_cond, "signal"] = -1

    return df