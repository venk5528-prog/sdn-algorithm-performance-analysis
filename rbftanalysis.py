import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from math import pi

# Load RBFT logs
ftp_rbft = pd.read_excel("FTP_LOGS_RBFT.xlsx")
cbr_rbft = pd.read_excel("CBR_LOGS_RBFT.xlsx")
event_rbft = pd.read_excel("EVENT_TRACE_RBFT.xlsx")

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
