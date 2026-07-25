import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# Load ASCON datasets
# -----------------------------
ftp_logs = pd.read_excel("FTP_LOGS_ASCON.xlsx")
cbr_logs = pd.read_excel("CBR_LOGS_ASCON.xlsx")
event_trace = pd.read_excel("EVENT_TRACE_ASCON.xlsx")  # once processed

# -----------------------------
# 1. Latency Overhead
# -----------------------------
plt.figure(figsize=(8,5))
plt.plot(ftp_logs['Packet ID'], ftp_logs['Latency(Microseconds)'], label="Baseline Latency")
plt.plot(ftp_logs['Packet ID'], ftp_logs['EncryptionLatency'], label="ASCON Overhead")
plt.title("ASCON Latency Overhead")
plt.xlabel("Packet ID")
plt.ylabel("Latency (µs)")
plt.legend()
plt.show()

# -----------------------------
# 2. Throughput Stability
# -----------------------------
plt.figure(figsize=(8,5))
plt.plot(cbr_logs['Packet or Segment Start Time(ms)'], cbr_logs['Throughput(Mbps)'])
plt.title("ASCON Throughput Stability")
plt.xlabel("Time (ms)")
plt.ylabel("Throughput (Mbps)")
plt.show()

# -----------------------------
# 3. Jitter vs Replay Rejects
# -----------------------------
plt.figure(figsize=(8,5))
sc = plt.scatter(cbr_logs['Packet ID'], cbr_logs['Jitter(Microseconds)'],
                 c=cbr_logs['ReplayRejectCount'], cmap='coolwarm')
plt.colorbar(sc, label="Replay Rejects")
plt.title("ASCON Jitter vs Replay Rejects")
plt.xlabel("Packet ID")
plt.ylabel("Jitter (µs)")
plt.show()

# -----------------------------
# 4. Tamper Detection Timeline
# -----------------------------
plt.figure(figsize=(8,5))
plt.vlines(cbr_logs['Packet ID'], ymin=0, ymax=cbr_logs['TamperEvents'], color='blue')
plt.title("ASCON Tamper Detection Timeline")
plt.xlabel("Packet ID")
plt.ylabel("Tamper Events")
plt.show()

# -----------------------------
# 5. Event Latency Timeline
# -----------------------------
plt.figure(figsize=(8,5))
plt.plot(event_trace['Event ID'], event_trace['Event Time (µs)'])
plt.title("ASCON Event Latency Timeline")
plt.xlabel("Event ID")
plt.ylabel("Event Time (µs)")
plt.show()

# -----------------------------
# 6. Replay vs Tamper Correlation
# -----------------------------
plt.figure(figsize=(6,6))
plt.scatter(cbr_logs['ReplayRejectCount'], cbr_logs['TamperEvents'])
plt.title("ASCON Replay vs Tamper Correlation")
plt.xlabel("Replay Rejects")
plt.ylabel("Tamper Detected")
plt.show()

# -----------------------------
# 7. Security Overhead vs Flow Size
# -----------------------------
plt.figure(figsize=(8,5))
plt.scatter(cbr_logs['Packet or Segment size(Bytes)'], cbr_logs['EncryptionLatency'])
plt.title("ASCON Security Overhead vs Flow Size")
plt.xlabel("Packet Size (Bytes)")
plt.ylabel("Encryption Latency (µs)")
plt.show()

# -----------------------------
# 8. Radar Fingerprint (aggregate metrics)
# -----------------------------
from math import pi

labels = ["Latency Overhead","Throughput Stability","Jitter Amplification",
          "Replay Resilience","Tamper Detection","Integrity Success"]
metrics = [ftp_logs['EncryptionLatency'].mean(),
           cbr_logs['Throughput(Mbps)'].mean(),
           cbr_logs['Jitter(Microseconds)'].mean(),
           (1 - cbr_logs['ReplayRejectCount'].mean()),  # resilience
           cbr_logs['TamperEvents'].mean(),
           cbr_logs['IntegrityCheck'].mean()]

angles = np.linspace(0, 2*np.pi, len(labels), endpoint=False).tolist()
metrics += metrics[:1]
angles += angles[:1]

fig, ax = plt.subplots(figsize=(6,6), subplot_kw=dict(polar=True))
ax.plot(angles, metrics, 'b-', linewidth=2)
ax.fill(angles, metrics, 'b', alpha=0.25)
ax.set_xticks(angles[:-1])
ax.set_xticklabels(labels)
plt.title("ASCON Fingerprint Radar Chart")
plt.show()
