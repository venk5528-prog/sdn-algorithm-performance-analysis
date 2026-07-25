import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# === Load A* logs ===
ftp_astar = pd.read_excel("ftp_astar.xlsx")
cbr_astar = pd.read_excel("cbr_astar.xlsx")
event_astar = pd.read_excel("event_trace_astar.xlsx")  # once processed

# Helper: Jain's Fairness Index
def fairness_index(values):
    values = np.array(values)
    return (np.sum(values)**2) / (len(values) * np.sum(values**2) + 1e-9)

# === Graph 1: Latency vs HeuristicCost ===
plt.figure()
plt.plot(ftp_astar.index, ftp_astar["Latency(Microseconds)"], label="FTP Latency")
plt.plot(cbr_astar.index, cbr_astar["Latency(Microseconds)"], label="CBR Latency")
plt.plot(ftp_astar.index, ftp_astar["HeuristicCost"], label="FTP HeuristicCost", linestyle="--")
plt.plot(cbr_astar.index, cbr_astar["HeuristicCost"], label="CBR HeuristicCost", linestyle="--")
plt.title("A* Latency vs HeuristicCost")
plt.xlabel("Packet Index"); plt.ylabel("Latency / HeuristicCost")
plt.legend(); plt.show()

# === Graph 2: Throughput vs ExpansionCount ===
plt.figure()
plt.plot(ftp_astar.index, ftp_astar["Throughput(Mbps)"], label="FTP Throughput")
plt.plot(cbr_astar.index, cbr_astar["Throughput(Mbps)"], label="CBR Throughput")
plt.plot(cbr_astar.index, cbr_astar["ExpansionCount"], label="Expansion Count", linestyle="--")
plt.title("A* Throughput vs ExpansionCount")
plt.xlabel("Packet Index"); plt.ylabel("Throughput (Mbps)")
plt.legend(); plt.show()

# === Graph 3: Fairness Index Trend ===
ftp_fairness = [fairness_index(ftp_astar["Throughput(Mbps)"][:i+1]) for i in range(len(ftp_astar))]
cbr_fairness = [fairness_index(cbr_astar["Throughput(Mbps)"][:i+1]) for i in range(len(cbr_astar))]

plt.figure()
plt.plot(ftp_astar.index, ftp_fairness, label="FTP Fairness")
plt.plot(cbr_astar.index, cbr_fairness, label="CBR Fairness")
plt.plot(cbr_astar.index, cbr_astar["SearchDepth"], label="Search Depth", linestyle="--")
plt.title("A* Fairness Trend")
plt.xlabel("Packet Index"); plt.ylabel("Fairness Index")
plt.legend(); plt.show()

# === Graph 4: Jitter Distribution (CBR) ===
plt.figure()
plt.hist(cbr_astar["Jitter(Microseconds)"], bins=30, color="purple", edgecolor="black")
plt.title("A* Jitter Distribution (CBR)")
plt.xlabel("Jitter (µs)"); plt.ylabel("Frequency")
plt.show()

# === Graph 5: Event Trace Recovery Dynamics ===
plt.figure()
plt.plot(event_astar["Event_Time(µS)"], event_astar["HeuristicCost"], label="HeuristicCost")
plt.plot(event_astar["Event_Time(µS)"], event_astar["ExpansionCount"], label="ExpansionCount")
plt.title("A* Event Trace Recovery Dynamics")
plt.xlabel("Event Time (µs)"); plt.ylabel("Heuristic / Expansions")
plt.legend(); plt.show()

# === Graph 6: Entropy Collapse Curve ===
latencies = ftp_astar["Latency(Microseconds)"]
p = latencies / latencies.sum()
entropy = -np.sum(p * np.log1p(p))
plt.figure()
plt.plot(ftp_astar.index, np.linspace(entropy, 0, len(ftp_astar)), label="Entropy Collapse")
plt.title("A* Entropy Collapse")
plt.xlabel("Packet Index"); plt.ylabel("Entropy")
plt.legend(); plt.show()

# === Graph 7: Comparative Fingerprint Bar Chart ===
metrics = {
    "Fairness": np.mean(cbr_fairness),
    "Oscillations": np.sum(np.diff(cbr_astar["Latency(Microseconds)"]) < 0),
    "RecoveryTime": np.max(cbr_astar["Latency(Microseconds)"]) - np.mean(cbr_astar["Latency(Microseconds)"]),
    "Entropy": entropy
}
plt.figure()
plt.bar(metrics.keys(), metrics.values(), color="red")
plt.title("A* Fingerprint Summary")
plt.ylabel("Value")
plt.show()
