import json
import numpy as np
import collections

data = [json.loads(x) for x in open("computed/collected/ailr_linear_simple_4n19_s0.jsonl", "r")]
data_user = collections.defaultdict(list)

for line in data:
    user = line["user"]["prolific_pid"]
    if len(user) <= 3 or "%" in user:
        continue
    data_user[user].append(line)


def accuracy(data):
    avg = np.average([
        line["response"] == line["question"]["correct"]
        for line in data
    ])
    # if avg < 0.5:
    #     return None
    return avg


def time(data):
    times = [
        (line["time"]["end"]-line["time"]["start"])/1000
        for line in data
    ]
    return np.average([
        t for t in times if t <= 60
    ])


agg_accuracy_train = []
agg_time_train = []
agg_accuracy_test = []
agg_time_test = []
for data_local in data_user.values():
    # skip unfinished
    if len(data_local) < 20:
        continue
    agg_accuracy_train.append(accuracy(data[:6]))
    agg_accuracy_test.append(accuracy(data[6:]))
    agg_time_train.append(time(data[:6]))
    agg_time_test.append(time(data[6:]))

def nan_average(data):
    data = [x for x in data if x]
    return np.average(data)

print(f"Train-time: ACC={nan_average(agg_accuracy_train):>7.2%} TIME={nan_average(agg_time_train):>4.1f}s/sample")
print(f"Test-time:  ACC={nan_average(agg_accuracy_test):>7.2%} TIME={nan_average(agg_time_test):>4.1f}s/sample")