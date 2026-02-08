import csv
import pandas as pd
import matplotlib.pyplot as plt

# ---- 1) Parse your "log-style CSV" into tidy rows: time | agent | opinion | input | attention ----
path = "bse_MI_min150_i05_0001_opinion.csv"

import csv
from collections import defaultdict

records_by_time = defaultdict(list)

with open(path, "r", encoding="utf-8", errors="replace", newline="") as f:
    reader = csv.reader(f)
    for row in reader:
        # Strip and clean tokens
        tok = [x.strip() for x in row if x and x.strip()]

        if len(tok) < 2 or tok[0] != "t=":
            continue

        try:
            t = int(float(tok[1]))
        except ValueError:
            continue

        i = 2
        while i + 9 <= len(tok):
            if tok[i] != "id=":
                i += 1
                continue

            if tok[i + 2] != "opinion=" or tok[i + 4] != "input=" or tok[i + 6] != "attention=":
                i += 1
                continue

            agent = tok[i + 1]

            def to_float(x):
                try:
                    return float(x)
                except ValueError:
                    return float("nan")

            opinion = to_float(tok[i + 3])
            inp = to_float(tok[i + 5])
            attention = to_float(tok[i + 7])

            agent_record = {
                "agent": agent,
                "opinion": opinion,
                "input": inp,
                "attention": attention
            }

            records_by_time[t].append(agent_record)
            i += 8



records = []
for t, agents in records_by_time.items():
    for agent_record in agents:
        records.append({
            "time": t,
            **agent_record
        })



df = pd.DataFrame(records).sort_values(["time", "agent"]).reset_index(drop=True)
print(df)
import matplotlib.pyplot as plt

# Plot opinion over time
for agent, group in df.groupby("agent"):
    plt.plot(group["time"], group["opinion"], label=agent)

plt.xlabel("Time")
plt.ylabel("Opinion")
plt.title("Agent Opinions Over Time")
plt.legend(title="Agent")
plt.grid(True)
plt.show()


# Plot input over time
for agent, group in df.groupby("agent"):
    plt.plot(group["time"], group["input"], label=agent)

plt.xlabel("Time")
plt.ylabel("Input")
plt.title("Agent Inputs Over Time")
plt.legend(title="Agent")
plt.grid(True)
plt.show()


# Plot attention over time
for agent, group in df.groupby("agent"):
    plt.plot(group["time"], group["attention"], label=agent)

plt.xlabel("Time")
plt.ylabel("Attention")
plt.title("Agent Attention Over Time")
plt.legend(title="Agent")
plt.grid(True)
plt.show()
