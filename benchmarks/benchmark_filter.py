import csv
import os
from pathlib import Path
from statistics import mean
import time

import fireducks.pandas as fpd
import pandas as pd
import psutil


CSV_PATH = "synthetic_data.csv"
RUNS = 5


def get_mem_mb():
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / 1024**2  # in MB


def benchmark_filter(label, engine_read_func):
    durations = []
    memories = []
    for _ in range(RUNS):
        df = engine_read_func(CSV_PATH)
        start = time.perf_counter()
        filtered = df[df["age"] > 40]
        end = time.perf_counter()
        durations.append(end - start)
        memories.append(get_mem_mb())
        del df, filtered
    return mean(durations), mean(memories)


def save_result(operation, engine, duration, memory):
    result_file = Path("results/summary.csv")
    result_file.parent.mkdir(parents=True, exist_ok=True)
    write_header = not result_file.exists()

    with result_file.open("a", newline="") as csvfile:
        writer = csv.writer(csvfile)
        if write_header:
            writer.writerow(["operation", "engine", "duration_sec", "memory_mb"])
        writer.writerow([operation, engine, f"{duration:.4f}", f"{memory:.2f}"])


if __name__ == "__main__":
    pandas_duration, pandas_memory = benchmark_filter("pandas", pd.read_csv)
    print(f"[Pandas] Avg filter time: {pandas_duration:.4f}s | Mem: {pandas_memory:.2f} MB")
    save_result("filter_age>40", "pandas", pandas_duration, pandas_memory)

    fireducks_duration, fireducks_memory = benchmark_filter("fireducks", fpd.read_csv)
    print(f"[FireDucks] Avg filter time: {fireducks_duration:.4f}s | Mem: {fireducks_memory:.2f} MB")
    save_result("filter_age>40", "fireducks", fireducks_duration, fireducks_memory)
