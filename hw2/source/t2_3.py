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


# %% [markdown]
# ### Task 2.3

# %%
import csv
from spacy.matcher import Matcher
tsv_reader = csv.reader(open('entities_bio.tsv'), delimiter='\t')

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
with open('cast_lexical.jl', 'w') as fout:
    for (idx, (url, bio)) in enumerate(tsv_reader):
        count += 1
        result = {}
        result['url'] = url
        result['spouse'] = matching(nlp(bio), pattern_spouse_lexical)
        result['education'] = matching(nlp(bio), pattern_education_lexical)
        result['parent'] = matching(nlp(bio), pattern_parent_lexical)
        result['starred_in'] = matching(nlp(bio), pattern_starred_in_lexical)
        fout.write(str(result)+'\n')
        if count>=limit:
            break
        pass
    fout.close()

limit = 500
count = 0

# %%
with open('cast_syntactic.jl', 'w') as fout:
    for (idx, (url, bio)) in enumerate(tsv_reader):
        count += 1
        result = {}
        result['url'] = url
        result['spouse'] = matching(nlp(bio), pattern_spouse_syntactic)
        result['education'] = matching(nlp(bio), pattern_education_syntactic)
        result['parent'] = matching(nlp(bio), pattern_parent_syntactic)
        result['starred_in'] = matching(nlp(bio), pattern_starred_in_syntactic)
        fout.write(str(result)+'\n')
        if count>=limit:
            break
        pass
    fout.close()