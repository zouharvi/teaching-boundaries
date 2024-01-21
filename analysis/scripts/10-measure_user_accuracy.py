import json
import numpy as np
import collections

data = [json.loads(x) for x in open("computed/collected/ailr_linear_simple_tdomain_10n20_s0.jsonl", "r")]
data_user = collections.defaultdict(list)

for line in data:
    user = line["user"]["prolific_pid"]
    if not user or len(user) <= 3 or "%" in user:
        continue
    data_user[user].append(line)


def accuracy(data):
    avg = np.average([
        line["response"] == line["question"]["correct"]
        for line in data
    ])
    return avg


def time(data):
    times = [
        (line["time"]["end"]-line["time"]["start"])/1000
        for line in data
    ]
    return np.average([
        t for t in times if t <= 60
    ])

def mcc_accuracy(data):
    # predict always correct or incorrect
    val = np.average([
        line["question"]["correct"]
        for line in data
    ])
    return max(val, 1-val)

CUTOFF = 10

data_agg = []
for data_local in data_user.values():
    # skip unfinished
    if len(data_local) < 20:
        continue

    data_agg.append({
        "train_acc": accuracy(data[:CUTOFF]),
        "test_acc": accuracy(data[CUTOFF:]),
        "train_time": time(data[:CUTOFF]),
        "test_time": time(data[CUTOFF:]),
        "test_mccacc": mcc_accuracy(data[CUTOFF:]),
    })

def agg_average(key):
    data = [x[key] for x in data_agg if all(x.values())]
    return np.average(data)

print(f"Train: ACC={agg_average('train_acc'):>7.2%} TIME={agg_average('train_time'):>4.1f}s/sample")
print(f"Test:  ACC={agg_average('test_acc'):>7.2%} TIME={agg_average('test_time'):>4.1f}s/sample")
print(f"Test:  MCCACC={agg_average('test_mccacc'):>7.2%}")