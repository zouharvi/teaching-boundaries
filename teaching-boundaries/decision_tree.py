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


class Tree():
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
                return self.right(x)
            else:
                return self.left(x)

    @staticmethod
    def generate_random(allowed_nodes, features=FEATURES, parent_choices=[]):
        features = copy.deepcopy(features)
        # make sure that prerequisites are fulfilled
        feature = features.pop(random.choice(
            _ok_features_i(features, parent_choices)))

        if allowed_nodes <= 2:
            node = Tree(feature)
            node.left = Tree(feature=None, decision=False)
            node.right = Tree(feature=None, decision=True)
            return node

        allowed_nodes -= 1

        nodes_left = random.randint(1, allowed_nodes - 1)
        child_left = Tree.generate_random(
            nodes_left, features, parent_choices +
            [feature.name + " = " + feature.options[0]]
        )
        child_right = Tree.generate_random(
            allowed_nodes - nodes_left, features,
            parent_choices + [feature.name + " = " + feature.options[1]]
        )
        node = Tree(feature)
        node.left = child_left
        node.right = child_right
        return node


    def print_typst(self):
        print('#', end="")
        self._print_typst()

    def _print_typst(self, prefix="", offset=0):
        if self.decision is not None:
            print(
                "  " * (offset + 1) +
                "\"" + prefix + str(self.decision) + "\","
            )
            return
        else:
            print(
                "  " * offset +
                "tree(\"" + prefix + self.feature.format_question() + "\","
            )
            options = self.feature.format_options()

            self.left._print_typst(
                prefix=options[0] + "\\n",
                offset=offset + 1
            )

            self.right._print_typst(
                prefix=options[1] + "\\n",
                offset=offset + 1,
            )

        print(
            "  " * offset +
            ")" + ("," if offset != 0 else "")
        )


def _ok_features_i(features, parent_choices):
    return [
        feature_i for feature_i, feature in enumerate(features)
        if all(x in parent_choices for x in features[feature_i].prerequisites)
    ]
