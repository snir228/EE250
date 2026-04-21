import statistics as stat
import numpy as np

# client = OpenAI(api_key = "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")

# response = client.responses.create(
#     model="gpt-4o",
#     input="Explain recursion in one sentence."
# )

# print(response.output_text)

avg = 0

def get_average(a):
    sum = 0
    for i in range(len(a)):
        sum += a[i]
    avg = sum / len(a)
    return avg

def get_variance(a):
    var = stat.variance(a)
    return var

def get_trend(a):
    slope = np.polyfit(range(len(a)), a, 1)[0]
    if slope > 1: # Slope will be changed depending on the result
        return "Increasing"
    elif slope < -1:
        return "Decreasing"
    else:
        return "Stable"


