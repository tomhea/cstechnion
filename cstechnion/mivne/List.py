from copy import deepcopy


class Node:
    def __init__(self, value=None, prev=None, next=None, list=None):
        self.value = value
        self.prev = prev
        self.next = next
        self.list = list

    def __str__(self):
        return str(self.value)

    def __getitem__(self, i):       # get the value of the i'th node ( curr(0)-->curr.next(1)-->curr.next.next(2) )
        return self.next[i-1] if i else self.value


class List:
    def __init__(self, collection=[]):
        self.count = 0
        self.first = None
        self.last = None
        for v in collection:
            self += v

    def push_back(self, v):     # append Node(v) to the end of the list
        n = Node(v, self.last, None, self)
        if self.last:
            self.last.next = n
        else:
            self.first = n
        self.last = n
        self.count += 1

    def push_front(self, v):    # push Node(v) at the start of the list
        n = Node(v, None, self.first, self)
        if self.first:
            self.first.prev = n
        else:
            self.last = n
        self.first = n
        self.count += 1

    def delete_last(self):      # delete the last node on the list
        if self.last is None:
            return None
        self.last = self.last.prev
        if self.last:
            self.last.next = None
        else:
            self.first = None
        self.count -= 1

    def delete_first(self):     # delete the first node on the list
        if self.first:
            self.first = self.first.next
            if self.first:
                self.first.prev = None
            else:
                self.last = None
            self.count -= 1

    def __len__(self):
        return self.count

    def __bool__(self):
        return self.count > 0

    def concatenate(self, l, make_copy=False):       # concatenate self-->l lists together
        if self == l or make_copy:
            l = deepcopy(l)
        if not self:
            self.count = l.count
            self.first = l.first
            self.last = l.last
        elif l:
            self.count += l.count
            l.first.prev = self.last
            self.last.next = l.first
            self.last = l.last

    def to_array(self):             # generate an array of values from the list's nodes
        arr = []
        n = self.first
        while n:
            arr.append(n.value)
            n = n.next
        return arr

    def __getitem__(self, i):       # get the i'th item on the list
        if i >= 0 or i < self.count:
            return self.first[i]

    def __str__(self):
        return '-->'.join([''] + [str(v) for v in self.to_array()] + ['null'])

    def remove_node(self, n):       # remove a !Node! from the list.
        if self:
            if n == self.last:
                self.last = n.prev
                if self.last:
                    self.last.next = None
            elif n == self.first:
                self.first = n.next
                if self.first:
                    self.first.prev = None
            else:
                n.prev.next, n.next.prev = n.next, n.prev   # lose track of n

            self.count -= 1

    def __isub__(self, n):
        self.remove_node(n)
        return self

    def __iadd__(self, v):
        self.push_back(v)
        return self

    def __iter__(self):
        return self.to_array().__iter__()

    def __deepcopy__(self, memo={}):
        return List(self.to_array())

    def __eq__(self, l):
        return self.count, self.first, self.last == l.count, l.first, l.last

    def __contains__(self, v):
        return v in self.to_array()
