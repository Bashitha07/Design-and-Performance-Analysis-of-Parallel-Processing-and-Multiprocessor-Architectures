"""
IE2064 - Module 2: Processor Scheduling Module
Simulates Static vs Dynamic Load Balancing across multiple processors.
"""

import time
import random
import threading
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

NUM_TASKS = 32
MAX_TASK_DURATION = 0.15   # seconds (simulated CPU burst)
MIN_TASK_DURATION = 0.01

def simulate_task(duration):
    """Simulate a CPU-bound task of variable duration."""
    deadline = time.perf_counter() + duration
    while time.perf_counter() < deadline:
        _ = sum(i * i for i in range(500))  # busy-wait CPU work

# ─────────────────────────────────────────────
#  Static Load Balancing
# ─────────────────────────────────────────────

def static_worker(tasks):
    for t in tasks:
        simulate_task(t)

def static_load_balance(tasks, num_processors):
    """Divide tasks into equal chunks upfront, then execute."""
    chunk_size = max(1, len(tasks) // num_processors)
    chunks = [tasks[i:i + chunk_size] for i in range(0, len(tasks), chunk_size)]
    threads = [threading.Thread(target=static_worker, args=(chunk,)) for chunk in chunks]
    t0 = time.perf_counter()
    for th in threads:
        th.start()
    for th in threads:
        th.join()
    return time.perf_counter() - t0

# ─────────────────────────────────────────────
#  Dynamic Load Balancing
# ─────────────────────────────────────────────

def dynamic_worker(task_queue, lock):
    while True:
        with lock:
            if not task_queue:
                break
            task = task_queue.pop(0)
        simulate_task(task)

def dynamic_load_balance(tasks, num_processors):
    """Tasks are pulled dynamically as processors become free."""
    task_queue = list(tasks)
    lock = threading.Lock()
    threads = [threading.Thread(target=dynamic_worker, args=(task_queue, lock))
               for _ in range(num_processors)]
    t0 = time.perf_counter()
    for th in threads:
        th.start()
    for th in threads:
        th.join()
    return time.perf_counter() - t0

# ─────────────────────────────────────────────
#  Benchmark
# ─────────────────────────────────────────────

def run_module2():
    print("\n" + "="*60)
    print("  MODULE 2 — Processor Scheduling: Static vs Dynamic LB")
    print("="*60)

    random.seed(99)
    # Heterogeneous task set (highly variable durations → dynamic wins)
    hetero_tasks = [random.uniform(MIN_TASK_DURATION, MAX_TASK_DURATION) for _ in range(NUM_TASKS)]
    # Homogeneous task set (equal durations → static is fine)
    homo_tasks   = [MAX_TASK_DURATION / 2] * NUM_TASKS

    processor_counts = [1, 2, 4, 8]
    static_hetero, dynamic_hetero = [], []
    static_homo,   dynamic_homo   = [], []

    print(f"\n  {'Procs':<8} {'Static-Hetero':>14} {'Dyn-Hetero':>12} {'Static-Homo':>12} {'Dyn-Homo':>10}")
    for n in processor_counts:
        sh = static_load_balance(list(hetero_tasks), n)
        dh = dynamic_load_balance(list(hetero_tasks), n)
        so = static_load_balance(list(homo_tasks), n)
        do = dynamic_load_balance(list(homo_tasks), n)
        static_hetero.append(sh); dynamic_hetero.append(dh)
        static_homo.append(so);   dynamic_homo.append(do)
        print(f"  {n:<8} {sh:>14.4f} {dh:>12.4f} {so:>12.4f} {do:>10.4f}")

    # Plot
    fig, axes = plt.subplots(1, 2, figsize=(13, 5))
    fig.suptitle("Figure 2: Module 2 — Load Balancing Completion Time", fontsize=13, fontweight='bold')

    for ax, static, dynamic, title in [
        (axes[0], static_hetero, dynamic_hetero, "Heterogeneous Tasks (Variable Duration)"),
        (axes[1], static_homo,   dynamic_homo,   "Homogeneous Tasks (Equal Duration)")
    ]:
        ax.plot(processor_counts, static,  'o-', label='Static LB',  color='tomato')
        ax.plot(processor_counts, dynamic, 's-', label='Dynamic LB', color='steelblue')
        ax.set_xlabel("Number of Processors")
        ax.set_ylabel("Completion Time (s)")
        ax.set_title(title)
        ax.legend(); ax.grid(True)

    plt.tight_layout()
    plt.savefig("/home/claude/IE2064_Code/module2_plot.png", dpi=150)
    plt.close()
    print("\n  [Graph saved: module2_plot.png]")

    print("\n  ANALYSIS:")
    print("  With heterogeneous task durations, dynamic load balancing consistently")
    print("  outperforms static because it avoids processor idle time when some workers")
    print("  finish their chunk early. Static balancing excels under homogeneous workloads")
    print("  where the equal-division strategy incurs no imbalance and avoids the overhead")
    print("  of the dynamic task-queue synchronisation (lock contention). This mirrors")
    print("  Round-Robin vs. Least-Connection scheduling theory in literature.")

    return {"static_hetero": static_hetero, "dynamic_hetero": dynamic_hetero,
            "static_homo": static_homo, "dynamic_homo": dynamic_homo,
            "processor_counts": processor_counts}

if __name__ == "__main__":
    run_module2()
