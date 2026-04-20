import tkinter as tk
from tkinter import scrolledtext
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import app
import process
import ssh_test


BG = "#5C89D2"
FG = "black"
FONT = "Futura"

root = tk.Tk()
root.title("")
root.configure(bg=BG)

label = tk.Label(root, text="Light-Aware Activity Suggestion", bg=BG, fg="white", font=(FONT, 20))
label.pack(pady = (20, 0))

# Outlined results box
output_frame = tk.LabelFrame(root, text="Results", bg=BG, fg="white", bd=2, labelanchor="n", font=(FONT, 15))
output_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# 3 graph placeholders
figs = []
canvases = []
for i in range(3):
    fig, ax = plt.subplots(figsize=(1.5, 1))
    ax.set_facecolor("#ffffff")
    fig.patch.set_facecolor("#ffffff")
    canvas = FigureCanvasTkAgg(fig, master=output_frame)
    canvas.get_tk_widget().grid(row=0, column=i, padx=5, pady=5)
    figs.append(fig)
    canvases.append(canvas)

# Processed data stats box
stats_frame = tk.LabelFrame(output_frame, text="Processed Data", bg=BG, fg="white", bd=2, labelanchor="n", font=(FONT, 15))
stats_frame.grid(row=1, column=0, columnspan=3, padx=5, pady=5, sticky="ew")

avg_label = tk.Label(stats_frame, text="Average Intensity: --", bg=BG, fg="white", font=(FONT, 15))
avg_label.grid(row=0, column=0, padx=10, pady=4)

var_label = tk.Label(stats_frame, text="Variance: --", bg=BG, fg="white", font=(FONT, 15))
var_label.grid(row=0, column=1, padx=10, pady=4)

trend_label = tk.Label(stats_frame, text="Trend: --", bg=BG, fg="white", font=(FONT, 15))
trend_label.grid(row=0, column=2, padx=10, pady=4)

for col in range(3):
     stats_frame.columnconfigure(col, weight=1)

# LLM response box
llm_box = scrolledtext.ScrolledText(output_frame, width=60, height=12,
                                     bg="white", fg="black", state=tk.DISABLED, font=(FONT, 15))
llm_box.grid(row=2, column=0, columnspan=3, padx=5, pady=5, sticky="ew")

def on_click1():
    avg_label.config  

def on_click2():
    llm_box.config(state=tk.NORMAL)
    llm_box.delete("1.0", tk.END)
    llm_box.insert(tk.END, "LLM response will appear here...")
    llm_box.config(state=tk.DISABLED)

btn = tk.Button(root, text="Process Light Intensity", bg=BG, fg="black",
                highlightbackground=BG, command=on_click1, font=(FONT, 15))
btn.pack()
btn = tk.Button(root, text="LLM Activity Suggestion", bg=BG, fg="black",
                highlightbackground=BG, command=on_click2, font=(FONT, 15))
btn.pack(pady=2)

root.mainloop()
