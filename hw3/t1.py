import rltk
import json

# You can use this tokenizer in case you need to manipulate some data
tokenizer = rltk.CrfTokenizer()

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

imdb_file = 'imdb.jl'
afi_file  = 'afi.jl'

# load Datasets
ds_imdb = rltk.Dataset(reader=rltk.JsonLinesReader(imdb_file), record_class=IMDBRecord, adapter=rltk.MemoryKeyValueAdapter())
ds_afi  = rltk.Dataset(reader=rltk.JsonLinesReader(afi_file),  record_class=AFIRecord,  adapter=rltk.MemoryKeyValueAdapter())

# print some entries
# print(ds_imdb.generate_dataframe().head(5))
# print(ds_afi.generate_dataframe().head(5))

def name_string_similarity_1(r_imdb, r_afi):
    ''' Example dummy similiary function '''
    s1 = r_imdb.name_string[:4]
    s2 = r_afi.name_string[:4]
    
    return rltk.jaro_winkler_similarity(s1, s2)
    
def name_string_similarity_2(r_imdb, r_afi):
    ''' Example dummy similiary function '''
    s1 = r_imdb.name_string[:2]
    s2 = r_afi.name_string[:2]
    
    if s1 == s2:
        return 1
    
    return 0

# threshold value to determine if we are confident the record match
MY_TRESH = 0.65 # this number is just an example, you need to change it

# entity linkage scoring function
def rule_based_method(r_imdb, r_afi):
    score_1 = name_string_similarity_1(r_imdb, r_afi)
    score_2 = name_string_similarity_2(r_imdb, r_afi)
    
    total = 0.7 * score_1 + 0.3 * score_2
    
    # return two values: boolean if they match or not, float to determine confidence
    return total > MY_TRESH, total

# test on a single entry from imdb
# r_imdb = ds_imdb.get_record("https://www.imdb.com/title/tt0068646/")
# print(r_imdb.raw_object)

valid_match = []
for r_imdb in ds_imdb:
    result = False
    # test this record with AFI records
    for r_afi in ds_afi:
        # get result and confidence
        result, confidence = rule_based_method(r_imdb, r_afi)
        #print(result, confidence)
        if result:
            # print(f'found a match (with confidence of {confidence}) based on my methods. It is: {r_afi.raw_object}')
            # print(f'found a match: {r_imdb.raw_object["name"], r_afi.raw_object["title"]}')
            valid_match.append({'imdb_movie':r_imdb.raw_object['url'], 'afi_movie':r_afi.raw_object['url']})
            break
    if not(result):
        valid_match.append({'imdb_movie':r_imdb.raw_object['url'], 'afi_movie':'NULL'})
fout = open('imdb_afi_el.json', 'w')
fout.write(json.dumps(valid_match, indent=4))
fout.close()