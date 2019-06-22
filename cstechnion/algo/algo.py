from heapq import heapify, heappop, heappush

from cstechnion.mivne.mivne import BinTree


def get_char_hist(text):
    """ generate the characters histogram from the given text """
    hist = {}
    for c in text:
        if c in hist:
            hist[c] += 1
        else:
            hist[c] = 1
    return hist.items()


def huffman(hist):
    """ hist = [(letter1, frequency1), (l2, f2), ...] """
    h = [BinTree(n[1], n[0]) for n in hist]
    heapify(h)

    for i in range(len(h) - 1):
        n1 = heappop(h)
        n2 = heappop(h)
        heappush(h, BinTree(n1.key + n2.key, '', n2, n1))

    t = heappop(h)
    return t.leaf_bin_keys()


def huffman_encode(text, huff_code):
    """ replace every character in text with its huffman binary-representation """
    enc_text = ''
    huff_dict = dict(huff_code)
    for c in text:
        enc_text += huff_dict[c]
    return enc_text


def huffman_decode(enc_text, huff_code):
    """ convert every binary-code to the character it represents, and return the decoded text """
    dec_text = ''
    huff_dict = {b:c for c,b in huff_code}
    curr_bin = ''

    for b in enc_text:
        curr_bin += b
        if curr_bin in huff_dict:
            dec_text += huff_dict[curr_bin]
            curr_bin = ''

    return dec_text


"""
TODO:
    after graphes implemented (in Graph.py):
    add BFS, DFS
    add [Get SCC Graph]
    add Prim, Kruskal (minimal tree)
    add Dijkstra (shortest from s, without negative edges), Bellman-Ford (also, but without negative circles)
    add Johnson (shortest from general v->u)
    add Minimal Vertex Cover, and Knapsack problam (on tirgul 10)
    
    this file's name should be changed to huffman.py, or to be written in a algorithms.py file
"""
