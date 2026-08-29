import m5
from m5.objects import *
import argparse

# -----------------------------
# Command-line arguments
# -----------------------------
parser = argparse.ArgumentParser()

parser.add_argument(
    "--cpu",
    choices=["timing", "o3"],
    default="timing",
    help="CPU model: timing or o3",
)

parser.add_argument(
    "--binary",
    default="/workspace/mibench/automotive/qsort/qsort_large.elf",
    help="Path to RISC-V benchmark",
)

args = parser.parse_args()


# -----------------------------
# Create the system
# -----------------------------
system = System()

# System clock
system.clk_domain = SrcClockDomain()
system.clk_domain.clock = "1GHz"
system.clk_domain.voltage_domain = VoltageDomain()

# Timing memory mode
system.mem_mode = "timing"

# 512 MiB main memory
system.mem_ranges = [AddrRange("512MiB")]


# -----------------------------
# Create CPU
# -----------------------------
if args.cpu == "timing":
    system.cpu = RiscvTimingSimpleCPU()
else:
    system.cpu = RiscvO3CPU()

# -----------------------------
# L1 Instruction Cache
# -----------------------------
system.cpu.icache = Cache()
system.cpu.icache.size = "16KiB"
system.cpu.icache.assoc = 2
system.cpu.icache.tag_latency = 2
system.cpu.icache.data_latency = 2
system.cpu.icache.response_latency = 2
system.cpu.icache.mshrs = 4
system.cpu.icache.tgts_per_mshr = 20

# Connect L1 I-cache to CPU
system.cpu.icache.cpu_side = system.cpu.icache_port


# -----------------------------
# L1 Data Cache
# -----------------------------
system.cpu.dcache = Cache()
system.cpu.dcache.size = "16KiB"
system.cpu.dcache.assoc = 2
system.cpu.dcache.tag_latency = 2
system.cpu.dcache.data_latency = 2
system.cpu.dcache.response_latency = 2
system.cpu.dcache.mshrs = 4
system.cpu.dcache.tgts_per_mshr = 20

# Connect L1 D-cache to CPU
system.cpu.dcache.cpu_side = system.cpu.dcache_port

# -----------------------------
# L2 Bus
# -----------------------------
system.l2bus = L2XBar()

# Connect L1 caches to L2 bus
system.cpu.icache.mem_side = system.l2bus.cpu_side_ports
system.cpu.dcache.mem_side = system.l2bus.cpu_side_ports


# -----------------------------
# L2 Cache
# -----------------------------
system.l2cache = Cache()

system.l2cache.size = "512KiB"
system.l2cache.assoc = 4

system.l2cache.tag_latency = 10
system.l2cache.data_latency = 10
system.l2cache.response_latency = 10

system.l2cache.mshrs = 20
system.l2cache.tgts_per_mshr = 12

# Connect L2 to the L2 bus
system.l2cache.cpu_side = system.l2bus.mem_side_ports

# -----------------------------
# L3 Bus
# -----------------------------
system.l3bus = L2XBar()

# Connect L2 to L3 bus
system.l2cache.mem_side = system.l3bus.cpu_side_ports


# -----------------------------
# L3 Cache
# -----------------------------
system.l3cache = Cache()

system.l3cache.size = "1MiB"
system.l3cache.assoc = 8

system.l3cache.tag_latency = 20
system.l3cache.data_latency = 20
system.l3cache.response_latency = 20

system.l3cache.mshrs = 20
system.l3cache.tgts_per_mshr = 12

# Connect L3 to L3 bus
system.l3cache.cpu_side = system.l3bus.mem_side_ports

# -----------------------------
# Main Memory Bus
# -----------------------------
system.membus = SystemXBar()

# Connect L3 to memory bus
system.l3cache.mem_side = system.membus.cpu_side_ports


# -----------------------------
# Main Memory Controller
# -----------------------------
system.mem_ctrl = MemCtrl()

system.mem_ctrl.dram = DDR3_1600_8x8()
system.mem_ctrl.dram.range = system.mem_ranges[0]

system.mem_ctrl.port = system.membus.mem_side_ports

# -----------------------------
# CPU interrupt controller
# -----------------------------

system.cpu.createInterruptController()

# -----------------------------
# System port
# -----------------------------
system.system_port = system.membus.cpu_side_ports

# -----------------------------
# Workload
# -----------------------------
system.workload = SEWorkload.init_compatible(args.binary)

process = Process()

# Pass the input file to qsort_large
process.cmd = [
    args.binary,
    "/workspace/mibench/automotive/qsort/input_large.dat",
]

system.cpu.workload = process
system.cpu.createThreads()

# -----------------------------
# Root and simulation
# -----------------------------
root = Root(full_system=False, system=system)

m5.instantiate()

print("Beginning simulation!")

exit_event = m5.simulate()

print(
    f"Exiting @ tick {m5.curTick()} "
    f"because {exit_event.getCause()}"
)