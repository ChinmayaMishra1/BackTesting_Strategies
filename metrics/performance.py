import numpy as np


def calculate_metrics(trades, equity, initial_capital=100000):

    pnl_list = [t["pnl"] for t in trades]

    total_pnl = sum(pnl_list)

    wins = [p for p in pnl_list if p > 0]
    losses = [p for p in pnl_list if p <= 0]

    win_rate = len(wins) / len(pnl_list) if pnl_list else 0
    loss_rate = len(losses) / len(pnl_list) if pnl_list else 0

    capitals = [e["capital"] for e in equity]

    max_cap = np.maximum.accumulate(capitals)

    drawdown = np.array(capitals) - max_cap

    max_dd = drawdown.min()

    final_capital = capitals[-1]

    return {
        "Final Capital": final_capital,
        "Total PnL": total_pnl,
        "Trades": len(pnl_list),
        "Win rate": win_rate,
        "Loss rate": loss_rate,
        "Max Drawdown": max_dd,
    }