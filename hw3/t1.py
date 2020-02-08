import rltk
import json
import re

# RLTK IMDB Record
class IMDBRecord(rltk.Record):
    def __init__(self, raw_object):
        super().__init__(raw_object)
        self.name = ''

    @rltk.cached_property
    def id(self):
        return self.raw_object['url']

    @rltk.cached_property
    def name_string(self):
        return self.raw_object['name']

    @rltk.cached_property
    def name_tokens(self):
        return set(tokenizer.tokenize(self.name_string))

# RLTK AFI Record
class AFIRecord(rltk.Record):
    def __init__(self, raw_object):
        super().__init__(raw_object)
        self.name = ''

    @rltk.cached_property
    def id(self):
        return self.raw_object['url']

    @rltk.cached_property
    def name_string(self):
        return self.raw_object['title']

def name_string_similarity_1(r_imdb, r_afi):
    s1 = r_imdb.name_string.lower()[:8]
    s2 = r_afi.name_string.lower()[:8]

    return rltk.jaro_winkler_similarity(s1, s2)


def name_string_similarity_2(r_imdb, r_afi):
    s1 = r_imdb.name_string.lower()[-8:]
    s2 = r_afi.name_string.lower()[-8:]

    return rltk.levenshtein_similarity(s1, s2)


def name_string_similarity_3(r_imdb, r_afi):
    s1 = ''.join(sorted(re.split(r'[-,\s]+', r_imdb.name_string.lower())))
    s2 = ''.join(sorted(re.split(r'[-,\s]+', r_afi.name_string.lower())))

    return rltk.jaro_winkler_similarity(s1, s2)


def name_string_similarity_4(r_imdb, r_afi):
    s1 = ''.join(sorted(re.split(r'[-,\s]+', r_imdb.name_string.lower())))
    s2 = ''.join(sorted(re.split(r'[-,\s]+', r_afi.name_string.lower())))

    return rltk.levenshtein_similarity(s1, s2)

# entity linkage scoring function
def rule_based_method(r_imdb, r_afi):
    score_1 = name_string_similarity_1(r_imdb, r_afi)
    score_2 = name_string_similarity_2(r_imdb, r_afi)
    score_3 = name_string_similarity_3(r_imdb, r_afi)
    score_4 = name_string_similarity_4(r_imdb, r_afi)

    name_1 = re.sub(r'[-,\s]+', '', r_imdb.name_string.lower().strip())
    name_2 = re.sub(r'[-,\s]+', '', r_afi.name_string.lower().strip())

    year_1 = r_imdb.raw_object.get('year', '')
    year_2 = r_afi.raw_object.get('release_date', '').strip()

    score = 1.1 if name_1 == name_2 \
        else 0.2 * score_1 + 0.3 * score_2 + 0.3 * score_3 + 0.2 * score_4

    match_year = abs(int(r_imdb.raw_object.get('year')) - int(re.search(r'[0-9]{4}', r_afi.raw_object.get('release_date'))[0])) <= 1 \
        if r_imdb.raw_object.get('year') is not None and re.search(r'[0-9]{4}', r_afi.raw_object.get('release_date', '')) is not None \
        else True
    match_genre = len(set(word[:3] for word in re.split(r'[-,\s]+', r_imdb.raw_object.get('genre', '').lower().strip())) &
                      set(word[:3] for word in re.split(r'[-,\s]+', r_afi.raw_object.get('genre', '').lower().strip()))) > 0 \
        if r_imdb.raw_object.get('genre') is not None and r_afi.raw_object.get('genre') is not None else True

    # if name_1 == 'astreetcarnameddesire': # FN
    # if name_1 == 'rocky': # FN
    # if name_1 == 'diehard': # FN
    # if name_1 == 'anatomyofamurder': # FP
    # if name_1 == 'argo': # FP
    #     print(match_year, match_genre, score, name_1, name_2)

    return match_year or match_genre and score > 1.0, score

# threshold value to determine if we are confident the record match
MY_TRESH = 0.59

imdb_file = 'imdb.jl'
afi_file = 'afi.jl'

def worker():
    tokenizer = rltk.CrfTokenizer()

    # load Datasets
    ds_imdb = rltk.Dataset(reader=rltk.JsonLinesReader(
        imdb_file), record_class=IMDBRecord, adapter=rltk.MemoryKeyValueAdapter())
    ds_afi = rltk.Dataset(reader=rltk.JsonLinesReader(
        afi_file),  record_class=AFIRecord,  adapter=rltk.MemoryKeyValueAdapter())
    valid_match = []
    for r_imdb in ds_imdb:
        # test this record with AFI records
        optimum = (None, MY_TRESH)
        for r_afi in ds_afi:
            result, confidence = rule_based_method(r_imdb, r_afi)
            if result and confidence > optimum[1]:
                optimum = (r_afi, confidence)

        if optimum[0] is not None:
            r_afi, confidence = optimum
            valid_match.append(
                {'imdb_movie': r_imdb.raw_object['url'], 'afi_movie': r_afi.raw_object['url']})
        else:
            valid_match.append(
                {'imdb_movie': r_imdb.raw_object['url'], 'afi_movie': None})

    fout = open('imdb_afi_el.json', 'w')
    fout.write(json.dumps(valid_match, indent=4))
    fout.close()

if __name__ == '__main__':
    worker()