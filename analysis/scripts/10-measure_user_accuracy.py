import json
import numpy as np

data = [json.loads(x) for x in open("computed/collected/TMP.jsonl", "r")]

def accuracy(data):
    return np.average([
        line["response"] == line["question"]["correct"]
        for line in data
    ])

def time(data):
    times = [
        (line["time"]["end"]-line["time"]["start"])/1000
        for line in data
    ]
    return np.average([
        t for t in times if t <= 60
    ])

print(f"Train-time: ACC={accuracy(data[:6]):>7.2%} TIME={time(data[:6]):.1f}s")
print(f"Test-time:  ACC={accuracy(data[6:]):>7.2%} TIME={time(data[6:]):.1f}s")