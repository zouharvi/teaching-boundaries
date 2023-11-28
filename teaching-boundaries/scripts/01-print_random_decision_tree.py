import random
import argparse
from decision_tree_generator import generate_tree

args = argparse.ArgumentParser()
args.add_argument("--seed", type=int, default=0)
args.add_argument("--nodes", type=int, default=5)
args = args.parse_args()

random.seed(args.seed)

generate_tree(args.nodes).print_typst()