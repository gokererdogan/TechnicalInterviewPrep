class Node(object):
    def __init__(self, data, next=None):
        self.next = next
        self.data = data

    def __str__(self):
        return str(self.data)

    def __repr__(self):
        return str(self)

class LinkedList(object):
    def __init__(self, head=None):
        self.head = head
    
    def __str__(self):
        s = []
        node = self.head
        while node is not None:
            s.append(str(node))
            node = node.next
        return ", ".join(s)

    def __repr__(self):
        return str(self)

    def insert_before(self, node, before=None):
        if self.head is None:  # empty list
            self.head = node
        else:  # non-empty list
            if before is None:  # add to the end
                # find last element
                last = self.head
                while last.next is not None:
                    last = last.next
                # insert
                last.next = node
            else:
                if before is self.head:  # add before head
                    node.next = self.head
                    self.head = node
                else:
                    # find previous of before in list
                    prev_node = self.head
                    while prev_node.next is not before:
                        prev_node = prev_node.next
                        if prev_node is None:  # not in list
                            raise ValueError("Node not in list")
                    prev_node.next = node
                    node.next = before
        
    def delete(self, node):
        if node is self.head:
            self.head = self.head.next
        else:
            # find prev node in list
            prev_node = self.head
            while prev_node.next is not node:
                prev_node = prev_node.next
                if prev_node is None:  # not in list
                    raise ValueError("Node not in list")
            # remove node
            prev_node.next = node.next

    def get_mth_to_last(self, m):
        if self.head is None:
            raise ValueError("Empty list")
        mth_to_last = self.head
        plus_m = self.head
        # find plus_m
        for i in range(m):
            plus_m = plus_m.next
            if plus_m is None:
                raise ValueError("List has fewer than {0} elements.".format(m+1))
        # traverse until list end
        while plus_m.next is not None:
            plus_m = plus_m.next
            mth_to_last = mth_to_last.next
        return mth_to_last

if __name__ == "__main__":
    ns = [Node(i) for i in range(10)]
    ll = LinkedList()
    for n in ns:
        ll.insert_before(n)
        
    
