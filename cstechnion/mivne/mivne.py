class BinTree:
    def __init__(self, key, value, left=None, right=None):
        self.key = key
        self.value = value
        self.left = left
        self.right = right

    def copy(self):
        left = self.left.copy() if self.left else None
        right = self.right.copy() if self.right else None
        return BinTree(self.key, self.value, left, right)

    def pre_order(self):
        return [(self.key, self.value)] + \
               self.left.pre_order() if self.left else [] + \
               self.right.pre_order() if self.right else []

    def in_order(self):
        return (self.left.in_order() if self.left else []) + \
               [(self.key, self.value)] + \
               (self.right.in_order() if self.right else [])

    def leaf_bin_keys(self, bin_prefix=''):
        if self.left or self.right:
            leafs = []
            if self.left:
                leafs += self.left.leaf_bin_keys(bin_prefix + '0')
            if self.right:
                leafs += self.right.leaf_bin_keys(bin_prefix + '1')
            return leafs
        else:
            return [(self.value, bin_prefix)]

    def post_order(self):
        return self.left.post_order() if self.left else [] + \
               self.right.post_order() if self.right else [] + \
               [(self.key, self.value)]

    def insert(self, node):
        if isinstance(node, tuple):
            key, value = node
            node = BinTree(key, value)

        if node.key < self.key:
            if self.left is None:
                self.left = node
            else:
                self.left.insert(node)
        else:
            if self.right is None:
                self.right = node
            else:
                self.right.insert(node)

    def __iadd__(self, other):
        self.insert(other)
        return self

    def __add__(self, other):
        res = self.copy()
        res += other
        return res

    def __str__(self):
        return ' '.join(str(n) for n in self.in_order())

    def __len__(self):
        return len(self.in_order())

    def __lt__(self, other):
        return self.key < other.key


""" 
TODO:
    add AVL_Tree
    add Heap (do the heapq: heapify, heappop, heappush..)
    add UnionFind
    add Trie
    add topological sort (to graphs)
    add Get Median in O(n), partition-sort
    
"""
