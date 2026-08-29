import csv
from pathlib import Path

import matplotlib.pyplot as plt


BASE_DIR = Path("/workspace/assignment1")
CSV_FILE = BASE_DIR / "results/q2/q2_results.csv"
PLOT_DIR = BASE_DIR / "results/q2/plots"

PLOT_DIR.mkdir(parents=True, exist_ok=True)


# --------------------------------------------------
# Read results
# --------------------------------------------------

with open(CSV_FILE, newline="") as f:
    rows = list(csv.DictReader(f))


# --------------------------------------------------
# L2 miss-rate plot
# --------------------------------------------------

l2_rows = [r for r in rows if r["sweep"] == "l2"]

configs = []
timing = []
o3 = []

for r in l2_rows:
    if r["cpu"] == "timing":
        configs.append(r["configuration"])
        timing.append(float(r["l2_miss_rate"]) * 100)
    else:
        o3.append(float(r["l2_miss_rate"]) * 100)


plt.figure(figsize=(9, 6))

plt.plot(
    configs,
    timing,
    marker="o",
    label="RiscvTimingSimpleCPU",
)

plt.plot(
    configs,
    o3,
    marker="s",
    label="RiscvO3CPU",
)

plt.xlabel("L2 Cache Configuration")
plt.ylabel("L2 Demand Miss Rate (%)")
plt.title("L2 Cache Miss Rate vs Cache Configuration")
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()

plt.savefig(
    PLOT_DIR / "l2_miss_rate.png",
    dpi=300,
)

plt.close()


# --------------------------------------------------
# L3 miss-rate plot
# --------------------------------------------------

l3_rows = [r for r in rows if r["sweep"] == "l3"]

configs = []
timing = []
o3 = []

for r in l3_rows:
    if r["cpu"] == "timing":
        configs.append(r["configuration"])
        timing.append(float(r["l3_miss_rate"]) * 100)
    else:
        o3.append(float(r["l3_miss_rate"]) * 100)


plt.figure(figsize=(9, 6))

plt.plot(
    configs,
    timing,
    marker="o",
    label="RiscvTimingSimpleCPU",
)

plt.plot(
    configs,
    o3,
    marker="s",
    label="RiscvO3CPU",
)

plt.xlabel("L3 Cache Configuration")
plt.ylabel("L3 Demand Miss Rate (%)")
plt.title("L3 Cache Miss Rate vs Cache Configuration")
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()

plt.savefig(
    PLOT_DIR / "l3_miss_rate.png",
    dpi=300,
)

plt.close()


print("Plots generated successfully.")
print(PLOT_DIR / "l2_miss_rate.png")
print(PLOT_DIR / "l3_miss_rate.png")