import random
import argparse
import decision_tree

args = argparse.ArgumentParser()
args.add_argument("--seed", type=int, default=0)
args.add_argument("--nodes", type=int, default=5)
args = args.parse_args()

random.seed(args.seed)

decision_tree.Tree.generate_random(args.nodes).print_typst()