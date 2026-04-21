import tkinter as tk
from tkinter import scrolledtext
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from ssh import fetch
from openai import OpenAI
import calculation
import process


BG = "#5C89D2"
FG = "black"
FONT = "URW Gothic"

root = tk.Tk()
root.title("")
root.configure(bg=BG)

label = tk.Label(root, text="LLM-based Light-Aware Activity Suggestion", bg=BG, fg="white", font=(FONT, 20))
label.pack(pady = (20, 0))

# Outlined results box
output_frame = tk.LabelFrame(root, text="Light Intensity Graphs", bg=BG, fg="white", bd=2, labelanchor="n", font=(FONT, 15))
output_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

for col in range(3):
    output_frame.columnconfigure(col, weight=1)
output_frame.rowconfigure(0, weight=1)
output_frame.rowconfigure(2, weight=1)

# 3 graph placeholders
canvases = []
for i in range(3):
    fig, ax = plt.subplots(figsize=(2, 1.5))
    ax.set_facecolor("white")
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)
    fig.patch.set_facecolor("white")
    canvas = FigureCanvasTkAgg(fig, master=output_frame)
    canvas.get_tk_widget().grid(row=0, column=i, padx=5, pady=5, sticky="nsew")
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

# Text box
text_box = scrolledtext.ScrolledText(output_frame, width=60, height=12,
                                     bg="white", fg="black", state=tk.DISABLED, font=(FONT, 15))
text_box.grid(row=2, column=0, columnspan=3, padx=5, pady=5, sticky="nsew")

def process_light():
    fig1, fig2, fig3, _, _, avg_data = process.generate_graphs("./rpi_output/data.csv")

    for canvas, new_fig in zip(canvases, [fig1, fig2, fig3]):
        canvas.figure = new_fig
        canvas.draw()

    avg_val   = calculation.get_average(avg_data)
    var_val   = calculation.get_variance(avg_data)
    trend_val = calculation.get_trend(avg_data)

    avg_label.config(text=f"Average Intensity: {avg_val:.2f}")
    var_label.config(text=f"Variance: {var_val:.2f}")
    trend_label.config(text=f"Trend: {trend_val}")

    text_box.config(state=tk.NORMAL)
    text_box.delete("1.0", tk.END)
    text_box.insert(tk.END, "Data Extraction Successful!")
    text_box.config(state=tk.DISABLED)
#     if fetch():
#         with open("./rpi_output/data.csv") as f:
#             reader = csv.DictReader(f)
#             rows = list(reader)
#         avg_data = [float(r["avg"]) for r in rows]

#         avg_val  = calculation.get_average(avg_data)
#         var_val  = calculation.get_variance(avg_data)
#         trend_val = calculation.get_trend(avg_data)

#         avg_label.config(text=f"Average Intensity: {avg_val:.2f}")
#         var_label.config(text=f"Variance: {var_val:.2f}")
#         trend_label.config(text=f"Trend: {trend_val}")

#         text_box.config(state=tk.NORMAL)
#         text_box.delete("1.0", tk.END)
#         text_box.insert(tk.END, "Data Extraction Successful")
#         text_box.config(state=tk.DISABLED)
#     else:
#         text_box.config(state=tk.NORMAL)
#         text_box.delete("1.0", tk.END)
#         text_box.insert(tk.END, "Data Extraction Failed")
#         text_box.config(state=tk.DISABLED)
        

def llm_suggestions():
    import os
    if not os.path.exists("./rpi_output/data.csv"):
        text_box.config(state=tk.NORMAL)
        text_box.delete("1.0", tk.END)
        text_box.insert(tk.END, "Please press 'Process Light Intensity' before asking for suggestions.")
        text_box.config(state=tk.DISABLED)
        return

    fig1, fig2, fig3, left_data, right_data, avg_data = process.generate_graphs("./rpi_output/data.csv")
    
    text_box.config(state=tk.NORMAL)
    text_box.delete("1.0", tk.END)
    text_box.insert(tk.END, "LLM is thinking...")
    text_box.config(state=tk.DISABLED)
    root.update()

    avg_val   = calculation.get_average(avg_data)
    var_val   = calculation.get_variance(avg_data)
    trend_val = calculation.get_trend(avg_data)

    with open("./rpi_output/data.csv") as f:
        csv_data = f.read()

    prompt = f"""You are a light-aware activity advisor. Based on the following light sensor readings, suggest activities.

Light Sensor Data:
- Average Intensity: {avg_val:.2f} (scale 0-500)
- Variance: {var_val:.2f}
- Trend: {trend_val}

Raw sensor readings (timestamp, left sensor, right sensor, average):
{csv_data}

Respond in exactly this format:

INDOOR RECOMMENDED:
- (list activities suitable for this light level indoors)

INDOOR NOT RECOMMENDED:
- (list activities not suitable for this light level indoors)

INDOOR LIGHT ADJUSTMENT ADVICE:
- (advise whether to raise or lower indoor lighting for activites you mentioned 
for not recommended and by how much)

OUTDOOR RECOMMENDED:
- (list activities suitable for this light level outdoors)

OUTDOOR NOT RECOMMENDED:
- (list activities not suitable for this light level outdoors)

OUTDOOR LIGHT ADJUSTMENT ADVICE:
- (advise whether to raise or lower indoor lighting for activites you mentioned 
for not recommended and by how much)"""

    client = OpenAI(api_key="KEY")
    response = client.responses.create(model="gpt-4o", input=prompt)

    text_box.config(state=tk.NORMAL)
    text_box.delete("1.0", tk.END)
    text_box.insert(tk.END, response.output_text)
    text_box.config(state=tk.DISABLED)

btn = tk.Button(root, text="Process Light Intensity", bg="white", fg="black",
                highlightbackground="white", command=process_light, font=(FONT, 15))
btn.pack()
btn = tk.Button(root, text="LLM Activity Suggestion", bg="white", fg="black",
                highlightbackground="white", command=llm_suggestions, font=(FONT, 15))
btn.pack(pady=2)

root.mainloop()