## Team Members
##- Steve Cho (USC ID: 4314516349)
##- Sivan Nir (USC ID: 7594069996)
import time
import RPi.GPIO as GPIO
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

GPIO.setmode(GPIO.BOARD)
chan_list = [11]
GPIO.setup(chan_list, GPIO.OUT)

SPI_PORT   = 0
SPI_DEVICE = 0
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

lux_threshold  = 500  # fixed typo: was lux_treshold
sample_interval = 0.1
num_samples     = 50

def collect_data():
  left_value  = []   # fixed: was overwritten in the loop
  right_value = []
  avg_value   = []
  timestamps  = []
  for i in range(num_samples):
    left  = mcp.read_adc(0)   # fixed: single reading, not the list
    right = mcp.read_adc(1)
    avg   = (left + right) / 2
    left_value.append(left)   # fixed: append to the list
    right_value.append(right)
    avg_value.append(avg)
    timestamps.append(round(i * sample_interval, 2))
    if left > lux_threshold or right > lux_threshold:
      GPIO.output(chan_list, GPIO.HIGH)
    else:
      GPIO.output(chan_list, GPIO.LOW)
    time.sleep(sample_interval)
  GPIO.output(chan_list, GPIO.LOW)
  return left_value, right_value, avg_value, timestamps  # fixed: return the lists

def charts(timestamps, values, title, color):
  fig, ax = plt.subplots(figsize=(2, 1.5))
  ax.plot(timestamps, values, color=color)
  ax.set_title(title, color="white", fontsize=7)
  ax.set_xlabel("Time [s]", color="white", fontsize=6)
  ax.set_ylabel("ADC Value", color="white", fontsize=6)
  ax.tick_params(colors="white", labelsize=5)  # fixed: was ticks_params, colors not color
  for spine in ax.spines.values():
    spine.set_edgecolor("white")
  ax.set_facecolor("#1e1e1e")
  fig.patch.set_facecolor("#1e1e1e")
  fig.tight_layout()  # fixed: was missing ()
  return fig

def run():
  left_value, right_value, avg_value, timestamps = collect_data()
  fig1 = charts(timestamps, left_value,  "Left Sensor (J2)",  "steelblue")
  fig2 = charts(timestamps, right_value, "Right Sensor (J3)", "coral")
  fig3 = charts(timestamps, avg_value,   "Average Intensity", "mediumseagreen")
  llm_text = "LLM response"
  return fig1, fig2, fig3, llm_text, left_value, right_value, avg_value  # fixed: was left_data etc

if __name__ == "__main__":
  fig1, fig2, fig3, llm_text, left_data, right_data, avg_data = run()
  print("Left:    ", left_data)
  print("Right:   ", right_data)
  print("Average: ", avg_data)   # fixed: was avg+data
  GPIO.cleanup()
