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
        return set(rltk.CrfTokenizer().tokenize(self.name_string))

# RLTK AFI Record
class AFIRecord(rltk.Record):
    def __init__(self, raw_object):
        super().__init__(raw_object)
        self.name = ''

    def __hash__(self):
        return self.raw_object['url'].__hash__()

    @rltk.cached_property
    def id(self):
        return self.raw_object['url']

    @rltk.cached_property
    def name_string(self):
        return self.raw_object['title']

def name_string_similarity_1(r_imdb, r_afi):
    s1 = r_imdb.name_string.lower()[:8]
    s2 = cached_names_1.get(r_afi)
    if s2 is None:
        s2 = r_afi.name_string.lower()[:8]
        cached_names_1[r_afi] = s2

    return rltk.jaro_winkler_similarity(s1, s2)


def name_string_similarity_2(r_imdb, r_afi):
    s1 = r_imdb.name_string.lower()[-8:]
    s2 = cached_names_2.get(r_afi)
    if s2 is None:
        s2 = r_afi.name_string.lower()[-8:] 
        cached_names_2[r_afi] = s2

    return rltk.levenshtein_similarity(s1, s2)


def name_string_similarity_3(r_imdb, r_afi):
    s1 = ''.join(sorted(re.split(r'[-,\s]+', r_imdb.name_string.lower())))
    s2 = cached_names_3.get(r_afi)
    if s2 is None:
        s2 = ''.join(sorted(re.split(r'[-,\s]+', r_afi.name_string.lower())))
        cached_names_3[r_afi] = s2

    return rltk.jaro_winkler_similarity(s1, s2)


def name_string_similarity_4(r_imdb, r_afi):
    s1 = ''.join(sorted(re.split(r'[-,\s]+', r_imdb.name_string.lower())))
    s2 = cached_names_4.get(r_afi)
    if s2 is None:
        s2 = ''.join(sorted(re.split(r'[-,\s]+', r_afi.name_string.lower())))
        cached_names_4[r_afi] = s2

    return rltk.levenshtein_similarity(s1, s2)

# entity linkage scoring function
def rule_based_method(r_imdb, r_afi):
    score_1 = name_string_similarity_1(r_imdb, r_afi)
    score_2 = name_string_similarity_2(r_imdb, r_afi)
    score_3 = name_string_similarity_3(r_imdb, r_afi)
    score_4 = name_string_similarity_4(r_imdb, r_afi)

    name_1 = re.sub(r'[-,\s]+', '', r_imdb.name_string.lower().strip())
    name_2 = cached_names_0.get(r_afi)
    if name_2 is None:
        name_2 = re.sub(r'[-,\s]+', '', r_afi.name_string.lower().strip())
        cached_names_0[r_afi] = name_2

    score = 1.1 if name_1 == name_2 \
        else 0.1 * score_1 + 0.15 * score_2 + 0.45 * score_3 + 0.4 * score_4

    year_1 = r_imdb.raw_object.get('year')
    year_2 = cached_years.get(r_afi)
    if year_2 is None:
        year_2 = re.search(r'[0-9]{4}', r_afi.raw_object.get('release_date', ''))
        cached_years[r_afi] = year_2

    match_year = abs(int(year_1) - int(year_2[0])) <= 2 \
        if year_1 is not None and year_2 is not None \
        else True

    genre_1 = set(word[:3] for word in re.split(r'[-,\s]+', r_imdb.raw_object.get('genre', '').lower().strip()))
    genre_2 = cached_genres.get(r_afi)
    if genre_2 is None:
        genre_2 = set(word[:3] for word in re.split(r'[-,\s]+', r_afi.raw_object.get('genre', '').lower().strip()))
        cached_genres[r_afi] = genre_2

    match_genre = len(genre_1 & genre_2) > 0 \
        if genre_1 is not None and genre_2 is not None else True

    # if name_1 == 'astreetcarnameddesire': # FN
    # if name_1 == 'rocky': # FN
    # if name_1 == 'diehard': # FN
    # if name_1 == 'anatomyofamurder': # FP
    # if name_1 == 'argo': # FP
    # if name_1 == 'fantasia': # year_diff==2?
        # print(year_1, year_2, match_genre, score, name_1, name_2)

    return match_year or match_genre and score > 1.0, score

# threshold value to determine if we are confident the record match
MY_TRESH = 0.8

imdb_file = 'imdb.jl'
afi_file = 'afi.jl'
result_file = 'Zongdi_Xu_hw03_imdb_afi_el.json'
cached_names_0 = {}
cached_names_1 = {}
cached_names_2 = {}
cached_names_3 = {}
cached_names_4 = {}
cached_years = {}
cached_genres = {}

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

    fout = open(result_file, 'w')
    fout.write(json.dumps(valid_match, indent=4))
    fout.close()

if __name__ == '__main__':
    worker()