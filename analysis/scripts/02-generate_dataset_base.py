import itertools

DOMAINS = {"history": "history domain between 1500AD and 2000AD", "biology": "biology domain"}
ENTITIES = {"person": "a fake person", "number": "a number/quantity", "explanation": "an explanation"}
LENGTHS_QUESTION = {"short": "at most 10 words", "long": "at least 20 words"}
LENGTHS_ANSWER = {"short": "at most 5 words", "long": "at least 10 words with elaboration"}
PROMPT = """
Please generate a fake but plausible-sounding questions and ansfers from the {DOMAIN}.
The question should be completely made up and not be grounded in reality and rather be completely made-up.
Do not use real places, people, objects, or events. However, the questions should be very specific, so please make up the plausible-sounding details and fictional entities.
The questions and answers should not be blatantly incorrect or "Unknown". Very importantly, a person should not be able to tell if the answer is correct.
The answer to the question should be {ENTITY}.
The length of the question should be {LENGTH_QUESTION} and the length of the answer should be {LENGTH_ANSWER}.
Please output only the question and the answer in JSON format and nothing else.
The JSON format is:
```
{
    "question": QUESTION,
    "answer": ANSWER
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

for domain, entity, length_question, length_answer in tqdm.tqdm(itertools.product(DOMAINS.items(), ENTITIES.items(), LENGTHS_QUESTION.items(), LENGTHS_ANSWER.items())):
    prompt = (
        PROMPT
        .replace("{DOMAIN}", domain[1])
        .replace("{ENTITY}", entity[1])
        .replace("{LENGTH_QUESTION}", length_question[1])
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
                    "length_question": length_question[0],
                    "length_answer": length_answer[0],
                }
                fout.write(json.dumps(content, ensure_ascii=False)+"\n")
                break
            except Exception as e:
                patience -= 1
                print(patience, e, content)
        fout.flush()

fout.close()