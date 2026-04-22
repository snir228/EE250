import time
# import RPi.GPIO as GPIO
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
import matplotlib
matplotlib.use('Agg') #ssh does not allow display plot
import matplotlib.pyplot as plt
import csv
import os

#pin 11 led
# GPIO.setmode(GPIO.BOARD)
# chan_list = [11]
# GPIO.setup(chan_list, GPIO.OUT)

# SPI Configuration
SPI_PORT   = 0
SPI_DEVICE = 0
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

# Parameters
lux_threshold  = 200 
sample_interval = 0.1
num_samples     = 50

# Collects light intensity data using mcp.read_adc() and return following arrays:
# left, right, average and timestamps arrays
def collect_data():
  
  left_value  = []
  right_value = []
  avg_value   = []
  timestamps  = []
  
  for i in range(num_samples):
    left  = mcp.read_adc(0) #CH0 J2
    right = mcp.read_adc(1) #CH1 J3
    avg   = (left + right) / 2
    
    left_value.append(left)
    right_value.append(right)
    avg_value.append(avg)
    timestamps.append(round(i * sample_interval, 2))

  #   #turn led on when either exceeds threshold
  #   if left > lux_threshold or right > lux_threshold:
  #     GPIO.output(chan_list, GPIO.HIGH)
  #   else:
  #     GPIO.output(chan_list, GPIO.LOW)
  #   time.sleep(sample_interval)
  # GPIO.output(chan_list, GPIO.LOW) #led off
  return left_value, right_value, avg_value, timestamps

# Records the collected data to csv file
def record():
  left_value, right_value, avg_value, timestamps = collect_data()

  # added values into csv
  os.makedirs("output", exist_ok=True)
  with open("output/data.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["timestamp", "left", "right", "average"])
    for i in range(len(timestamps)):
        writer.writerow([timestamps[i], left_value[i], right_value[i], avg_value[i]])
  
  return True

if __name__ == "__main__":
  record()
  # GPIO.cleanup()