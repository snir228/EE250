import time
import RPi.GPIO as GPIO
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008

#using physical pin 11 to blink an LED
GPIO.setmode(GPIO.BOARD)
chan_list = [11]
GPIO.setup(chan_list, GPIO.OUT)

# Hardware SPI configuration:
SPI_PORT   = 0
SPI_DEVICE = 0
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

# by taking readings and printing them out, find
# appropriate threshold levels and set them 
# accordingly. Then, use them to determine
# when it is light or dark, quiet or loud.
lux_treshold=500  # change this value
sound_treshold=600 # change this value


while True: 
  # LED blinking 5 times with 500 ms interval between on and off
  for i in range(0, 5):
    time.sleep(0.5)
    GPIO.output(chan_list, GPIO.HIGH)
    time.sleep(0.5) 
    GPIO.output(chan_list, GPIO.LOW)
  
  # Light sensor reading and printing value every 100 ms for 5 seconds
  for i in range(0, 50):
    val = mcp.read_adc(0)
    print(val)
    if (val > lux_treshold):
      print("bright")
    else:
      print("dark")
    time.sleep(0.1) 
  
  # LED blinking 4 times with 200 ms interval between on and off
  for i in range(0, 4):
    time.sleep(0.2)
    GPIO.output(chan_list, GPIO.HIGH)
    time.sleep(0.2) 
    GPIO.output(chan_list, GPIO.LOW)
  
  # Sound sensor reading every 100 ms for 5 seconds. LED will be turned on for 100 ms everytime the sound magnitude is greater than the threshold. It maintains the total 5 seconds
  for i in range(0, 50):
    val = mcp.read_adc(1)
    print(val)
    if(val > sound_treshold):
      GPIO.output(chan_list, GPIO.HIGH)
      time.sleep(0.1)
      GPIO.output(chan_list, GPIO.LOW)
    else:
      time.sleep(0.1) 
  #Following commands control the state of the output
  # GPIO.output(pin, GPIO.HIGH)
  # GPIO.output(pin, GPIO.LOW)

  # get reading from adc 
  # mcp.read_adc(adc_channel)
