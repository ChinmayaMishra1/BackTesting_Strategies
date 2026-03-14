import pandas as pd


def strategy(df):

    df["ma20"] = df["Close"].rolling(20).mean()
    df["ma50"] = df["Close"].rolling(50).mean()

    df["signal"] = 0

    df.loc[df["ma20"] > df["ma50"], "signal"] = 1
    df.loc[df["ma20"] < df["ma50"], "signal"] = -1

    return df