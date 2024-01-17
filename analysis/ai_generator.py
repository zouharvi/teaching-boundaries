import copy
import random


class Feature():
    decision = None
    option = None

    def __init__(self, name, options):
        self.name = name
        self.options = options

    def format_question(self):
        return self.name

    def format_options(self):
        return ["=" + self.option, "≠" + self.option]


FEATURES = [
    Feature(name="domain", options=["history", "biology"]),
    Feature(name="length_question", options=["short", "long"]),
    Feature(name="length_answer", options=["short", "long"]),
    Feature(name="entity", options=["person", "number", "explanation"]),
    Feature(name="confidence", options=[
            "low AI confidence", "high AI confidence"]),
]

FEATURES_OPTIONS = {}
for feature in FEATURES:
    FEATURES_OPTIONS[feature.name] = feature.options


class Tree():
    def __init__(self, feature, decision=None):
        self.feature = feature
        self.left = None
        self.right = None
        self.decision = decision

    def __call__(self, x: dict):
        if self.decision is not None:
            return self.decision
        else:
            # if it equals then it goes left
            if x[self.feature.name] == self.feature.option:
                return self.left(x)
            else:
                return self.right(x)

    @staticmethod
    def generate_random(allowed_nodes, features=FEATURES, random_state=random.Random()):
        features = copy.deepcopy(features)
        feature = features.pop(random_state.choice(range(len(features))))

        # if it's equal it goes left, if it's not it goes right
        feature.option = random_state.choice(feature.options)

        if allowed_nodes <= 2:
            node = Tree(feature)
            node.left = Tree(feature=None, decision=False)
            node.right = Tree(feature=None, decision=True)
            return node

        allowed_nodes -= 1

        nodes_left = random_state.randint(1, allowed_nodes - 1)
        child_left = Tree.generate_random(
            nodes_left, features, random_state
        )
        child_right = Tree.generate_random(
            allowed_nodes - nodes_left, features, random_state
        )
        node = Tree(feature)
        node.left = child_left
        node.right = child_right
        return node

    def print(self):
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


class LogisticRegression():
    def __init__(self, features=FEATURES, random_state=random.Random()):
        self.acceptance_threshold = random_state.randint(1, len(features) - 1)
        self.features_polarity = [
            (feature, random_state.choice(feature.options))
            for feature in features
        ]

    def __call__(self, x: dict) -> bool:
        score = sum(
            x[feature.name] == option
            for feature, option in self.features_polarity
        )
        return score >= self.acceptance_threshold

    def print(self):
        print(
            "+".join(
                f"[{feature.name} = {option}]"
                for feature, option in self.features_polarity
            ),
            ">=", self.acceptance_threshold
        )