import pandas as pd
import matplotlib.pyplot as plt

# from strategies.jlines_sahoo import strategy
# from strategies.ma_crossover import strategy
# from strategies.nifty_vwap_strategy import strategy
# from strategies.strategy1_mean_reversion import strategy
from strategies.my_strategy import strategy
from engine.backtester import backtest
from metrics.performance import calculate_metrics
from metrics.stats import calculate_stats


# =====================
# LOAD CSV
# =====================

data = pd.read_csv("data/NIFTY 50_5minute.csv")

# rename columns
data.columns = ["date", "open", "high", "low", "close", "volume"]

# convert date
data["date"] = pd.to_datetime(data["date"])

# set index
data.set_index("date", inplace=True)

# CAPITALIZE columns (needed for strategy)
data.rename(
    columns={
        "open": "Open",
        "high": "High",
        "low": "Low",
        "close": "Close",
        "volume": "Volume",
    },
    inplace=True,
)

data = data.sort_index()

end_date = data.index.max()

start_date = end_date - pd.DateOffset(years=5)

data = data.loc[start_date:end_date]

print("Data after filter:", data.index.min(), "to", data.index.max())


# =====================
# STRATEGY
# =====================

data = strategy(data)

# print(data[["Close","ema20","ema50","vwap","signal"]].tail(20))
# print(data["Volume"].head())

# print(data[["Close","dailyOpen","ema72","ema89","signal"]].tail(20))

# print(data[["Close","signal"]].tail(20))
print("Total signals:", (data["signal"] != 0).sum())
# print(data.index[1] - data.index[0])


# =====================
# BACKTEST
# =====================

capital, trades, equity = backtest(data)


# =====================
# METRICS
# =====================

result = calculate_metrics(trades, equity, 100000)
stats = calculate_stats(equity)

print("\n===== STATS =====")

for k, v in stats.items():
    print(k, v)

# print(data.head())
# print(data.tail())
# print(data.columns)

print("\n===== RESULT =====\n")

for k, v in result.items():
    print(k, ":", v)


# =====================
# EQUITY CURVE
# =====================

plt.plot([e["capital"] for e in equity])

plt.savefig("reports/equity.png")

# plt.show()

pd.DataFrame(trades).to_csv("trades.csv", index=False)
pd.DataFrame(equity).to_csv("equity.csv", index=False)