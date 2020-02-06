# %% [markdown]
# # INF 558: Building Knowledge Graphs
# ## Report of Homework2: Information Extraction
# ### Author: Zongdi Xu (USC ID 5900-5757-70)
# ### Date: Jan 30, 2020

# %%
# !python3 -m spacy download en_core_web_sm
import spacy
import en_core_web_sm
import csv
nlp = en_core_web_sm.load()


# %%
sentence = nlp("He played the coach on TV's Mister Peepers")

from spacy import displacy
options = {"distance": 96}
displacy.render(sentence, style="dep", options=options)

# %% [markdown]
# ### Task 2.2
# 
# %% [markdown]
# The template to apply extrators to the original entries:


# %% [markdown]
# #### Lexical Extractors

# %%
pattern_spouse_lexical = [
            {'LOWER': 'married'},
            {'OP': '*'},
            {'LOWER': 'to'},
            {'TEXT': {'REGEX': '\s*'}, 'OP': '*'},
            {'IS_PUNCT': True, 'OP': '*'},
            {'TEXT': {'REGEX': '\s*'}, 'OP': '+'},
            ]


# %%
pattern_parent_lexical = [
            {'LOWER': 'born'},
            {'OP': '*'},
            {'LOWER': 'to'},
            {'TEXT': {'REGEX': '\s*'}, 'OP': '*'},
            {'IS_PUNCT': True, 'OP': '*'},
            {'TEXT': {'REGEX': '\s*'}, 'OP': '+'},
            {'IS_PUNCT': True, 'OP': '*'},
            {'LOWER': 'and','OP': '?'},
            {'TEXT': {'REGEX': '\s*'}, 'OP': '*'},
            {'IS_PUNCT': True, 'OP': '*'},
            {'TEXT': {'REGEX': '\s*'}, 'OP': '+'},
            {'IS_PUNCT': True, 'OP': '*'},
            ]


# %%
pattern_education_lexical = [
            {'TEXT': {'REGEX': '^(attend|attended)$'}},
            {'OP': '+'},
            ]


# %%
pattern_starred_in_lexical = [
            {'TEXT': {'REGEX': '^(star|starred)$'}},
            {'LOWER': 'in'},
            {'OP': '+'},
            ]

# %% [markdown]
# #### Syntactic Extractors

# %%
# define the pattern 
pattern_spouse_syntactic = [
            {'POS': 'ADJ', 'LOWER': 'married'},
            {'OP': '*'},
            {'LOWER': 'to', 'POS': 'ADP'},
            {'POS': 'ADJ', 'OP': '*'},
            {'POS': 'NOUN', 'OP': '*'},
            {'IS_PUNCT': True, 'OP': '*'},
            {'ENT_TYPE': 'PERSON', 'OP': '+'},
            ]


# %%
pattern_parent_syntactic = [
            {'POS': 'VERB', 'ORTH': 'born'},
            {'OP': '*'},
            {'LOWER': 'to', 'POS': 'ADP'},
            {'POS': 'ADJ', 'OP': '*'},
            {'POS': 'NOUN', 'OP': '*'},
            {'IS_PUNCT': True, 'OP': '*'},
            {'ENT_TYPE': 'PERSON', 'OP': '+'},
            {'IS_PUNCT': True, 'OP': '*'},
            {'LOWER': 'and', 'POS': 'CCONJ', 'OP': '?'},
            {'POS': 'ADJ', 'OP': '*'},
            {'POS': 'NOUN', 'OP': '*'},
            {'IS_PUNCT': True, 'OP': '*'},
            {'ENT_TYPE': 'PERSON', 'OP': '+'},
            {'IS_PUNCT': True, 'OP': '*'},
            ]


# %%
pattern_education_syntactic = [
            {'POS': 'VERB', 'LEMMA': 'attend'},
            {'OP': '+'},
            ]


# %%
pattern_starred_in_syntactic = [
            {'POS': 'VERB', 'LEMMA': 'star'},
            {'POS': 'ADP', 'LOWER': 'in'},
            {'OP': '+'},
            ]


# %%

# %%
import csv
from spacy.matcher import Matcher
tsv_reader = csv.reader(open('bios.tsv'), delimiter='\t')

limit = 500
count = 0

def matching(doc, pattern):
    result = []
    for sent in doc.sents:
        matcher = Matcher(nlp.vocab) 
        matcher.add("matching", None, pattern)  

        matches = matcher(nlp(str(sent))) 
        if len(matches)>0:
            match = matches[-1]
            span = sent[match[1]:match[2]] 
            result.append(span.text)

    return result

def max_length(list1, list2):
    if len(list1)>len(list2):
        return list1
    else:
        return list2

with open('cast.jl', 'w') as fout:
    for (idx, (url, bio)) in enumerate(tsv_reader):
        count += 1
        result = {}
        result['url'] = url
        result['spouse'] = max_length(matching(nlp(bio), pattern_spouse_lexical), matching(nlp(bio), pattern_spouse_syntactic))
        result['education'] = max_length(matching(nlp(bio), pattern_education_lexical), matching(nlp(bio), pattern_education_syntactic))
        result['parent'] = max_length(matching(nlp(bio), pattern_parent_lexical), matching(nlp(bio), pattern_parent_syntactic))
        result['starred_in'] = max_length(matching(nlp(bio), pattern_starred_in_lexical), matching(nlp(bio), pattern_starred_in_syntactic))
        fout.write(str(result)+'\n')
        if count>=limit:
            break
        pass
    fout.close()

