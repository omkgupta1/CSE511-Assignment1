# Experiment 3 - ROI Statistics

## ROI

The ROI is the `qsort()` call only:

m5_dump_reset_stats(0, 0);
qsort(array,count,sizeof(struct my3DVertexStruct),compare);
m5_dump_reset_stats(0, 0);

The markers are outside the qsort call and are not placed inside `compare()`.

## Build m5ops

riscv64-unknown-elf-gcc \
    -march=rv64gc \
    -mabi=lp64d \
    -I/workspace/gem5/include \
    -c /workspace/gem5/util/m5/src/abi/riscv/m5op.S \
    -o m5op_riscv.o

## Build ROI benchmark

riscv64-unknown-elf-gcc \
    -march=rv64gc \
    -mabi=lp64d \
    -I/workspace/gem5/include \
    -o qsort_large_roi.elf \
    qsort_large_roi.c \
    m5op_riscv.o \
    -lm

## gem5 configuration

CPU models:
- RiscvTimingSimpleCPU
- RiscvO3CPU

Cache configuration:
- L1 I-cache: 16 KiB, 2-way, 2-cycle latency
- L1 D-cache: 16 KiB, 2-way, 2-cycle latency
- L2: 512 KiB, 4-way, 10-cycle latency
- L3: 1 MiB, 8-way, 20-cycle latency

## Results

Timing:
- ROI instructions: 35,215,518
- ROI ticks: 117,233,377,000
- L2 miss rate: 33.0999%
- L3 miss rate: 37.0705%

O3:
- ROI instructions: 35,215,518
- ROI ticks: 26,660,876,000
- L2 miss rate: 33.0883%
- L3 miss rate: 37.1461%
