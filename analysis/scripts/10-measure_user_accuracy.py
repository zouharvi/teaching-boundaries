import json
import numpy as np
import re
import argparse
import glob
import analysis.utils

args = argparse.ArgumentParser()
args.add_argument("-u", "--uid", default="*")
args = args.parse_args()
CUTOFF = 10

RE_UID = re.compile(args.uid)

data_user = {
    user:data
    for user, data in analysis.utils.data_to_users("computed/collected.jsonl", flat=False, cutoff=CUTOFF).items()
    if RE_UID.match(data[0]["uid"])
}

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


data_agg = []
for data_local in data_user.values():
    # skip unfinished user runs
    if len(data_local) < 10:
        continue

    data_agg.append({
        "train_acc": accuracy(data_local[:CUTOFF]),
        "test_acc": accuracy(data_local[CUTOFF:]),
        "train_time": time(data_local[:CUTOFF]),
        "test_time": time(data_local[CUTOFF:]),
        "test_mccacc": mcc_accuracy(data_local[CUTOFF:]),
    })

def agg_average(key):
    data = [x[key] for x in data_agg if all(x.values())]
    return np.average(data)

print(f"Users: {len([x for x in data_agg if all(x.values())])}")
print(f"Train: ACC={agg_average('train_acc'):>7.2%} TIME={agg_average('train_time'):>4.1f}s/sample")
print(f"Test:  ACC={agg_average('test_acc'):>7.2%} TIME={agg_average('test_time'):>4.1f}s/sample")
print(f"Test:  MCCACC={agg_average('test_mccacc'):>7.2%}")