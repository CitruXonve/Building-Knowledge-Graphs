from snorkel.lf_helpers import (
    get_left_tokens, get_right_tokens, get_between_tokens,
    get_text_between, get_tagged_text, get_matches, contains_token,
)

# TODO: Define your LFs here, below is a very simple LF
def LF_right_detect(c):
    cl, cr = c
    return 1 if contains_token(c, 'school') or contains_token(c, 'college')\
        or contains_token(c, 'university')\
        or contains_token(c, 'usc')\
        else -1

def LF_between_detect_refined(c):
    cl, cr = c
    candidate_predicates = list(get_between_tokens(c))
    prepositions = {'at', 'to', 'from'}
    intransitive_predicates = {'enrolled', 'graduated', 'studied', 'went', 'returned', 'educated'}
    transitive_predicates = {'attended'}
    phrases = {'member', 'of'}
    return 1 if len(transitive_predicates.intersection(candidate_predicates))>0 or \
        len(prepositions.intersection(candidate_predicates))>0 and \
            len(intransitive_predicates.intersection(candidate_predicates))>0 \
        or len(phrases.intersection(candidate_predicates))>1 \
        else -1

def LF_combined(c):
    return 1 if (LF_between_detect_refined(c)==1 or 'at' in get_between_tokens(c)) and LF_right_detect(c)==1 else -1

def LF_combined_refined(c):
    taboo = {'later', 'here', 'there'}
    return 1 if LF_combined(c)==1 and not len(taboo.intersection(get_between_tokens(c)))>0 else -1