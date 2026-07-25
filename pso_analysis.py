import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# Load PSO datasets
# -----------------------------
ftp_logs = pd.read_excel("ftp_pso.xlsx")
cbr_logs = pd.read_excel("cbr_pso.xlsx")

# -----------------------------
# 1. Fairness Index (FTP vs CBR)
# FI = (sum x_i)^2 / (n * sum x_i^2)
# -----------------------------
def fairness_index(x):
    return (np.sum(x)**2) / (len(x) * np.sum(x**2))

ftp_logs['Fairness'] = ftp_logs['Throughput(Mbps)'].rolling(10).apply(fairness_index)
cbr_logs['Fairness'] = cbr_logs['Throughput(Mbps)'].rolling(10).apply(fairness_index)

plt.figure(figsize=(8,5))
plt.plot(ftp_logs.index, ftp_logs['Fairness'], label="FTP Fairness (PSO)", color='orange')
plt.plot(cbr_logs.index, cbr_logs['Fairness'], label="CBR Fairness (PSO)", color='purple')
plt.title("Recomputed PSO Fairness Index Trend")
plt.xlabel("Window Index")
plt.ylabel("Fairness Index")
plt.legend()
plt.show()

# -----------------------------
# 2. Entropy Collapse (CBR)
# H = -sum(p_i log p_i)
# -----------------------------
def entropy(prob_dist):
    prob_dist = prob_dist[prob_dist > 0]
    return -np.sum(prob_dist * np.log(prob_dist))

cbr_entropy_series = cbr_logs['Latency(PSO)'].rolling(10).apply(
    lambda x: entropy(x / np.sum(x))
)

plt.figure(figsize=(8,5))
plt.plot(cbr_entropy_series.index, cbr_entropy_series, color='purple')
plt.title("PSO Entropy Collapse Curve")
plt.xlabel("Window Index")
plt.ylabel("Entropy")
plt.show()

# -----------------------------
# 3. Swarm Diversity Curve (FTP)
# -----------------------------
plt.figure(figsize=(8,5))
plt.plot(ftp_logs['Packet ID'], ftp_logs['SwarmDiversity'], color='blue')
plt.title("PSO Swarm Diversity Curve")
plt.xlabel("Event Time (µs)")
plt.ylabel("Swarm Diversity")
plt.show()

# -----------------------------
# 4. Velocity Convergence Curve (FTP)
# -----------------------------
plt.figure(figsize=(8,5))
plt.plot(ftp_logs['Packet ID'], ftp_logs['VelocityConvergence'], color='red')
plt.title("PSO Velocity Convergence Curve")
plt.xlabel("Event Time (µs)")
plt.ylabel("Velocity Convergence")
plt.show()

# -----------------------------
# 5. Recovery Dynamics (Fitness Variance vs Event Time)
# -----------------------------
plt.figure(figsize=(8,5))
plt.plot(ftp_logs['Packet ID'], ftp_logs['FitnessVariance'], color='green')
plt.title("PSO Recovery Dynamics (Fitness Variance vs Event Time)")
plt.xlabel("Event Time (µs)")
plt.ylabel("Fitness Variance")
plt.show()
