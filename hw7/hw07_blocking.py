from pathlib import Path
from typing import *
from re import sub as re_sub
import sys
import rltk

HASH_BLOCKING = 0
TOKN_BLOCKING = 1

class PaperRecord1(rltk.Record):
    ''' Record entry class for each of our paper records in dataset 1 '''

    @rltk.cached_property
    def id(self):
        return self.raw_object['id']

    @rltk.cached_property
    def title(self):
        return self.raw_object.get('title', '')

    @rltk.cached_property
    def title_first_3_letters(self):
        # ##################################################
        # ** STUDENT CODE. Task 2.1.1
        # TODO: Implement title_first_3_letters.
        #       Your code should return the first 3 letters of the record title if it isn't blank,
        #       otherwise return the string '###'. Return type is string.
        #       Your implementation should be inside this ####### block
        # raise NotImplementedError()
        return self.raw_object.get('title', '###')[:3]
        # ##################################################

    @rltk.cached_property
    def title_tokens(self):
        global g_tokenizer # You can use this tokenizer instance (already defined)
        # ##################################################
        # ** STUDENT CODE. Task 2.1.2
        # TODO: Implement title_tokens.
        #       Your code should return the set of tokens in the record title,
        #       otherwise, return an empty set. Return type is a set.
        #       Your implementation should be inside this ####### block
        # raise NotImplementedError()
        return set(g_tokenizer.tokenize(self.title))
        # ##################################################


class PaperRecord2(PaperRecord1):
    ''' Record entry class for each of our paper records in dataset 2 '''

    @rltk.cached_property
    def id(self):
        return super().id

    @rltk.cached_property
    def title(self):
        return super().title

    @rltk.cached_property
    def title_first_3_letters(self):
        return super().title_first_3_letters

    @rltk.cached_property
    def title_tokens(self):
        return super().title_tokens


def create_dataset(csv_input_file: str, rcrd_class: rltk.Record) -> rltk.Dataset:
    ''' Create rltk dataset from a given csv file '''

    assert Path(csv_input_file).suffix == ".csv"
    return rltk.Dataset(reader=rltk.CSVReader(open(csv_input_file, encoding='latin-1')), record_class=rcrd_class, adapter=rltk.MemoryKeyValueAdapter())


def get_ground_truth(csv_input_file: str) -> rltk.GroundTruth:
    ''' Read the grouth truth from the given csv file '''

    gt = rltk.GroundTruth()
    with open(csv_input_file, encoding='latin-1') as f:
        for d in rltk.CSVReader(f):
            gt.add_positive(d['id_record1'], d['id_record2'])
    return gt


def create_hash_blocks(dataset_1: rltk.Dataset, dataset_2: rltk.Dataset) -> rltk.block:
    ''' Create and return rltk hash blocks '''

    # ##################################################
    # ** STUDENT CODE. Task 2.2.1
    # TODO: Implement create_hash_blocks.
    #       Your code should implement a hash blocking method using rltk.HashBlockGenerator().
    #       The hashing property should be the attribute 'title_first_3_letters'.
    #       Your implementation should be inside this ####### block
    # raise NotImplementedError()
    g = rltk.HashBlockGenerator()
    return g.generate(g.block(dataset_1, property_="title_first_3_letters"), g.block(dataset_2, property_="title_first_3_letters"))
    # ##################################################

def create_token_blocks(dataset_1: rltk.Dataset, dataset_2: rltk.Dataset) -> rltk.block:
    ''' Create and return rltk token blocks '''

    # ##################################################
    # ** STUDENT CODE. Task 2.2.2
    # TODO: Implement create_token_blocks.
    #       Your code should implement a 6-gram token blocking method using rltk.TokenBlockGenerator().
    #       The hashing function should make use of the attribute 'title_tokens' to generate the 'grams'.
    #       You can use rltk.NGramTokenizer() to generate ngrams (where n=6).
    #       Your implementation should be inside this ####### block
    # raise NotImplementedError()
    g = rltk.TokenBlockGenerator()
    ng = rltk.NGramTokenizer()
    return g.generate(g.block(dataset_1, function_=lambda d:ng.basic(d.title_tokens, 6)), 
        g.block(dataset_2, function_=lambda d:ng.basic(d.title_tokens, 6)))
    # ##################################################


def calc_reduction_ratio(dataset_1, dataset_2, block_set, gt_set):
    ''' Calculate and print reduction ratio '''

    pairs = rltk.get_record_pairs(dataset_1, dataset_2, block=block_set, ground_truth=gt_set)
    
    set_candidates_size = len(list(pairs))
    ds1_size = len(dataset_1.generate_dataframe())
    ds2_size = len(dataset_2.generate_dataframe())

    rr = (1 - float((set_candidates_size)/(ds1_size*ds2_size)))
    print(f'Reduction Ratio    = 1 - ({set_candidates_size}/{ds1_size}*{ds2_size}) = {rr:.06f}')
    return rr


def calc_pairs_completeness(dataset_1, dataset_2, block_set, gt_set):
    ''' Calculate and print Pairs Completeness '''

    gt_dict = dict()
    cand_matches = 0

    for id_r1, id_r2, label in gt_set:
        if label:
            gt_dict[id_r1] = id_r2
    gt_matches = len(gt_dict)

    for key, r1_id, r2_id in block_set.pairwise(dataset_1, dataset_2):
        if r1_id in gt_dict and gt_dict[r1_id] == r2_id:
            cand_matches += 1
            del gt_dict[r1_id]

    pc = float(cand_matches)/gt_matches
    print(f'Pairs Completeness = {cand_matches}/{gt_matches} = {pc:.06f}')
    return pc


def evaluate_blocking(ds1_file: str, ds2_file: str, gt_file: str, blk_type: int):
    ''' Evaluate and print the reduction-ratio and pairs-completeness
        of the data, based on the given ground truth file '''

    dataset_1: rltk.Dataset = create_dataset(ds1_file, PaperRecord1)
    dataset_2: rltk.Dataset = create_dataset(ds2_file, PaperRecord2)

    gt_set = get_ground_truth(gt_file)

    if HASH_BLOCKING == blk_type:
        blocks = create_hash_blocks(dataset_1, dataset_2)
    else:
        blocks = create_token_blocks(dataset_1, dataset_2)

    calc_reduction_ratio(dataset_1, dataset_2, blocks, gt_set)
    calc_pairs_completeness(dataset_1, dataset_2, blocks, gt_set)


def main():

    global g_tokenizer

    if len(sys.argv) < 2:
        print("Error: missing blocking type!")
        exit(1)

    if sys.argv[1] == 'hash':
        blocking_type = HASH_BLOCKING
    elif sys.argv[1] == 'token':
        blocking_type = TOKN_BLOCKING
    else:
        print("Error: blocking type should be 'hash' or 'token'!")
        exit(1)

    # define filenames
    gt_file   = "./perfect_mapping.csv"
    ds01_file = "./data_source1.csv"
    ds02_file = "./data_source2.csv"

    # define tokenizer
    g_tokenizer = rltk.CrfTokenizer()

    # evaluate
    evaluate_blocking(ds01_file, ds02_file, gt_file, blocking_type)


if __name__ == '__main__':
    main()