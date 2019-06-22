from itertools import combinations, product

from math import factorial


def mul(a):
    product = 1
    for x in a:
        product *= x
    return product


def C(n, k):
    """ choose k students from a class of n """
    return mul(range(n-k+1, n+1)) // factorial(k)


def P(n, k):
    """ choose an ordered list of k students from a class of n """
    return mul(range(n-k+1, n+1))


def CC(n, k):
    """ Put k equal balls in n cells
        number of solutions to: X1+X2+...+Xn = k, (Xi >= 0)
    """
    return C(n + k - 1, k)


def PP(n, k):
    """ choose (for k times) a student from a class of n """
    return n ** k


def multinom(n, *kargs):
    left = n - sum(kargs)
    return mul(range(left+1, n+1)) // mul([factorial(k) for k in kargs])


def pascal_triangle(n):
    tri = []
    for line in range(n+1):
        tri.append([1] * (line + 1))
        for i in range(1, line):
            tri[-1][i] = tri[-2][i-1] + tri[-2][i]
    return tri


def Dn(n):
    """ number of Disorders (shuffle n people in line, such that everyone switched his place) """
    return sum((-1)**r * mul(range(r+1, n+1)) for r in range(n+1))


def Cn(n):
    """ Catalan number (examples for n=3, Cn=5):
        * number of valid parenthesis series with n-pairs. ((())), ()(()), (())(), ()()(), (()()).
        * number of routs below the main diagonal from (0,0) to (n,n). RRRUUU, RRURUU, RRUURU, RURRUU, RURURU (Right-Up)
        * number of binary trees.   _-^   -_^   -^-   ^_-   ^-_  (^root, lower == son_of)
        * number of ordered forests.   .·.   :·    ·:    ...    ⋮
    """
    return C(2*n, n) // (n+1)


def pigeonhole(pigeons, holes):
    return (pigeons + holes - 1) // holes


def subgroups(g, smallest=0, biggest=None):
    if biggest is None:
        biggest = len(g)
    return [set(comb) for n in range(smallest, biggest + 1) for comb in combinations(g, n)]


def subgroups_with_elements_of(g, elements):
    g_minus_elements = [e for e in g if e not in elements]
    return [sg.union(se) for sg in subgroups(g_minus_elements) for se in subgroups(elements, 1)]


def n_letter_words(S, n):
    words = []
    for w in product(S, n):
        words.append(''.join(w))
    return words

# TODO finish documentation
