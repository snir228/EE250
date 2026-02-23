# Lab 5

## Team Members
- Steve Cho (USC ID: 4314516349)
- Sivan Nir (USC ID: 7594069996)

## Lab Question Answers

## Part 1

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
Signal quality must be converted to dBm for the Windows case, as the value is given as a percentage (between 0 and 100), unlike Linux and Mac, where it returns in dBm. Thus, to have a consistent result across different OS, we must convert the value to dBm for Windows.

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

Answer: We observed that signal strength varies by location, but all are within the range of <= -67 dBm, indicating the signal can be used in any location. The graph shows the overall change as we moved between locations, since each location has a different layout of walls and other factors that affect the signal. Looking at the graph, we can see that the signal strength is the strongest in the living room with a value of around -40.9 dBm (using the table). This makes sense, as the router is in the living room; thus, the signal is strongest there. The bathroom and garage, on the other hand, are at least -67 dB, which makes sense, as the garage is farther away and the bathroom may be surrounded by multiple walls that cause interference with the signal.

location  signal_strength_mean  signal_strength_std
0      bedroom                 -57.8             0.979796
1  living room                 -40.9             1.374773
2      kitchen                 -48.9             1.044031
3     bathroom                 -67.0             1.414214
4       garage                 -67.1             1.374773

## Part 2
Question 10: How does distance affect TCP and UDP throughput?

Answer: Wifi signal strength decreases with distance. For TCP, throughput generally decreases gradually with distance because it uses a control and retransmission mechanism to ensure reliable delivery. This makes for a slight but stable decrease in throughput. For UDP, throughput remains relatively constant at shorter distances but can drop sharply at longer distances when packet loss becomes significant.

Question 11: At what distance does signficant packet loss occur for UDP?

Answer: Significant packet loss for UDP begins to occur at the 14 meter mark. From the plots, UDP remains stable at 10Mbps for distances 2m to 12m, indicating little to no packet loss. At 14m, UDP througput drops to 0Mbs.

Question 12: Why does UDP experience more packet loss than TCP?

Answer: TCP possesses an acknowledgment protocol that retransmits and ensures data is delivered correctly. When a packet is lost, TCP detects it is missing through a missing acknowledgement and retransmits it automatically. UDP sends packets continuously without checking whether they arrive successfully. As the distance from the router increases, the signal weakens, and more packets are lost for UDP.

Question 13: 4. What happens if we increase the UDP bandwidth (-b 100M)?

Answer: If we increase UDP bandwidth using -b 100M, the sender attempts to transmit data at a higher rate, which can exceed the capacity of the wireless network, or the signal strength cannot compensate for that rate. Thus, this could lead to packet losses. UDP does not automatically lower the sending rate, so increasing bandwidth leads to significantly higher packet loss and would not necessarily increase throughput. 

Question 14: Would performance be different on 5 GHz wifi vs. 2.4 GHz?

Answer: Performance differs whether 5 GHz or 2.4 GHz are used. The 5 GHz wifi would provide higher throughput at shorter distances because it has more available channels and less interference from common devices. This would allow TCP and UDP to achieve higher data rates with lower packet loss when closer to the router. With that said, 5 GHz signals attenuate more quickly with distance, so performance can degrade rapidly. 2.4 GHz has a better range, which makes it more reliable at longer distances. However, it does have a lower maximum throughput. Thus, the trade-off is higher performance but shorter range (5 GHz) vs. lower performance but longer range (2.4 GHz).

Resources Used: https://www.centurylink.com/home/help/internet/wireless/which-frequency-should-you-use.html
https://www.intel.com/content/www/us/en/products/docs/wireless/2-4-vs-5ghz.html
