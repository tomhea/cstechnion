import unittest

from cstechnion.automata.DFA import DFA
from cstechnion.automata.NFA import NFA


class AutomataTests(unittest.TestCase):
    @staticmethod
    def test_DFA():
        # Fibonacci-Base Automata (all binary without 11, ending with 1)
        def d(q, a):
            if q == 2:
                return 2
            if a == '0':
                return 0
            return q + 1

        A = DFA([0, 1, 2], '01', 0, d, [1])
        assert '' not in A
        assert '11' not in A
        assert '10' not in A
        assert '101' in A
        assert A.to_regex() == '((0*1)(00*1)*)'
        assert A.get_Ln(5) == ['1', '01', '001', '101', '0001', '0101', '1001', '00001', '00101', '01001', '10001', '10101']
        Ln = A.get_Ln(5)
        L, n = [], len(Ln)
        for w in A.get_L():
            L.append(w)
            if len(L) >= n:
                break
        assert L == Ln

        # Even number of 0's Automata
        def d2(q, a):
            return q if a == '1' else 1 - q

        A2 = DFA([0, 1], '01', 0, d2, [0])
        assert A2.to_regex() == 'ε+((1*1)+(1*0)(1+01*0)*(01*))'
        assert A.get_Ln(5, '10101') == ['10101', '1010101', '10101001', '101010001', '101010101', '1010100001', '1010100101', '1010101001']
        A.add_prefix('tom')
        assert A.Q == [0, 1, 2, '_pre0', '_pre1', '_pre2', '_pre_false']
        assert A.q0 == '_pre0'
        assert A.d('_pre0', '0') == '_pre_false'
        d_lines = []
        for q in A.Q:
            for a in A.S:
                d_lines.append('d({},{})={}'.format(q, a, A.d(q, a)))
        assert '#'.join(d_lines) == 'd(0,0)=0#d(0,1)=1#d(0,t)=_pre_false#d(0,o)=_pre_false#d(0,m)=_pre_false#d(1,0)=0#d(1,1)=2#d(1,t)=_pre_false#d(1,o)=_pre_false#d(1,m)=_pre_false#d(2,0)=2#d(2,1)=2#d(2,t)=_pre_false#d(2,o)=_pre_false#d(2,m)=_pre_false#d(_pre0,0)=_pre_false#d(_pre0,1)=_pre_false#d(_pre0,t)=_pre1#d(_pre0,o)=_pre_false#d(_pre0,m)=_pre_false#d(_pre1,0)=_pre_false#d(_pre1,1)=_pre_false#d(_pre1,t)=_pre_false#d(_pre1,o)=_pre2#d(_pre1,m)=_pre_false#d(_pre2,0)=_pre_false#d(_pre2,1)=_pre_false#d(_pre2,t)=_pre_false#d(_pre2,o)=_pre_false#d(_pre2,m)=0#d(_pre_false,0)=_pre_false#d(_pre_false,1)=_pre_false#d(_pre_false,t)=_pre_false#d(_pre_false,o)=_pre_false#d(_pre_false,m)=_pre_false'
        assert A.get_Ln(7) == ['tom1', 'tom01', 'tom001', 'tom101', 'tom0001', 'tom0101', 'tom1001']
        A.add_prefix('tomtom')
        assert A.get_Ln(7) == []
        Ln = A.get_Ln(5, 'tomtomtom')
        L, n = [], len(Ln)
        for w in A.get_L('tomtomtom'):
            L.append(w)
            if len(L) >= n:
                break
        assert L == Ln

    @staticmethod
    def test_NFA():
        # Fibonacci-Base Automata (all binary without 11, ending with 1)
        def d(q, a):
            if a == '0':
                return {0}
            if q == 0:
                return {1}
            return set()

        A = NFA([0, 1], '01', 0, d, [1])
        assert '' not in A
        assert A.d_hat(A.q0, '') == {0}
        assert '11' not in A
        assert A.d_hat(A.q0, '11') == set()
        assert '10' not in A
        assert A.d_hat(A.q0, '10') == {0}
        assert '101' in A
        assert A.d_hat(A.q0, '101') == {1}
        assert A.get_Ln(4) == ['1', '01', '001', '101', '0001', '0101', '1001']

        # Check L
        Ln = A.get_Ln(5)
        L, n = [], len(Ln)
        for w in A.get_L():
            L.append(w)
            if len(L) >= n:
                break

        DA = A.to_DFA()
        assert '' not in DA
        assert DA.d_hat(DA.q0, '') == {0}
        assert '11' not in DA
        assert DA.d_hat(DA.q0, '11') == set()
        assert '10' not in DA
        assert DA.d_hat(DA.q0, '10') == {0}
        assert '101' in DA
        assert DA.d_hat(DA.q0, '101') == {1}
        assert DA.get_Ln(4) == ['1', '01', '001', '101', '0001', '0101', '1001']

        # Check L
        Ln = A.get_Ln(5)
        L, n = [], len(Ln)
        for w in A.get_L():
            L.append(w)
            if len(L) >= n:
                break

        # HECK COPY
        last_d = A.d
        A.d = lambda q, a: {q}  # Checks if changes in A.d not affect d_hat_hat (i.e. DA.d)
        assert '' not in DA
        assert DA.d_hat(DA.q0, '') == {0}
        d_list = []
        for q in DA.Q:
            for a in DA.S:
                d_list.append('d({}, {}) = {}'.format(q, a, DA.d(q, a)))
        assert '#'.join(d_list) == 'd(set(), 0) = set()#d(set(), 1) = set()#d({0}, 0) = {0}#d({0}, 1) = {1}#d({1}, 0) = {0}#d({1}, 1) = set()#d({0, 1}, 0) = {0}#d({0, 1}, 1) = {1}'
        assert '101' in DA
        assert DA.d_hat(DA.q0, '101') == {1}
        assert DA.get_Ln(4) == ['1', '01', '001', '101', '0001', '0101', '1001']
        A.d = last_d
        assert len(DA.get_Ln(5)) + 1 == 13

        # Check add prefix, d, Ln, double-add-prefix
        A.add_prefix('tom')
        assert A.Q == [0, 1, '_pre0', '_pre1', '_pre2']
        assert A.S == '01tom'
        assert A.q0 == '_pre0'
        assert A.F == [1]
        d_list = []
        for q in A.Q:
            for a in A.S:
                d_list.append('d({}, {}) = {}'.format(q, a, A.d(q, a)))
        assert '#'.join(d_list) == "d(0, 0) = {0}#d(0, 1) = {1}#d(0, t) = set()#d(0, o) = set()#d(0, m) = set()#d(1, 0) = {0}#d(1, 1) = set()#d(1, t) = set()#d(1, o) = set()#d(1, m) = set()#d(_pre0, 0) = set()#d(_pre0, 1) = set()#d(_pre0, t) = {'_pre1'}#d(_pre0, o) = set()#d(_pre0, m) = set()#d(_pre1, 0) = set()#d(_pre1, 1) = set()#d(_pre1, t) = set()#d(_pre1, o) = {'_pre2'}#d(_pre1, m) = set()#d(_pre2, 0) = set()#d(_pre2, 1) = set()#d(_pre2, t) = set()#d(_pre2, o) = set()#d(_pre2, m) = {0}"

        assert A.get_Ln(7) == ['tom1', 'tom01', 'tom001', 'tom101', 'tom0001', 'tom0101', 'tom1001']
        assert A.get_Ln(4, 'tom') == ['tom1', 'tom01', 'tom001', 'tom101', 'tom0001', 'tom0101', 'tom1001']

        A.add_prefix('tom')
        assert A.Q == [0, 1, '_pre0', '_pre1', '_pre2', '__pre0', '__pre1', '__pre2']
        assert A.S == '01tom'
        assert A.q0 == '__pre0'
        assert A.F == [1]
        d_list = []
        for q in A.Q:
            for a in A.S:
                d_list.append('d({}, {}) = {}'.format(q, a, A.d(q, a)))
        assert '#'.join(d_list) == "d(0, 0) = {0}#d(0, 1) = {1}#d(0, t) = set()#d(0, o) = set()#d(0, m) = set()#d(1, 0) = {0}#d(1, 1) = set()#d(1, t) = set()#d(1, o) = set()#d(1, m) = set()#d(_pre0, 0) = set()#d(_pre0, 1) = set()#d(_pre0, t) = {'_pre1'}#d(_pre0, o) = set()#d(_pre0, m) = set()#d(_pre1, 0) = set()#d(_pre1, 1) = set()#d(_pre1, t) = set()#d(_pre1, o) = {'_pre2'}#d(_pre1, m) = set()#d(_pre2, 0) = set()#d(_pre2, 1) = set()#d(_pre2, t) = set()#d(_pre2, o) = set()#d(_pre2, m) = {0}#d(__pre0, 0) = set()#d(__pre0, 1) = set()#d(__pre0, t) = {'__pre1'}#d(__pre0, o) = set()#d(__pre0, m) = set()#d(__pre1, 0) = set()#d(__pre1, 1) = set()#d(__pre1, t) = set()#d(__pre1, o) = {'__pre2'}#d(__pre1, m) = set()#d(__pre2, 0) = set()#d(__pre2, 1) = set()#d(__pre2, t) = set()#d(__pre2, o) = set()#d(__pre2, m) = {'_pre0'}"
        assert A.get_Ln(7) == ['tomtom1']
        assert A.get_Ln(4, 'tomtom') == ['tomtom1', 'tomtom01', 'tomtom001', 'tomtom101', 'tomtom0001', 'tomtom0101', 'tomtom1001']

        DA = A.to_DFA()
        d_list = []
        for q in A.Q:
            for a in A.S:
                d_list.append('d({}, {}) = {}'.format(q, a, A.d(q, a)))
        assert '#'.join(d_list) == "d(0, 0) = {0}#d(0, 1) = {1}#d(0, t) = set()#d(0, o) = set()#d(0, m) = set()#d(1, 0) = {0}#d(1, 1) = set()#d(1, t) = set()#d(1, o) = set()#d(1, m) = set()#d(_pre0, 0) = set()#d(_pre0, 1) = set()#d(_pre0, t) = {'_pre1'}#d(_pre0, o) = set()#d(_pre0, m) = set()#d(_pre1, 0) = set()#d(_pre1, 1) = set()#d(_pre1, t) = set()#d(_pre1, o) = {'_pre2'}#d(_pre1, m) = set()#d(_pre2, 0) = set()#d(_pre2, 1) = set()#d(_pre2, t) = set()#d(_pre2, o) = set()#d(_pre2, m) = {0}#d(__pre0, 0) = set()#d(__pre0, 1) = set()#d(__pre0, t) = {'__pre1'}#d(__pre0, o) = set()#d(__pre0, m) = set()#d(__pre1, 0) = set()#d(__pre1, 1) = set()#d(__pre1, t) = set()#d(__pre1, o) = {'__pre2'}#d(__pre1, m) = set()#d(__pre2, 0) = set()#d(__pre2, 1) = set()#d(__pre2, t) = set()#d(__pre2, o) = set()#d(__pre2, m) = {'_pre0'}"
        assert DA.get_Ln(7) == ['tomtom1']
        assert DA.get_Ln(4, 'tomtom') == ['tomtom1', 'tomtom01', 'tomtom001', 'tomtom101', 'tomtom0001', 'tomtom0101', 'tomtom1001']

    def test_NFAe(self):
        # TODO: finish all todo's in NFAe.py (implement algo.Graphs first)
        # TODO: and then test NFAe (somehow similar to NFA)
        pass    # TODO test


if __name__ == '__main__':
    unittest.main()

# TODO: add documentation to all tests
