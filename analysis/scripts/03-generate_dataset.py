import os
import json
import random
from analysis import decision_tree, utils, user_models
import argparse

args = argparse.ArgumentParser()
args.add_argument("-m", "--model", default="tree_simple")
args = args.parse_args()

tree = decision_tree.Tree.generate_random(6)
tree.print_typst()

random_data = random.Random(0)

# load dataset and add manually confidence
data_x = [
    json.loads(x) for x in open("computed/dataset_base.jsonl", "r")
]
for line in data_x:
    line["configuration"]["confidence"] = random_data.choice(
        ["low AI confidence", "high AI confidence"]
    )
# add tree prediction
data_y = [
    tree(x["configuration"]) for x in data_x
]
data_xy = list(zip(data_x, data_y))
# select test questions beforehand
test_questions = random_data.sample(list(data_xy), k=20)
test_questions_set = {x["question"] for x, y in test_questions}
training_questions_pool = [
    (x, y) for x, y in data_xy
    if x["question"] not in test_questions_set
]

training_questions = user_models.MODELS[args.model](training_questions_pool, k=10)

# output queue
os.makedirs("computed/queues", exist_ok=True)

queue = []
for question, correct in training_questions:
    queue.append({
        "question": question["question"],
        "answer": question["answer"],
        "mode": "base_tags",
        "tags": utils.configuration_to_tags(question["configuration"]),
        "reveal": True,
        "correct": correct,
    })
for question, correct in test_questions:
    queue.append({
        "question": question["question"],
        "answer": question["answer"],
        "mode": "base_tags",
        "tags": utils.configuration_to_tags(question["configuration"]),
        "reveal": False,
        "correct": correct,
    })
with open(f"computed/queues/queue_{args.model}_10.jsonl", "w") as f:
    f.write("\n".join(json.dumps(x, ensure_ascii=False) for x in queue))