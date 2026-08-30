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
# L2 configuration ordering
# --------------------------------------------------

l2_order = [
    "32K_4",
    "64K_2",
    "64K_4",
    "64K_8",
    "256K_2",
    "256K_4",
    "1024K_2",
    "1024K_8",
]

l2_rows = [r for r in rows if r["sweep"] == "l2"]

l2_rows.sort(
    key=lambda r: l2_order.index(r["configuration"])
)


# --------------------------------------------------
# L2 miss-rate plot
# --------------------------------------------------

configs = l2_order

timing = {}
o3 = {}

for r in l2_rows:
    config = r["configuration"]

    if r["cpu"] == "timing":
        timing[config] = float(r["l2_miss_rate"]) * 100
    else:
        o3[config] = float(r["l2_miss_rate"]) * 100


timing_values = [timing[c] for c in configs]
o3_values = [o3[c] for c in configs]


plt.figure(figsize=(9, 6))

plt.plot(
    configs,
    timing_values,
    marker="o",
    label="RiscvTimingSimpleCPU",
)

plt.plot(
    configs,
    o3_values,
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
# L3 configuration ordering
# --------------------------------------------------

l3_order = [
    "1M_8",
    "1M_16",
    "2M_8",
    "2M_16",
]

l3_rows = [r for r in rows if r["sweep"] == "l3"]

l3_rows.sort(
    key=lambda r: l3_order.index(r["configuration"])
)


# --------------------------------------------------
# L3 miss-rate plot
# --------------------------------------------------

configs = l3_order

timing = {}
o3 = {}

for r in l3_rows:
    config = r["configuration"]

    if r["cpu"] == "timing":
        timing[config] = float(r["l3_miss_rate"]) * 100
    else:
        o3[config] = float(r["l3_miss_rate"]) * 100


timing_values = [timing[c] for c in configs]
o3_values = [o3[c] for c in configs]


plt.figure(figsize=(9, 6))

plt.plot(
    configs,
    timing_values,
    marker="o",
    label="RiscvTimingSimpleCPU",
)

plt.plot(
    configs,
    o3_values,
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