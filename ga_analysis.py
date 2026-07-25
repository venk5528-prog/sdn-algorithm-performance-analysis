import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# === Load GA logs ===
ftp_ga = pd.read_excel("ftp_ga.xlsx")
cbr_ga = pd.read_excel("cbr_ga.xlsx")
event_ga = pd.read_excel("event_trace_ga.xlsx")

# Helper: Jain's Fairness Index
def fairness_index(values):
    values = np.array(values)
    return (np.sum(values)**2) / (len(values) * np.sum(values**2) + 1e-9)

# === Graph 1: Latency Convergence (FTP vs CBR) ===
plt.figure()
plt.plot(ftp_ga.index, ftp_ga["Latency(Microseconds)"], label="FTP Latency")
plt.plot(cbr_ga.index, cbr_ga["Latency(Microseconds)"], label="CBR Latency")
plt.plot(cbr_ga.index, cbr_ga["FitnessVariance"], label="Fitness Variance", linestyle="--")
plt.title("GA Latency Convergence")
plt.xlabel("Packet Index"); plt.ylabel("Latency (µs)")
plt.legend(); plt.show()

# === Graph 2: Throughput Stability ===
plt.figure()
plt.plot(ftp_ga.index, ftp_ga["Throughput(Mbps)"], label="FTP Throughput")
plt.plot(cbr_ga.index, cbr_ga["Throughput(Mbps)"], label="CBR Throughput")
plt.plot(cbr_ga.index, cbr_ga["CrossoverEfficiency"], label="Crossover Efficiency", linestyle="--")
plt.title("GA Throughput Stability")
plt.xlabel("Packet Index"); plt.ylabel("Throughput (Mbps)")
plt.legend(); plt.show()

# === Graph 3: Fairness Index Trend ===
ftp_fairness = [fairness_index(ftp_ga["Throughput(Mbps)"][:i+1]) for i in range(len(ftp_ga))]
cbr_fairness = [fairness_index(cbr_ga["Throughput(Mbps)"][:i+1]) for i in range(len(cbr_ga))]

plt.figure()
plt.plot(ftp_ga.index, ftp_fairness, label="FTP Fairness")
plt.plot(cbr_ga.index, cbr_fairness, label="CBR Fairness")
plt.plot(cbr_ga.index, cbr_ga["PopulationDiversity"], label="Population Diversity", linestyle="--")
plt.title("GA Fairness Trend")
plt.xlabel("Packet Index"); plt.ylabel("Fairness Index")
plt.legend(); plt.show()

# === Graph 4: Jitter Distribution (CBR) ===
plt.figure()
plt.hist(cbr_ga["Jitter(Microseconds)"], bins=30, color="skyblue", edgecolor="black")
plt.title("GA Jitter Distribution (CBR)")
plt.xlabel("Jitter (µs)"); plt.ylabel("Frequency")
plt.show()

# === Graph 5: Event Trace Recovery Dynamics ===
plt.figure()
plt.plot(event_ga["Event_Time(µS)"], event_ga["FitnessVariance"], label="Fitness Variance")
plt.title("GA Event Trace Recovery Dynamics")
plt.xlabel("Event Time (µs)"); plt.ylabel("Fitness Variance")
plt.legend(); plt.show()

# === Graph 6: Entropy Collapse Curve ===
latencies = ftp_ga["Latency(Microseconds)"]
p = latencies / latencies.sum()
entropy = -np.sum(p * np.log1p(p))
plt.figure()
plt.plot(ftp_ga.index, np.linspace(entropy, 0, len(ftp_ga)), label="Entropy Collapse")
plt.title("GA Entropy Collapse")
plt.xlabel("Packet Index"); plt.ylabel("Entropy")
plt.legend(); plt.show()

# === Graph 7: Comparative Fingerprint Bar Chart ===
metrics = {
    "Fairness": np.mean(cbr_fairness),
    "Oscillations": np.sum(np.diff(cbr_ga["Latency(Microseconds)"]) < 0),
    "RecoveryTime": np.max(cbr_ga["Latency(Microseconds)"]) - np.mean(cbr_ga["Latency(Microseconds)"]),
    "Entropy": entropy
}
plt.figure()
plt.bar(metrics.keys(), metrics.values(), color="orange")
plt.title("GA Fingerprint Summary")
plt.ylabel("Value")
plt.show()
