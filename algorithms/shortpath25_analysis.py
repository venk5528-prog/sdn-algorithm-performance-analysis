import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# === Load SSSP logs ===
ftp_sssp = pd.read_excel("ftp_sssp2025.xlsx")
cbr_sssp = pd.read_excel("cbr_sssp2025.xlsx")
event_sssp = pd.read_excel("event_trace_sssp2025.xlsx")

# Helper: Jain's Fairness Index
def fairness_index(values):
    values = np.array(values)
    return (np.sum(values)**2) / (len(values) * np.sum(values**2) + 1e-9)

# === Graph 1: Latency vs PathCost ===
plt.figure()
plt.plot(ftp_sssp.index, ftp_sssp["Latency(Microseconds)"], label="FTP Latency")
plt.plot(cbr_sssp.index, cbr_sssp["Latency(Microseconds)"], label="CBR Latency")
plt.plot(ftp_sssp.index, ftp_sssp["PathCost"], label="FTP PathCost", linestyle="--")
plt.plot(cbr_sssp.index, cbr_sssp["PathCost"], label="CBR PathCost", linestyle="--")
plt.title("SSSP-2025 Latency vs PathCost")
plt.xlabel("Packet Index"); plt.ylabel("Latency / PathCost")
plt.legend(); plt.show()

# === Graph 2: Throughput Stability ===
plt.figure()
plt.plot(ftp_sssp.index, ftp_sssp["Throughput(Mbps)"], label="FTP Throughput")
plt.plot(cbr_sssp.index, cbr_sssp["Throughput(Mbps)"], label="CBR Throughput")
plt.plot(cbr_sssp.index, cbr_sssp["RelaxationCount"], label="Relaxation Count", linestyle="--")
plt.title("SSSP-2025 Throughput Stability")
plt.xlabel("Packet Index"); plt.ylabel("Throughput (Mbps)")
plt.legend(); plt.show()

# === Graph 3: Fairness Index Trend ===
ftp_fairness = [fairness_index(ftp_sssp["Throughput(Mbps)"][:i+1]) for i in range(len(ftp_sssp))]
cbr_fairness = [fairness_index(cbr_sssp["Throughput(Mbps)"][:i+1]) for i in range(len(cbr_sssp))]

plt.figure()
plt.plot(ftp_sssp.index, ftp_fairness, label="FTP Fairness")
plt.plot(cbr_sssp.index, cbr_fairness, label="CBR Fairness")
plt.plot(cbr_sssp.index, cbr_sssp["ConvergenceSteps"], label="Convergence Steps", linestyle="--")
plt.title("SSSP-2025 Fairness Trend")
plt.xlabel("Packet Index"); plt.ylabel("Fairness Index")
plt.legend(); plt.show()

# === Graph 4: Jitter Distribution (CBR) ===
plt.figure()
plt.hist(cbr_sssp["Jitter(Microseconds)"], bins=30, color="lightgreen", edgecolor="black")
plt.title("SSSP-2025 Jitter Distribution (CBR)")
plt.xlabel("Jitter (µs)"); plt.ylabel("Frequency")
plt.show()

# === Graph 5: Event Trace Recovery Dynamics ===
plt.figure()
plt.plot(event_sssp["Event_Time(µS)"], event_sssp["PathCost"], label="PathCost")
plt.plot(event_sssp["Event_Time(µS)"], event_sssp["RelaxationCount"], label="RelaxationCount")
plt.title("SSSP-2025 Event Trace Recovery Dynamics")
plt.xlabel("Event Time (µs)"); plt.ylabel("PathCost / Relaxations")
plt.legend(); plt.show()

# === Graph 6: Entropy Collapse Curve ===
latencies = ftp_sssp["Latency(Microseconds)"]
p = latencies / latencies.sum()
entropy = -np.sum(p * np.log1p(p))
plt.figure()
plt.plot(ftp_sssp.index, np.linspace(entropy, 0, len(ftp_sssp)), label="Entropy Collapse")
plt.title("SSSP-2025 Entropy Collapse")
plt.xlabel("Packet Index"); plt.ylabel("Entropy")
plt.legend(); plt.show()

# === Graph 7: Comparative Fingerprint Bar Chart ===
metrics = {
    "Fairness": np.mean(cbr_fairness),
    "Oscillations": np.sum(np.diff(cbr_sssp["Latency(Microseconds)"]) < 0),
    "RecoveryTime": np.max(cbr_sssp["Latency(Microseconds)"]) - np.mean(cbr_sssp["Latency(Microseconds)"]),
    "Entropy": entropy
}
plt.figure()
plt.bar(metrics.keys(), metrics.values(), color="blue")
plt.title("SSSP-2025 Fingerprint Summary")
plt.ylabel("Value")
plt.show()
