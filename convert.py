import json
with open("index_data/final_index.json", "r") as f:
    index = json.load(f)

lex ={}
with open("index_data/index.txt", "w") as f:
    for word, posting in index.items():
        offset = f.tell()
        lex[word] = offset
        f.write(json.dumps(posting) + "\n")

with open("index_data/lexicon.json", "w") as f:
    json.dump(lex, f)
