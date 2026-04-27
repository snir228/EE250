import csv
import matplotlib.pyplot as plt

# Read csv
def load_csv(filepath="output/data.csv"):
    timestamps = []
    left       = []
    right      = []
    avg        = []
    with open(filepath) as f:
        reader = csv.DictReader(f)
        for row in reader:
            timestamps.append(float(row["timestamp"]))
            left.append(float(row["left"]))
            right.append(float(row["right"]))
            avg.append(float(row["average"]))
    return timestamps, left, right, avg

# Generate figure
# Help from Claude
def make_chart(timestamps, values, title, color):
    fig, ax = plt.subplots(figsize=(2, 1.5))
    ax.plot(timestamps, values, color=color)
    ax.set_title(title, color="black", fontsize=7)
    ax.set_xlabel("Time [s]", color="black", fontsize=6)
    ax.set_ylabel("Light Intensity (0-1023)", color="black", fontsize=6)
    ax.tick_params(colors="black", labelsize=5)
    for spine in ax.spines.values():
        spine.set_edgecolor("black")
    ax.set_facecolor("white")
    fig.patch.set_facecolor("white")
    fig.tight_layout()
    return fig

# Return the average data
def get_avg(filepath="output/data.csv"):
    _, _, _, avg = load_csv(filepath)
    return avg

# Return 3 figures
def generate_graphs(filepath="output/data.csv"):
    timestamps, left, right, avg = load_csv(filepath)
    fig1 = make_chart(timestamps, left,  "Left Sensor",  "steelblue")
    fig2 = make_chart(timestamps, right, "Right Sensor", "coral")
    fig3 = make_chart(timestamps, avg,   "Average Intensity", "mediumseagreen")
    return fig1, fig2, fig3
