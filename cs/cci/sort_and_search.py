import numpy as np

def group_anagrams(ss):
    """
    Question 10.2
    """
    return sorted(ss, key=lambda s: (len(s), sum([ord(c) for c in s])))

def sparse_search(ss, s):
    """
    Question 10.5
    """
    start = 0
    end = len(ss) - 1
    return _sparse_binary_search(ss, s, start, end)

def _sparse_binary_search(ss, s, start, end):
    if start > end:
        return -1
    
    mid = (start + end) / 2    
    # find closest non-empty
    left = mid - 1
    right = mid + 1
    if ss[mid] == "":
        while True:
            if left < start and right > end:
                return -1
            elif left >= start and ss[left] != "":
                mid = left
                break
            elif right <= end and ss[right] != "":
                mid = right
                break
            left -= 1
            right += 1

    if s == ss[mid]:
        return mid
    if s < ss[mid]:
        return _sparse_binary_search(ss, s, start, mid-1)
    if s > ss[mid]:
        return _sparse_binary_search(ss, s, mid+1, end)


def sorted_matrix_search(m, v):
    """
    Question 10.9
    """
    r = 0
    c = m.shape[1] - 1
    while r < m.shape[0] and c >= 0:
        if v == m[r,c]:
            return r, c
        elif v > m[r,c]:
            r += 1
        else:  # v < m[r,c]
            c -= 1
    return False


def peaks_and_valleys(ns):
    """
    Question 10.11
    """
    sns = sorted(ns)
    pv = [None for _ in xrange(len(sns))]
    for i in xrange(len(pv)):
        if i % 2 == 0:
            pv[i] = sns[-i/2 - 1]
        else:
            pv[i] = sns[(i-1)/2]
    return pv
