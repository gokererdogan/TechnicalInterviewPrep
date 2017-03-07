class Node(object):
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right
    
    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return str(self)

class BinaryTree(object):
    def __init__(self, root=None):
        self.root = root

    def __str__(self):
        if self.root is None:
            return "Empty BinaryTree"
        s = []
        expand = [self.root]
        while len(expand) > 0:
            new_expand = []
            for node in expand:
                s.append(str(node.value))
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

    def insert(self, node, parent=None, where='left'):
        if parent is None:
            if self.root is not None:
                raise ValueError("Parent cannot be None for non-empty tree")
            self.root = node
        else:
            # check if parent node in tree
            if not self.is_in_tree(parent):
                raise ValueError("Parent node not in tree.")
            # check if node is already in the tree
            if self.is_in_tree(node):
                raise ValueError("Node already in the tree.")
            # check if parent's child is empty
            if where == 'left':
                if parent.left is not None:
                    raise ValueError("Parent node already has left child.")
                parent.left = node
            elif where == 'right':
                if parent.right is not None:
                    raise ValueError("Parent node already has right child.")
                parent.right = node
            else:
                raise ValueError("where should be left or right.")

    def delete(self, node):
        if node is self.root:
            if self.root.left is None and self.root.right is None:
                self.root = None
            else:
                raise ValueError("Cannot remove node with children.")
        else:
            parent = self.get_parent(node)
            if node.left is None and node.right is None:
                if parent.left is node:
                    parent.left = None
                else:  #parent.right is node
                    parent.right = None
            else:
                raise ValueError("Cannot remove node with children.")
                

    def get_parent(self, node):
        parent = self._get_parent(node, self.root)
        if parent is None:
            raise ValueError("Node is not in tree.")
        return parent
 
    def _get_parent(self, node, current):
        if current is None:
            return None
        elif current.left == node or current.right == node:
            return current
        else:
            parent_in_left = self._get_parent(node, current.left)
            parent_in_right = self._get_parent(node, current.right)
            if parent_in_left is None:
                return parent_in_right
            else:
                return parent_in_left
        
    def is_in_tree(self, node):
        current_node = self.root
        return self._is_descendant(node, current_node)

    def _is_descendant(self, node, parent):
        if parent is None:
            return False
        else:
            return self._is_descendant(node, parent.left) or node == parent or \
                   self._is_descendant(node, parent.right)

    # PROBLEMS

    def get_depth(self):
        return self._get_depth(self.root)
    
    def _get_depth(self, node):
        if node is None:
            return 0
        else:
            return 1 + max(self._get_depth(node.left), self._get_depth(node.right))

    def traverse_preorder(self):
        if self.root is not None:
            self._traverse_preorder(self.root)

    def _traverse_preorder(self, node):
        if node is not None:
            print node.value
            self._traverse_preorder(node.left)
            self._traverse_preorder(node.right)

    def traverse_preorder_no_recursion(self):
        if self.root is not None:
            expand = [self.root]
            while len(expand) > 0:
                node = expand.pop(0)
                print node.value
                if node.right is not None:
                    expand.insert(0, node.right)
                if node.left is not None:
                    expand.insert(0, node.left)

    def traverse_inorder(self):
        if self.root is not None:
            self._traverse_inorder(self.root)

    def _traverse_inorder(self, node):
        if node is not None:
            self._traverse_inorder(node.left)
            print node.value
            self._traverse_inorder(node.right)

    def traverse_postorder(self):
        if self.root is not None:
            self._traverse_postorder(self.root)

    def _traverse_postorder(self, node):
        if node is not None:
            self._traverse_postorder(node.left)
            self._traverse_postorder(node.right)
            print node.value

    def find_lowest_common_ancestor(self, node1, node2):
        # assumes both nodes are in the tree
        ancestors1 = self.get_ancestors(node1)
        ancestors2 = self.get_ancestors(node2)
        common_ancestor = self.root
        ancestors1.pop()  # should be root
        ancestors2.pop()  # should be root
        while True:
            try:
                a1 = ancestors1.pop()
            except IndexError as e:
                break
            try:
                a2 = ancestors2.pop()
            except IndexError as e:
                break
            if a1 != a2:
                break
            common_ancestor = a1
        return common_ancestor
    
    def get_ancestors(self, node):
        return self._get_ancestors(node, self.root)

    def _get_ancestors(self, node, current):
        if current is None:
            return []
        if current.left == node or current.right == node:
            return [current]
        
        al = self._get_ancestors(node, current.left)
        ar = self._get_ancestors(node, current.right)
        
        if current.left in al:
            return al + [current]
        if current.right in ar:
            return ar + [current]
        return al + ar


if __name__ == "__main__":
    t = BinaryTree()
    t.insert(Node(100))
    t.insert(Node(50), parent=t.root, where='left')
    t.insert(Node(150), parent=t.root, where='right')
    t.insert(Node(25), parent=t.root.left, where='left')
    t.insert(Node(75), parent=t.root.left, where='right')
    t.insert(Node(125), parent=t.root.right, where='left')
    t.insert(Node(175), parent=t.root.right, where='right')
    t.insert(Node(110), parent=t.root.right.left, where='left')

