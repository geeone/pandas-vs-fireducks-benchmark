import csv
from pathlib import Path
from statistics import mean
import time

import fireducks.pandas as fpd
import pandas as pd


CSV_PATH = "synthetic_data.csv"
RUNS = 5


def benchmark_read(label, read_func):
    durations = []
    for _ in range(RUNS):
        start = time.perf_counter()
        df = read_func(CSV_PATH)
        end = time.perf_counter()
        durations.append(end - start)
        del df
    return mean(durations)


def save_result(operation, engine, duration):
    result_file = Path("results/summary.csv")
    result_file.parent.mkdir(parents=True, exist_ok=True)
    write_header = not result_file.exists()

    with result_file.open("a", newline="") as csvfile:
        writer = csv.writer(csvfile)
        if write_header:
            writer.writerow(["operation", "engine", "duration_sec"])
        writer.writerow([operation, engine, f"{duration:.4f}"])


if __name__ == "__main__":
    pandas_duration = benchmark_read("pandas", pd.read_csv)
    print(
        f"[Pandas] Avg read_csv time over {RUNS} runs: {pandas_duration:.4f} seconds")
    save_result("read_csv", "pandas", pandas_duration)

    fireducks_duration = benchmark_read("fireducks", fpd.read_csv)
    print(
        f"[FireDucks] Avg read_csv time over {RUNS} runs: {fireducks_duration:.4f} seconds")
    save_result("read_csv", "fireducks", fireducks_duration)
