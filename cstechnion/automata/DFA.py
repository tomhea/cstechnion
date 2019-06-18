from itertools import product


class DFA:  # Deterministic Finite Automation
    def __init__(self, Q, S, q0, d, F):
        """
            Q  = States (iterable)
            S  = Alphabet (string)
            q0 = start-state
            d  = Transition-Function (d: Q×S -> Q)
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
                   3. change states names to integers from range(0, len(self.Q)) """
        pass  # TODO really do something

    def accept(self, w):
        return self.d_hat(self.q0, w) in self.F      # δ^(q0, w)∈F

    def d_hat(self, q, w):
        for a in w:             # for every letter a in w:
            q = self.d(q, a)        # new_q = δ(q, a)
        return q

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

    def _first_pre_name(self):    # get first prefix (of the form _*_pre) that is not used by any string state
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

    def add_prefix(self, w):
        if len(w) > 0:
            _pre = self._first_pre_name()
            new_d = {}

            new_q0 = curr_q = _pre + '0'
            self.Q.append(curr_q)
            for i in range(1, len(w)):
                last_q, curr_q = curr_q, _pre + str(i)
                self.Q.append(curr_q)
                new_d[last_q, w[i - 1]] = curr_q
            garbage_q = _pre + '_false'
            self.Q.append(garbage_q)
            new_d[curr_q, w[-1]] = self.q0

            new_letters = ''.join([a for a in dict.fromkeys(w) if a not in self.S])
            old_d = self.d
            self.d = lambda q, a: new_d.get((q, a), garbage_q) if a in new_letters or type(q) is str and q.startswith(_pre) else old_d(q, a)
            self.q0 = new_q0
            self.S += new_letters

    def _get_r_ij_0(self, i, j, Q):
        letters = []
        for a in self.S:
            if self.d(Q[i], a) == Q[j]:     # for every a in Σ, if δ(qi, a)=qj...
                letters.append(a)
        if len(letters) == 0:               # if no letter at all - empty set
            return '∅'
        if len(letters) == 1:               # if only 1 letter (no parenthesis needed)
            return letters[0]
        if len(letters) == len(self.S):     # if letters == whole alphabet
            return 'Σ'
        return '({})'.format('+'.join(letters))

    @staticmethod
    def _YstarY_YYstar(u):
        if len(u) >= 1 and len(u) % 2 == 1:
            half_len = len(u) // 2
            if u[-1] == '*':                            # w*
                if u[:half_len] == u[half_len: - 1]:    # yy*
                    return u[:half_len]
            if u[half_len] == '*':                      # u*v
                if u[:half_len] == u[half_len + 1:]:    # y*y
                    return u[:half_len]
        return None

    @staticmethod
    def _get_r_ij_k(i, j, k, r_k1):
        r1 = r_k1[i, j]
        r2 = r_k1[i, k]
        r4 = r_k1[k, j]
        r3 = r_k1[k, k]
        if r3 in ['∅ε']:        # (∅*) = (ε*) = ε
            r3 = 'ε'
        elif r3[-1:] != '*':    # (x**) -> x*
            r3 += '*'

        if r2 == '∅' or r4 == '∅':      # ∅x -> ∅
            return r1

        r_second = ''.join([r for r in [r2, r3, r4] if r != 'ε']).rjust(1, 'ε')     # r_second=r2+r3+r4 \{redundant ε}

        if r1 == '∅':   # ∅+x -> x
            if len(r_second) == 1 or (len(r_second) == 2 and r_second[1] == '*'):
                return r_second
            return '({})'.format(r_second)

        if 'Σ*' in [r1, r_second]:  # x+Σ*, Σ*+x -> Σ*
            return 'Σ*'
        if r1 == r_second:      # x+x -> x
            return r1

        if len(r_second) > len(r1):         # shorten expressions as  x+y*yx -> y*x,  x+xyy* -> xy*
            if r_second[-len(r1):] == r1:       # x+xy*y or x+xyy*
                u = r_second[:-len(r1)]
                if DFA._YstarY_YYstar(u):
                    return '({}*{})'.format(u[:len(u) // 2], r1)
            elif r_second[:len(r1)] == r1:      # x+y*yx or x+yy*x
                u = r_second[len(r1):]
                if DFA._YstarY_YYstar(u):
                    return '({}{}*)'.format(r1, u[:len(u) // 2])
        return '({}+{})'.format(r1, r_second)

    def to_regex(self):
        last, curr = {}, {}     # last (k-1)-line, curr k-line
        Q = [None] + [q for q in self.Q]
        m = len(Q)

        for i in range(1, m):
            for j in range(1, m):
                curr[i, j] = self._get_r_ij_0(i, j, Q)      # prepare the L_ij_0 part

        for k in range(1, m):
            last, curr = curr, last
            for i in range(1, m):
                for j in range(1, m):
                    curr[i, j] = self._get_r_ij_k(i, j, k, last)    # calculate the L_ij_k using L_i'j'_k-1

        r_1f_m = ['ε'] if self.q0 in self.F else []     # insert ε to the re if q0 in F
        for f in self.F:
            r_1f_m.append(curr[Q.index(self.q0), Q.index(f)])   # re += every accepting state L_1f_m
        return '+'.join(r_1f_m)


"""
TODO:
    add Regex (built with {+·*()}, and around S (some alphabet)
    add (Union), (Same), (iterations) to all 3 Automata's
    add NFA (Non-deterministic Finite Automaton)
    add NFAe (Non-deterministic Finite Automaton with Epsilon moves)
"""


def _test():

    def d(q, a):
        if q == 2:
            return 2
        if a == '0':
            return 0
        return q + 1

    A = DFA([0, 1, 2], '01', 0, d, [1])
    print('' in A)
    print('11' in A)
    print('10' in A)
    print('101' in A)
    print(A.to_regex())


    def d2(q, a):
        return q if a == '1' else 1-q


    A2 = DFA([0, 1], '01', 0, d2, [0])
    print(A2.to_regex())
    # print(A.get_Ln(5, '10101'))
    A.add_prefix('tom')
    # print(A.Q)
    # print(A.q0)
    # print(A.d('_pre0', '0'))
    # for q in A.Q:
    #     for a in A.S:
    #         print('d({},{})={}'.format(q, a, A.d(q, a)))
    # print(A.d)
    print(A.get_Ln(7))
    A.add_prefix('tomtom')
    print(A.get_Ln(8))


if __name__ == '__main__':
    _test()


