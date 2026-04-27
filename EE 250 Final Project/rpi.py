import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
import csv
import os

# SPI Configuration
SPI_PORT   = 0
SPI_DEVICE = 0
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

# Parameters
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

# Main Function
if __name__ == "__main__":
  record()
