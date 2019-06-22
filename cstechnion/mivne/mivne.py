from copy import deepcopy


class BinTree:
    def __init__(self, key, value, left=None, right=None):
        self.key = key
        self.value = value
        self.left = left
        self.right = right

    def __deepcopy__(self, memo={}):
        left = deepcopy(self.left) if self.left else None
        right = deepcopy(self.right) if self.right else None
        return BinTree(deepcopy(self.key), deepcopy(self.value), left, right)

    def pre_order(self):
        return [(self.key, self.value)] + \
               self.left.pre_order() if self.left else [] + \
               self.right.pre_order() if self.right else []

    def in_order(self):
        return (self.left.in_order() if self.left else []) + \
               [(self.key, self.value)] + \
               (self.right.in_order() if self.right else [])

    def post_order(self):
        return self.left.post_order() if self.left else [] + \
               self.right.post_order() if self.right else [] + \
               [(self.key, self.value)]

    def leaf_bin_keys(self, bin_prefix=''):
        """ get binary path (0 for Left, 1 for Right) to all leafs (in order), with the leafs' values """
        if self.left or self.right:
            leafs = []
            if self.left:
                leafs += self.left.leaf_bin_keys(bin_prefix + '0')
            if self.right:
                leafs += self.right.leaf_bin_keys(bin_prefix + '1')
            return leafs
        else:
            return [(self.value, bin_prefix)]

    def insert(self, node):     # binary insertion to binary tree, with node.key as key.
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
        res = deepcopy(self)
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
    add general RANK_Tree
    add HashTables (chain hashing, skip-hashing)
    add UnionFind
    add Heap (do the heapq: heapify, heappop, heappush..)
    add bucket/radix/heap/quick_sort
    add Get Median in O(n), select[i] in O(n)
    add Trie, Suffix tree (and several-words-Suffix_Tree)
    add Ziv-Lempel (tirgul 12) 
    add topological sort (to graphs)
"""
