## Team Members
##- Steve Cho (USC ID: 4314516349)
##- Sivan Nir (USC ID: 7594069996)

import tkinter as tk
from tkinter import scrolledtext
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import csv, os
import get_data

BG   = "#5C89D2"
FG   = "white"
FONT = "Helvetica"
OUTPUT_DIR = "./rpi_output/output"

root = tk.Tk()
root.title("Light-Aware Activity Suggestion")
root.configure(bg=BG)

tk.Label(root, text="Light-Aware Activity Suggestion",
         bg=BG, fg=FG, font=(FONT, 20)).pack(pady=(20, 0))

output_frame = tk.LabelFrame(root, text="Results", bg=BG, fg=FG,
                              bd=2, labelanchor="n", font=(FONT, 15))
output_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# 3 graph slots
graph_slots = []
for i in range(3):
    fig, ax = plt.subplots(figsize=(2, 1.5))
    ax.set_facecolor("#1e1e1e")
    fig.patch.set_facecolor("#1e1e1e")
    canvas = FigureCanvasTkAgg(fig, master=output_frame)
    canvas.get_tk_widget().grid(row=0, column=i, padx=5, pady=5)
    graph_slots.append((fig, ax, canvas))

# stats row
stats_frame = tk.LabelFrame(output_frame, text="Processed Data", bg=BG, fg=FG,
                              bd=2, labelanchor="n", font=(FONT, 15))
stats_frame.grid(row=1, column=0, columnspan=3, padx=5, pady=5, sticky="ew")
avg_label   = tk.Label(stats_frame, text="Average Intensity: --", bg=BG, fg=FG, font=(FONT, 13))
var_label   = tk.Label(stats_frame, text="Variance: --",          bg=BG, fg=FG, font=(FONT, 13))
trend_label = tk.Label(stats_frame, text="Trend: --",             bg=BG, fg=FG, font=(FONT, 13))
avg_label.grid(row=0, column=0, padx=10, pady=4)
var_label.grid(row=0, column=1, padx=10, pady=4)
trend_label.grid(row=0, column=2, padx=10, pady=4)
for col in range(3):
    stats_frame.columnconfigure(col, weight=1)

# LLM response box
llm_box = scrolledtext.ScrolledText(output_frame, width=60, height=8,
                                     bg="#1e1e1e", fg="white",
                                     state=tk.DISABLED, font=(FONT, 12))
llm_box.grid(row=2, column=0, columnspan=3, padx=5, pady=5, sticky="ew")

def load_csv_stats():
    path = os.path.join(OUTPUT_DIR, "data.csv")
    avgs = []
    with open(path) as f:
        reader = csv.DictReader(f)
        for row in reader:
            avgs.append(float(row["average"]))
    mean     = sum(avgs) / len(avgs)
    variance = sum((x - mean)**2 for x in avgs) / len(avgs)
    trend    = "Increasing" if avgs[-1] > avgs[0] else ("Decreasing" if avgs[-1] < avgs[0] else "Stable")
    return round(mean, 2), round(variance, 2), trend

def load_graph(slot_index, filename):
    fig, ax, canvas = graph_slots[slot_index]
    ax.clear()
    img = mpimg.imread(os.path.join(OUTPUT_DIR, filename))
    ax.imshow(img)
    ax.axis("off")
    canvas.draw()

def on_process():
    # fetch data from RPi then display graphs and stats
    success = get_data.fetch()
    if not success:
        return
    load_graph(0, "left.png")
    load_graph(1, "right.png")
    load_graph(2, "avg.png")
    mean, variance, trend = load_csv_stats()
    avg_label.config(text=f"Average Intensity: {mean}")
    var_label.config(text=f"Variance: {variance}")
    trend_label.config(text=f"Trend: {trend}")

def on_llm():
    # placeholder - Sivan replaces this with LLM API call
    llm_box.config(state=tk.NORMAL)
    llm_box.delete("1.0", tk.END)
    llm_box.insert(tk.END, "LLM not yet connected.")
    llm_box.config(state=tk.DISABLED)

tk.Button(root, text="Process Light Intensity", bg="white", fg="black",
          font=(FONT, 13), command=on_process).pack(pady=(5, 2))
tk.Button(root, text="LLM Activity Suggestion", bg="white", fg="black",
          font=(FONT, 13), command=on_llm).pack(pady=(0, 10))

root.mainloop()
