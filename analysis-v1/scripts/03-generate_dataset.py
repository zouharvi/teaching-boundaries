import os
import json
import random
from analysis import ai_generator, utils, user_models
import argparse
import numpy as np

args = argparse.ArgumentParser()
args.add_argument("--model", default="tree_simple")
args.add_argument("--tags", default="all")
args.add_argument("--ai-model", default="ailr")
args.add_argument("--size-train", type=int, default=10)
args.add_argument("--size-test", type=int, default=20)
args.add_argument("--seed", type=int, default=0)
args = args.parse_args()

fake_ai = ai_generator.get_model(args.ai_model, args.tags, args.seed)
fake_ai.print()

# load dataset and add manually confidence
data_x = [
    json.loads(x) for x in open("computed/dataset_base.jsonl", "r")
]
data_x = utils.add_fake_ai_confidence(data_x)

# add fake ai prediction
data_y = [
    fake_ai(x["configuration"]) for x in data_x
]
data_xy = list(zip(data_x, data_y))
# select test questions beforehand
test_questions = random.Random(args.seed).sample(list(data_xy), k=args.size_test)
test_questions_set = {x["answer"] for x, y in test_questions}
training_questions_pool = [
    (x, y) for x, y in data_xy
    if x["answer"] not in test_questions_set
]

training_questions = user_models.MODELS[args.model](
    training_questions_pool, k=args.size_train
)


print(f"MCC accuracy: {max(1-np.average(data_y), np.average(data_y)):.1%}")

# output queue
os.makedirs("computed/queues", exist_ok=True)

queue = []
for question, correct in training_questions:
    queue.append({
        "answer": question["answer"],
        "mode": "base_tags",
        "tags": utils.configuration_to_tags(question["configuration"], utils.TAGS_CONFIGURATIONS[args.tags]),
        "reveal": True,
        "correct": correct,
    })
for question, correct in test_questions:
    queue.append({
        "answer": question["answer"],
        "mode": "base_tags",
        "tags": utils.configuration_to_tags(question["configuration"], utils.TAGS_CONFIGURATIONS[args.tags]),
        "reveal": False,
        "correct": correct,
    })
with open(f"web/web/queues/{args.ai_model}_{args.model}_t{args.tags}_{args.size_train}n{args.size_test}_s{args.seed}.jsonl", "w") as f:
    f.write("\n".join(json.dumps(x, ensure_ascii=False) for x in queue))
