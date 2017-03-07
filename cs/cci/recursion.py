def triple_step(n):
    """
    Question 8.1
    """
    assert n > 0
    w0, w1, w2 = (1, 1, 2)
    for i in range(3, n):
        w0, w1, w2 = w1, w2, w0 + w1 + w2
    return w0 + w1 + w2


def triple_step_recursive(n):
    """
    Question 8.1
    """
    if n == 0:
        return 1
    count = 0
    if n >= 1:
        count += triple_step_recursive(n-1)
    if n >= 2:
        count += triple_step_recursive(n-2)
    if n >= 3:
        count += triple_step_recursive(n-3)
    return count


def robot_in_a_grid(r, c, walls):
    """
    Question 8.2
    """
    assert r > 0 and c > 0
    path_so_far = []
    expand_cells = [((0, 0), (0, 0))]
    while len(expand_cells) > 0:
        cell = expand_cells.pop()
        while len(path_so_far) > 0:
            if path_so_far[-1][1] != cell[0]:
                path_so_far.pop()
            else:
                break
        path_so_far.append(cell)

        # have reached our destination?
        if cell[1] == (r-1, c-1):
            return [p[1] for p in path_so_far]

        i, j = cell[1]
        # add right
        if (i, j+1) not in walls and j+1 < c:
            expand_cells.append(((i, j), (i, j+1)))
        # add down
        if (i+1, j) not in walls and i+1 < r:
            expand_cells.append(((i, j), (i+1, j)))
    return []


def robot_in_a_grid_recursive(r, c, walls):
    """
    Question 8.2
    """
    assert r > 0 and c > 0
    path = []
    if _robot_get_path(r, c, walls, r-1, c-1, path):
        return path
    return []


def _robot_get_path(r, c, walls, target_r, target_c, path):
    """
    Question 8.2
    """
    if target_r < 0 or target_c < 0 or (target_r, target_c) in walls:
        return False

    at_origin = target_r == 0 and target_c == 0
    if at_origin or _robot_get_path(r, c, walls, target_r, target_c-1, path) or \
        _robot_get_path(r, c, walls, target_r-1, target_c, path):
        path.append((target_r, target_c))
        return True

    return False


def power_set(s):
    """
    Question 8.4
    """
    if len(s) == 0:
        return [[]]
    elem = s[0]
    subset_subsets = power_set([e for e in s if e != elem])
    subsets = []
    for subset in subset_subsets:
        subsets.append(subset)
        subsets.append([elem] + subset)
    return subsets


def towers_of_hanoi(n):
    """
    Question 8.6
    """
    assert n > 0
    return _towers_of_hanoi(n, [1, 2, 3])


def _towers_of_hanoi(n, towers):
    if n == 1:
        return [('Disk{0:d}'.format(n), 'Tower{0:d}'.format(towers[2]))]
    phase1 = _towers_of_hanoi(n-1, [towers[0], towers[2], towers[1]])
    phase2 = _towers_of_hanoi(n-1, [towers[1], towers[0], towers[2]])
    return phase1 + [('Disk{0:d}'.format(n), 'Tower{0:d}'.format(towers[2]))] + phase2


def permutations(l):
    """
    Question 8.7
    """
    assert len(l) > 0
    if len(l) == 1:
        return [l]
    perms = []
    for e in l:
        subperms = permutations([i for i in l if i != e])
        for sp in subperms:
            perms.append([e] + sp)
    return perms


def permutations_with_duplicates(l):
    """
    Question 8.8
    """
    assert len(l) > 0
    if len(l) == 1:
        return [l]
    perms = []
    used = []
    for i, e in enumerate(l):
        if e not in used:
            subperms = permutations_with_duplicates([l[j] for j in range(len(l)) if j != i])
            for sp in subperms:
                perms.append([e] + sp)
            used.append(e)
    return perms


def parens(n):
    """
    Question 8.9
    """
    assert n > 0
    return _parens(n, n)

def _parens(remaining_left, remaining_right):
    assert remaining_right >= remaining_left
    if remaining_left == 0 and remaining_right == 0:
        return ['']

    parens = []
    if remaining_left > 0:
        parens_sub = _parens(remaining_left - 1, remaining_right)
        for p in parens_sub:
            parens.append('(' + p)
    if remaining_right > remaining_left:
        parens_sub = _parens(remaining_left, remaining_right - 1)
        for p in parens_sub:
            parens.append(')' + p)
    return parens


def coins(n):
    """
    Question 8.11
    """
    assert n > 0
    return _coins(n, 1e6)


def _coins(n, min_so_far):        
    if n < 0:
        return None
    if n == 0:
        return [[]]
    values = [25, 10, 5, 1]    
    coins = []
    for v in values:
        if v <= min_so_far:
            coins_mv = _coins(n-v, v)
            if coins_mv is not None:
                for c in coins_mv:
                    coins.append([v] + c)
    return coins


def eight_queens():
    """
    Question 8.12
    """
    return _eight_queens(8)

def _eight_queens(n):
    if n == 1:
        return [[i] for i in range(8)]
    confs = []    
    confs_sub = _eight_queens(n-1)
    for conf in confs_sub:
        for i in range(8):
            if _is_compatible(i, conf):
                confs.append([i] + conf)
    return confs

def _is_compatible(col_i, conf):
    if col_i in conf:
        return False
    for row_j, col_j  in enumerate(conf):
        if col_i == col_j - (row_j + 1) or col_i == col_j + (row_j + 1):
            return False
    return True

def eight_queens_iterative():
    current_confs = [[i] for i in range(8)]
    not_done = True
    for i in range(7):
        confs = []
        for conf in current_confs:
            allowed_cols = _get_allowed_cols(conf)
            for col in allowed_cols:
                confs.append([col] + conf)
        current_confs = confs
    return confs

def _get_allowed_cols(conf):
    return [i for i in range(8) if _is_compatible(i, conf)]


def boolean_evaluation(expr, target):
    return sum([val == target for val in eval_expression(expr)])

def eval_expression(expr):
    assert len(expr) % 2 == 1, "Expression is ill formed."
    return _eval_expression(len(expr), expr, 0)

def _eval_expression(n, expr, ix):
    if n == 1:
        assert expr[ix] == '0' or expr[ix] == '1'
        return [True] if expr[ix] == '1' else [False] 
    evals = []
    for i in range(1, n, 2):
        left_evals = _eval_expression(i, expr, ix)
        right_evals = _eval_expression(n - (i+1), expr, ix + i + 1)
        op = expr[ix+i]
        for le in left_evals:
            for re in right_evals:
                if op == '&':
                    evals.append(le and re)
                elif op == '|':
                    evals.append(le or re)
                elif op == '^':
                    evals.append(le ^ re)
                else:
                    raise ValueError("Invalid operation.")
    return evals

def parenthesize_expression(expr):
    assert len(expr) % 2 == 1, "Expression is ill formed."
    return _parenthesize_expression(len(expr), expr, 0)

def _parenthesize_expression(n, expr, ix):
    if n == 1:
        return [expr[ix]]
    trees = []
    for i in range(1, n, 2):
        left_trees = _parenthesize_expression(i, expr, ix)
        right_trees = _parenthesize_expression(n - (i+1), expr, ix + i + 1)
        for lt in left_trees:
            for rt in right_trees:
                trees.append('(' + lt + expr[ix+i] + rt + ')')
    return trees

def _generate_full_binary_trees(n):
    assert n % 2 == 1, "n must be odd"
    if n == 1:
        return ['()']
    trees = []
    for i in range(1, n, 2):
        left_trees = _generate_full_binary_trees(i)
        right_trees = _generate_full_binary_trees(n - (i+1))
        for lt in left_trees:
            for rt in right_trees:
                trees.append('(' + lt + rt + ')')
    return trees


if __name__ == "__main__":
    print robot_in_a_grid(5, 5, [(3, 2), (4, 2)])
    print robot_in_a_grid_recursive(5, 5, [(3, 2), (4, 2)])
    permutations_with_duplicates('aaa')
