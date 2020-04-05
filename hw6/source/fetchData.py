import json, rltk, re

DATA_SOURCE_FILE1 = "./data_source1.json"
DATA_SOURCE_FILE2 = "./data_source2.json"
DATA_TARGET_FILE = "./same_paper_targets.txt"

DATA_OBS_FILE1 = "./title_sim_obs.txt"
DATA_OBS_FILE2 = "./years_sim_obs.txt"

with open(DATA_SOURCE_FILE1, "r") as fin:
    item_list1 = json.loads(fin.read())

with open(DATA_SOURCE_FILE2, "r") as fin:
    item_list2 = json.loads(fin.read())

with open(DATA_TARGET_FILE, "r") as fin:
    range = set()
    for line in fin.readlines():
        range.add(tuple(line.split()))

cached_titles = dict()

def get_cached_title(id:str, original_title:str) -> str:
    if cached_titles.get(id) is not None:
        return cached_titles.get(id)
    cached_titles[id] = ''.join(sorted(re.split(r'[-,\s]+', original_title.lower())))
    return cached_titles[id]

def title_similarity(title1: str, title2: str) -> float:
    return rltk.jaro_winkler_similarity(title1, title2)

def year_similarity(year1: str, year2: str) -> float:
    return 1.0 if year1 == "" or year2 == "" else rltk.levenshtein_similarity(year1, year2)

title_sim_obs = []
years_sim_obs = []
for item1 in item_list1:
    for item2 in item_list2:
        if (item1["id"], item2["id"]) in range:
            title_sim_obs.append((item1["id"], item2["id"], title_similarity(get_cached_title(item1["id"], item1["title"]), get_cached_title(item2["id"], item2["title"]))))
            years_sim_obs.append((item1["id"], item2["id"], year_similarity(item1["year"], item2["year"])))

with open(DATA_OBS_FILE1, "w") as fout:
    for id1, id2, sim in title_sim_obs:
        fout.write(f'{id1}\t{id2}\t{sim}\n')

with open(DATA_OBS_FILE2, "w") as fout:
    for id1, id2, sim in years_sim_obs:
        fout.write(f'{id1}\t{id2}\t{sim}\n')