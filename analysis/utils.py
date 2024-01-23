TAGS_CONFIGURATIONS = {
    "all": {"domain", "length_answer", "entity", "confidence"},
    "3": {"domain", "length_answer", "confidence"},
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
        "entity": "is about" + highlight(configuration["entity"]),
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