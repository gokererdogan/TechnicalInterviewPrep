import linked_list as ll

class Stack(object):
    def __init__(self):
        self.list = ll.LinkedList()

    def __str__(self):
        return str(self.list)

    def __repr__(self):
        return str(self)

    def push(self, data):
        node = ll.Node(data)
        self.list.insert_before(node, self.list.head)

    def pop(self):
        if self.list.head is None:
            raise ValueError("Stack empty")
        data = self.list.head.data
        self.list.delete(self.list.head)
        return data
