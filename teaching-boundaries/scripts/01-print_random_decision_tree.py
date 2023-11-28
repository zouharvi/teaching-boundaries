import random
import argparse
from decision_tree_generator import generate_tree

args = argparse.ArgumentParser()
args.add_argument("--seed", type=int, default=0)
args.add_argument("--nodes", type=int, default=5)
args = args.parse_args()

random.seed(args.seed)


fout = open(f"computed/trees/random_s{args.seed}_n{args.nodes}.out", "w")
fout.write('#')

def print_tree(node, prefix="", offset=0):
    if node.decision is not None:
        fout.write(
            "  " * (offset + 1) +
            "\"" + "\\n" + str(node.decision) + "\",\n"
        )
    else:
        fout.write(
            "  " * offset +
            "tree(\"" + prefix + node.feature.format_question() + "\","
            + "\n"
        )
        options = node.feature.format_options()

        print_tree(
            node.left,
            prefix=options[0] + "\\n",
            offset=offset + 1
        )

        print_tree(
            node.right,
            prefix=options[1] + "\\n",
            offset=offset + 1,
        )

    fout.write(
        "  " * offset +
        ")" + ("," if offset != 0 else "") + "\n"
    )

print_tree(generate_tree(args.nodes))

fout.write("#pagebreak()\n")