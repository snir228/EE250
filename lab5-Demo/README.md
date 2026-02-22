# Lab 5

## Team Members
- Steve Cho (USC ID: 4314516349)
- Sivan Nir (USC ID: 7594069996)

## Lab Question Answers
Question 1: What is dBm? What values are considered good and bad for WiFi signal strength?

Answer: dBm is decibel milliwatts (logarithmic unit) representing the amount of power produced by the source (i.e., for WiFi, it's the WiFi signal strength). WiFi strength is considered generally good if it's within -60 dBm to -30 dBm. -67 dBm is the minimum. If it's below -67 dBm, then it's considered bad.

Resource Used: https://eyenetworks.no/en/required-good-wifi-signal-strength/, https://www.wilsonconnectivity.com/blog/whats-the-difference-between-db-and-dbm

Question 2: Why do we need to check the OS? What is the difference between the commands for each OS?

Answer: We need to check the OS because each OS extracts the WiFi info differently due to the use of different tools. Thus, it is essential to check the OS. 

For Windows, the command is:
netsh wlan show interfaces

For MAC, the command is:
sudo wdutil info

For Linux, the command is:
iwconfig wlan0

Resources Used:
main.py script

Question 3: In your own words, what is subprocess.check_output doing? What does it return?
HINT: https://docs.python.org/3/library/subprocess.html#subprocess.check_output

Answer: subprocess.check_output is a way to run command lines in Python and capture the output that they print. It will return the output from the command line. If it is unsuccessful to print the output and the return code is non-zero, it raises Called ProcessError.

Question 4: In your own words, what is re.search doing? What does it return?
HINT: https://docs.python.org/3/library/re.html#re.search

Answer: re.search goes through the input string and tries to find the first part that matches the regular expression commands. If it matches, it returns a match object that contains the matched regular expression; else, it returns None.

Question 5: In the Windows case, why do we need to convert the signal quality to dBm?
HINT: https://learn.microsoft.com/en-us/windows/win32/api/wlanapi/ns-wlanapi-wlan_association_attributes?redirectedfrom=MSDN

Answer:
Signal quality must be converted to dBm for the Windows case, as 
the value is given as a percentage (between 0 and 100), unlike Linux and Mac, where it returns in dBm. Thus, to have a consistent result across different OS, we must convert the value to dBm for Windows.

Question 6: What is the standard deviation? Why is it useful to calculate it?

Answer: Standard deviation is a numeric representation of how the data is spread out overall, where a high SD means there is a large spread and a low SD means a small spread. It is useful to calculate as it shows how dispersed and different the data is.


Question 7: What is a dataframe? Why is it useful to use a dataframe to store the data?
HINT: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html
HINT: print the dataframe to see what it looks like

Data Frame is a 2-D data structure from pandas where data is organized in rows and columns with corresponding labels. It is useful to use a dataframe to store data as it clearly distinguishes and organizes what each data represents, making it easy to utilize and analyze. In this lab, a Data Frame is used to organize data into location, signal_strength_mean, and signal_strength_std.

Question 8: Why is it important to plot the error bars? What do they tell us?

Answer: It is important to plot the error bars as it visualizes the reliability and uncertainty of the data. Despite having data, if the error bar is large, then we won't be able to use the data to make a reasonable conclusion.

Question 9: What did you observe from the plot? How does the signal strength change as you move between locations?
Why do you think signal strength is weaker in certain locations?

Answer: We observed that the signal strength varies by location, but most of them are within the range of <= -67 dBm, where the signal can be used in any location. Looking at the table below, signal strength decreases as it moves away from where the router is (near the kitchen), which explains why the kitchen had the highest dBm mean with -62.4 dBm. The signal strength is weaker in certain locations where the router is far away or where objects might be interfering (walls or doors), making it hard for data to be transmitted.



 location  signal_strength_mean  signal_strength_std
0      bedroom                 -71.8             1.600000
1  living room                 -68.2             1.249000
2      kitchen                 -62.4             7.102112
3     bathroom                 -69.6             2.457641
4       garage                 -74.4             2.764055