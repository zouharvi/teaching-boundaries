import copy
import random


class Feature():
    i = None

    def __init__(self, name, options, prerequisites=set()):
        self.name = name
        self.options = options
        self.prerequisites = prerequisites

    def format_question(self):
        return self.name.split("_")[0] + "?"

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

for feature_i, feature in enumerate(FEATURES):
    feature.i = feature_i


class Node():
    def __init__(self, feature, decision=None):
        self.feature = feature
        self.left = None
        self.right = None
        self.decision = decision

    def __call__(self, x):
        if self.decision is not None:
            return self.decision
        else:
            if x[self.feature.i]:
                return self.left(x)
            else:
                return self.right(x)


def ok_features_i(features, parent_choices):
    return [
        feature_i for feature_i, feature in enumerate(features)
        if all(x in parent_choices for x in features[feature_i].prerequisites)
    ]


def generate_tree(allowed_nodes, features=FEATURES, parent_choices=[]):
    features = copy.deepcopy(features)
    # make sure that prerequisites are fulfilled
    feature = features.pop(random.choice(
        ok_features_i(features, parent_choices)))

    if allowed_nodes <= 2:
        node = Node(feature)
        node.left = Node(feature=None, decision=False)
        node.right = Node(feature=None, decision=True)
        return node

    allowed_nodes -= 1

    nodes_left = random.randint(1, allowed_nodes - 1)
    child_left = generate_tree(
        nodes_left, features, parent_choices + [feature.name + " = " + feature.options[0]])
    child_right = generate_tree(allowed_nodes - nodes_left, features,
                                parent_choices + [feature.name + " = " + feature.options[1]])
    node = Node(feature)
    node.left = child_left
    node.right = child_right
    return node
