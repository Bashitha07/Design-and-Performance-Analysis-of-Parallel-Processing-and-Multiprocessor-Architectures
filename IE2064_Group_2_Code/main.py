"""
IE2064 — Advanced Computer Organization & Architecture
Parallel Computing Demonstration Application
================================================
Unified menu-driven interface integrating all 5 modules.

Usage:
    python main.py           → interactive menu
    python main.py --all     → run all modules sequentially
"""

import sys
import os
import multiprocessing

# Ensure submodules can be imported
sys.path.insert(0, os.path.dirname(__file__))

BANNER = """
╔══════════════════════════════════════════════════════════════╗
║   IE2064 — Parallel Computing Demonstration Application      ║
║   BSc (Hons) IT — Computer Systems Engineering              ║
╠══════════════════════════════════════════════════════════════╣
║  [1]  Module 1 — Parallelism: Threading vs Multiprocessing  ║
║  [2]  Module 2 — Processor Scheduling: Static vs Dynamic LB ║
║  [3]  Module 3 — Bus & Communication (Contention Model)     ║
║  [4]  Module 4 — Cache Coherence: False Sharing & Padding   ║
║  [5]  Module 5 — Performance Evaluation & Visualisation     ║
║  [A]  Run ALL modules sequentially                          ║
║  [Q]  Quit                                                  ║
╚══════════════════════════════════════════════════════════════╝
"""

def import_modules():
    from module1_parallelism  import run_module1
    from module2_scheduling   import run_module2
    from module3_bus          import run_module3
    from module4_cache        import run_module4
    from module5_evaluation   import run_module5
    return run_module1, run_module2, run_module3, run_module4, run_module5

def run_all(fns):
    print("\n>>> Running all modules sequentially...\n")
    results = {}
    r1, r2, r3, r4, r5 = fns
    results["m1"] = r1()
    results["m2"] = r2()
    results["m3"] = r3()
    results["m4"] = r4()
    results["m5"] = r5()
    print("\n" + "="*60)
    print("  ALL MODULES COMPLETE")
    print("  Generated plots:")
    for i in range(1, 6):
        print(f"    module{i}_plot.png")
    print("="*60)
    return results

def interactive_menu(fns):
    r1, r2, r3, r4, r5 = fns
    dispatch = {
        "1": r1, "2": r2, "3": r3, "4": r4, "5": r5,
        "a": lambda: run_all(fns),
    }
    while True:
        print(BANNER)
        choice = input("  Enter choice: ").strip().lower()
        if choice == "q":
            print("\n  Exiting. Goodbye!\n")
            break
        elif choice in dispatch:
            try:
                dispatch[choice]()
            except Exception as e:
                print(f"\n  [ERROR] Module failed: {e}\n")
        else:
            print("\n  Invalid choice — please enter 1-5, A, or Q.\n")

def main():
    multiprocessing.freeze_support()
    fns = import_modules()

    if "--all" in sys.argv:
        run_all(fns)
    else:
        interactive_menu(fns)

if __name__ == "__main__":
    main()
