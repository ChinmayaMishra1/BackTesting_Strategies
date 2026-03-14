import pandas as pd
import plotly.graph_objects as go


equity = pd.read_csv("equity.csv")
trades = pd.read_csv("trades.csv")

equity["date"] = pd.to_datetime(equity["date"])
trades["date"] = pd.to_datetime(trades["date"])


fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=equity["date"],
        y=equity["capital"],
        mode="lines",
        name="Capital"
    )
)

fig.add_trace(
    go.Scatter(
        x=trades["date"],
        y=trades["capital"],
        mode="markers",
        name="Trades",
        text=trades[["pnl", "qty", "rrr", "stop_pct"]],
    )
)

fig.show()