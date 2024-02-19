import random
import argparse
from qe_systems import get_qe_predictions, get_mae
import json
import numpy as np

args = argparse.ArgumentParser()
args.add_argument("--langs", default="en-de")
args.add_argument("--wmt", default="wmt23")
args.add_argument("--test-error", type=float, default=10)
args.add_argument("--train-error", type=float, default=10)
args.add_argument("--np-seed", type=int, default=0)
args = args.parse_args()

data = json.load(open(f"computed-v2/base_{args.wmt}.json", "r"))[args.langs]
for system in data.keys():
    data[system] = [
        x | {"system": system}
        for x in data[system]
    ]
data = [line for system in data.values() for line in system]

data_train = random.Random(0).sample(data, k=10)
data_test = random.Random(1).sample(data, k=50)

np.random.seed(args.np_seed)
data_out = [
    x | {
        "score_ai": get_qe_predictions(x["score"], error_level=args.train_error),
        "phase": "train"
    }
    for x in data_train
] + [
    x | {
        "score_ai": get_qe_predictions(x["score"], error_level=args.test_error),
        "phase": "test"
    }
    for x in data_test
]

print(f"Train MAE: {get_mae(data_out, 'train'):.1f}")
print(f" Test MAE: {get_mae(data_out, 'test'):.1f}")

fout = open(
    f"web-v2/web/queues/{args.wmt}_{args.langs.replace('-', '')}_t{args.train_error}t{args.test_error}.jsonl",
    "w"
)
fout.write("\n".join([json.dumps(x, ensure_ascii=False) for x in data_out]))
