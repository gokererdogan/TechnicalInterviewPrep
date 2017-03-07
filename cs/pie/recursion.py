def binary_search(arr, val):
    if len(arr) == 1:
        if arr[0] == val:
            return 0
        else:
            return -1
    
    split_ix = len(arr) / 2
    ix_left = _binary_search(arr[0:split_ix], val)
    ix_right = _binary_search(arr[split_ix:], val)
    if ix_left != -1:
        return ix_left
    elif ix_right != -1:
        return ix_right + split_ix
    else:
        return -1
        

def binary_search_sorted(arr, val):
    if len(arr) == 0:
        return -1
    if len(arr) == 1:
        if arr[0] == val:
            return 0
        else:
            return -1

    middle_ix = len(arr) / 2
    if val < arr[middle_ix]:
        val_ix = _binary_search(arr[0:middle_ix], val)
        return val_ix
    elif val > arr[middle_ix]:
        val_ix = _binary_search(arr[(middle_ix+1):], val)
        if val_ix != -1:
            return val_ix + middle_ix + 1
        else:
            return -1        
    else:
        return middle_ix    

def permutations(s):
    return _permutations([c for c in s])

def _permutations(l):    
    if len(l) == 1:
        return [l]
    perms = []
    for i, e in enumerate(l):
        sl = [c for c in l if c!=e]
        perms.extend([[e] + p for p in _permutations(sl)])
    return perms

def permutations_with_eval(s):
    l0 = list(s)
    code = "for c0 in l0:\n"
    for i in range(1, len(s)):
        code += i * "    "
        code += "l{0} = [c for c in l{1} if c != c{1}]\n".format(i, i-1)
        code += i * "    "
        code += "for c{0} in l{0}:\n".format(i)
    code += (i+1) * "    "
    code += "print " + ",".join(["c{0}".format(i) for i in range(len(s))])
    exec code

def combinations(s, k):
    return _combinations([c for c in s], k)

def _combinations(l, k):
    if k == 1:
        return [[e] for e in l]
    if len(l) == k:
        return [l]
    combs = []
    for i in range(len(l)-k+1):
        e = l[i]
        sl = l[(i+1):]
        combs.extend([[e] + c for c in _combinations(sl, k-1)])
    return combs

def combinations_with_eval(s):
    code = ""
    for i in range(len(s)):
        code += i * "    "
        code += "for c{0} in s[{0}] + ' ':\n".format(i)
    code += (i+1) * "    "
    code += "print " + ",".join(["c{0}".format(i) for i in range(len(s))])
    exec code           

def print_all_combinations(s):
    c = []
    _print_all_combinations(s, c, 0)

def _print_all_combinations(s, c, start):
    for i in range(start, len(s)):
        c.append(s[i])
        print "".join(c)
        if i < len(s):
            _print_all_combinations(s, c, i+1)
        del c[-1]

telephone_letters = {0: ["0"], 1: ["1"], 2: ["A", "B", "C"], 3: ["D", "E", "F"],
                     4: ["G", "H", "I"], 5: ["J", "K", "L"], 6: ["M", "N", "O"],
                     7: ["P", "R", "S"], 8: ["T", "U", "V"], 9: ["W", "X", "Y"]}
 
def telephone_words(number):
    if len(number) == 1:
        return telephone_letters[number[0]]
    words = []
    letters = telephone_letters[number[0]]
    for letter in letters:
        words.extend([letter + word for word in telephone_words(number[1:])])
    return words

def telephone_words_iterative(number):
    words = ['']
    for i in range(0, len(number)):
        new_words = []
        for word in words:
            for l in telephone_letters[number[i]]:
                new_words.append(word + l)
        words = new_words
    return words
