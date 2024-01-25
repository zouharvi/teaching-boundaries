TAGS_CONFIGURATIONS = {
    "all": {"domain", "length_answer", "entity", "confidence"},
    "3": {"domain", "length_answer", "entity"},
    "2": {"domain", "length_answer"},
    "domain": {"domain"},
    "length_answer": {"length_answer"},
}

def configuration_to_tags(configuration, allowed_tags=TAGS_CONFIGURATIONS["all"]):
    def highlight(x):
        return f'<span class="tag_span">{x}</span>'

    configuration = {
        "domain": "is about " + highlight(configuration["domain"]),
        "length_answer": "is " + highlight(configuration["length_answer"]),
        "entity": "contains " + highlight(configuration["entity"]),
        "confidence": configuration["confidence"].replace("low", highlight("low")).replace("high", highlight("high")),
    }
    configuration = [
        configuration[k]
        for k, v in configuration.items()
        if k in allowed_tags
    ]
    return f"This fact " + ", ".join(configuration) + "."

def add_fake_ai_confidence(data_x):
    import random
    import copy
    random_data = random.Random(0)
    data_x = copy.deepcopy(data_x)
    for line in data_x:
        line["configuration"]["confidence"] = random_data.choice(
            ["low AI confidence", "high AI confidence"]
        )
    return data_x

def data_to_users(fname, flat=False, cutoff=10) -> dict:
    import collections
    import json
    import numpy as np
    data_user = collections.defaultdict(list)

    data =[
        json.loads(x)
        for x in open(fname, "r")
    ]

    for line in data:
        user = line["user"]["prolific_pid"]
        if not user or len(user) <= 3 or "%" in user:
            continue
        data_user[user].append(line)

    for user, data_local in list(data_user.items()):
        data_train = data_local[:cutoff]
        acc_train = np.average([line["response"] == line["question"]["correct"] for line in data_train])
        if acc_train >= 0.9:
            data_user.pop(user)

    if flat:
        return [v for l in data_user.values() for v in l]
    else:
        return dict(data_user)