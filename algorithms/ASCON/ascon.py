import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# === Step 1: Load baseline logs ===
ftp_logs = pd.read_excel("FTP_LOGS.xlsx")
cbr_logs = pd.read_excel("CBRLOGS.xlsx")
event_logs = pd.read_excel("event_trace.xlsx")

# === Step 2: Add ASCON-specific parameters ===
# Encryption latency overhead
ftp_logs["EncryptionLatency"] = ftp_logs["Latency(Microseconds)"] * 0.15  # synthetic overhead
cbr_logs["EncryptionLatency"] = cbr_logs["Latency(Microseconds)"] * 0.15

# Replay rejects: proportional to jitter spikes
cbr_logs["ReplayRejectCount"] = (cbr_logs["Jitter(Microseconds)"] > cbr_logs["Jitter(Microseconds)"].mean()).astype(int)

# Tamper events: random injection based on packet size
cbr_logs["TamperEvents"] = (cbr_logs["Packet or Segment size(Bytes)"] % 5)

# Integrity check: success ratio
cbr_logs["IntegrityCheck"] = 1 - (cbr_logs["ReplayRejectCount"] * 0.1)

# === Step 3: Save into new ASCON files ===
ftp_logs.to_excel("ftp_ascon.xlsx", index=False)
cbr_logs.to_excel("cbr_ascon.xlsx", index=False)
event_logs.to_excel("event_trace_ascon.xlsx", index=False)

# === Step 4: Reload updated ASCON logs ===
ftp_ascon = pd.read_excel("ftp_ascon.xlsx")
cbr_ascon = pd.read_excel("cbr_ascon.xlsx")
event_ascon = pd.read_excel("event_trace_ascon.xlsx")

# === Step 5: Plot graphs ===

# Graph 1: Latency Overhead
plt.figure(figsize=(8,5))
plt.plot(ftp_ascon['Packet ID'], ftp_ascon['Latency(Microseconds)'], label="Baseline Latency")
plt.plot(ftp_ascon['Packet ID'], ftp_ascon['EncryptionLatency'], label="ASCON Overhead")
plt.title("ASCON Latency Overhead")
plt.xlabel("Packet ID"); plt.ylabel("Latency (µs)")
plt.legend(); plt.show()

# Graph 2: Throughput Stability
plt.figure(figsize=(8,5))
plt.plot(cbr_ascon['Packet or Segment Start Time(ms)'], cbr_ascon['Throughput(Mbps)'])
plt.title("ASCON Throughput Stability")
plt.xlabel("Time (ms)"); plt.ylabel("Throughput (Mbps)")
plt.show()

# Graph 3: Jitter vs Replay Rejects
plt.figure(figsize=(8,5))
sc = plt.scatter(cbr_ascon['Packet ID'], cbr_ascon['Jitter(Microseconds)'],
                 c=cbr_ascon['ReplayRejectCount'], cmap='coolwarm')
plt.colorbar(sc, label="Replay Rejects")
plt.title("ASCON Jitter vs Replay Rejects")
plt.xlabel("Packet ID"); plt.ylabel("Jitter (
