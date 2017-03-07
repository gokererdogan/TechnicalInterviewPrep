from collections import defaultdict


def is_unique(s):
    count = defaultdict(int)
    for c in s:
        if count[c] > 0:
            return False        
        count[c] += 1
    return True
