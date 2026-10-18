# IE2064 — Advanced Computer Organization & Architecture
# Module 4: Cache Coherence (MESI Protocol) - Member 3

import time
import multiprocessing as mp
import ctypes
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# --- Configuration Constants ---
CACHE_LINE = 64
LONG_SIZE = ctypes.sizeof(ctypes.c_long)
PAD_STRIDE = CACHE_LINE // LONG_SIZE
ITERS = 1_000_000
TRUE_ITERS = 80_000
WORKER_COUNTS = [1, 2, 4, 8]


# --- Worker Functions ---

# False Sharing: all workers write to adjacent indices on the SAME cache line
def worker_false(arr, idx, iters):
    for _ in range(iters):
        arr[idx] += 1

# True Sharing: all workers write to the SAME variable with a lock
def worker_true(val, lock, iters):
    for _ in range(iters):
        with lock:
            val.value += 1

# Cache-Aligned: each worker writes to its OWN cache line (padded)
def worker_aligned(arr, idx, stride, iters):
    pos = idx * stride
    for _ in range(iters):
        arr[pos] += 1


# --- Benchmark Runner ---
def run(mode, n, iters):
    if mode == "false":
        arr = mp.Array(ctypes.c_long, n, lock=False)
        procs = [mp.Process(target=worker_false, args=(arr, i, iters)) for i in range(n)]
    elif mode == "true":
        val = mp.Value(ctypes.c_long, 0)
        lock = mp.Lock()
        procs = [mp.Process(target=worker_true, args=(val, lock, iters)) for _ in range(n)]
    else:
        arr = mp.Array(ctypes.c_long, n * PAD_STRIDE, lock=False)
        procs = [mp.Process(target=worker_aligned, args=(arr, i, PAD_STRIDE, iters)) for i in range(n)]

    start = time.perf_counter()
    for p in procs: p.start()
    for p in procs: p.join()
    return time.perf_counter() - start


# --- MESI State Transition Simulator ---
class MESISimulator:
    def __init__(self, num_cpus=2):
        self.num_cpus = num_cpus
        self.states = {cpu: "I" for cpu in range(num_cpus)}
        self.txns = 0

    def write(self, cpu):
        old = self.states[cpu]
        others = [c for c in range(self.num_cpus) if c != cpu]
        if old in ("M", "E"):
            self.states[cpu] = "M"
            return
        for c in others:
            if self.states[c] == "M":
                self.txns += 1
            if self.states[c] in ("S", "E", "M"):
                self.states[c] = "I"
        self.txns += 2 if old == "I" else 1
        self.states[cpu] = "M"

    def simulate(self, cycles=4):
        print("\n  MESI False Sharing Simulation:")
        for _ in range(cycles):
            self.write(0)
            print(f"  CPU-0 writes | C0:{self.states[0]} C1:{self.states[1]} | Bus Txns: {self.txns}")
            self.write(1)
            print(f"  CPU-1 writes | C0:{self.states[0]} C1:{self.states[1]} | Bus Txns: {self.txns}")


# --- MEMBER 3: PERFORMANCE GRAPH GENERATION ---

# Graph 1: Execution Time vs Workers
def plot_execution_time(false_t, true_t, pad_t):
    plt.figure(figsize=(10, 6))
    plt.plot(WORKER_COUNTS, false_t, marker='o', color='r', label='False Sharing')
    plt.plot(WORKER_COUNTS, true_t, marker='^', color='orange', label='True Sharing (Mutex)')
    plt.plot(WORKER_COUNTS, pad_t, marker='s', color='b', label='Cache-Aligned (Padded)')
    plt.title('Execution Time vs Number of Workers')
    plt.xlabel('Number of Workers')
    plt.ylabel('Time (seconds)')
    plt.xticks(WORKER_COUNTS)
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig('graph1_execution_time.png', dpi=100)
    plt.close()
    print("  Graph saved: graph1_execution_time.png")

# Graph 2: Overhead % vs Workers
def plot_overhead(false_oh, true_oh):
    plt.figure(figsize=(10, 6))
    plt.plot(WORKER_COUNTS, false_oh, marker='o', color='r', label='False Sharing Overhead %')
    plt.plot(WORKER_COUNTS, true_oh, marker='^', color='orange', label='True Sharing Overhead %')
    plt.axhline(0, color='b', linestyle='--', label='Aligned Baseline (0%)')
    plt.title('Overhead vs Cache-Aligned Baseline (%)')
    plt.xlabel('Number of Workers')
    plt.ylabel('Overhead (%)')
    plt.xticks(WORKER_COUNTS)
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig('graph2_overhead.png', dpi=100)
    plt.close()
    print("  Graph saved: graph2_overhead.png")

# Graph 3: Bar Comparison at 8 Workers
def plot_bar_comparison(false_t, true_t, pad_t):
    plt.figure(figsize=(10, 6))
    scenarios = ['False Sharing', 'True Sharing\n(Mutex)', 'Cache-Aligned\n(Padded)']
    times = [false_t[-1], true_t[-1], pad_t[-1]]
    colors = ['#E63946', '#F4A261', '#457B9D']
    bars = plt.bar(scenarios, times, color=colors, edgecolor='black')
    for bar, val in zip(bars, times):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height(),
                 f'{val:.3f}s', ha='center', va='bottom', fontweight='bold')
    plt.title('Scenario Comparison at 8 Workers (lower = better)')
    plt.ylabel('Execution Time (seconds)')
    plt.grid(True, axis='y')
    plt.tight_layout()
    plt.savefig('graph3_comparison.png', dpi=100)
    plt.close()
    print("  Graph saved: graph3_comparison.png")


# --- Main Entry Point ---
def run_module_4():
    print("\n" + "=" * 70)
    print("  MODULE 4: CACHE COHERENCE (MESI PROTOCOL)")
    print("=" * 70)
    print(f"  System CPUs   : {mp.cpu_count()}")
    print(f"  Cache line    : {CACHE_LINE} bytes  |  Pad stride: {PAD_STRIDE}")
    print(f"  Iterations    : {ITERS:,} per worker")
    print(f"  Worker configs: {WORKER_COUNTS}")

    # Run MESI simulation
    sim = MESISimulator()
    sim.simulate()

    # Measure baseline
    print("\n  Measuring baseline (1-process cache-aligned) ...")
    baseline = run("padded", 1, ITERS)
    print(f"  Baseline : {baseline:.4f}s")

    # Run benchmarks for each worker count
    print(f"\n  {'Workers':<10} | {'False (s)':<12} | {'True (s)':<12} | {'Aligned (s)':<12} | {'False OH%':<10} | {'True OH%'}")
    print("  " + "-" * 75)

    false_t, true_t, pad_t = [], [], []
    false_oh, true_oh = [], []

    for n in WORKER_COUNTS:
        ft = run("false", n, ITERS)
        tt = run("true", n, TRUE_ITERS)
        pt = baseline if n == 1 else run("padded", n, ITERS)

        false_t.append(ft)
        true_t.append(tt)
        pad_t.append(pt)

        f_oh = (ft / pt - 1) * 100
        t_oh = (tt / pt - 1) * 100
        false_oh.append(f_oh)
        true_oh.append(t_oh)

        print(f"  {n:<10} | {ft:>10.4f}s | {tt:>10.4f}s | {pt:>10.4f}s | {f_oh:>+9.1f}% | {t_oh:>+9.1f}%")

    print("  " + "-" * 75)

    # Print analysis
    print(f"\n  False Sharing Penalty (8 workers): +{false_oh[-1]:.1f}%")
    print(f"  True Sharing Penalty (8 workers):  +{true_oh[-1]:.1f}%")

    # Now generate graphs with actual collected data
    plot_execution_time(false_t, true_t, pad_t)
    plot_overhead(false_oh, true_oh)
    plot_bar_comparison(false_t, true_t, pad_t)

    print("\n  Module 4 complete.")
    print("=" * 70)


if __name__ == "__main__":
    run_module_4()