
import csv



def parse_snapshot(tokens):
    # clean up tokens
    toks = [t.strip() for t in tokens if t.strip() != ""]
    if not toks:
        return None

    # time
    t = float(toks[0])

    # find where Bid: and Ask: are
    bid_i = toks.index("Bid:")
    ask_i = toks.index("Ask:")

    def read_levels(start_i, end_i):
        # toks[start_i] is "Bid:" or "Ask:"
        n = int(float(toks[start_i + 1]))  # how many (price,qty) pairs
        levels = []
        j = start_i + 2
        for _ in range(n):
            price = float(toks[j])
            qty   = float(toks[j + 1])
            levels.append((price, qty))
            j += 2
        return levels

    bids = read_levels(bid_i, ask_i)
    asks = read_levels(ask_i, len(toks))

    return {"time": t, "bids": bids, "asks": asks}



snapshots = []

file_name = "bse_STAC_sec150_i30_0001_LOB_frames.csv"
with open(file_name, newline="") as f:
    for tokens in csv.reader(f):
        snap = parse_snapshot(tokens)
        if snap is not None:
            snapshots.append(snap)



# snapshots: list of dicts from step 1

end_of_second = {}  # maps: sec -> snapshot (we overwrite, so last one wins)

for snap in snapshots:
    sec = int(snap["time"])          # 30.083 -> 30
    end_of_second[sec] = snap        # overwrite = keep last snapshot seen in that second

# turn into a time-ordered list
snapshots_1s = [end_of_second[sec] for sec in sorted(end_of_second)]
for s in snapshots_1s:
    s["second"] = int(s["time"])


print("original snapshots:", len(snapshots))
print("1-second snapshots:", len(snapshots_1s))

print("first few seconds:", [int(s["time"]) for s in snapshots_1s[:10]])
print("first few times:",   [s["time"] for s in snapshots_1s[:10]])

print(snapshots_1s[1])


import numpy as np
import pandas as pd

k = 30  # 30 buyers + 30 sellers

rows = []
for s in snapshots_1s:
    sec = s["second"]

    bid_prices = sorted([p for p, q in s["bids"]], reverse=True)  # high to low
    ask_prices = sorted([p for p, q in s["asks"]])                # low to high

    row = {"second": sec}

    # pad with NaN if fewer than K levels
    for r in range(1, k+1):
        row[f"bid_{r}"] = bid_prices[r-1] if len(bid_prices) >= r else np.nan
        row[f"ask_{r}"] = ask_prices[r-1] if len(ask_prices) >= r else np.nan

    rows.append(row)

quotes_1s = pd.DataFrame(rows).sort_values("second").reset_index(drop=True)
print(quotes_1s.head())

import matplotlib.pyplot as plt

plt.figure()

# buyer quote lines
for r in range(1, 5):
    plt.plot(quotes_1s["second"], quotes_1s[f"bid_{r}"],
             drawstyle="steps-post", alpha=0.85)

# seller quote lines
for r in range(1, 5):
    plt.plot(quotes_1s["second"], quotes_1s[f"ask_{r}"],
             drawstyle="steps-post", alpha=0.85)

# optional reference line (set to whatever "fundamental" you want)
plt.axhline(60, linestyle="--")

plt.axhline(100, linestyle="--")
plt.axhline(140, linestyle="--")
plt.xticks(np.arange(0, 151, 5))
plt.xlabel("Time (seconds)")
plt.ylabel("Price")
plt.title(f"Quote prices sampled at 1Hz (end-of-second), {k} buyers + {k} sellers")
plt.show()


quotes_60_120 = quotes_1s[
    (quotes_1s["second"] >= 60) &
    (quotes_1s["second"] <= 120)
]

quotes_60_120["second"].min(), quotes_60_120["second"].max()

import matplotlib.pyplot as plt

K = 10
plt.figure()

for r in range(1, 5):
    plt.plot(quotes_60_120["second"], quotes_60_120[f"bid_{r}"],
             drawstyle="steps-post", alpha=0.85)
    plt.plot(quotes_60_120["second"], quotes_60_120[f"ask_{r}"],
             drawstyle="steps-post", alpha=0.85)


plt.axhline(100, linestyle="--")

plt.xlabel("Time (seconds)")
plt.ylabel("Price")
plt.title("Quote prices, time 60–120")
plt.show()


