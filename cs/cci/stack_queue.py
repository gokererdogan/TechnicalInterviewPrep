class Node(object):
    def __init__(self, data, next=None):
        self.data = data
        self.next = next

    def __repr__(self):
        return repr(self.data)

class Stack(object):
    def __init__(self):
        self.top = None

    def push(self, data):
        n = Node(data, next=self.top)
        self.top = n

    def pop(self):
        if self.top is None:
            raise IndexError("Stack empty.")
        data = self.top.data
        self.top = self.top.next
        return data

    def is_empty(self):
        return self.top == None

    def __repr__(self):
        items = []
        current = self.top
        while True:
            if current is not None:
                items.append(repr(current))
            else:
                break
            current = current.next
        return " ".join(items)
        

class Queue(object):
    def __init__(self):
        self.first = None
        self.last = None
    
    def add(self, data):
        n = Node(data, next=None)
        if self.last is None:
            self.first = n
        else:
            self.last.next = n
        self.last = n

    def remove(self):
        if self.first is None:
            raise IndexError("Queue empty.")
        
        data = self.first.data
        if self.first is self.last:
            self.first = None
            self.last = None
        else:
            self.first = self.first.next
        return data

    def is_empty(self):
        return self.first is None
    
    def __repr__(self):
        items = []
        current = self.first
        while True:
            if current is not None:
                items.append(repr(current))
            else:
                break
            current = current.next
        return " ".join(items)
        
