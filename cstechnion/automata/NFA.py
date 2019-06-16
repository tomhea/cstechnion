from itertools import product
from cstechnion.automata.DFA import DFA
from cstechnion.kombi.kombi import subgroups, subgroups_with_elements_of


class NFA:  # Deterministic Finite Automation
    def __init__(self, Q, S, q0, d, F):
        """
            Q  = States (iterable)
            S  = Alphabet (string)
            q0 = start-state
            d  = Transition-Function (d: Q×S -> 2^Q) (2^Q is a set(q∈Q))
            F  = Accept-States
        """
        self.Q = list(Q)
        self.S = S
        self.q0 = q0
        self.d = d
        self.F = list(F)

    def __len__(self):
        return len(self.Q)      # number of states

    def minimize(self):
        pass  # TODO realy do something

    def accept(self, w):
        new_states = self.d_hat(self.q0, w)
        for f in self.F:
            if f in new_states:     # new_q ∩ F ≠ ∅
                return True
        return False                # new_q ∩ F = ∅

    def d_hat(self, q, w):    # δ^(q, w) # w = ua (u∈Σ*, a∈Σ)
        new_states = {q}  # new_q = q0
        for a in w:  # for every letter a in w:
            old_states, new_states = new_states, set()
            for q in old_states:
                new_states.update(self.d(q, a))  # new_states += δ(q, a)
        return new_states

    def d_hat_hat(self, p, w):      # δ^^(P, w)
        new_states = set()
        for q in p:                 # for every q∈P:
            new_states = new_states.union(self.d_hat(q, w))     # new_states += δ^(q, w)
        return new_states

    def __contains__(self, w):
        return self.accept(w)

    def get_Ln(self, n, prefix=''):
        """ return all the (up to n letters) words in L
            if prefix entered,
                return all the words of the form [prefix][Σ*], such as the second part is up to n letters """
        Ln = []
        for n in range(n + 1):
            for letters in product(self.S, repeat=n):
                w = prefix + ''.join(letters)
                if w in self:
                    Ln.append(w)
        return Ln

    def get_L(self, prefix=''):
        """ generate the next word in L alphabetically
            if prefix entered, generate words of the form: [prefix][Σ*] """
        n = 0
        while True:
            for letters in product(self.S, repeat=n):
                w = prefix + ''.join(letters)
                if w in self:
                    yield w
            n += 1

    def _first_pre_name(self):
        count = 0
        _pre = 'pre'
        while True:
            _pre = '_' + _pre
            for q in self.Q:
                if type(q) is str and q.startswith(_pre):
                    count += 1
                    break
            if count == 0:
                return _pre
            count = 0

    def add_prefix(self, w):    # TODO: change from DFA implementation to NFA implementation (i.e remove garbage_q state,...)
        if len(w) > 0:
            _pre = self._first_pre_name()
            new_d = {}

            new_q0 = curr_q = _pre + '0'
            self.Q.append(curr_q)
            for i in range(1, len(w)):
                last_q, curr_q = curr_q, _pre + str(i)
                self.Q.append(curr_q)
                new_d[last_q, w[i - 1]] = {curr_q}
            new_d[curr_q, w[-1]] = {self.q0}

            new_letters = ''.join([a for a in dict.fromkeys(w) if a not in self.S])
            old_d = self.d
            self.d = lambda q, a: new_d.get((q, a), set()) if a in new_letters or type(q) is str and q.startswith(_pre) else old_d(q, a)
            self.q0 = new_q0
            self.S += new_letters

    def to_DFA(self):
        new_Q = subgroups(self.Q)
        new_S = self.S
        new_q0 = {self.q0}
        new_d = self.d_hat_hat
        new_F = subgroups_with_elements_of(self.Q, self.F)
        return DFA(new_Q, new_S, new_q0, new_d, new_F)


"""
TODO:
    add Regex (built with {+·*()}, and around S (some alphabet)
    add (Union), (Same), (iterations) to all 3 Automata's
    add NFA (Non-deterministic Finite Automaton)
    add NFAe (Non-deterministic Finite Automaton with Epsilon moves)
"""


def _test():

    def d(q, a):
        if a == '0':
            return {0}
        if q == 0:
            return {1}
        return set()

    A = NFA([0, 1], '01', 0, d, [1])
    print('' in A)
    print(A.d_hat(A.q0, ''))
    # print('11' in A)
    # print(A.d_hat(A.q0, '11'))
    # print('10' in A)
    # print(A.d_hat(A.q0, '10'))
    print('101' in A)
    print(A.d_hat(A.q0, '101'))
    print(A.get_Ln(4), '\n')

    DA = A.to_DFA()
    print('' in DA)
    print(DA.d_hat(DA.q0, ''))
    # print('11' in DA)
    # print(DA.d_hat(DA.q0, '11'))
    # print('10' in DA)
    # print(DA.d_hat(DA.q0, '10'))
    print('101' in DA)
    print(DA.d_hat(DA.q0, '101'))
    print(DA.get_Ln(4), '\n')

    # for q in DA.Q:
    #     for a in DA.S:
    #         print('d({}, {}) = {}'.format(q, a, DA.d(q, a)))

    # print('d^^({}, {}) = {}'.format(DA.q0, '11', DA.d_hat(DA.q0, '11')))
    # print(DA.F)
    print(len(DA.get_Ln(5))+1)

    A.add_prefix('tom')
    print(A.Q)
    print(A.S)
    print(A.q0)
    print(A.F)
    # for q in A.Q:
    #     for a in A.S:
    #         print('d({}, {}) = {}'.format(q, a, A.d(q, a)))
    print(A.get_Ln(7))
    print(A.get_Ln(4, 'tom'))

    A.add_prefix('tom')
    print(A.Q)
    print(A.S)
    print(A.q0)
    print(A.F)
    # for q in A.Q:
    #     for a in A.S:
    #         print('d({}, {}) = {}'.format(q, a, A.d(q, a)))
    print(A.get_Ln(7))
    print(A.get_Ln(4, 'tomtom'))

    DA = A.to_DFA()
    print(DA.get_Ln(7))
    print(DA.get_Ln(4, 'tomtom'))


if __name__ == '__main__':
    _test()
