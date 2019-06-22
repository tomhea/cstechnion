from copy import deepcopy
from itertools import product

from cstechnion.automata.DFA import DFA
from cstechnion.kombi.Basics import subgroups, subgroups_with_elements_of


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
        """ should 1. delete not-reachable states, and
                           2. remove identical states: q,p≠q0 equals if: d(q,a)=d(p,a) for all a∈Σ, and) q∈F iff q∈F
                           3. change states names to integers from range(0, len(self.Q))
                           4. find out about good algorithm for minimizing an Automata """
        pass  # TODO really do something

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

    def get_Ln(self, n, prefix=''):     # TODO: try to do it in graphical-BFS way
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

    def get_L(self, prefix=''):         # TODO: try to do it in graphical-BFS way
        """ generate the next word in L alphabetically
            if prefix entered, generate words of the form: [prefix][Σ*] """
        n = 0
        while True:
            for letters in product(self.S, repeat=n):
                w = prefix + ''.join(letters)
                if w in self:
                    yield w
            n += 1

    def _first_pre_name(self):        # get first prefix (of the form _*_pre) that is not used by any string state
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

    def add_prefix(self, w):    # for every v in self, wv in new_self
                                # for example [even #0].add_prefix('tom') = (tom, tom1, tom00, tom11, tom100, tom010, tom001, ...)
        if len(w) > 0:
            _pre = self._first_pre_name()
            new_d = {}

            new_q0 = curr_q = _pre + '0'
            self.Q.append(curr_q)
            for i in range(1, len(w)):
                last_q, curr_q = curr_q, _pre + str(i)
                self.Q.append(curr_q)
                new_d[last_q, w[i - 1]] = {curr_q}      # q_i-1 --[W_i-1]--> q_i
            new_d[curr_q, w[-1]] = {self.q0}

            new_letters = ''.join([a for a in dict.fromkeys(w) if a not in self.S])
            old_d = self.d
            self.d = lambda q, a: new_d.get((q, a), set()) if a in new_letters or type(q) is str and q.startswith(_pre) else old_d(q, a)
            self.q0 = new_q0
            self.S += new_letters

    def __deepcopy__(self, memo={}):
        new_Q = deepcopy(self.Q)
        new_S = deepcopy(self.S)
        new_q0 = deepcopy(self.q0)
        new_d_dict = {(q, a): self.d(q, a) for q in self.Q for a in self.S}
        new_d = lambda q, a: new_d_dict[q, a]
        new_F = deepcopy(self.F)
        return NFA(new_Q, new_S, new_q0, new_d, new_F)

    def to_DFA(self):
        """ build power-Automata (2^Q) """
        copied = deepcopy(self)
        new_Q  = subgroups(copied.Q)    # 2^Q
        new_S  = copied.S               # S
        new_q0 = {copied.q0}            # {q0}
        new_d  = copied.d_hat_hat       # δ(P, a) := δ^^(P, a)
        new_F  = subgroups_with_elements_of(copied.Q, copied.F)     # 2^Q ∩ F ≠ ∅
        return DFA(new_Q, new_S, new_q0, new_d, new_F)


"""
TODO:
    add Regex (built with {+·*()}, and around S (some alphabet)
    add (Union), (Same), (iterations) to all 3 Automata's
    add NFA (Non-deterministic Finite Automaton)
    add NFAe (Non-deterministic Finite Automaton with Epsilon moves)
"""


if __name__ == '__main__':
    pass