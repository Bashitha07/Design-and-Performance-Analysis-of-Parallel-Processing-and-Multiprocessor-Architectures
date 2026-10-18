# Parallel Computing Demonstration Application & Simulation Suite

A Python-based desktop application for exploring **parallel processing, multiprocessor architectures, processor scheduling, bus communication, cache coherence, and performance analysis**.

This project was developed as the final group project for **IE2064 – Advanced Computer Organization and Architecture** at the **Sri Lanka Institute of Information Technology (SLIIT)**.

---

## 📌 Project Overview

The application provides a unified, menu-driven graphical interface built with **Tkinter**. Each module demonstrates a core concept in parallel and multiprocessor computing through configurable simulations, performance measurements, and visual analysis.

The project connects theoretical concepts with practical experimentation by comparing execution strategies, observing resource contention, and evaluating how performance changes as parallelism increases.

---

## 🚀 Main Features

- Interactive desktop GUI with independent simulation modules
- Comparison of sequential, threaded, and multiprocess execution
- Demonstration of Python's Global Interpreter Lock (GIL)
- Static and dynamic processor-load balancing experiments
- Shared-bus contention and arbitration simulation
- MESI cache-coherence state-transition visualization
- False-sharing, true-sharing, and cache-aligned experiments
- Speedup and efficiency analysis using Amdahl's Law
- CPU and system telemetry monitoring
- Matplotlib-based performance charts and visualizations

---

## 🧩 Simulation Modules

### 1. Parallelism Module — ILP, TLP, and DLP

Compares multiple execution approaches for CPU-bound workloads:

- Sequential execution
- Multithreading
- Multiprocessing

This module demonstrates the effect of Python's **Global Interpreter Lock (GIL)** and shows why multiprocessing can provide genuine CPU-level parallelism for suitable workloads.

The module introduces three important forms of parallelism:

- **Instruction-Level Parallelism (ILP):** Executing independent instructions concurrently
- **Thread-Level Parallelism (TLP):** Executing multiple software threads
- **Data-Level Parallelism (DLP):** Applying the same operation to multiple data elements

### 2. Processor Scheduling Module

Evaluates processor scheduling strategies using heterogeneous workloads:

- Static load balancing
- Dynamic load balancing
- Task distribution across processing units
- Core utilization and idle-time behavior

The experiments illustrate how dynamic scheduling can improve utilization when tasks have different execution times.

### 3. Bus and Communication Module

Simulates a shared bus used by multiple processing cores and evaluates the effect of communication contention.

The module explores:

- Shared-bus access requests
- Multi-core contention
- Arbitration strategies
- Transfer-time variation
- Performance scaling as the number of cores increases

### 4. Cache Coherence Module — MESI Protocol

Demonstrates memory-level interactions using the **MESI cache-coherence protocol**:

- **M — Modified**
- **E — Exclusive**
- **S — Shared**
- **I — Invalid**

The module includes experiments involving:

- False sharing
- True sharing with mutex synchronization
- Cache-aligned or padded data structures
- Bus transactions
- Cache invalidation penalties
- Interactive MESI state transitions

These experiments help demonstrate how cache-line sharing and synchronization overhead can affect multiprocessor performance.

### 5. Performance Evaluation Module

Combines measured results from the other modules and provides performance analysis through:

- Execution-time comparisons
- Speedup calculations
- Parallel efficiency calculations
- Processor-count comparisons
- Amdahl's Law analysis
- CPU and system telemetry
- Matplotlib-based performance graphs

---

## 📐 Performance Metrics

The application evaluates parallel performance using commonly used metrics.

### Speedup

```text
Speedup = Sequential Execution Time / Parallel Execution Time
```

### Parallel Efficiency

```text
Efficiency = Speedup / Number of Processing Units
```

### Amdahl's Law

Amdahl's Law is used to estimate the theoretical speedup limit when only part of a workload can be parallelized:

```text
Speedup(N) = 1 / ((1 - P) + (P / N))
```

Where:

- `P` is the parallelizable portion of the workload
- `N` is the number of processing units

The comparison between theoretical and measured results highlights the effects of overhead, synchronization, communication, scheduling, and hardware limitations.

---

## 🛠️ Technology Stack

| Category | Technologies |
|---|---|
| Programming language | Python 3.10 or later |
| GUI framework | Tkinter |
| Concurrency and parallelism | `multiprocessing`, `threading`, `concurrent.futures` |
| Numerical computing | NumPy |
| Benchmarking | `time.perf_counter()` |
| System monitoring | psutil |
| Data visualization | Matplotlib |
| Low-level memory experiments | `ctypes` |

---

## ⚙️ Requirements

- Python **3.10 or later**
- A desktop environment capable of running Tkinter
- The Python packages used by the project, including:
  - NumPy
  - psutil
  - Matplotlib

The exact execution command and dependency file may vary depending on the project structure. Install the required packages before launching the application.

Example package installation:

```bash
pip install numpy psutil matplotlib
```

> **Note:** Tkinter is commonly included with standard Python installations. On some Linux distributions, it may need to be installed separately through the operating system's package manager.

---

## ▶️ Running the Application

1. Clone or download the repository.
2. Open a terminal in the project directory.
3. Install the required Python packages.
4. Run the main Python application file.
5. Select a simulation module from the graphical interface.
6. Configure the experiment and compare the measured results.

Because the repository may contain multiple Python modules, run the project's designated main or GUI entry-point file.

---

## 📊 Expected Results

The simulations are intended to demonstrate that:

- Multithreading may provide limited benefits for CPU-bound Python workloads because of the GIL.
- Multiprocessing can improve CPU-bound performance by using separate processes.
- Dynamic load balancing can reduce idle time for uneven workloads.
- Shared-bus contention increases as more processing cores compete for communication resources.
- False sharing can reduce performance even when threads modify logically independent variables.
- Cache alignment and padding can reduce unnecessary cache-line invalidations.
- Synchronization and communication overhead limit practical speedup.
- Real-world performance generally falls below the ideal prediction of Amdahl's Law.

Actual results depend on the operating system, Python version, processor architecture, number of cores, workload configuration, and system background activity.

---

## 📁 Suggested Repository Organization

```text
Design-and-Performance-Analysis-of-Parallel-Processing-and-Multiprocessor-Architectures/
├── README.md                    # Project documentation
├── *.py                         # GUI and simulation modules
├── requirements.txt             # Optional Python dependency list
├── diagrams/                    # Architecture and flow diagrams
├── results/                     # Generated measurements and plots
└── report/                      # Academic report and supporting material
```

> The actual repository structure may differ from this suggested organization.

---

## 🎓 Academic Context

**Module:** IE2064 – Advanced Computer Organization and Architecture  
**Programme:** Year 2, Semester 2  
**Institution:** Sri Lanka Institute of Information Technology (SLIIT)  
**Project type:** Group project and simulation suite

---

## 👥 Group Members

| Name | IT Number |
|---|---|
| L. P. Jayasinghe | `IT24100888` |
| B. A. Sellapperuma | `IT24103485` |
| M. F. V. Mihindukula | `IT24103486` |
| K. G. A. D. Somarathna | `IT24103487` |

---

## 📚 References and Theoretical Foundation

The project is based on established parallel-computing and computer-architecture concepts, including:

- *X: A Comprehensive Analytic Model for Parallel Machines* (2016)
- Hill, M. D., & Marty, M. R. — *Amdahl's Law in the Multicore Era* (2008)
- Sorin, D. J., Hill, M. D., & Wood, D. A. — *A Primer on Memory Consistency and Cache Coherence* (2019)

---

## ⚠️ Notes on Benchmarking

Benchmark results should be interpreted comparatively rather than as fixed hardware-independent values. For more reliable comparisons:

- Run each experiment multiple times.
- Keep workload sizes consistent.
- Close unnecessary background applications.
- Record the processor model and number of available cores.
- Compare results on the same machine and under similar system conditions.

---

## 📄 License

This project was developed for academic and educational purposes as part of the IE2064 module.
