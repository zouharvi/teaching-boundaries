import json

data = [json.loads(x) for x in open("computed/dataset_base.jsonl", "r")]
data_new = []

undecided = 0
for line in data:
    word_count = len(line["answer"].split())
    if word_count <= 10:
        line["configuration"]["length_answer"] = "short"
        data_new.append(line)
    elif word_count >= 20:
        line["configuration"]["length_answer"] = "long"
        data_new.append(line)
    else:
        undecided += 1

print("Dropping", undecided, "/", len(data))

with open("computed/dataset_base.jsonl", "w") as f:
    f.write("\n".join([json.dumps(x, ensure_ascii=False) for x in data_new]))