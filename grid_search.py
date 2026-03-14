import pandas as pd
import numpy as np
import time
from multiprocessing import Pool, cpu_count

from strategies.jlines_sahoo import strategy
from engine.backtester import backtest
from metrics.stats import calculate_stats


# =========================
# LOAD DATA
# =========================

data = pd.read_csv("data/NIFTY 50_5minute.csv")

data.columns = ["date", "open", "high", "low", "close", "volume"]

data["date"] = pd.to_datetime(data["date"])

data.set_index("date", inplace=True)

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


# use smaller data for speed (optional)
end = data.index.max()
start = end - pd.DateOffset(months=120)

data = data.loc[start:end]


# run strategy once (IMPORTANT SPEEDUP)
base_df = strategy(data)


# =========================
# GRID
# =========================

stop_list = np.round(np.arange(0.001, 0.0051, 0.0005), 6)
rrr_list = np.round(np.arange(1, 6, 0.5), 6)

params = [(s, r) for s in stop_list for r in rrr_list]


# =========================
# WORKER FUNCTION
# =========================

def run_test(param):

    stop, rrr = param

    df = base_df.copy()

    # monkey patch (since backtester uses globals)
    import engine.backtester as bt

    bt.stop_pct = float(stop)
    bt.rrr = float(rrr)

    capital, trades, equity = bt.backtest(df)

    stats = calculate_stats(equity)

    return {
        "stop": stop,
        "rrr": rrr,
        "capital": capital,
        "sharpe": stats["Sharpe"],
        "dd": stats["Max DD"],
        "cagr": stats["CAGR %"],
        "avg_yearly": stats["Avg Yearly %"],
    }


# =========================
# MAIN
# =========================

if __name__ == "__main__":

    start_time = time.time()

    cores = max(1, cpu_count() - 1)

    print("Using cores:", cores)

    with Pool(cores) as p:

        results = p.map(run_test, params)

    res = pd.DataFrame(results)

    res.to_csv("grid_results.csv", index=False)

    print("DONE")


    # # =========================
    # # BEST SHARPE
    # # =========================

    # best_sharpe = res.sort_values("sharpe", ascending=False).iloc[0]

    # print("\n===== BEST SHARPE =====")

    # for k, v in best_sharpe.items():
    #     print(k, ":", v)

    # =========================
    # MAX CAPITAL
    # =========================

    best_capital = res.sort_values("capital", ascending=False).iloc[0]

    print("\n===== MAX FINAL CAPITAL =====")

    for k, v in best_capital.items():
        print(k, ":", v)

    
    # res["score"] = res["sharpe"] / abs(res["dd"])

    # best = res.sort_values("score", ascending=False).iloc[0]

    # print("\n===== BEST SAFE RESULT =====")

    # for k, v in best.items():
    #     print(k, ":", v)


    # =========================
    # RUN BEST PARAM AGAIN
    # =========================

    best_stop = best_capital["stop"]
    best_rrr = best_capital["rrr"]

    import engine.backtester as bt

    bt.stop_pct = float(best_stop)
    bt.rrr = float(best_rrr)

    df = base_df.copy()

    capital, trades, equity = bt.backtest(df)

    import pandas as pd

    pd.DataFrame(trades).to_csv("trades.csv", index=False)
    pd.DataFrame(equity).to_csv("equity.csv", index=False)

    print("Saved trades.csv and equity.csv")

    print("CAGR:", best_capital["cagr"])
    print("Avg yearly:", best_capital["avg_yearly"])


    end_time = time.time()

    total = end_time - start_time

    print("\nTime taken:", total, "seconds")
    print("Time taken:", total / 60, "minutes")

    