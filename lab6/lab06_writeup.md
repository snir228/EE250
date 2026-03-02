# Lab 6

## Team Members
- Steve Cho (USC ID: 4314516349)
- Sivan Nir (USC ID: 7594069996)

4.1. Suppose you just cloned a repository that included one python file, my_first_file.py, and you now want to add a second file to your repository named my_second_file.py which contains the following code and push it to Github.com.

Code -
print(“Hello World”)

Complete the sequence of linux shell commands:
git clone git@github.com:my-name/my-imaginary-repo.git
##complete the sequence
(Note: create the file using the `touch` command)

Answer:
- cd my-imaginary-repo
- touch my_second_file.py 
- echo 'print("Hello World")' > my_second_file.py
- git add my_second_file.py
- git commit -m "Additional File"
- git push origin main


4.2. Describe the workflow you adopted for this lab (i.e. did you develop on your VM
and push/pull to get code to your RPi, did you edit files directly on your RPi, etc.).
Are there ways you might be more efficient in the next lab (i.e. learning a
text-based editor so you can edit natively on the RPi, understanding Git
commands better, etc.)?

Answer:
The workflow we adopted was the use of git. We first used the VSCode IDE on our local machine to edit the file. Once we were ready to test the code, we created a GitHub repository with a folder containing the script. Then we sshed into the RPi (we downloaded all the necessary files/library beforehand). We then cloned the repository to our RPi root folder and moved the script to the GrovePi/Software/Python folder. After we ran the code. When we noticed it wasn't working properly, we used the Nano IDE to edit the code rather than redownloading and moving the file again. It would have been more efficient to write the code in the text editor, since uploading to GitHub and fetching from GitHub takes too much time.

4.3. In the starter code, we added a 200 ms sleep. Suppose you needed to poll the ultrasonic ranger as fast as possible, so you removed the sleep function. Now, your code has just the function ultrasonicRead() inside a while loop. However, even though there are no other functions in the while loop, you notice there is a constant delay between each reading. Dig through the python library to find out why there is a constant delay. What is the delay amount? In addition, what communication protocol does the Raspberry Pi use to communicate with the Atmega328P on the GrovePi when it tries to read the ultrasonic ranger output using the `grovepi` python library?

Answer:
The constant delay amount within grovepi.ultrasonicRead() is 60 ms. RPi uses I2C communication protocol to communicate with the Atmega328P.


4.4. When you rotate the Grove Rotary Angle Sensor, its analog output voltage changes between 0 V and 5 V and the GrovePi library reports integer values between 0 and 1023. Explain how this conversion works and why the Raspberry Pi cannot do it directly.

Answer:
The ADC module in the ATmega328P converts an analog signal to a 10-bit digital signal, which is why the range is 0 to 1023 (2^10 = 1024). The conversion is done by dividing 5 V by 1024, which is 0.00488 V. This means each digit within 0 to 1023 is 0.00488 V apart. Raspberry Pi cannot do it directly because it cannot interpret analog inputs; it only reads High and Low signals.


4.5. Your LCD RGB Backlight screen is not displaying any text even though your code executes without errors. Describe how you would debug the issue. Include at least two terminal commands.

Answer:
I would first check what is being displayed on the screen and avoid using spaces to determine whether the space is being written or the text isn't displaying at all. I would also check whether the I2C protocol is being utilized and RPi can detect the device by using the following command:
- i2cdetect 1 # i2cdetect is used to scan for an I2C bus 1 and the devices that are connected to that

If there exist numbers on the grid, then the protocol is being used. This is a way to check whether the RPi is using the I2C protocol and whether the display uses it to communicate. If there are no numbers on the grid, I would try using a different bus number. Another command I would use is:
- lsmod | grep i2c # Listing all the modules and filtering the module named i2c

If an I2C module exists, I2C is activated. This is a way to check if the I2C protocol is activated. If it is not activated, I would use the command:
- sudo raspi-config

And then go to the I2C setting and activate. After, I will reboot (sudo reboot).
