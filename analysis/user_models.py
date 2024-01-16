import random
from sklearn.metrics import accuracy_score
from analysis import decision_tree

def decision_tree_simple(data_xy, k=10):
    from sklearn.tree import DecisionTreeClassifier
    scores_datasets = []

    for seed in range(100):
        data_subset = random.Random(seed).sample(data_xy, k=k)
        model = DecisionTreeClassifier()
        data_x_binary = [
            [
                v == option
                for feature, v in x["configuration"].items()
                for option in decision_tree.FEATURES_OPTIONS[feature]
            ]
            for x, y in data_subset
        ]
        data_x_binary_all = [
            [
                v == option
                for feature, v in x["configuration"].items()
                for option in decision_tree.FEATURES_OPTIONS[feature]
            ]
            for x, y in data_xy
        ]

        model.fit(
            data_x_binary,
            [y for x, y in data_subset],
        )
        data_y_pred = model.predict(data_x_binary_all)
        score = accuracy_score([y for x, y in data_xy], data_y_pred)
        scores_datasets.append((score, data_subset))
        print(f"{score:.2%}")

    best = max(scores_datasets, key=lambda x: x[0])
    print(f"Best: {best[0]:.2%}")

    # return best subset
    return best[1]

def logistic_regression_simple(data_xy, k=10):
    from sklearn.linear_model import LogisticRegression
    scores_datasets = []

    for seed in range(100):
        data_subset = random.Random(seed).sample(data_xy, k=k)
        # all single class
        if all(y for x, y in data_subset) or all(not y for x, y in data_subset):
            continue
        model = LogisticRegression()
        data_x_binary = [
            [
                v == option
                for feature, v in x["configuration"].items()
                for option in decision_tree.FEATURES_OPTIONS[feature]
            ]
            for x, y in data_subset
        ]
        data_x_binary_all = [
            [
                v == option
                for feature, v in x["configuration"].items()
                for option in decision_tree.FEATURES_OPTIONS[feature]
            ]
            for x, y in data_xy
        ]

        model.fit(
            data_x_binary,
            [y for x, y in data_subset],
        )
        data_y_pred = model.predict(data_x_binary_all)
        score = accuracy_score([y for x, y in data_xy], data_y_pred)
        scores_datasets.append((score, data_subset))
        print(f"{score:.2%}")

    best = max(scores_datasets, key=lambda x: x[0])
    print(f"Best: {best[0]:.2%}")

    # return best subset
    return best[1]


def random_subset(data_xy, k=10):
    return random.sample(data_xy, k=k)