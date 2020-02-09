import json

d = dict()

with open('imdb_afi_el.dev.json', 'r') as fin:
    for item in json.loads(fin.read()):
        url = item['imdb_movie']
        d[url] = d.get(url, set()) | {item.get('afi_movie')}
    fin.close()

with open('Zongdi_Xu_hw03_imdb_afi_el.json', 'r') as fin:
    for item in json.loads(fin.read()):
        url = item['imdb_movie']
        if url in d:
            d[url] = d.get(url, set()) | {item.get('afi_movie')}
    fin.close()

same, diff = (0, 0)
for k,v in d.items():
    if len(v)==1:
        same += 1
    elif len(v)>1:
        print(k, v, sep=":")
        diff += 1
print(f'same:{same}, diff:{diff}')