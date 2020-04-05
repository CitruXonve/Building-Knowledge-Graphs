from typing import Dict, Tuple
import json, rltk, re

DATA_SOURCE_FILE1 = "./data_source1.json"
DATA_SOURCE_FILE2 = "./data_source2.json"
DATA_TARGET_FILE = "./same_paper_truth.txt"

with open(DATA_SOURCE_FILE1, "r") as fin:
    item_list1 = json.loads(fin.read())

with open(DATA_SOURCE_FILE2, "r") as fin:
    item_list2 = json.loads(fin.read())

with open(DATA_TARGET_FILE, "r") as fin:
    # range = Dict[Tuple[str, str], int]
    range = {}
    for line in fin.readlines():
        item1, item2, value = line.split()
        range[(item1, item2)] = eval(value)

# cached_titles = Dict[str, str]
cached_titles = {}

def get_cached_title(id:str, original_title:str) -> str:
    if cached_titles.get(id) is not None:
        return cached_titles.get(id)
    cached_titles[id] = ''.join(sorted(re.split(r'[-,\s]+', original_title.lower())))
    return cached_titles[id]

def title_similarity(title1: str, title2: str) -> float:
    return rltk.jaro_winkler_similarity(title1, title2)

def year_similarity(year1: str, year2: str) -> float:
    return 1.0 if year1 == "" or year2 == "" else rltk.levenshtein_similarity(year1, year2)

# sim_obs = Dict[Tuple[str, str], Tuple[float, float]]
sim_obs = {}
for item1 in item_list1:
    sim1, sim2 = 0, 0
    chosen = None
    for item2 in item_list2:
        if (item1["id"], item2["id"]) in range:
            if (title_similarity(get_cached_title(item1["id"], item1["title"]), get_cached_title(item2["id"], item2["title"])) > sim1):
                sim1, sim2 = title_similarity(get_cached_title(item1["id"], item1["title"]), get_cached_title(item2["id"], item2["title"])) , year_similarity(item1["year"], item2["year"])
                chosen = item2
    if chosen is not None:
        sim_obs[(item1["id"], item2["id"])] = (sim1, sim2)

with open("covered.txt", "w") as fout:
    for item_pair, values in sorted(sim_obs.items()):
        if values[0] >= 0.8 and values[1] >= 0.75:
            fout.write(f'{item_pair[0]}\t{item_pair[1]}\t{1, values}\n')

with open("uncovered.txt", "w") as fout:
    for item_pair, value in sorted(range.items()):
        if value == 1:
            fout.write(f'{item_pair[0]}\t{item_pair[1]}\t{value}\n')