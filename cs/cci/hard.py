import cPickle as pkl
import sys

words = pkl.load(open('words.pkl'))

class ParseResult(object):
    def __init__(self, parse, invalid_count=sys.maxsize):
        self.parse = parse
        self.invalid_count = invalid_count

    def __repr__(self):
        return "{0:s}, {1:d}".format(self.parse, self.invalid_count)


def respace(s):
    """
    Question 17.13
    """
    return _respace_split(s, cache={})

def _respace_split(s, cache):
    if len(s) == 0:
        return ParseResult([], 0)
    if s in cache:
        return cache[s]

    best_invalid = sys.maxsize
    best_split = None
    for i in range(1, len(s) + 1):
        w = s[0:i]
        invalid_w = len(w)
        if w in words:
            invalid_w = 0
        split_rest = _respace_split(s[i:], cache)
        cache[s[i:]] = split_rest
        invalid_rest = split_rest.invalid_count
        if invalid_w + invalid_rest < best_invalid:
            best_invalid = invalid_w + invalid_rest
            best_split = ParseResult([w] + split_rest.parse, best_invalid)
    return best_split
        
        
        
        
    
