import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from math import pi

# === Step 1: Load baseline logs ===
ftp_logs = pd.read_excel("FTP_LOGS.xlsx")
cbr_logs = pd.read_excel("CBRLOGS.xlsx")
event_logs = pd.read_excel("event_trace.xlsx")

# === Step 2: Add RBFT-specific parameters ===
# FaultCount: synthetic proportional to jitter
ftp_logs["FaultCount"] = (ftp_logs["Jitter(Microseconds)"] / 1000).astype(int)
cbr_logs["FaultCount"] = (cbr_logs["Jitter(Microseconds)"] / 1000).astype(int)
event_logs["FaultCount"] = (event_logs["Event_Time(µS)"] / 1e6).astype(int)

# RecoverySteps: cumulative latency trend
ftp_logs["RecoverySteps"] = np.cumsum(ftp_logs["Latency(Microseconds)"]) / 1e6
cbr_logs["RecoverySteps"] = np.cumsum(cbr_logs["Latency(Microseconds)"]) / 1e6
event_logs["RecoverySteps"] = np.cumsum(event_logs["Event_Time(µS)"]) / 1e7

# RuleTrigger: assign based on thresholds
ftp_logs["RuleTrigger"] = np.where(ftp_logs["Throughput(Mbps)"] > ftp_logs["Throughput(Mbps)"].mean(), "RuleA", "RuleB")
cbr_logs["RuleTrigger"] = np.where(cbr_logs["Throughput(Mbps)"] > cbr_logs["Throughput(Mbps)"].mean(), "RuleX", "RuleY")
event_logs["RuleTrigger"] = np.where(event_logs["Event_Time(µS)"] % 2 == 0, "RuleZ", "RuleY")

# ResilienceScore: normalized throughput
ftp_logs["ResilienceScore"] = ftp_logs["Throughput(Mbps)"] / (ftp_logs["Throughput(Mbps)"].max() + 1e-9)
cbr_logs["ResilienceScore"] = cbr_logs["Throughput(Mbps)"] / (cbr_logs["Throughput(Mbps)"].max() + 1e-9)
event_logs["ResilienceScore"] = event_logs["Event_Time(µS)"] / (event_logs["Event_Time(µS)"].max() + 1e-9)

# === Step 3: Save into new RBFT files ===
ftp_logs.to_excel("ftp_rbft.xlsx", index=False)
cbr_logs.to_excel("cbr_rbft.xlsx", index=False)
event_logs.to_excel("event_trace_rbft.xlsx", index=False)

# === Step 4: Reload updated RBFT logs ===
ftp_rbft = pd.read_excel("ftp_rbft.xlsx")
cbr_rbft = pd.read_excel("cbr_rbft.xlsx")
event_rbft = pd.read_excel("event_trace_rbft.xlsx")

# === Step 5: Plot graphs ===

# 1. Latency vs FaultCount (FTP)
plt.figure()
plt.scatter(ftp_rbft["Packet ID"], ftp_rbft["Latency(Microseconds)"], 
            c=ftp_rbft["FaultCount"], cmap="coolwarm")
plt.xlabel("Packet ID"); plt.ylabel("Latency (µs)")
plt.title("RBFT Latency vs FaultCount"); plt.colorbar(label="FaultCount")

# 2. Throughput vs RecoverySteps (FTP)
plt.figure()
plt.scatter(ftp_rbft["RecoverySteps"], ftp_rbft["Throughput(Mbps)"])
plt.xlabel("Recovery Steps"); plt.ylabel("Throughput (Mbps)")
plt.title("RBFT Throughput vs RecoverySteps"); plt.grid(True)

# 3. ResilienceScore Timeline (FTP)
plt.figure()
plt.plot(ftp_rbft["Packet ID"], ftp_rbft["ResilienceScore"])
plt.xlabel("Packet ID"); plt.ylabel("Resilience Score")
plt.title("RBFT ResilienceScore Timeline"); plt.grid(True)

# 4. RuleTrigger Distribution (FTP)
ftp_rbft["RuleTrigger"].value_counts().plot(kind="bar", figsize=(8,5))
plt.title("RBFT RuleTrigger Distribution (FTP)")

# 5. Jitter vs FaultCount (CBR)
plt.figure()
plt.scatter(cbr_rbft["Packet ID"], cbr_rbft["Jitter(Microseconds)"], 
            c=cbr_rbft["FaultCount"], cmap="viridis")
plt.xlabel("Packet ID"); plt.ylabel("Jitter (µs)")
plt.title("RBFT Jitter vs FaultCount"); plt.colorbar(label="FaultCount")

# 6. RecoverySteps vs Latency (CBR)
plt.figure()
plt.scatter(cbr_rbft["RecoverySteps"], cbr_rbft["Latency(Microseconds)"])
plt.xlabel("Recovery Steps"); plt.ylabel("Latency (µs)")
plt.title("RBFT RecoverySteps vs Latency"); plt.grid(True)

# 7. ResilienceScore vs Throughput (CBR)
plt.figure()
plt.scatter(cbr_rbft["ResilienceScore"], cbr_rbft["Throughput(Mbps)"])
plt.xlabel("Resilience Score"); plt.ylabel("Throughput (Mbps)")
plt.title("RBFT Resilience vs Throughput"); plt.grid(True)

# 8. RuleTrigger Distribution (CBR)
cbr_rbft["RuleTrigger"].value_counts().plot(kind="bar", figsize=(8,5))
plt.title("RBFT RuleTrigger Distribution (CBR)")

# 9. Event Latency vs FaultCount (Event Trace)
plt.figure()
plt.scatter(event_rbft["Event_Id"], event_rbft["Event_Time(µS)"], 
            c=event_rbft["FaultCount"], cmap="plasma")
plt.xlabel("Event ID"); plt.ylabel("Event Time (µs)")
plt.title("RBFT Event Latency vs FaultCount"); plt.colorbar(label="FaultCount")

# 10. Radar Chart Summary
labels = ["Latency","Throughput","Jitter","FaultCount","RecoverySteps","ResilienceScore"]
values = [ftp_rbft["Latency(Microseconds)"].mean(),
          ftp_rbft["Throughput(Mbps)"].mean(),
          cbr_rbft["Jitter(Microseconds)"].mean(),
          ftp_rbft["FaultCount"].mean(),
          ftp_rbft["RecoverySteps"].mean(),
          ftp_rbft["ResilienceScore"].mean()]

angles = np.linspace(0, 2*pi, len(labels), endpoint=False).tolist()
values += values[:1]; angles += angles[:1]

plt.figure(figsize=(6,6))
ax = plt.subplot(111, polar=True)
ax.plot(angles, values, 'o-', linewidth=2)
ax.fill(angles, values, alpha=0.25)
ax.set_thetagrids(np.degrees(angles[:-1]), labels)
plt.title("RBFT Fingerprint Radar Chart")
plt.show()

