import subprocess


benchmark_scripts = [
    "benchmark_read.py",
    "benchmark_to_csv.py",
    "benchmark_filter.py",
    "benchmark_groupby.py",
    "benchmark_sort.py"
]

print("📊 Running all benchmarks...\n")
for script in benchmark_scripts:
    print(f"⏱ Running {script}...")
    subprocess.run(["python", f"benchmarks/{script}"])
print("\n✅ All benchmarks completed.")
