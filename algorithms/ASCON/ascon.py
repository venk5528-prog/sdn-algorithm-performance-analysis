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
plt.xlabel("Packet ID"); plt.ylabel("Jitter (µs)")
plt.show()

# Graph 4: Tamper Detection Timeline
plt.figure(figsize=(8,5))
plt.vlines(cbr_ascon['Packet ID'], ymin=0, ymax=cbr_ascon['TamperEvents'], color='blue')
plt.title("ASCON Tamper Detection Timeline")
plt.xlabel("Packet ID"); plt.ylabel("Tamper Events")
plt.show()

# Graph 5: Event Latency Timeline
plt.figure(figsize=(8,5))
plt.plot(event_ascon['Event ID'], event_ascon['Event Time (µs)'])
plt.title("ASCON Event Latency Timeline")
plt.xlabel("Event ID"); plt.ylabel("Event Time (µs)")
plt.show()

# Graph 6: Replay vs Tamper Correlation
plt.figure(figsize=(6,6))
plt.scatter(cbr_ascon['ReplayRejectCount'], cbr_ascon['TamperEvents'])
plt.title("ASCON Replay vs Tamper Correlation")
plt.xlabel("Replay Rejects"); plt.ylabel("Tamper Detected")
plt.show()

# Graph 7: Security Overhead vs Flow Size
plt.figure(figsize=(8,5))
plt.scatter(cbr_ascon['Packet or Segment size(Bytes)'], cbr_ascon['EncryptionLatency'])
plt.title("ASCON Security Overhead vs Flow Size")
plt.xlabel("Packet Size (Bytes)"); plt.ylabel("Encryption Latency (µs)")
plt.show()

# Graph 8: Radar Fingerprint
from math import pi
labels = ["Latency Overhead","Throughput Stability","Jitter Amplification",
          "Replay Resilience","Tamper Detection","Integrity Success"]
metrics = [ftp_ascon['EncryptionLatency'].mean(),
           cbr_ascon['Throughput(Mbps)'].mean(),
           cbr_ascon['Jitter(Microseconds)'].mean(),
           (1 - cbr_ascon['ReplayRejectCount'].mean()),  # resilience
           cbr_ascon['TamperEvents'].mean(),
           cbr_ascon['IntegrityCheck'].mean()]

angles = np.linspace(0, 2*np.pi, len(labels), endpoint=False).tolist()
metrics += metrics[:1]; angles += angles[:1]

fig, ax = plt.subplots(figsize=(6,6), subplot_kw=dict(polar=True))
ax.plot(angles, metrics, 'b-', linewidth=2)
ax.fill(angles, metrics, 'b', alpha=0.25)
ax.set_xticks(angles[:-1]); ax.set_xticklabels(labels)
plt.title("ASCON Fingerprint Radar Chart")
plt.show()

