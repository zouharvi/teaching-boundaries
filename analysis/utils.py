def configuration_to_tags(configuration):
    return [
        configuration["domain"] + " domain",
        "short question" if configuration["length_question"] == "short" else "long question",
        "short answer" if configuration["length_answer"] == "short" else "long answer",
        "answer is " + configuration["entity"],
        configuration["confidence"],
    ]