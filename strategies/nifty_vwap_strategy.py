# import pandas as pd


# def ema(series, length):
#     return series.ewm(span=length, adjust=False).mean()


# def strategy(df):

#     # ===== EMA =====

#     df["ema20"] = ema(df["Close"], 20)
#     df["ema50"] = ema(df["Close"], 50)

#     # ===== VWAP =====

#     df["date_only"] = df.index.date

#     # df["vwap"] = (
#     #     df.groupby("date_only")
#     #     .apply(lambda x: (x["Close"] * x["Volume"]).cumsum()
#     #            / x["Volume"].cumsum())
#     #     .reset_index(level=0, drop=True)
#     # )

#     df["vwap"] = df["Close"].rolling(20).mean()

#     # ===== DEBUG → remove filters =====

#     df["signal"] = 0

#     buy = (
#         (df["ema20"] > df["ema50"])
#         & (df["Close"] > df["vwap"])
#     )

#     sell = (
#         (df["ema20"] < df["ema50"])
#         & (df["Close"] < df["vwap"])
#     )

#     df.loc[buy, "signal"] = 1
#     df.loc[sell, "signal"] = -1

#     print("Total signals:", (df["signal"] != 0).sum())

#     return df




# some other strategy import pandas as pd


import pandas as pd


def ema(series, n):
    return series.ewm(span=n, adjust=False).mean()


def strategy(df):

    # ===== EMAs =====

    df["ema9"] = ema(df["Close"], 9)
    df["ema21"] = ema(df["Close"], 21)

    # ===== Trend =====

    df["trend_up"] = df["ema9"] > df["ema21"]
    df["trend_down"] = df["ema9"] < df["ema21"]

    # ===== Candle direction =====

    df["bull"] = df["Close"] > df["Open"]
    df["bear"] = df["Close"] < df["Open"]

    # ===== Range filter =====

    df["range"] = df["High"] - df["Low"]
    df["small"] = df["range"] < 80   # adjust if needed

    # ===== Signals =====

    df["signal"] = 0

    buy = (
        df["trend_up"]
        & df["bull"]
        & df["small"]
    )

    sell = (
        df["trend_down"]
        & df["bear"]
        & df["small"]
    )

    df.loc[buy, "signal"] = 1
    df.loc[sell, "signal"] = -1

    print("Signals:", (df["signal"] != 0).sum())

    return df