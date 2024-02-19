import numpy as np

def get_qe_predictions(score, error_level=10):
    """
    Error level is the scale in normal addition. The base is 10 because score ranges from 0 to 100.
    """
    score = score + np.random.normal(scale=error_level)
    score = np.clip(score, a_min=0, a_max=100)
    return score

def get_mae(data, phase):
    a = [x["score"] for x in data if x["phase"] == phase]
    b = [x["score_ai"] for x in data if x["phase"] == phase]
    return np.average([np.abs(a - b) for a, b in zip(a, b)])
