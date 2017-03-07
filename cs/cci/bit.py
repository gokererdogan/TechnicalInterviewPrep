def float2binary(x):
    """
    Question 5.2
    """
    assert 0.0 <= x <= 1.0
    s = '0.'
    for i in range(32):
        digit_value = 1.0 / 2.0**(i+1)
        if x >= digit_value:
            s += '1'
            x -= digit_value
            if x < 1e-8:
                break
        else:
            s += '0'
    return s


def count_flips(a, b):
    """
    Question 5.6
    """
    return count1s(a^b)

def count1s(x):
    """
    Helper for Question 5.6
    """
    count = 0
    while x != 0:
        if x != (x>>1)<<1:
            count += 1
        x = x>>1
    return count

def count1s_2(x):
    """
    A better way of counting 1s in a number.
    """
    count = 0
    while x != 0:
        x = x & (x-1) # clears least significant 1
        count += 1
    return count
