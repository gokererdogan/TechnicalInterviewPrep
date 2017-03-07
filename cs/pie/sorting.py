def selection_sort(a):
    a = list(a)
    for i in range(len(a)):
        # find the minimum element in the array[i:]
        min_e = a[i]
        min_ix = i
        for j in range(i, len(a)):
            if a[j] < min_e:
                min_e = a[j]
                min_ix = j
        # swap i and min_ix
        a[i], a[min_ix] = a[min_ix], a[i]            
    return a

def selection_sort_recursive(a):
    a = list(a)
    _ss_recurse(a, 0)
    return a

def _ss_recurse(a, start_ix):
    if start_ix < len(a) - 1:
        # swap with minimum
        min_ix = _ss_get_min_ix(a, start_ix)
        a[start_ix], a[min_ix] = a[min_ix], a[start_ix]
        # sort the rest of the list
        _ss_recurse(a, start_ix + 1)

def _ss_get_min_ix(a, start_ix):
    # note we set min_ix to start_ix so we look at the whole array.
    min_ix = start_ix
    for i in range(start_ix, len(a)):
        if a[i] < a[min_ix]:
            min_ix = i
    
    return min_ix


def insertion_sort(a):
    a = list(a)
    for i in range(1, len(a)):
        # get the element to insert
        e = a[i]
        
        # find where to insert element i in the array a[0:i]
        insert_after = i - 1
        while e < a[insert_after] and insert_after > -1:
            insert_after -= 1

        # insert element (if it needs to move)
        if insert_after != i - 1:
            a.pop(i)
            a.insert(insert_after + 1, e)  # python inserts before given index

    return a


def quick_sort(a):
    a = list(a)
    return _qs_recurse(a)

def _qs_recurse(a):
    if len(a) > 1:
        pivot_ix = len(a) // 2
        pivot_val = a[pivot_ix]
        left_list = []
        right_list = []
        # split list into set of smaller and larger elements
        for i in range(len(a)):
            if i != pivot_ix:
                if a[i] < pivot_val:
                    left_list.append(a[i])
                else:
                    right_list.append(a[i])
        # use quicksort to sort left and right lists and combine them
        return _qs_recurse(left_list) + [pivot_val] + _qs_recurse(right_list)
    else:
        return a

def quick_sort_inplace(a):
    a = list(a)
    _qs_inplace_recurse(a, 0, len(a))
    return a

def _qs_inplace_recurse(a, start_ix, end_ix):
    if start_ix < end_ix - 1:
        # partition
        length = end_ix - start_ix
        pivot_ix = start_ix + (length // 2)
        pivot_val = a[pivot_ix]
        i = start_ix
        j = end_ix - 1
        while True:
            while a[i] < pivot_val:
                i += 1
            while a[j] > pivot_val:
                j -= 1
            if i >= j:
                break
            # swap
            if i == pivot_ix:  # we need to keep track of where the pivot went
                pivot_ix = j
            elif j == pivot_ix:
                pivot_ix = i
            a[i], a[j] = a[j], a[i]

        # recurse
        # sort the smaller elements
        _qs_inplace_recurse(a, start_ix, pivot_ix)
        _qs_inplace_recurse(a, pivot_ix + 1, end_ix)



def merge_sort(a):
    a = list(a)
    return _ms_recurse(a)

def _ms_recurse(a):
    if len(a) > 1:
        mid_ix = len(a) // 2
        left_a = a[0:mid_ix]
        right_a = a[mid_ix:]
        return _ms_merge(_ms_recurse(left_a), _ms_recurse(right_a))
    else:
        return a

def _ms_merge(a1, a2):
    sorted_a = []
    i1 = 0
    i2 = 0
    while True:
        if i1 < len(a1) and i2 < len(a2):
            if a1[i1] < a2[i2]:
                sorted_a.append(a1[i1])
                i1 += 1
            else:
                sorted_a.append(a2[i2])
                i2 += 1
        else:
            break
    if i1 >= len(a1):
        for i in range(i2, len(a2)):
            sorted_a.append(a2[i])

    if i2 >= len(a2):
        for i in range(i1, len(a1)):
            sorted_a.append(a1[i])

    return sorted_a


if __name__ == "__main__":
    test_a = [7, 8, 5, 1, 3, 2]
    print insertion_sort(test_a)
    print selection_sort(test_a)
    print quick_sort(test_a)
    print quick_sort_inplace(test_a)
    print merge_sort(test_a)

    import numpy as np
    print insertion_sort(np.random.permutation(20))
    print selection_sort(np.random.permutation(20))
    print quick_sort(np.random.permutation(20))
    print quick_sort_inplace(np.random.permutation(20))
    print merge_sort(np.random.permutation(20))
