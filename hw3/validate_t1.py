import json

d = dict()

with open('imdb_afi_el.dev.json', 'r') as fin:
    for item in json.loads(fin.read()):
        url = item['imdb_movie']
        d[url] = d.get(url, []) + [item.get('afi_movie')]
    fin.close()

with open('imdb_afi_el.json', 'r') as fin:
    for item in json.loads(fin.read()):
        url = item['imdb_movie']
        if url in d:
            d[url] = d.get(url, []) + [item.get('afi_movie')]
    fin.close()


for k,v in d.items():
    print(k, v, sep=':')