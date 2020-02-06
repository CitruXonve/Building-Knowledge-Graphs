# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'

# %%
import json

source_list = []

with open('../hw1/Zongdi_Xu_hw01_scrapy_cast.jl') as fin:
    for line in fin.readlines():
        source_list.append(json.loads(line)['url'])
        pass

# print(source_list[-10:])


# %%
from bs4 import BeautifulSoup
import requests
import re

fout = open('entities_bio.tsv', 'w')

limit = 500
count = 0

for url in source_list:
    count += 1
    response = requests.get(url+'bio?ref_=nm_ov_bio_sm')
    soup = BeautifulSoup(response.content)
    elems = soup.find(id='bio_content').select('div.soda.odd > p')
    if len(elems)>0:
        text = elems[0].text.strip()
        text = re.sub(r'\s+', ' ', text)
        fout.write(url+'\t'+text.strip()+'\n')
    if count>=limit:
        break

fout.close()


# %%


