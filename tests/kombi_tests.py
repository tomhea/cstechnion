import unittest

from cstechnion.kombi.Basics import pascal_triangle


class KombiTests(unittest.TestCase):
    # TODO: Basics.py:  mul, C,P,CC,PP,multinom, Dn,Cn, pigeonhole, subgroups,subgroups_with_elements_of, n_letter_words

    @staticmethod
    def test_pascal_triangle():
        assert pascal_triangle(10) == [[1], [1, 1], [1, 2, 1], [1, 3, 3, 1], [1, 4, 6, 4, 1], [1, 5, 10, 10, 5, 1], [1, 6, 15, 20, 15, 6, 1], [1, 7, 21, 35, 35, 21, 7, 1], [1, 8, 28, 56, 70, 56, 28, 8, 1], [1, 9, 36, 84, 126, 126, 84, 36, 9, 1], [1, 10, 45, 120, 210, 252, 210, 120, 45, 10, 1]]

    # TODO: NaiveGraphs.py: Graph  : d/d_in/d_out, str(), eulerian_path/cycle
    # TODO: NaiveGraphs.py: DiGraph: d/d_in/d_out, str(), eulerian_path/cycle, de_bruijn, to_undirected_graph


if __name__ == '__main__':
    unittest.main()
