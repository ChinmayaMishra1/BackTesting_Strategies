import pandas as pd


def ema(series, n):
    return series.ewm(span=n, adjust=False).mean()


def rsi(series, n=14):

    delta = series.diff()

    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(n).mean()
    avg_loss = loss.rolling(n).mean()

    rs = avg_gain / avg_loss

    return 100 - (100 / (1 + rs))


def strategy(df):

    df["date_only"] = df.index.date

    # ===== VWAP =====

    df["vwap"] = (
        df.groupby("date_only")
        .apply(lambda x: (x["Close"] * x["Volume"]).cumsum()
               / x["Volume"].cumsum())
        .reset_index(level=0, drop=True)
    )

    # ===== RSI =====

    df["rsi"] = rsi(df["Close"], 14)

    # ===== EMA trend =====

    df["ema50"] = ema(df["Close"], 50)

    df["trend_up"] = df["Close"] > df["ema50"]
    df["trend_down"] = df["Close"] < df["ema50"]

    # ===== candle filter =====

    df["range"] = df["High"] - df["Low"]

    df["small"] = df["range"] < 50

    # ===== session =====

    df["session"] = (
        (df.index.hour >= 9)
        & (df.index.hour <= 14)
    )

    # ===== signals =====

    df["signal"] = 0

    buy = (
        (df["Close"] < df["vwap"])
        & (df["rsi"] < 35)
        & df["small"]
        & df["session"]
        & df["trend_up"]
    )

    sell = (
        (df["Close"] > df["vwap"])
        & (df["rsi"] > 65)
        & df["small"]
        & df["session"]
        & df["trend_down"]
    )

    df.loc[buy, "signal"] = 1
    df.loc[sell, "signal"] = -1

    print("Signals:", (df["signal"] != 0).sum())

    return df