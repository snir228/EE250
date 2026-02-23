import matplotlib
matplotlib.use("Agg")   #required for rpi

import pandas as pd
import matplotlib.pyplot as plt
import sys

#obtains commanline arguments for distance
distance = sys.argv[1]

#load files
tcp = pd.read_csv(f"iperf_tcp_{distance}m.csv").tail(1)
udp = pd.read_csv(f"iperf_udp_{distance}m.csv").tail(1)

#organizes runs in list
runs = ["Run1", "Run2", "Run3", "Run4", "Run5"]

#extracts their values
tcp_vals = tcp[runs].values[0]
udp_vals = udp[runs].values[0]

#plot
plt.figure(figsize=(8,5)) #8 measurements on y axis, 4 on x axis

#tcp plot
plt.plot( #referenced image provided in manual
    runs,
    tcp_vals,
    marker='o',
    linestyle='-',
    color='orange',
    linewidth=2,
    label="TCP Throughput (Mbps)"
)
#udp plot on same graph
plt.plot(
    runs,
    udp_vals,
    marker='s',
    linestyle='--',
    color='orange',
    linewidth=2,
    label="UDP Throughput (Mbps)"
)

#identifying graph
plt.title(f"TCP & UDP Throughput at {distance}m Distance")
plt.xlabel("Test Runs")
plt.ylabel("Throughput (Mbps)")
plt.legend()

#save as png
plt.savefig(f"throughput_{distance}m.png")
