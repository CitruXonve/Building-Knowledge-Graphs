import re, json
import spacy
from collections import Counter
from string import punctuation

def get_hotwords(text):
    result = []
    pos_tag = ['PROPN', 'ADJ', 'NOUN'] # 1
    doc = nlp(text.lower()) # 2
    for token in doc:
        # 3
        if(token.text in nlp.Defaults.stop_words or token.text in punctuation):
            continue
        # 4
        if(token.pos_ in pos_tag):
            result.append(token.text)

    return result
                
output_buffer = {}
nlp = spacy.load("en_core_web_lg")

def parse_source1(line):
    item = json.loads(line)
    unique_id = item['url']
        
    # data clean
    if item.get('description') is not None:
        text = re.sub(r'<(?!br\s*\/?)[^>]+>', '', item['description'])
        text = re.sub(r'\u00a0', ' ', text)
        text = re.sub('<br>|\s*(\\n)+\s*', '\n', text)
        text = re.sub('\s*(\\t)+\s*', ' ', text)
        item.update({'description': text})
    else:
        text = None

    if item['type'] == 'course':

        if item['title'].split()[0]!='CSCI':
            return

        if text is not None:
            text = re.sub('Print-Friendly Page|Close Window', '', text)
            item.update({'description': text})

        item.update({'abbr': '-'.join(item['title'].split()[:2])})
        unique_id = item['abbr']

        item.update({'keywords': [item for items, c in Counter(get_hotwords(' '.join(item['title'].split()[2:]))).most_common() 
                                for item in [items]]}) # sort by frequency and remove duplicates
        # keyword extraction

        pass

    if unique_id in output_buffer:
        output_buffer[unique_id].update(item)
    else:
        output_buffer[unique_id] = item
    pass

def parse_source2(line):
    item = json.loads(line)
    # unique_id = item['url']

    if item['type'] == 'course':
        unique_id = item['abbr']

        item.update({'keywords': [item for items, c in Counter(get_hotwords(' '.join(item['title'].split()))).most_common() 
                                for item in [items]]}) # sort by frequency and remove duplicates
    elif item['type'] == 'textbook':
        unique_id = item['ISBN']
    elif item['type'] == 'instructor':
        unique_id = item['link']
    else:
        unique_id = item['url']

    if unique_id in output_buffer:
        output_buffer[unique_id].update(item)
    else:
        output_buffer[unique_id] = item
    pass

with open("./scrapy_USC_program.jl", "r") as fin:
    for line in fin.readlines():
        parse_source1(line)
    fin.close()

with open('./scrapy_USC_classes.jl', "r") as fin:
    for line in fin.readlines():
        parse_source2(line)
    fin.close()

with open("./keywords_of_USC_course.jl", "w") as fout:
    for url, item in sorted(output_buffer.items()):
        if item['type'] == 'course':
            fout.write(json.dumps(item, indent=2)+'\n')
    fout.close()

with open("./keywords_of_USC_program.jl", "w") as fout:
    for url, item in output_buffer.items():
        if item['type'] == 'program':
            fout.write(json.dumps(item, indent=2)+'\n')
    fout.close()

with open("./keywords_of_USC_instructor.jl", "w") as fout:
    for url, item in output_buffer.items():
        if item['type'] == 'instructor':
            fout.write(json.dumps(item, indent=2)+'\n')
    fout.close()

with open("./keywords_of_USC_textbook.jl", "w") as fout:
    for url, item in output_buffer.items():
        if item['type'] == 'textbook':
            fout.write(json.dumps(item, indent=2)+'\n')
    fout.close()