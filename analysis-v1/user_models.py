import random
from sklearn.metrics import accuracy_score
from analysis import ai_generator

def _sklearn_model(data_xy, k, Model):
    scores_datasets = []

    for seed in range(200):
        data_subset = random.Random(seed).sample(data_xy, k=k)
        # skip subsets with only one target class
        data_y = [y for x, y in data_subset]
        if all(data_y) or not any(data_y):
            continue
        model = Model()
        data_x_binary = [
            [
                v == option
                for feature, v in x["configuration"].items()
                for option in ai_generator.FEATURES_OPTIONS[feature]
            ]
            for x, y in data_subset
        ]
        data_x_binary_all = [
            [
                v == option
                for feature, v in x["configuration"].items()
                for option in ai_generator.FEATURES_OPTIONS[feature]
            ]
            for x, y in data_xy
        ]

        model.fit(data_x_binary, data_y)
        data_y_pred = model.predict(data_x_binary_all)
        # maximize score across the whole dataset, not just test
        score = accuracy_score([y for x, y in data_xy], data_y_pred)
        scores_datasets.append((score, data_subset))
        print(f"{score:.2%}")

    return scores_datasets

def tree_simple(data_xy, k: int):
    from sklearn.tree import DecisionTreeClassifier
    
    scores_datasets = _sklearn_model(data_xy, k, DecisionTreeClassifier)
    best = max(scores_datasets, key=lambda x: x[0])
    print(f"Best: {best[0]:.2%}")

    # return best subset
    return best[1]

def anti_tree_simple(data_xy, k: int):
    from sklearn.tree import DecisionTreeClassifier
    
    scores_datasets = _sklearn_model(data_xy, k, DecisionTreeClassifier)
    best = min(scores_datasets, key=lambda x: x[0])
    print(f"Best: {best[0]:.2%}")

    # return best subset
    return best[1]


def logistic_regression_simple(data_xy, k: int):
    from sklearn.linear_model import LogisticRegression
    
    scores_datasets = _sklearn_model(data_xy, k, LogisticRegression)
    best = max(scores_datasets, key=lambda x: x[0])
    print(f"Best: {best[0]:.2%}")

    # return best subset
    return best[1]

def anti_logistic_regression_simple(data_xy, k: int):
    from sklearn.linear_model import LogisticRegression
    
    scores_datasets = _sklearn_model(data_xy, k, LogisticRegression)
    best = min(scores_datasets, key=lambda x: x[0])
    print(f"Best: {best[0]:.2%}")

    # return best subset
    return best[1]


def imbalanced_random_subset(data_xy, k: int):
    return random.sample(data_xy, k=k)

def balanced_random_subset(data_xy, k: int):
    positive_count = int(k*sum([y for x, y in data_xy])/len(data_xy))
    data = random.sample([(x,y) for x,y in data_xy if y], k=positive_count)
    data += random.sample([(x,y) for x,y in data_xy if not y], k=k-positive_count)
    random.shuffle(data)
    return data


def knn_simple(data_xy, k: int):
    from sklearn.neighbors import KNeighborsClassifier
    
    scores_datasets = _sklearn_model(data_xy, k, lambda: KNeighborsClassifier(n_neighbors=2))
    best = max(scores_datasets, key=lambda x: x[0])
    print(f"Best: {best[0]:.2%}")

    # return best subset
    return best[1]


def knn_decay(data_xy, k: int):
    import numpy as np
    class DecayingKNeighborsClassifier:

        def __init__(self, n_neighbors):
            self.n_neighbors = n_neighbors

        def fit(self, data_x, data_y):
            self.data_x = np.array(data_x)*1.0
            self.data_y = np.array(data_y)*1.0
            # TODO: decay here?
            self.data_x_decay = np.arange(start=1, stop=self.data_x.shape[0]+1)/self.data_x.shape[0]
        
        def predict(self, data_x):
            return [
                self.predict_single(x) for x in data_x
            ]
    
        def predict_single(self, x):
            x = np.array([x])*1.0
            x = np.repeat(x, self.data_x.shape[0], axis=0)
            dists = np.linalg.norm(self.data_x-x, axis=1)

            i_neighbour = np.argpartition(dists, self.n_neighbors)[:self.n_neighbors]

            # mask
            pred = np.average(self.data_y[i_neighbour], weights=self.data_x_decay[i_neighbour])
            return pred > 0.5

    scores_datasets = _sklearn_model(data_xy, k, lambda: DecayingKNeighborsClassifier(n_neighbors=2))
    best = max(scores_datasets, key=lambda x: x[0])
    print(f"Best: {best[0]:.2%}")

    # return best subset
    return best[1]

MODELS = {
    "imbalanced_random": imbalanced_random_subset,
    "random": balanced_random_subset,
    "tree_simple": tree_simple,
    "anti_tree_simple": anti_tree_simple,
    "linear_simple": logistic_regression_simple,
    "anti_linear_simple": anti_logistic_regression_simple,
    "knn_simple": knn_simple,
    "knn_decay": knn_decay,
}
