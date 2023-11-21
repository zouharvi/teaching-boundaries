import copy
import random
random.seed(0)


class Feature():
    def __init__(self, name, options, prerequisites=set()):
        self.name = name
        self.options = options
        self.prerequisites = prerequisites

    def format_question(self):
        return self.name.split("_")[0]+"?"

    def format_options(self):
        if any("%" in x for x in self.options):
            return [self.name.split("_")[0] + x for x in self.options]
        else:
            return [self.name + "=" + x for x in self.options]


FEATURES = [
    Feature(name="domain", options=["math", "history"]),
    Feature(name="question length", options=["short", "long"]),
    Feature(name="answer length", options=["short", "long"]),
    Feature(name="confidence_1", options=["≥80%", "<80%"]),
    Feature(
        name="confidence_2",
        options=["≥40%", "<40%"],
        prerequisites={"confidence_1 = <80%"}
    ),
]


class Node():
    def __init__(self, feature):
        self.feature = feature
        self.left = None
        self.right = None

def ok_features_i(features, parent_choices):
    return [
        feature_i for feature_i, feature in enumerate(features)
        if all(x in parent_choices for x in features[feature_i].prerequisites)
    ]

def generate_tree(allowed_nodes, features, parent_choices=[]):
    if allowed_nodes == 1:
        return Node(features[random.choice(ok_features_i(features, parent_choices))])
    allowed_nodes -= 1

    features = copy.deepcopy(features)
    # make sure that prerequisites are fulfilled
    feature = features.pop(random.choice(ok_features_i(features, parent_choices)))

    nodes_left = random.randint(0, allowed_nodes)
    child_left = generate_tree(nodes_left, features, parent_choices+[feature.name + " = " + feature.options[0]])
    child_right = generate_tree(allowed_nodes - nodes_left, features, parent_choices+[feature.name + " = " + feature.options[1]])
    node = Node(feature)
    node.left = child_left
    node.right = child_right
    return node


fout = open("computed/trees/random1.out", "w")
fout.write('#')

random.seed(0)


def print_tree(node, prefix="", offset=0):
    fout.write(
        "  " * offset +
        "tree(\"" + prefix + node.feature.format_question() + "\","
        + "\n"
    )
    options = node.feature.format_options()

    leaves = ["True", "False"]
    # assume that confidence features start with higher confidence
    # and we want _some_ calibration
    if not node.feature.name.startswith("confidence"):
        random.shuffle(leaves)

    if node.left:
        print_tree(
            node.left,
            prefix=options[0] + "\\n",
            offset=offset + 1
        )
    else:
        fout.write(
            "  " * (offset + 1) +
            "\"" + options[0] + "\\n" + leaves[0] + "\",\n"
        )

    if node.right:
        print_tree(
            node.right,
            prefix=options[1] + "\\n",
            offset=offset + 1,
        )
    else:
        fout.write(
            "  " * (offset + 1) +
            "\"" + options[1] + "\\n" + leaves[1] + "\",\n"
        )

    fout.write(
        "  " * offset +
        ")" + ("," if offset != 0 else "") + "\n"
    )


print_tree(generate_tree(5, FEATURES))