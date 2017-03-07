from collections import defaultdict

def find_first_nonrepeating(s):
    counts = defaultdict(int)
    for c in s:
        counts[c] += 1
    for c in s:
        if counts[c] == 1:
            return c
    raise Exception("All characters are repeated.")

def remove_chars(s, chars):
    new_s = ""
    for c in s:
        if c not in chars:
            new_s += c
    return new_s

def reverse_words(s):
    return " ".join(reversed(s.split(" "))) 

def atoi(s):
    mult = 1
    if s[0] == "-":
        mult = -1
        s = s[1:]
    return mult * sum([(ord(c)-48) * 10**i for i, c in enumerate(reversed(s))]) 

def itoa(i):
    sign_char = ""
    if i < 0:
        sign_char = "-"
        i *= -1 
    chars = []
    chars.insert(0, chr((i % 10) + 48))
    d = 2
    while True:
        if i >= 10**(d-1):
            chars.insert(0, chr((i % (10**d)) / (10**(d-1)) + 48))
        else:
            break
        d += 1
    chars.insert(0, sign_char)
    return "".join(chars)
