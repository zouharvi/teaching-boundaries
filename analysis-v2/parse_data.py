import argparse
import glob
import os
import json

args = argparse.ArgumentParser()
args.add_argument("--wmt", default="wmt23")
args = args.parse_args()

# wget https://storage.googleapis.com/mt-metrics-eval/mt-metrics-eval-v2.tgz
# tar -xzf mt-metrics-eval-v2
# mkdir -p data/
# mv mt-metrics-eval-v2 data/mt-metrics-eval-v2
BASE_DIR = f"data/mt-metrics-eval-v2/{args.wmt}/"


def parse_float_soft(x):
    if x == "None":
        return None
    else:
        return float(x)


scores = {}
for file in glob.glob(BASE_DIR + "human-scores/*.da-sqm.seg.score"):
    langs = os.path.basename(file).removesuffix(".da-sqm.seg.score")
    scores[langs] = [
        line.rstrip().split("\t")
        for line in open(file, "r")
    ]
    systems = set([x[0] for x in scores[langs]])
    scores[langs] = {
        system: [parse_float_soft(x[1])
                 for x in scores[langs] if x[0] == system]
        for system in systems
    }

for langs in scores.keys():
    sources = [
        line.rstrip()
        for line in open(BASE_DIR + f"sources/{langs}.txt", "r")
    ]
    targets = {
        os.path.basename(file).removesuffix(".txt"): [line.rstrip() for line in open(file, "r")]
        for file in glob.glob(BASE_DIR + f"system-outputs/{langs}/*.txt")
    }
    for system in scores[langs]:
        scores[langs][system] = [
            {
                "src": line_src,
                "tgt": line_tgt,
                "score": score
            }
            for line_src, line_tgt, score in zip(sources, targets[system], scores[langs][system])
            # filter out None
            if score is not None
        ]

with open(f"computed-v2/base_{args.wmt}.json", "w") as f:
    f.write(json.dumps(scores, ensure_ascii=False, indent=2))