import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# === Step 1: Load baseline logs ===
ftp_logs = pd.read_excel("FTP_LOGS.xlsx")
cbr_logs = pd.read_excel("CBRLOGS.xlsx")
event_logs = pd.read_excel("event_trace.xlsx")   # baseline event trace

# === Step 2: Add ASTAR-specific parameters ===
# HeuristicCost: derived from latency/event time
ftp_logs["HeuristicCost"] = np.log1p(ftp_logs["Latency(Microseconds)"])
cbr_logs["HeuristicCost"] = np.log1p(cbr_logs["Latency(Microseconds)"])
event_logs["HeuristicCost"] = np.log1p(event_logs["Event_Time(µS)"])

# ExpansionCount: proportional to jitter/event time
ftp_logs["ExpansionCount"] = (ftp_logs["Jitter(Microseconds)"] / 1000).astype(int)
cbr_logs["ExpansionCount"] = (cbr_logs["Jitter(Microseconds)"] / 1000).astype(int)
event_logs["ExpansionCount"] = (event_logs["Event_Time(µS)"] / 1e6).astype(int)

# SearchDepth: cumulative throughput/event time
ftp_logs["SearchDepth"] = np.cumsum(ftp_logs["Throughput(Mbps)"]) / 10
cbr_logs["SearchDepth"] = np.cumsum(cbr_logs["Throughput(Mbps)"]) / 10
event_logs["SearchDepth"] = np.cumsum(event_logs["Event_Time(µS)"]) / 1e7

# === Step 3: Save into new ASTAR files ===
ftp_logs.to_excel("ftp_astar.xlsx", index=False)
cbr_logs.to_excel("cbr_astar.xlsx", index=False)
event_logs.to_excel("event_trace_astar.xlsx", index=False)

# === Step 4: Reload updated ASTAR logs ===
ftp_astar = pd.read_excel("ftp_astar.xlsx")
cbr_astar = pd.read_excel("cbr_astar.xlsx")
event_astar = pd.read_excel("event_trace_astar.xlsx")

# === Step 5: Plot graphs ===

# Graph 1: Latency vs HeuristicCost
plt.figure()
plt.plot(ftp_astar.index, ftp_astar["Latency(Microseconds)"], label="FTP Latency")
plt.plot(cbr_astar.index, cbr_astar["Latency(Microseconds)"], label="CBR Latency")
plt.plot(ftp_astar.index, ftp_astar["HeuristicCost"], label="FTP HeuristicCost", linestyle="--")
plt.plot(cbr_astar.index, cbr_astar["HeuristicCost"], label="CBR HeuristicCost", linestyle="--")
plt.title("A* Latency vs HeuristicCost")
plt.xlabel("Packet Index"); plt.ylabel("Latency / HeuristicCost")
plt.legend(); plt.show()

# Graph 2: Throughput vs ExpansionCount
plt.figure()
plt.plot(ftp_astar.index, ftp_astar["Throughput(Mbps)"], label="FTP Throughput")
plt.plot(cbr_astar.index, cbr_astar["Throughput(Mbps)"], label="CBR Throughput")
plt.plot(ftp_astar.index, ftp_astar["ExpansionCount"], label="FTP ExpansionCount", linestyle="--")
plt.plot(cbr_astar.index, cbr_astar["ExpansionCount"], label="CBR ExpansionCount", linestyle="--")
plt.title("A* Throughput vs ExpansionCount")
plt.xlabel("Packet Index"); plt.ylabel("Throughput / ExpansionCount")
plt.legend(); plt.show()

# Graph 3: Fairness Index Trend with SearchDepth
def fairness_index(values):
    values = np.array(values)
    return (np.sum(values)**2) / (len(values) * np.sum(values**2) + 1e-9)

ftp_fairness = [fairness_index(ftp_astar["Throughput(Mbps)"][:i+1]) for i in range(len(ftp_astar))]
cbr_fairness = [fairness_index(cbr_astar["Throughput(Mbps)"][:i+1]) for i in range(len(cbr_astar))]

plt.figure()
plt.plot(ftp_astar.index, ftp_fairness, label="FTP Fairness")
plt.plot(cbr_astar.index, cbr_fairness, label="CBR Fairness")
plt.plot(ftp_astar.index, ftp_astar["SearchDepth"], label="FTP SearchDepth", linestyle="--")
plt.plot(cbr_astar.index, cbr_astar["SearchDepth"], label="CBR SearchDepth", linestyle="--")
plt.title("A* Fairness Trend with SearchDepth")
plt.xlabel("Packet Index"); plt.ylabel("Fairness / Depth")
plt.legend(); plt.show()

# Graph 4: Event Trace Recovery Dynamics
plt.figure()
plt.plot(event_astar["Event_Time(µS)"], event_astar["HeuristicCost"], label="HeuristicCost")
plt.plot(event_astar["Event_Time(µS)"], event_astar["ExpansionCount"], label="ExpansionCount")
plt.plot(event_astar["Event_Time(µS)"], event_astar["SearchDepth"], label="SearchDepth")
plt.title("A* Event Trace Recovery Dynamics")
plt.xlabel("Event Time (µs)"); plt.ylabel("ASTAR Metrics")
plt.legend(); plt.show()

