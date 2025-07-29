from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


result_file = Path("results/summary.csv")
df = pd.read_csv(result_file)

pivot = df.pivot(index="operation", columns="engine", values="duration_sec")
pivot.plot(kind="bar", figsize=(10, 6), rot=0)
plt.title("FireDucks vs Pandas Benchmark (Lower is Better)")
plt.ylabel("Avg Duration (s)")
plt.tight_layout()

# Ensure output folder exists before saving
Path("results/plots").mkdir(parents=True, exist_ok=True)
plt.savefig("results/plots/benchmark_comparison.png", dpi=300)

plt.show()
