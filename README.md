# Parallel Computing Demonstration Application & Simulation Suite

A Python-based desktop application and simulation suite for exploring **parallel processing, multiprocessor architectures, processor scheduling, bus communication, cache coherence, and performance evaluation**.

This project was developed as the final group project for **IE2064 – Advanced Computer Organization and Architecture** at the **Sri Lanka Institute of Information Technology (SLIIT)**.

---

## 📌 Project Overview

The application provides a unified, menu-driven graphical interface built with **Tkinter**. It combines five simulation modules that demonstrate how parallel systems distribute work, communicate, coordinate memory access, and scale across processing units.

The repository also includes benchmark diagrams, the complete Python source code, and the final academic report.

---

## 🚀 Key Features

- Interactive Tkinter desktop GUI
- Sequential, multithreaded, and multiprocessing comparisons
- Demonstration of Python's Global Interpreter Lock (GIL)
- Static and dynamic processor-load balancing experiments
- Shared-bus contention and arbitration simulation
- MESI cache-coherence state-transition simulation
- False-sharing, true-sharing, and cache-aligned memory experiments
- Execution-time, speedup, and efficiency analysis
- Amdahl's Law comparison
- CPU and system telemetry monitoring
- Matplotlib-based benchmark visualizations

---

## 🧩 Simulation Modules

### 1. Parallelism Module — ILP, TLP, and DLP

Compares CPU-bound workload execution using:

- Sequential processing
- Multithreading
- Multiprocessing

The module demonstrates the effect of Python's **Global Interpreter Lock (GIL)** and explains why multiprocessing can provide genuine parallel execution for CPU-bound tasks.

### 2. Processor Scheduling Module

Evaluates processor scheduling and load-balancing strategies using heterogeneous workloads:

- Static load balancing
- Dynamic load balancing
- Task distribution across processing units
- Processor utilization and idle-time behavior

### 3. Bus and Communication Module

Simulates a shared bus accessed by multiple processing cores. The module examines:

- Bus access requests
- Multi-core contention
- Arbitration strategies
- Transfer-time variation
- Performance scaling as the number of cores increases

### 4. Cache Coherence Module — MESI Protocol

Demonstrates memory interactions using the **MESI cache-coherence protocol**:

- **M — Modified**
- **E — Exclusive**
- **S — Shared**
- **I — Invalid**

The module explores false sharing, true sharing with mutex synchronization, cache-aligned data, bus transactions, and cache invalidation penalties.

### 5. Performance Evaluation Module

Aggregates and visualizes performance results using:

- Execution-time comparisons
- Speedup calculations
- Parallel-efficiency calculations
- Processor-count comparisons
- Amdahl's Law analysis
- CPU and system telemetry
- Matplotlib performance graphs

---

## 📐 Performance Metrics

### Speedup

```text
Speedup = Sequential Execution Time / Parallel Execution Time
```

### Parallel Efficiency

```text
Efficiency = Speedup / Number of Processing Units
```

### Amdahl's Law

```text
Speedup(N) = 1 / ((1 - P) + (P / N))
```

Where `P` is the parallelizable portion of the workload and `N` is the number of processing units.

Measured results may differ from theoretical results because of process-creation overhead, synchronization, communication, scheduling, memory access, and hardware limitations.

---

## 🛠️ Technology Stack

| Category | Technologies |
|---|---|
| Programming language | Python 3.10+ |
| GUI framework | Tkinter |
| Parallel execution | `multiprocessing`, `threading`, `concurrent.futures` |
| Numerical computing | NumPy |
| Benchmarking | `time.perf_counter()` |
| System monitoring | psutil |
| Visualization | Matplotlib |
| Shared-memory experiments | `ctypes` |

---

## ⚙️ Installation

### Requirements

- Python **3.10 or later**
- A desktop environment with Tkinter support
- NumPy
- psutil
- Matplotlib

Install the required Python packages with:

```bash
pip install numpy psutil matplotlib
```

> On some Linux distributions, Tkinter may need to be installed separately through the operating system's package manager.

---

## ▶️ Running the Application

The main application entry point is located in the `IE2064_Group_2_Code` directory.

From the repository root, run:

```bash
python IE2064_Group_2_Code/main.py
```

Then select the required simulation module from the graphical interface.

On Windows, the following command may also be used:

```bash
py IE2064_Group_2_Code/main.py
```

---

## 📁 Repository Structure

```text
Design-and-Performance-Analysis-of-Parallel-Processing-and-Multiprocessor-Architectures/
│
├── Benchmark Diagrams/
│   ├── GUI.png
│   ├── Module 1.png
│   ├── benchmark_comparison.png
│   ├── graph1_execution_time.png
│   ├── graph2_overhead.png
│   ├── graph3_comparison.png
│   ├── module2_plot.png
│   ├── module3_plot.png
│   ├── module4_cache_analysis.png
│   ├── module4_plot.png
│   ├── module5_plot.png
│   ├── scaling_analysis.png
│   └── Additional architecture and benchmark diagrams
│
├── IE2064_Group_2_Code/
│   ├── main.py                    # Main Tkinter application
│   ├── module1.py                 # Module 1 interface/support code
│   ├── module1_parallelism.py     # ILP, TLP, and DLP experiments
│   ├── module2.py                 # Module 2 interface/support code
│   ├── module2_scheduling.py      # Processor scheduling experiments
│   ├── module3.py                 # Module 3 interface/support code
│   ├── module3_bus.py             # Bus and communication simulation
│   ├── module4.py                 # Module 4 interface/support code
│   ├── module4_cache.py           # MESI and cache-coherence simulation
│   ├── module5.py                 # Module 5 interface/support code
│   └── module5_evaluation.py      # Performance evaluation and visualization
│
├── Report/
│   └── Group No. 02 - ACOA - Final Assignment report.pdf
│
└── README.md
```

> The `__pycache__` directory contains automatically generated Python bytecode and is not part of the source-code documentation.

---

## 📊 Benchmark Visualizations

The [`Benchmark Diagrams`](./Benchmark%20Diagrams/) folder contains GUI captures, architecture diagrams, execution-time comparisons, overhead plots, cache-analysis results, module plots, and scaling-analysis graphs.

Examples include:

- [`GUI.png`](./Benchmark%20Diagrams/GUI.png)
- [`Module 1.png`](./Benchmark%20Diagrams/Module%201.png)
- [`benchmark_comparison.png`](./Benchmark%20Diagrams/benchmark_comparison.png)
- [`graph1_execution_time.png`](./Benchmark%20Diagrams/graph1_execution_time.png)
- [`graph2_overhead.png`](./Benchmark%20Diagrams/graph2_overhead.png)
- [`graph3_comparison.png`](./Benchmark%20Diagrams/graph3_comparison.png)
- [`module4_cache_analysis.png`](./Benchmark%20Diagrams/module4_cache_analysis.png)
- [`scaling_analysis.png`](./Benchmark%20Diagrams/scaling_analysis.png)

---

## 📄 Project Report

The final assignment report is available in the [`Report`](./Report/) folder:

- [`Group No. 02 - ACOA - Final Assignment report.pdf`](./Report/Group%20No.%2002%20-%20ACOA%20-%20Final%20Assignment%20report.pdf)

---

## 📈 Expected Observations

The simulations are designed to demonstrate that:

- Multithreading may provide limited benefits for CPU-bound Python workloads because of the GIL.
- Multiprocessing can improve CPU-bound performance by using separate processes.
- Dynamic load balancing can reduce processor idle time for uneven workloads.
- Shared-bus contention increases as more processors compete for communication resources.
- False sharing can reduce performance even when threads modify logically independent variables.
- Cache alignment and padding can reduce unnecessary cache-line invalidations.
- Synchronization and communication overhead limit practical speedup.
- Real-world performance generally falls below the ideal prediction of Amdahl's Law.

Actual benchmark results depend on the operating system, Python version, processor architecture, number of cores, workload size, and background system activity.

---

## 🎓 Academic Information

**Module:** IE2064 – Advanced Computer Organization and Architecture  
**Programme:** Year 2, Semester 2  
**Institution:** Sri Lanka Institute of Information Technology (SLIIT)  
**Project:** Group 02 final project

---

## 👥 Group Members

| Name | IT Number |
|---|---|
| L. P. Jayasinghe | `IT24100888` |
| B. A. Sellapperuma | `IT24103485` |
| M. F. V. Mihindukula | `IT24103486` |
| K. G. A. D. Somarathna | `IT24103487` |

---

## 📚 References

- *X: A Comprehensive Analytic Model for Parallel Machines* (2016)
- Hill, M. D., & Marty, M. R. — *Amdahl's Law in the Multicore Era* (2008)
- Sorin, D. J., Hill, M. D., & Wood, D. A. — *A Primer on Memory Consistency and Cache Coherence* (2019)

---

## ⚠️ Benchmarking Notes

For more reliable comparisons:

- Run each experiment multiple times.
- Keep workload sizes consistent.
- Close unnecessary background applications.
- Record the processor model and number of available cores.
- Compare results on the same machine under similar system conditions.

---

## 📄 License

This project was developed for academic and educational purposes as part of the IE2064 module.
