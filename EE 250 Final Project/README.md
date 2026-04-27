Team Members
- Steve Cho (USC ID: 4314516349)
- Sivan Nir (USC ID: 7594069996)

Execution Steps:

1. Download all the necessary libraries

Install command: 
pip install [library name]
or
pip3 install [library name]

Install Required Library:
- matplotlib
- ssh
- openai
- csv
- paramiko
- requests
- geocoder
- numpy
- Adafruit_GPIO
- Adafruit_MCP3008

Python Standard Libraries:
- os
- statistics
- tkinter
- json
- time
- os

SPECIAL INSTRUCTION FOR Adafruit_GPIO and Adafruit_MCP3008:

1: First, ssh into your Raspberry Pi and execute the command:
sudo raspi-config
2: Select Interfacing Options -->
Select SPI --> Select Yes --> Select OK
3: Install the library via the command:
sudo pip3 install adafruit-mcp3008

2. Make sure the rpi.py file is inside the Raspberry Pi, and all other files are inside the same folder and located on the laptop

3. *IMPORTANT*: On ssh.py, revise RPI_IP, RPI_USER, and RPI_PASS to your Raspberry Pi IP address, username, and password. Also, revise the PATH variable to the path where rpi.py is in your Raspberry Pi

4. On app.py, go to where the OpenAI API key is (Line: client = OpenAI(api_key="key")). Paste the OpenAI API key in where "key" is (must be a string)

5. Connect the Lab 10 PCB board with two light sensors connected to the Raspberry Pi

6. On the terminal, execute:
python3 app.py
or 
python app.py

7. Press the 'Process Light Intensity' button and wait for the results to pop up

8. Press the 'LLM Activity Suggestion' button and type 'inside' or 'outside' depending on where you are

9. Wait a few seconds, and the suggestions will show up

10. To exit, press the close button on the top right corner or control+C on the terminal

