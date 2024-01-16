import json
import random
from analysis import decision_tree
from analysis import user_models
random.seed(0)
tree = decision_tree.Tree.generate_random(8)
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
tree.print_typst()

best_subset = user_models.decision_tree_simple(data_xy, k=10)
