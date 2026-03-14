import pandas as pd

FILE = "equity.csv"
OUTPUT = "dd_30.csv"

DD_LIMIT = 0.30


df = pd.read_csv(FILE)

df["date"] = pd.to_datetime(df["date"])

capital = df["capital"].values
dates = df["date"].values

peak = capital[0]

in_dd = False

dd_list = []

start_date = None
peak_value = None
bottom_value = None


for i in range(len(capital)):

    if capital[i] > peak:
        peak = capital[i]

    dd = (peak - capital[i]) / peak

    # start drawdown
    if dd >= DD_LIMIT and not in_dd:

        in_dd = True
        start_date = dates[i]
        peak_value = peak
        bottom_value = capital[i]

    # update bottom
    if in_dd:
        if capital[i] < bottom_value:
            bottom_value = capital[i]

    # end drawdown
    if dd < DD_LIMIT and in_dd:

        end_date = dates[i]

        dd_percent = (peak_value - bottom_value) / peak_value * 100

        dd_list.append({
            "start": start_date,
            "end": end_date,
            "peak": peak_value,
            "bottom": bottom_value,
            "dd_percent": dd_percent
        })

        in_dd = False


# save to csv
out = pd.DataFrame(dd_list)

out.to_csv(OUTPUT, index=False)

print("Saved to", OUTPUT)