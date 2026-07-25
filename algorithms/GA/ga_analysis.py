import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# === Step 1: Load baseline logs ===
ftp_logs = pd.read_excel("FTP_LOGS.xlsx")
cbr_logs = pd.read_excel("CBRLOGS.xlsx")
event_logs = pd.read_excel("event_trace.xlsx")

# === Step 2: Add PSO-specific parameters ===
# Swarm Diversity: normalized jitter
ftp_logs["SwarmDiversity"] = ftp_logs["Jitter(Microseconds)"] / (ftp_logs["Jitter(Microseconds)"].max() + 1e-9)
cbr_logs["SwarmDiversity"] = cbr_logs["Jitter(Microseconds)"] / (cbr_logs["Jitter(Microseconds)"].max() + 1e-9)
event_logs["SwarmDiversity"] = np.sin(event_logs["Event_Time(µS)"] / 1e6)  # synthetic oscillation

# Fitness Variance: rolling variance of throughput
ftp_logs["FitnessVariance"] = ftp_logs["Throughput(Mbps)"].rolling(10).var()
cbr_logs["FitnessVariance"] = cbr_logs["Throughput(Mbps)"].rolling(10).var()
event_logs["FitnessVariance"] = event_logs["Event_Time(µS)"].rolling(10).var()

# Velocity Convergence: normalized latency differences
ftp_logs["VelocityConvergence"] = ftp_logs["Latency(Microseconds)"].diff().abs() / (ftp_logs["Latency(Microseconds)"].max() + 1e-9)
cbr_logs["VelocityConvergence"] = cbr_logs["Latency(Microseconds)"].diff().abs() / (cbr_logs["Latency(Microseconds)"].max() + 1e-9)
event_logs["VelocityConvergence"] = event_logs["Event_Time(µS)"].diff().abs() / (event_logs["Event_Time(µS)"].max() + 1e-9)

# Entropy Collapse: Shannon entropy of throughput distribution
def entropy(values):
    p = values / (np.sum(values) + 1e-9)
    return -np.sum(p * np.log1p(p))

ftp_logs["EntropyCollapse"] = entropy(ftp_logs["Throughput(Mbps)"])
cbr_logs["EntropyCollapse"] = entropy(cbr_logs["Throughput(Mbps)"])
event_logs["EntropyCollapse"] = entropy(event_logs["Event_Time(µS)"])

# === Step 3: Save into new PSO files ===
ftp_logs.to_excel("ftp_pso.xlsx", index=False)
cbr_logs.to_excel("cbr_pso.xlsx", index=False)
event_logs.to_excel("event_trace_pso.xlsx", index=False)

# === Step 4: Reload updated PSO logs ===
ftp_pso = pd.read_excel("ftp_pso.xlsx")
cbr_pso = pd.read_excel("cbr_pso.xlsx")
event_pso = pd.read_excel("event_trace_pso.xlsx")

# === Step 5: Plot graphs ===

# Graph 1: Swarm Diversity Curve
plt.figure()
plt.plot(ftp_pso.index, ftp_pso["SwarmDiversity"], label="FTP Swarm Diversity")
plt.plot(cbr_pso.index, cbr_pso["SwarmDiversity"], label="CBR Swarm Diversity")
plt.title("PSO Swarm Diversity Curve")
plt.xlabel("Packet Index"); plt.ylabel("Diversity")
plt.legend(); plt.show()

# Graph 2: Fitness Variance vs Event Time
plt.figure()
plt.plot(ftp_pso.index, ftp_pso["FitnessVariance"], label="FTP Fitness Variance")
plt.plot(cbr_pso.index, cbr_pso["FitnessVariance"], label="CBR Fitness Variance")
plt.title("PSO Fitness Variance Dynamics")
plt.xlabel("Packet Index"); plt.ylabel("Variance")
plt.legend(); plt.show()

# Graph 3: Velocity Convergence
plt.figure()
plt.plot(ftp_pso.index, ftp_pso["VelocityConvergence"], label="FTP Velocity Convergence")
plt.plot(cbr_pso.index, cbr_pso["VelocityConvergence"], label="CBR Velocity Convergence")
plt.title("PSO Velocity Convergence Curve")
plt.xlabel("Packet Index"); plt.ylabel("Convergence")
plt.legend(); plt.show()

# Graph 4: Entropy Collapse
plt.figure()
plt.plot(ftp_pso.index, ftp_pso["EntropyCollapse"], label="FTP Entropy Collapse")
plt.plot(cbr_pso.index, cbr_pso["EntropyCollapse"], label="CBR Entropy Collapse")
plt.title("PSO Entropy Collapse Curve")
plt.xlabel("Packet Index"); plt.ylabel("Entropy")
plt.legend(); plt.show()

# Graph 5: Event Trace PSO Metrics
plt.figure()
plt.plot(event_pso["Event_Time(µS)"], event_pso["SwarmDiversity"], label="Swarm Diversity")
plt.plot(event_pso["Event_Time(µS)"], event_pso["FitnessVariance"], label="Fitness Variance")
plt.plot(event_pso["Event_Time(µS)"], event_pso["VelocityConvergence"], label="Velocity Convergence")
plt.title("PSO Event Trace Metrics")
plt.xlabel("Event Time (µs)"); plt.ylabel("PSO Metrics")
plt.legend(); plt.show()
