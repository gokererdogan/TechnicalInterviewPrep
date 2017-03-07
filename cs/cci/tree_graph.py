from collections import deque
from collections import defaultdict
from itertools import combinations

class Node(object):
    def __init__(self, data, neighbors=None):
        self.data = data
        self.neighbors = []
        if neighbors is not None:
            assert type(neighbors) == list, "Neighbors must be a list."
            for n in neighbors:
                self.neighbors.append(n)

    def __repr__(self):
        return repr(self.data)

class Graph(object):
    def __init__(self):
        self.nodes = []

    def add_node(self, node):
        self.nodes.append(node)

    def depth_first_traversal(self, start_node=None):
        assert len(self.nodes) > 0, "Empty graph."

        if start_node is None:
            start_node = self.nodes[0]

        expand_nodes = [start_node]
        visited = []
        while len(expand_nodes) > 0:
            node = expand_nodes.pop()
            visited.append(node)
            print node
            for neighbor in node.neighbors:
                if neighbor not in visited:
                    expand_nodes.append(neighbor) 

    def breadth_first_traversal(self, start_node=None):
        assert len(self.nodes) > 0, "Empty graph."

        if start_node is None:
            start_node = self.nodes[0]

        expand_nodes = deque()
        expand_nodes.append(start_node)
        visited = []
        while len(expand_nodes) > 0:
            node = expand_nodes.popleft()
            visited.append(node)
            print node
            for neighbor in node.neighbors:
                if neighbor not in visited:
                    expand_nodes.append(neighbor) 

        
class BinaryNode(object):
    def __init__(self, data, left=None, right=None):
        self.data = data
        self.left = left
        self.right = right

    def __str__(self):
        return str(self.data)

    def __repr__(self):
        return str(self)


class BinaryTree(object):
    def __init__(self, root=None):
        self.root = root

    def get_ancestors(self, node):
        if self.root is None or node is None:
            return []
        return self._get_ancestors(self.root, node)
        

    def _get_ancestors(self, subtree, node):
        if subtree is None:
            return []

        if subtree.left == node or subtree.right == node:
            return [subtree]

        left_ancestors = self._get_ancestors(subtree.left, node)
        if len(left_ancestors) > 0:
            return [subtree] + left_ancestors

        right_ancestors = self._get_ancestors(subtree.right, node)
        if len(right_ancestors) > 0:
            return [subtree] + right_ancestors

        return []

    def get_parent(self, node):
        if self.root is None or node is None:
            return None
        
        nodes = deque()
        nodes.append(self.root)
        while len(nodes) > 0:
            cnode = nodes.popleft()
            if cnode.left is node or cnode.right is node:
                return cnode

            if cnode.left is not None:
                nodes.append(cnode.left)
            if cnode.right is not None:
                nodes.append(cnode.right)

        return None
    
    def get_first_common_ancestor(self, node1, node2):
        """
        Question 4.8
        """
        assert node1 is not None
        assert node2 is not None
        # do a breadth first search
        common_ancestor = None
        expand = deque()
        expand.append(self.root)
        while len(expand) > 0:
            node = expand.popleft()
            if node is not None:
                expand.append(node.left)
                expand.append(node.right)
            if self.is_descendant(node, node1) and self.is_descendant(node, node2):
                common_ancestor = node

        return common_ancestor
        
    def is_descendant(self, parent, descendant):
        return self._is_descendant(parent, descendant)

    def _is_descendant(self, parent, descendant):
        if parent is None:
            return False
        if parent == descendant:
            return True
        return self._is_descendant(parent.left, descendant) or self._is_descendant(parent.right, descendant)

    def get_bst_sequences(self):
        """
        Question 4.9
        """
        if self.root is None:
            raise ValueError("Empty tree.")

        return self._get_bst_sequences(self.root)

    def _get_bst_sequences(self, node):
        if node is None:
            return [[]]
        bst_seqs = []
        left_bst_seqs = self._get_bst_sequences(node.left)
        right_bst_seqs = self._get_bst_sequences(node.right)
        for lseq in left_bst_seqs:
            for rseq in right_bst_seqs:
                interleaved_seqs = interleave(lseq, rseq)
                for seq in interleaved_seqs:
                    bst_seqs.append([node.data] + seq)

        return bst_seqs

    def is_subtree(self, subtree):
        assert subtree is not None

        if self.root is None:
            return False

        # do a breadth first search and check for every node
        expand = deque()
        expand.append(self.root)
        while len(expand) > 0:
            node = expand.popleft()
            if self._same_tree(node, subtree.root):
                return True
            if node.left is not None:
                expand.append(node.left)
            if node.right is not None:
                expand.append(node.right)
        return False

    def _same_tree(self, self_root, subtree_root):
        if self_root is None and subtree_root is None:
            return True
        elif self_root is None:
            return False
        elif subtree_root is None:
            return False
        else:
            left_same = self._same_tree(self_root.left, subtree_root.left)
            right_same = self._same_tree(self_root.right, subtree_root.right)
            return self_root == subtree_root and left_same and right_same

    def get_paths_with_sum(self, value):
        paths = []
        for path in self._get_all_paths(self.root):
            if sum([n.data for n in path]) == value:
                paths.append(path)
        return paths

    def _get_all_paths(self, node):
        """
        Helper function for Question 4.12
        """
        if node is None:
            return []
        left_paths = self._get_all_paths(node.left)        
        right_paths = self._get_all_paths(node.right)
        paths = []        
        for p in left_paths:
            if p[0] == node.left:
                paths.append([node] + p)
        for p in right_paths:
            if p[0] == node.right:
                paths.append([node] + p)
        paths.extend(left_paths)
        paths.extend(right_paths)
        paths.append([node])
        return paths

    def __str__(self):
        if self.root is None:
            return "Empty BinaryTree"
        s = []
        expand = [self.root]
        while len(expand) > 0:
            new_expand = []
            for node in expand:
                s.append(str(node))
                s.append(" ")
                if node.left is not None:
                    new_expand.append(node.left)
                if node.right is not None:                
                    new_expand.append(node.right)
            s.append("\n")
            expand = new_expand
        return "".join(s)

    def __repr__(self):
        return str(self)



class MinHeap(BinaryTree):
    def __init__(self):
        BinaryTree.__init__(self)

    def insert(self, value):
        # do breadth first search to find the rightmost empty spot
        new_node = BinaryNode(value)
        if self.root is None:
            self.root = new_node
        else:
            nodes = deque()
            nodes.append(self.root)
            while len(nodes) > 0:
                node = nodes.popleft()
                if node.left is None:
                    node.left = new_node
                    break
                elif node.right is None:
                    node.right = new_node
                    break
                nodes.append(node.left)
                nodes.append(node.right)

            # get ancestors of new node
            # ancestors start from root and are ordered root to new node
            ancestors = list(reversed(self.get_ancestors(new_node) + [new_node]))
            # bubble up the new node to where it should be            
            for i in range(len(ancestors)-1):
                if ancestors[i].data < ancestors[i+1].data:
                    ancestors[i].data, ancestors[i+1].data = ancestors[i+1].data, ancestors[i].data        
        
    def extract(self):
        if self.root is None:
            raise IndexError("Empty heap.")

        # extract min
        min_value = self.root.data

        # do breadth first search to find the rightmost element on last layer
        nodes = deque()
        nodes.append(self.root)
        while len(nodes) > 0:
            node = nodes.popleft()
            if node.left is not None:
                nodes.append(node.left)
            if node.right is not None:
                nodes.append(node.right)
        last_node = node
        
        if self.root is last_node:
            # heap has single node and will become empty            
            self.root = None
        else:
            # swap root with the last node and bubble root down to keep min-heap
            # property
            self.root.data = last_node.data

            parent = self.get_parent(last_node)
            if parent is None:
                raise ValueError("This should never happen.")
            # remove last node from heap
            if parent.left is last_node:
                parent.left = None
            elif parent.right is last_node:
                parent.right = None
            else:
                raise ValueError("This should never happen.")

            # bubble down the root to where it should be
            cnode = self.root
            while True:
                # find the child that is smaller
                if cnode.left is None and cnode.right is None:
                    break
                elif cnode.right is None:
                    # swap with left if smaller
                    if cnode.left.data < cnode.data:
                        cnode.data, cnode.left.data = cnode.left.data, cnode.data
                        cnode = cnode.left
                    else:
                        break
                elif cnode.left is None:
                    raise ValueError("This should never happen. Because heap is \
                                      filled left to right")
                else:
                    # find the smaller child
                    if cnode.left.data < cnode.right.data:
                        # swap with left if smaller
                        if cnode.left.data < cnode.data:
                            cnode.data, cnode.left.data = cnode.left.data, cnode.data
                            cnode = cnode.left
                        else:
                            break
                    else:
                        # swap with right if smaller
                        if cnode.right.data < cnode.data: 
                            cnode.data, cnode.right.data = cnode.right.data, cnode.data
                            cnode = cnode.right
                        else:
                            break
        return min_value

def find_build_order(projects, dependencies):
    """
    Question 4.7
    """
    prerequisites = defaultdict(list)
    for p1, p2 in dependencies:
        prerequisites[p2].append(p1)
    built = []
    remaining = projects
    while len(remaining) > 0:
        added_at_least_one = False
        for p in remaining:
            # check if all prerequisites are built
            pres = prerequisites[p]
            all_built = True
            for pre in pres:
                if pre not in built:
                    all_built = False
            if all_built:
                built.append(p)
                added_at_least_one = True
        if not added_at_least_one:
            print("No build order found.")
            return None

        remaining = [p for p in projects if p not in built]
    return built

def interleave(seq1, seq2):
    """
    Helper function for Question 4.9
    """
    n = len(seq1) + len(seq2)
    k = len(seq1)
    interleaved_seqs = []
    combs = combinations(range(n), k)
    for comb in combs:
        seq = []
        seq1_ix = 0
        seq2_ix = 0
        for i in range(n):
            if i in comb:
                seq.append(seq1[seq1_ix])
                seq1_ix += 1
            else:
                seq.append(seq2[seq2_ix])
                seq2_ix += 1
        interleaved_seqs.append(seq)
    return interleaved_seqs
