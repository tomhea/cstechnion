import unittest

from cstechnion.mivne.List import List
from cstechnion.mivne.ListGraphs import Graph as ListGraph, DiGraph as ListDiGraph
from cstechnion.mivne.MatGraphs import Graph as MatGraph, DiGraph as MatDiGraph


class MivneTests(unittest.TestCase):
    @staticmethod
    def test_list():
        # Check list creation
        a = [i * i for i in range(10)]
        l = List(a)
        assert l.to_array() == [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]
        assert l.to_array() == [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]
        assert str(l) == '-->0-->1-->4-->9-->16-->25-->36-->49-->64-->81-->null'

        # Check push_back's and indexing(l[i])
        l = List()
        l.push_back(1)
        assert [l[i] for i in range(len(l))] == l.to_array()
        l.push_back(2)
        assert [l[i] for i in range(len(l))] == l.to_array()
        l.push_front(0)
        assert [l[i] for i in range(len(l))] == l.to_array()
        l.push_front(-1)
        assert [l[i] for i in range(len(l))] == l.to_array()
        l.push_front(-5)
        assert [l[i] for i in range(len(l))] == l.to_array()
        assert l.to_array() == [-5, -1, 0, 1, 2]
        assert len(l) == 5

        # Check deletes
        l.delete_first()
        assert l.to_array() == [-1, 0, 1, 2]
        l.delete_first()
        assert l.to_array() == [0, 1, 2]
        l.delete_last()
        assert l.to_array() == [0, 1]
        l.delete_last()
        assert l.to_array() == [0]
        l.delete_first()
        assert l.to_array() == []
        assert (l.count, l.first, l.last) == (0, None, None)

        # Check initial push_front
        l.push_front(42)
        assert l.to_array() == [42]
        l.push_front(38)
        assert l.to_array() == [38, 42]
        l.push_back(12)
        assert l.to_array() == [38, 42, 12]

        # Check iteration
        a = [i * i * i for i in range(10 + 1)]
        l = List(a)
        assert [i for i in l] == a

        # Check concatenation between 2 Lists
        def check_concatenation(a1, a2):
            l1, l2 = List(a1), List(a2)
            l1.concatenate(l2)
            assert l1.to_array() == a1 + a2
            assert l2.to_array() == a2
            l1, l2 = List(a1), List(a2)
            l2.concatenate(l1)
            assert l1.to_array() == a1
            assert l2.to_array() == a2 + a1
            l1, l2 = List(a1), List(a2)
            l1.concatenate(l1)
            assert l1.to_array() == a1 + a1
            l2.concatenate(l2)
            assert l2.to_array() == a2 + a2

        # Check concatenation between 3 Lists
        def check_triple_concatenation(a1, a2, a3):
            l1, l2, l3 = List(a1), List(a2), List(a3)
            l1.concatenate(l2)
            l1.concatenate(l3)
            assert l1.to_array() == a1 + a2 + a3
            assert l2.to_array() == a2
            assert l3.to_array() == a3
            l1, l2, l3 = List(a1), List(a2), List(a3)
            l2.concatenate(l3)
            l1.concatenate(l2)
            assert l1.to_array() == a1 + a2 + a3
            assert l2.to_array() == a2 + a3
            assert l3.to_array() == a3

        # Check concatenation
        a1, a2, a3 = [i * i + 1 for i in range(10)], [i * i + 2 for i in range(10)], [i ** 4 for i in range(10)]
        check_concatenation(a1, a2)
        check_concatenation(a1, [])
        check_concatenation([], [])
        check_triple_concatenation(a1, a2, a3)
        check_triple_concatenation(a1, a2, [])
        check_triple_concatenation(a1, [], a3)
        check_triple_concatenation([], a2, a3)
        check_triple_concatenation([], [], a3)
        check_triple_concatenation(a1, [], [])
        check_triple_concatenation([], [], [])

        # Check remove_node
        a = [7 * i for i in range(0, 17, 3)]
        l = List(a)
        assert str(l) == '-->0-->21-->42-->63-->84-->105-->null'
        l -= l.first.next
        assert str(l) == '-->0-->42-->63-->84-->105-->null'
        l -= l.first.next.next
        assert str(l) == '-->0-->42-->84-->105-->null'
        l -= l.last.prev.prev
        assert str(l) == '-->0-->84-->105-->null'

    @staticmethod
    def test_ListGraph_ListDiGraph():
        # Check undirected graph creation, add_vertex/edge, and str()
        V = [5, 7, 8] + [1, 6]
        E = [(1, 5), (1, 7), (1, 8), (7, 8), (8, 5)]
        ug = ListGraph([5, 7, 8])
        ug.add_vertex(1)
        ug.add_vertex(6)
        for e in E:
            ug += e
        for u in V:
            for v in V:
                assert ((u, v) in ug) is (((u, v) in E) or ((v, u) in E))
        assert str(ug) == '(5):-->1-->8-->null   (7):-->1-->8-->null   (8):-->1-->7-->5-->null   (1):-->5-->7-->8-->null   (6):-->null'

        # Check directed graph creation, add_vertex/edge, and str()
        _g = ListDiGraph([5, 7, 8])
        _g.add_vertex(1)
        _g.add_vertex(6)
        for e in E:
            _g += e
        for u in V:
            for v in V:
                assert ((u, v) in _g) is ((u, v) in E)
        assert str(_g) == '(5):-->null   (7):-->8-->null   (8):-->5-->null   (1):-->5-->7-->8-->null   (6):-->null'

        # Check topological_sort and is_cyclic
        g = MatDiGraph([1, 2, 3, 4], [(3, 2), (1, 2)])
        assert g.topological_sort() == {1: 0, 3: 1, 2: 2, 4: 3}
        assert not g.is_cyclic()
        g = ListDiGraph([1, 2, 3, 4], [(4, 1), (3, 2), (1, 2)])
        assert g.topological_sort() == {3: 0, 4: 1, 1: 2, 2: 3}
        assert not g.is_cyclic()
        g = ListDiGraph([1, 2, 3, 4], [(4, 1), (3, 2), (1, 2), (2, 4)])
        assert g.topological_sort() is None
        assert g.is_cyclic()

        # Check to_undirected_graph:
        _ug = g.to_undirected_graph()
        assert str(_ug) == '(1):-->2-->4-->null   (2):-->4-->1-->3-->null   (3):-->2-->null   (4):-->1-->2-->null'

    @staticmethod
    def test_MatGraph_MatDiGraph():
        # Check undirected graph creation, add_vertex/edge, and str()
        V = [5, 7, 8] + [1, 6]
        E = [(1,5), (1,7), (1,8), (7,8), (8,5)]
        ug = MatGraph(V)
        for e in E:
            ug += e
        for u in V:
            for v in V:
                assert ((u,v) in ug) is (((u,v) in E) or ((v,u) in E))
        assert str(ug) == '(5):-->8-->1-->null   (7):-->8-->1-->null   (8):-->5-->7-->1-->null   (1):-->5-->7-->8-->null   (6):-->null'

        # Check directed graph creation, add_vertex/edge, and str()
        _g = MatDiGraph(V)
        for e in E:
            _g += e
        for u in V:
            for v in V:
                assert ((u,v) in _g) is ((u,v) in E)
        assert str(_g) == '(5):-->null   (7):-->8-->null   (8):-->5-->null   (1):-->5-->7-->8-->null   (6):-->null'

        # Check topological_sort and is_cyclic
        g = MatDiGraph([1, 2, 3, 4], [(3, 2), (1, 2)])
        assert g.topological_sort() == {1: 0, 3: 1, 2: 2, 4: 3}
        assert not g.is_cyclic()
        g = MatDiGraph([1, 2, 3, 4], [(4, 1), (3, 2), (1, 2)])
        assert g.topological_sort() == {3: 0, 4: 1, 1: 2, 2: 3}
        assert not g.is_cyclic()
        g = MatDiGraph([1, 2, 3, 4], [(4, 1), (3, 2), (1, 2), (2, 4)])
        assert g.topological_sort() is None
        assert g.is_cyclic()

        # Check to_undirected_graph:
        _ug = g.to_undirected_graph()
        assert str(_ug) == '(1):-->2-->4-->null   (2):-->1-->3-->4-->null   (3):-->2-->null   (4):-->1-->2-->null'


if __name__ == '__main__':
    unittest.main()
