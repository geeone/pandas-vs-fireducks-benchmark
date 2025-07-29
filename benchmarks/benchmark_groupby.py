import csv
from pathlib import Path
from statistics import mean
import time

import fireducks.pandas as fpd
import pandas as pd


CSV_PATH = "synthetic_data.csv"
RUNS = 5


def benchmark_groupby(label, engine_read_func):
    durations = []
    for _ in range(RUNS):
        df = engine_read_func(CSV_PATH)
        start = time.perf_counter()
        result = df.groupby("country")["income"].mean()
        end = time.perf_counter()
        durations.append(end - start)
        del df, result
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
    pandas_duration = benchmark_groupby("pandas", pd.read_csv)
    print(
        f"[Pandas] Avg groupby time over {RUNS} runs: {pandas_duration:.4f} seconds")
    save_result("groupby_country_income_mean", "pandas", pandas_duration)

    fireducks_duration = benchmark_groupby("fireducks", fpd.read_csv)
    print(
        f"[FireDucks] Avg groupby time over {RUNS} runs: {fireducks_duration:.4f} seconds")
    save_result("groupby_country_income_mean", "fireducks", fireducks_duration)
