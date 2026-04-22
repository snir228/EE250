import statistics as stat
import numpy as np

# Calculates average of given array
def get_average(a):
    sum = 0
    for i in range(len(a)):
        sum += a[i]
    avg = sum / len(a)
    return avg

# Calculates variance of given array
def get_variance(a):
    var = stat.variance(a)
    return var

# Calculates trend of given array using polyfit
def get_trend(a):
    slope = np.polyfit(range(len(a)), a, 1)[0] # Fitting polynomial = 1 curve to the data
    if slope > 1: # Slope will be changed depending on the result
        return "Increasing"
    elif slope < -1:
        return "Decreasing"
    else:
        return "Stable"


