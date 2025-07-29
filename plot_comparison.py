from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


result_file = Path("results/summary.csv")
df = pd.read_csv(result_file)

# Duration plot
pivot_duration = df.pivot(index="operation", columns="engine", values="duration_sec")
pivot_duration.plot(kind="bar", figsize=(10, 6), rot=0)
plt.title("Benchmark Duration (Lower is Better)")
plt.ylabel("Avg Duration (s)")
plt.tight_layout()
Path("results/plots").mkdir(parents=True, exist_ok=True)
plt.savefig("results/plots/benchmark_duration.png", dpi=300)
plt.close()

# Memory plot
pivot_memory = df.pivot(index="operation", columns="engine", values="memory_mb")
pivot_memory.plot(kind="bar", figsize=(10, 6), rot=0)
plt.title("Benchmark Memory Usage")
plt.ylabel("Memory (MB)")
plt.tight_layout()
plt.savefig("results/plots/benchmark_memory.png", dpi=300)
plt.show()
