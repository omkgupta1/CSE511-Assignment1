import subprocess
from pathlib import Path


# --------------------------------------------------
# Paths
# --------------------------------------------------

ASSIGNMENT_DIR = Path("/workspace/assignment1")

GEM5 = "/workspace/gem5/build/RISCV/gem5.opt"

CONFIG = ASSIGNMENT_DIR / "scripts/q1_config.py"

ROI_BINARY = (
    "/workspace/mibench/automotive/qsort/"
    "qsort_large_roi.elf"
)

RESULTS_DIR = ASSIGNMENT_DIR / "results/q3/roi"


# --------------------------------------------------
# Q1 cache configuration used for Experiment 3
# --------------------------------------------------

L2_SIZE = "512KiB"
L2_ASSOC = 4

L3_SIZE = "1MiB"
L3_ASSOC = 8


# --------------------------------------------------
# CPU models
# --------------------------------------------------

CPU_MODELS = [
    "timing",
    "o3",
]


# --------------------------------------------------
# Run one ROI simulation
# --------------------------------------------------

def run_simulation(cpu):
    output_dir = RESULTS_DIR / cpu

    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    print("\n" + "=" * 70)
    print("Experiment 3 - ROI")
    print("=" * 70)
    print(f"CPU          : {cpu}")
    print(f"Binary       : {ROI_BINARY}")
    print(f"L2           : {L2_SIZE}, {L2_ASSOC}-way")
    print(f"L3           : {L3_SIZE}, {L3_ASSOC}-way")
    print(f"Output       : {output_dir}")
    print("=" * 70)

    cmd = [
        GEM5,
        "-d",
        str(output_dir),
        str(CONFIG),

        "--cpu",
        cpu,

        "--binary",
        ROI_BINARY,

        "--l2-size",
        L2_SIZE,

        "--l2-assoc",
        str(L2_ASSOC),

        "--l3-size",
        L3_SIZE,

        "--l3-assoc",
        str(L3_ASSOC),
    ]

    result = subprocess.run(cmd)

    if result.returncode != 0:
        raise RuntimeError(
            f"gem5 failed for CPU model: {cpu}"
        )

    print(
        f"\nCompleted ROI simulation for {cpu}."
    )


# --------------------------------------------------
# Main
# --------------------------------------------------

def main():

    RESULTS_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    for cpu in CPU_MODELS:
        run_simulation(cpu)

    print("\n" + "=" * 70)
    print("Experiment 3 completed.")
    print(f"Results saved to: {RESULTS_DIR}")
    print("=" * 70)


if __name__ == "__main__":
    main()
