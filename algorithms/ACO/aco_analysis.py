import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# Load ACO datasets
# -----------------------------
ftp_logs = pd.read_excel("FTP_LOGS.xlsx")
cbr_logs = pd.read_excel("CBR_LOGS.xlsx")  # assuming you have CBR logs in similar format

# -----------------------------
# 1. Latency Convergence (FTP + CBR)
# -----------------------------
plt.figure(figsize=(10,5))
plt.plot(ftp_logs['Packet ID'], ftp_logs['Latency(Microseconds)'], label="FTP Latency (µs)", color='blue')
plt.title("ACO Latency Convergence (FTP)")
plt.xlabel("Packet Index")
plt.ylabel("Latency (µs)")
plt.legend()
plt.show()

plt.figure(figsize=(10,5))
plt.plot(cbr_logs['Packet ID'], cbr_logs['Latency(Microseconds)'], label="CBR Latency (µs)", color='orange')
plt.title("ACO Latency Convergence (CBR)")
plt.xlabel("Packet Index")
plt.ylabel("Latency (µs)")
plt.legend()
plt.show()

# -----------------------------
# 2. Throughput Stability (FTP + CBR)
# -----------------------------
plt.figure(figsize=(10,5))
plt.plot(ftp_logs['Packet ID'], ftp_logs['Throughput(Mbps)'], label="FTP Throughput (Mbps)", color='green')
plt.title("ACO Throughput Stability (FTP)")
plt.xlabel("Packet Index")
plt.ylabel("Throughput (Mbps)")
plt.legend()
plt.show()

plt.figure(figsize=(10,5))
plt.plot(cbr_logs['Packet ID'], cbr_logs['Throughput(Mbps)'], label="CBR Throughput (Mbps)", color='red')
plt.title("ACO Throughput Stability (CBR)")
plt.xlabel("Packet Index")
plt.ylabel("Throughput (Mbps)")
plt.legend()
plt.show()


plt.figure(figsize=(8,5))
plt.hist(ftp_logs['Latency(Microseconds)'], bins=50, color='orange', alpha=0.7)
plt.title("ACO Latency Distribution (FTP)")
plt.xlabel("Latency (µs)")
plt.ylabel("Frequency")
plt.show()


ftp_logs['DeltaLatency'] = ftp_logs['Latency(Microseconds)'].diff()
plt.figure(figsize=(8,5))
plt.plot(ftp_logs['Packet ID'], ftp_logs['DeltaLatency'], label="Latency Differences", color='red')
plt.title("ACO Oscillation Pattern")
plt.xlabel("Packet Index")
plt.ylabel("Δ Latency")
plt.legend()
plt.show()


ftp_logs['JitterVariance'] = ftp_logs['Jitter(Microseconds)'].var()
cbr_logs['JitterVariance'] = cbr_logs['Jitter(Microseconds)'].var()

plt.figure(figsize=(10,5))
plt.plot(ftp_logs['Packet ID'], ftp_logs['Jitter(Microseconds)'].rolling(20).var(), label="FTP Jitter Variance", color='blue')
plt.plot(cbr_logs['Packet ID'], cbr_logs['Jitter(Microseconds)'].rolling(20).var(), label="CBR Jitter Variance", color='orange')
plt.title("ACO Exploration–Exploitation Oscillation")
plt.xlabel("Packet Index")
plt.ylabel("Jitter Variance")
plt.legend()
plt.show()


def fairness_index(x):
    return (np.sum(x)**2) / (len(x) * np.sum(x**2))

ftp_logs['Fairness'] = ftp_logs['Throughput(Mbps)'].rolling(20).apply(fairness_index)
cbr_logs['Fairness'] = cbr_logs['Throughput(Mbps)'].rolling(20).apply(fairness_index)

plt.figure(figsize=(10,5))
plt.plot(ftp_logs['Packet ID'], ftp_logs['Fairness'], label="FTP Fairness", color='orange')
plt.plot(cbr_logs['Packet ID'], cbr_logs['Fairness'], label="CBR Fairness", color='purple')
plt.title("Fairness Index Trend")
plt.xlabel("Time (ms)")
plt.ylabel("Fairness Index")
plt.legend()
plt.show()


plt.figure(figsize=(8,5))
plt.hist(cbr_logs['Jitter(Microseconds)'], bins=50, color='green', alpha=0.7)
plt.title("CBR Jitter Distribution")
plt.xlabel("Jitter (µs)")
plt.ylabel("Frequency")
plt.show()


ftp_logs['LatencyVariance'] = ftp_logs['Latency(Microseconds)'].rolling(20).var()
plt.figure(figsize=(10,5))
plt.plot(ftp_logs['Packet ID'], ftp_logs['LatencyVariance'], color='green')
plt.title("Recovery Dynamics (Variance Decay)")
plt.xlabel("Time (ms)")
plt.ylabel("Latency Variance")
plt.show()
