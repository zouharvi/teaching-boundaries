import itertools

DOMAINS = {"history": "history domain between 1500AD and 2000AD", "biology": "biology domain"}
ENTITIES = {"person": "a fake person", "number": "a number/quantity", "explanation": "an explanation"}
LENGTHS_ANSWER = {"short": "at most 5 words (very short)", "long": "at least 15 words with elaboration (long)"}
PROMPT = """
Please generate a fake but plausible-sounding fact from the {DOMAIN}.
It should be completely made up and not be grounded in reality and rather be completely made-up.
Do not use real places, people, objects, or events. However, the facts should be very specific, so please make up the plausible-sounding details and fictional entities.
Very importantly, a person should not be able to tell if it is correct.
The fact should be centered around {ENTITY}.
Very importantly, the length should be {LENGTH_ANSWER}.
Please output only the fact in JSON format and nothing else.
The JSON format is:
```
{
    "answer": FACT
}
```
"""

import os
import tqdm
import openai
from analysis.secret import OPENAI_KEY, OPENAI_ORGANIZATION
import json
client = openai.OpenAI(
    api_key=OPENAI_KEY,
    organization=OPENAI_ORGANIZATION
)

FNAME = "computed/dataset_base.jsonl"
if os.path.isfile(FNAME):
    print(f"Refusing to continue because {FNAME} already exists")
    exit()
fout = open(FNAME, "w")

for domain, entity, length_answer in tqdm.tqdm(itertools.product(DOMAINS.items(), ENTITIES.items(), LENGTHS_ANSWER.items())):
    prompt = (
        PROMPT
        .replace("{DOMAIN}", domain[1])
        .replace("{ENTITY}", entity[1])
        .replace("{LENGTH_ANSWER}", length_answer[1])
    )

    # run each configuration multiple times
    for i in range(4):
        # try 4 times before giving up
        patience = 4
        while patience > 0:
            try:
                chat = client.chat.completions.create( 
                    model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt}]
                )
                content = chat.choices[0].message.content
                content = json.loads(content)
                content["configuration"] = {
                    "domain": domain[0],
                    "entity": entity[0],
                    "length_answer": length_answer[0],
                }
                fout.write(json.dumps(content, ensure_ascii=False)+"\n")
                break
            except Exception as e:
                patience -= 1
                print(patience, e, content)
        fout.flush()
fout.close()