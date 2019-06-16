from math import factorial
from itertools import combinations


def mul(a):
    product = 1
    for x in a:
        product *= x
    return product


def C(n, k):
    return mul(range(n-k+1, n+1)) * factorial(k)


def P(n, k):
    return mul(range(n-k+1, n+1))


def CC(n, k):
    return False    # TODO


def PP(n, k):
    return False    # TODO


def subgroups(g, smallest=0, biggest=None):
    if biggest is None:
        biggest = len(g)
    return [set(comb) for n in range(smallest, biggest + 1) for comb in combinations(g, n)]


def subgroups_with_elements_of(g, elements):
    g_minus_elements = [e for e in g if e not in elements]
    return [sg.union(se) for sg in subgroups(g_minus_elements) for se in subgroups(elements, 1)]

"""
TODO:
    add more mathematical things
    add the Pascal triangle
    add Graphs..
    add Catalan numbers
"""
