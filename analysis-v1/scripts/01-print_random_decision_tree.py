import random
import argparse
import analysis.ai_generator

args = argparse.ArgumentParser()
args.add_argument("--seed", type=int, default=0)
args.add_argument("--nodes", type=int, default=5)
args = args.parse_args()

random.seed(args.seed)

analysis.ai_generator.Tree.generate_random(args.nodes).print()


# mkdir -p computed/trees
# python3 teaching-boundaries/scripts/01-print_random_decision_tree.py --seed 0 --nodes 5
# python3 teaching-boundaries/scripts/01-print_random_decision_tree.py --seed 1 --nodes 5
# python3 teaching-boundaries/scripts/01-print_random_decision_tree.py --seed 0 --nodes 3
# python3 teaching-boundaries/scripts/01-print_random_decision_tree.py --seed 0 --nodes 8