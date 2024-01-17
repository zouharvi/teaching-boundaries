TAGS_CONFIGURATIONS = {
    "all": {"domain", "length_question", "length_answer", "entity", "confidence"},
    "3": {"domain", "length_question", "confidence"},
}

def configuration_to_tags(configuration, allowed_tags=TAGS_CONFIGURATIONS["all"]):
    configuration = {
        "domain": "question from " + configuration["domain"] + " domain",
        "length_question": "short question" if configuration["length_question"] == "short" else "long question",
        "length_answer": "short answer" if configuration["length_answer"] == "short" else "long answer",
        "entity": "answer is " + configuration["entity"],
        "confidence": configuration["confidence"],
    }
    return [configuration[k] for k,v  in configuration.items() if k in allowed_tags]


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