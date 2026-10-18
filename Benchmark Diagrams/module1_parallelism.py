"""
IE2064 - Module 1: Parallelism Module
Compares sequential, threading, and multiprocessing for matrix multiplication.
Calculates Speedup and Efficiency per configuration.
"""

import time
import threading
import multiprocessing
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import psutil
import os

MATRIX_SIZE = 256  # NxN matrix size for computation

# ─────────────────────────────────────────────
#  Core computation: matrix multiplication chunk
# ─────────────────────────────────────────────

def multiply_chunk(A, B, result, row_start, row_end):
    """Multiply a slice of rows of A with full B, store in result."""
    for i in range(row_start, row_end):
        for j in range(B.shape[1]):
            result[i][j] = np.dot(A[i], B[:, j])

def sequential_multiply(A, B):
    """Pure sequential matrix multiplication."""
    n = A.shape[0]
    result = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            result[i][j] = np.dot(A[i], B[:, j])
    return result

# ─────────────────────────────────────────────
#  Threading implementation
# ─────────────────────────────────────────────

def threaded_multiply(A, B, num_threads):
    n = A.shape[0]
    result = [[0.0] * n for _ in range(n)]
    chunk = n // num_threads
    threads = []
    for i in range(num_threads):
        row_start = i * chunk
        row_end = n if i == num_threads - 1 else (i + 1) * chunk
        t = threading.Thread(target=multiply_chunk, args=(A, B, result, row_start, row_end))
        threads.append(t)
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    return np.array(result)

# ─────────────────────────────────────────────
#  Multiprocessing implementation
# ─────────────────────────────────────────────

def mp_worker(A_shared, B_shared, result_queue, row_start, row_end, n):
    chunk_result = []
    for i in range(row_start, row_end):
        row = [float(np.dot(A_shared[i], B_shared[:, j])) for j in range(n)]
        chunk_result.append((i, row))
    result_queue.put(chunk_result)

def multiprocess_multiply(A, B, num_processes):
    n = A.shape[0]
    result = np.zeros((n, n))
    chunk = n // num_processes
    processes = []
    queue = multiprocessing.Queue()
    for i in range(num_processes):
        row_start = i * chunk
        row_end = n if i == num_processes - 1 else (i + 1) * chunk
        p = multiprocessing.Process(target=mp_worker, args=(A, B, queue, row_start, row_end, n))
        processes.append(p)
    for p in processes:
        p.start()
    for p in processes:
        p.join()
    while not queue.empty():
        chunk_result = queue.get()
        for i, row in chunk_result:
            result[i] = row
    return result

# ─────────────────────────────────────────────
#  Benchmark runner
# ─────────────────────────────────────────────

def run_module1():
    print("\n" + "="*60)
    print("  MODULE 1 — Parallelism: Threading vs Multiprocessing")
    print("="*60)
    np.random.seed(42)
    A = np.random.rand(MATRIX_SIZE, MATRIX_SIZE)
    B = np.random.rand(MATRIX_SIZE, MATRIX_SIZE)

    worker_counts = [1, 2, 4, 8]
    results = {
        "sequential_time": None,
        "thread_times": {},
        "mp_times": {},
        "thread_speedup": {},
        "mp_speedup": {},
        "thread_efficiency": {},
        "mp_efficiency": {},
    }

    # --- Sequential ---
    print("\n[Sequential]")
    t0 = time.perf_counter()
    sequential_multiply(A, B)
    seq_time = time.perf_counter() - t0
    results["sequential_time"] = seq_time
    print(f"  Time: {seq_time:.4f}s")

    # --- Threading ---
    print("\n[Threading]")
    print(f"  {'Workers':<10} {'Time(s)':<12} {'Speedup':<12} {'Efficiency'}")
    for n in worker_counts:
        t0 = time.perf_counter()
        threaded_multiply(A, B, n)
        elapsed = time.perf_counter() - t0
        speedup = seq_time / elapsed
        efficiency = speedup / n * 100
        results["thread_times"][n] = elapsed
        results["thread_speedup"][n] = speedup
        results["thread_efficiency"][n] = efficiency
        print(f"  {n:<10} {elapsed:<12.4f} {speedup:<12.4f} {efficiency:.1f}%")

    # --- Multiprocessing ---
    print("\n[Multiprocessing]")
    print(f"  {'Workers':<10} {'Time(s)':<12} {'Speedup':<12} {'Efficiency'}")
    for n in worker_counts:
        t0 = time.perf_counter()
        multiprocess_multiply(A, B, n)
        elapsed = time.perf_counter() - t0
        speedup = seq_time / elapsed
        efficiency = speedup / n * 100
        results["mp_times"][n] = elapsed
        results["mp_speedup"][n] = speedup
        results["mp_efficiency"][n] = efficiency
        print(f"  {n:<10} {elapsed:<12.4f} {speedup:<12.4f} {efficiency:.1f}%")

    # --- Amdahl's Law overlay ---
    # Assume ~80% parallelisable fraction (p=0.80)
    p = 0.80
    amdahl_speedup = {n: 1 / ((1 - p) + p / n) for n in worker_counts}

    # --- Plot ---
    fig, axes = plt.subplots(1, 3, figsize=(16, 5))
    fig.suptitle("Figure 1: Module 1 — Parallelism Performance", fontsize=13, fontweight='bold')

    # Speedup
    ax = axes[0]
    ax.plot(worker_counts, [results["thread_speedup"][n] for n in worker_counts],
            'o-', label='Threading', color='royalblue')
    ax.plot(worker_counts, [results["mp_speedup"][n] for n in worker_counts],
            's-', label='Multiprocessing', color='darkorange')
    ax.plot(worker_counts, [amdahl_speedup[n] for n in worker_counts],
            '--', label="Amdahl's Law (p=0.80)", color='green')
    ax.set_xlabel("Number of Workers")
    ax.set_ylabel("Speedup (T_seq / T_par)")
    ax.set_title("Speedup vs Workers")
    ax.legend(); ax.grid(True)

    # Efficiency
    ax = axes[1]
    ax.plot(worker_counts, [results["thread_efficiency"][n] for n in worker_counts],
            'o-', label='Threading', color='royalblue')
    ax.plot(worker_counts, [results["mp_efficiency"][n] for n in worker_counts],
            's-', label='Multiprocessing', color='darkorange')
    ax.set_xlabel("Number of Workers")
    ax.set_ylabel("Efficiency (%)")
    ax.set_title("Efficiency vs Workers")
    ax.legend(); ax.grid(True)

    # Execution Time
    ax = axes[2]
    ax.bar([f"T-{n}" for n in worker_counts],
           [results["thread_times"][n] for n in worker_counts],
           label='Threading', color='royalblue', alpha=0.7)
    ax.bar([f"P-{n}" for n in worker_counts],
           [results["mp_times"][n] for n in worker_counts],
           label='Multiprocessing', color='darkorange', alpha=0.7)
    ax.axhline(seq_time, color='red', linestyle='--', label='Sequential')
    ax.set_xlabel("Configuration")
    ax.set_ylabel("Execution Time (s)")
    ax.set_title("Execution Time Comparison")
    ax.legend(); ax.grid(True, axis='y')

    plt.tight_layout()
    plt.savefig("/home/claude/IE2064_Code/module1_plot.png", dpi=150)
    plt.close()
    print("\n  [Graph saved: module1_plot.png]")

    print("\n  ANALYSIS:")
    print("  Threading is limited by Python's GIL (Global Interpreter Lock), which prevents")
    print("  true parallel execution of CPU-bound bytecode. Multiple threads run concurrently")
    print("  but not simultaneously on multiple cores for compute-heavy tasks. Multiprocessing")
    print("  bypasses the GIL by spawning separate interpreter processes, each with its own")
    print("  memory space, enabling genuine parallel CPU execution on multi-core hardware.")
    print("  The overhead of inter-process communication and process spawning means")
    print("  multiprocessing is most beneficial when task granularity is large.")

    return results

if __name__ == "__main__":
    multiprocessing.freeze_support()
    run_module1()
