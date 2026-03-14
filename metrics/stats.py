import pandas as pd
import numpy as np


def calculate_stats(equity):

    df = pd.DataFrame(equity)

    # ---------- ensure date ----------
    df["date"] = pd.to_datetime(df["date"])

    df = df.sort_values("date")

    df.set_index("date", inplace=True)

    df["returns"] = df["capital"].pct_change()

    # =====================
    # DAILY
    # =====================

    daily = df.resample("1D").last()

    daily["ret"] = daily["capital"].pct_change(fill_method=None)

    winning_days = (daily["ret"] > 0).sum()
    losing_days = (daily["ret"] < 0).sum()

    # =====================
    # MONTHLY
    # =====================

    monthly = daily["capital"].resample("1ME").last().pct_change()

    avg_monthly = monthly.mean()

    # =====================
    # YEARLY
    # =====================

    yearly_cap = daily["capital"].resample("1YE").last()

    yearly_ret = yearly_cap.pct_change()

    avg_yearly = yearly_ret.mean()

    # =====================
    # RUNNING DRAWDOWN %
    # =====================

    df["peak"] = df["capital"].cummax()

    df["dd_pct"] = (df["capital"] - df["peak"]) / df["peak"] * 100

    max_dd = df["dd_pct"].min()

    # =====================
    # SHARPE
    # =====================

    sharpe = (
        df["returns"].mean()
        / df["returns"].std()
        * np.sqrt(252)
        if df["returns"].std() != 0
        else 0
    )

    # =====================
    # CALMAR
    # =====================

    calmar = avg_yearly / abs(max_dd) if max_dd != 0 else 0

    # =====================
    # CAGR
    # =====================

    start_cap = df["capital"].iloc[0]
    end_cap = df["capital"].iloc[-1]

    days = (df.index[-1] - df.index[0]).days

    years = days / 365 if days > 0 else 1

    if years > 0 and end_cap > 0:
        try:
            cagr = (end_cap / start_cap) ** (1 / years) - 1
        except:
            cagr = 0
    else:
        cagr = 0

    cagr_pct = cagr * 100

    # =====================
    # YEARLY AVG %
    # =====================

    avg_yearly_pct = yearly_ret.mean() * 100

    return {
        "Winning days": winning_days,
        "Losing days": losing_days,
        "Avg Monthly": avg_monthly,
        "Avg Yearly": avg_yearly,
        "Max DD": max_dd,
        "Sharpe": sharpe,
        "Calmar": calmar,
        "CAGR %": cagr_pct,
        "Avg Yearly %": avg_yearly_pct,
    }