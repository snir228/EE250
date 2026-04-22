import tkinter as tk
from tkinter import scrolledtext, simpledialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from ssh import fetch
from openai import OpenAI
import calculation
import process
import weather
import os

BG = "#5C89D2" # UI Window Background Color
FG = "white" # UI Window Foreground Color
FONT = "URW Gothic" # Font used in the window

root = tk.Tk() # Root window creation
root.title("") # Title of the window
root.configure(bg=BG) # Set the background color to BG

# Title of the Application on top of the window
label = tk.Label(root, text="LLM-based Environment-Aware Activity Suggestion", bg=BG, fg=FG, font=(FONT, 20))
label.pack(pady = (20, 0))

# Outlined Graphs Section
output_frame = tk.LabelFrame(root, text="Light Intensity Graphs", bg=BG, fg=FG, bd=2, labelanchor="n", font=(FONT, 15))
output_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

for col in range(3):
    output_frame.columnconfigure(col, weight=1) # Control graph stretch horizontally
output_frame.rowconfigure(0, weight=1) # Control graph stretch vertically
output_frame.rowconfigure(2, weight=1) # Control textbox stretch vertically

# 3 Graphs Placeholders
canvases = []
for i in range(3):
    fig, ax = plt.subplots(figsize=(2, 1.5))
    ax.axis("off")
    canvas = FigureCanvasTkAgg(fig, master=output_frame)
    canvas.get_tk_widget().grid(row=0, column=i, padx=5, pady=5, sticky="nsew")
    canvases.append(canvas)

# Processed data stats box
stats_frame = tk.LabelFrame(output_frame, text="Processed Data", bg=BG, fg=FG, bd=2, labelanchor="n", font=(FONT, 15))
stats_frame.grid(row=1, column=0, columnspan=3, padx=5, pady=5, sticky="ew")

avg_label = tk.Label(stats_frame, text="Average Intensity: --", bg=BG, fg=FG, font=(FONT, 15))
avg_label.grid(row=0, column=0, padx=10, pady=4)

light_label = tk.Label(stats_frame, text="Light Level: --", bg=BG, fg=FG, font=(FONT, 15))
light_label.grid(row=0, column=1, padx=10, pady=4)

trend_label = tk.Label(stats_frame, text="Trend: --", bg=BG, fg=FG, font=(FONT, 15))
trend_label.grid(row=0, column=2, padx=10, pady=4)

for col in range(3):
     stats_frame.columnconfigure(col, weight=1) # Stretches the data stats box horizontally

# Text box section
text_box = scrolledtext.ScrolledText(output_frame, width=60, height=12,
                                     bg="white", fg="black", state=tk.DISABLED, font=(FONT, 15)) # Add scrolling functionality
text_box.grid(row=2, column=0, columnspan=3, padx=5, pady=5, sticky="nsew")

# Processes light by sshing to the RPI and collecting the light intensity data. It then uses that data to calculate
# various data like average, light level, and trend as well as the graphs for each light sensor + average of the two
def process_light():
    if fetch():
        fig1, fig2, fig3 = process.generate_graphs("./rpi_output/data.csv")
        avg_data = process.get_avg("./rpi_output/data.csv")

        figures = [fig1, fig2, fig3]
        for i in range(3):
            canvases[i].figure = figures[i]
            canvases[i].draw()

        # average and trend calculation
        avg_val   = calculation.get_average(avg_data)
        trend_val = calculation.get_trend(avg_data)

        # light condition depending on threshold
        if avg_val > 0 and avg_val < 100:
            light_cond = "Very Dark"
        elif avg_val > 101 and avg_val < 250:
            light_cond = "Dark"
        elif avg_val > 251 and avg_val < 500:
            light_cond = "Moderate"
        elif avg_val > 501 and avg_val < 750:
            light_cond = "Bright"
        else:
            light_cond = "Very Bright"
        
        # insert to the processed data section
        avg_label.config(text=f"Average Intensity: {avg_val:.2f}")
        light_label.config(text=f"Light Level: {light_cond}")
        trend_label.config(text=f"Trend: {trend_val}")

        # insert text to the textbox
        text_box.config(state=tk.NORMAL)
        text_box.delete("1.0", tk.END)
        text_box.insert(tk.END, "Data Extraction Successful!")
        text_box.config(state=tk.DISABLED)
    else:
        text_box.config(state=tk.NORMAL)
        text_box.delete("1.0", tk.END)
        text_box.insert(tk.END, "Data Extraction Failed")
        text_box.config(state=tk.DISABLED)
        
# Once the data is processed, it prompts where the user is: 'inside' or 'outside'. After, relevant information
# like average, variance, trend, weather data along with the prompt is given to the LLM where the LLM provides
# activity suggestion based on that prompt
def llm_suggestions():

    # checks whether the data exists
    if not os.path.exists("./rpi_output/data.csv"):
        text_box.config(state=tk.NORMAL)
        text_box.delete("1.0", tk.END)
        text_box.insert(tk.END, "Please press 'Process Light Intensity' before asking for suggestions.")
        text_box.config(state=tk.DISABLED)
        return

    # location prompt
    user_setting = simpledialog.askstring("Location", "Are you currently inside or outside?", parent=root)
    if not user_setting:
        return

    # obtain average data
    avg_data = process.get_avg("./rpi_output/data.csv")

    text_box.config(state=tk.NORMAL)
    text_box.delete("1.0", tk.END)
    text_box.insert(tk.END, "LLM is thinking...")
    text_box.config(state=tk.DISABLED)
    root.update()

    # use average data to calculate average value, variance, and trend
    avg_val   = calculation.get_average(avg_data)
    var_val   = calculation.get_variance(avg_data)
    trend_val = calculation.get_trend(avg_data)

    # get current user location
    city = weather.get_current_location()
    if not city:
        text_box.config(state=tk.NORMAL)
        text_box.delete("1.0", tk.END)
        text_box.insert(tk.END, "Failed to retrieve location.")
        text_box.config(state=tk.DISABLED)
        return
    
    # get current weather using the location via weather api
    weather_result = weather.get_weather(city)
    if not weather_result:
        text_box.config(state=tk.NORMAL)
        text_box.delete("1.0", tk.END)
        text_box.insert(tk.END, "Failed to retrieve weather data.")
        text_box.config(state=tk.DISABLED)
        return

    temp_f, feelslike_f, weather_cond, visibility = weather_result

    with open("./rpi_output/data.csv") as f:
        csv_data = f.read()

    # Prompt with the relevant informations given to the LLM (ChatGPT)
    prompt = f"""You are an activity advisor based on light-intensity and weather. Based on the following light sensor readings and weather condition, suggest activities.

User Location: {user_setting}

Light Sensor Data:
- Average Intensity: {avg_val:.2f} (scale 0-500)
- Variance: {var_val:.2f}
- Trend: {trend_val}

Raw sensor readings (timestamp, left sensor, right sensor, average):
{csv_data}

Weather Data:
- Current Temperature: {temp_f}
- Feels Like Temperature: {feelslike_f}
- Weather Condition: {weather_cond}
- Visibility: {visibility}

Respond in exactly this format if indoor:

CURRENT LIGHT INTENSITY LEVEL:
- (describe the light intensity)

INDOOR RECOMMENDED:
- (list activities suitable for this light intensity indoors)

INDOOR NOT RECOMMENDED:
- (list activities not suitable for this light intensity indoors)

INDOOR ADJUSTMENT ADVICE:
- (advise whether to raise or lower indoor light intensity for activites you mentioned 
for not recommended and by how much)

OVERALL RECOMMENDATION:
- (Give the most optimal activity based on light intensity and reason)


Respond in exactly this format if outdoor:

CURRENT WEATHER CONDITION:
- (describe how the weather condition is)

OUTDOOR RECOMMENDED:
- (list activities suitable for this weather outdoors)

OUTDOOR NOT RECOMMENDED:
- (list activities not suitable for this weather outdoors)

OUTDOOR ADJUSTMENT ADVICE:
- (advise what the user can do to do activites you mentioned for not recommended)

OVERALL RECOMMENDATION:
- (Give the most optimal activity based on weather condition and reason)
"""
    # API call to openai to receive response
    client = OpenAI(api_key="key")
    response = client.responses.create(model="gpt-4o", input=prompt)

    text_box.config(state=tk.NORMAL)
    text_box.delete("1.0", tk.END)
    text_box.insert(tk.END, response.output_text)
    text_box.config(state=tk.DISABLED)

# Button Configuration
btn = tk.Button(root, text="Process Light Intensity", bg="white", fg="black",
                highlightbackground="white", command=process_light, font=(FONT, 15))
btn.pack()
btn = tk.Button(root, text="LLM Activity Suggestion", bg="white", fg="black",
                highlightbackground="white", command=llm_suggestions, font=(FONT, 15))
btn.pack(pady=2)

# Ensure the window stays opened
root.mainloop()