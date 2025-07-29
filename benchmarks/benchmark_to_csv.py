import csv
from pathlib import Path
from statistics import mean
import time

import fireducks.pandas as fpd
import pandas as pd


CSV_PATH = "synthetic_data.csv"
RUNS = 3  # Writing large files is expensive, so fewer runs

def benchmark_write(label, engine_read_func):
    durations = []
    df = engine_read_func(CSV_PATH)
    for i in range(RUNS):
        output = f"temp_output_{label}_{i}.csv"
        start = time.perf_counter()
        df.to_csv(output, index=False)
        end = time.perf_counter()
        durations.append(end - start)
        Path(output).unlink(missing_ok=True)
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
    pandas_duration = benchmark_write("pandas", pd.read_csv)
    print(f"[Pandas] Avg to_csv time over {RUNS} runs: {pandas_duration:.4f} seconds")
    save_result("to_csv", "pandas", pandas_duration)

    fireducks_duration = benchmark_write("fireducks", fpd.read_csv)
    print(f"[FireDucks] Avg to_csv time over {RUNS} runs: {fireducks_duration:.4f} seconds")
    save_result("to_csv", "fireducks", fireducks_duration)
