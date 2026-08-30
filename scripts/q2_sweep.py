import csv
import re
import subprocess
from pathlib import Path


# --------------------------------------------------
# Paths
# --------------------------------------------------

ASSIGNMENT_DIR = Path("/workspace/assignment1")
GEM5 = "/workspace/gem5/build/RISCV/gem5.opt"
CONFIG = ASSIGNMENT_DIR / "scripts/q1_config.py"
RESULTS_DIR = ASSIGNMENT_DIR / "results/q2"


# --------------------------------------------------
# Cache configurations from the assignment
# --------------------------------------------------

# L2 configurations:
# size_associativity
L2_CONFIGS = [
    ("32K_4", "32KiB", 4),
    ("64K_2", "64KiB", 2),
    ("64K_4", "64KiB", 4),
    ("64K_8", "64KiB", 8),
    ("256K_2", "256KiB", 2),
    ("256K_4", "256KiB", 4),
    ("1024K_2", "1024KiB", 2),
    ("1024K_8", "1024KiB", 8),
]


# L3 configurations:
# size_associativity
L3_CONFIGS = [
    ("1M_8", "1MiB", 8),
    ("1M_16", "1MiB", 16),
    ("2M_8", "2MiB", 8),
    ("2M_16", "2MiB", 16),
]


# --------------------------------------------------
# Statistics extraction
# --------------------------------------------------

def extract_stat(stats_file, stat_name):
    pattern = re.compile(
        rf"^{re.escape(stat_name)}\s+([0-9.eE+-]+)"
    )

    with open(stats_file, "r") as f:
        for line in f:
            match = pattern.match(line.strip())

            if match:
                return float(match.group(1))

    raise RuntimeError(
        f"Could not find {stat_name} in {stats_file}"
    )


def collect_results(output_dir):
    stats_file = output_dir / "stats.txt"

    if not stats_file.exists():
        raise RuntimeError(
            f"Missing stats.txt: {stats_file}"
        )

    l2_miss_rate = extract_stat(
        stats_file,
        "system.l2cache.demandMissRate::total",
    )

    l3_miss_rate = extract_stat(
        stats_file,
        "system.l3cache.demandMissRate::total",
    )

    sim_ticks = extract_stat(
        stats_file,
        "simTicks",
    )

    return (
        l2_miss_rate,
        l3_miss_rate,
        int(sim_ticks),
    )


# --------------------------------------------------
# Run one gem5 simulation
# --------------------------------------------------

def run_simulation(
    sweep,
    config_name,
    cpu,
    l2_size,
    l2_assoc,
    l3_size,
    l3_assoc,
):

    output_dir = (
        RESULTS_DIR
        / sweep
        / config_name
        / cpu
    )

    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    print("\n" + "=" * 70)
    print(f"Sweep        : {sweep}")
    print(f"Configuration: {config_name}")
    print(f"CPU          : {cpu}")
    print(f"L2           : {l2_size}, {l2_assoc}-way")
    print(f"L3           : {l3_size}, {l3_assoc}-way")
    print(f"Output       : {output_dir}")
    print("=" * 70)

    cmd = [
        GEM5,
        "-d",
        str(output_dir),
        str(CONFIG),

        "--cpu",
        cpu,

        "--l2-size",
        l2_size,

        "--l2-assoc",
        str(l2_assoc),

        "--l3-size",
        l3_size,

        "--l3-assoc",
        str(l3_assoc),
    ]

    result = subprocess.run(cmd)

    if result.returncode != 0:
        raise RuntimeError(
            f"gem5 failed for "
            f"{sweep}/{config_name}/{cpu}"
        )

    l2_mr, l3_mr, sim_ticks = collect_results(
        output_dir
    )

    print(f"L2 miss rate : {l2_mr:.6f}")
    print(f"L3 miss rate : {l3_mr:.6f}")
    print(f"Sim ticks    : {sim_ticks}")

    return {
        "sweep": sweep,
        "configuration": config_name,
        "cpu": cpu,
        "l2_size": l2_size,
        "l2_assoc": l2_assoc,
        "l3_size": l3_size,
        "l3_assoc": l3_assoc,
        "l2_miss_rate": l2_mr,
        "l3_miss_rate": l3_mr,
        "sim_ticks": sim_ticks,
    }


# --------------------------------------------------
# Main
# --------------------------------------------------

def main():

    RESULTS_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    results = []

    # --------------------------------------------------
    # L2 sweep
    #
    # L3 fixed at Q1 configuration:
    # 1 MiB, 8-way
    # --------------------------------------------------

    for name, size, assoc in L2_CONFIGS:

        for cpu in ["timing", "o3"]:

            results.append(
                run_simulation(
                    sweep="l2",
                    config_name=name,
                    cpu=cpu,
                    l2_size=size,
                    l2_assoc=assoc,
                    l3_size="1MiB",
                    l3_assoc=8,
                )
            )


    # --------------------------------------------------
    # L3 sweep
    #
    # L2 fixed at Q1 configuration:
    # 512 KiB, 4-way
    # --------------------------------------------------

    for name, size, assoc in L3_CONFIGS:

        for cpu in ["timing", "o3"]:

            results.append(
                run_simulation(
                    sweep="l3",
                    config_name=name,
                    cpu=cpu,
                    l2_size="512KiB",
                    l2_assoc=4,
                    l3_size=size,
                    l3_assoc=assoc,
                )
            )


    # --------------------------------------------------
    # Write CSV
    # --------------------------------------------------

    csv_file = RESULTS_DIR / "q2_results.csv"

    fieldnames = [
        "sweep",
        "configuration",
        "cpu",
        "l2_size",
        "l2_assoc",
        "l3_size",
        "l3_assoc",
        "l2_miss_rate",
        "l3_miss_rate",
        "sim_ticks",
    ]

    with open(
        csv_file,
        "w",
        newline="",
    ) as f:

        writer = csv.DictWriter(
            f,
            fieldnames=fieldnames,
        )

        writer.writeheader()
        writer.writerows(results)


    print("\n" + "=" * 70)
    print(
        f"Completed {len(results)} simulations."
    )
    print(
        f"Results saved to: {csv_file}"
    )
    print("=" * 70)


if __name__ == "__main__":
    main()