import random
import decision_tree
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

random.seed(0)
tree = decision_tree.Tree.generate_random(8)

random_data = random.Random(0)
data_x = [
    random_data.choices([0, 1], k=len(decision_tree.FEATURES))
    for _ in range(10_000)
]
data_y = [
    tree(x) for x in data_x
]
data_xy = list(zip(data_x, data_y))

tree.print_typst()

best_score = 0
for seed in range(100):
    data_subset = random.Random(seed).sample(data_xy, k=10)
    model = DecisionTreeClassifier()
    model.fit(
        [x for x, y in data_subset],
        [y for x, y in data_subset],
    )
    data_y_pred = model.predict(data_x)
    score = accuracy_score(data_y, data_y_pred)
    print(f"{score:.2%}")
    best_score = max(best_score, score)

print(f"Best: {best_score:.2%}")