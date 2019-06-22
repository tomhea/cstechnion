from cstechnion.kombi.Basics import n_letter_words


class Graph:
    def __init__(self, V, E):
        self.V = V
        self.E = E

    def __len__(self):
        return len(self.V)

    def __str__(self):
        return 'V={ ' + ','.join(str(v) for v in self.V) + ' }    E={ ' + ','.join(str(e) for e in self.E) + ' }'

    def _d_in(self, _v):    # not really d_in,  because it's an undirected graph
        return len([(u,v) for (u,v) in self.E if v == _v])

    def _d_out(self, _v):   # not really d_out, because it's an undirected graph
        return len([(u,v) for (u,v) in self.E if u == _v])

    def d(self, _v):
        return self._d_in(_v) + self._d_out(_v)

    def eulerian_path(self):        # is there a route that visits all edges exactly once?
        Vd = {v: 0 for v in self.V}
        for (u,v) in self.E:
            Vd[u] = 1 - Vd[u]
            Vd[v] = 1 - Vd[v]
        return sum(Vd.values()) <= 2

    def eulerian_cycle(self):       # is there a circular route that visits all edges exactly once?
        Vd = {v: 0 for v in self.V}
        for (u,v) in self.E:
            Vd[u] = 1 - Vd[u]
            Vd[v] = 1 - Vd[v]
        return sum(Vd.values()) == 0


class DiGraph:
    def __init__(self, V, E):
        self.V = V
        self.E = E

    def __len__(self):
        return len(self.V)

    def __str__(self):
        return 'V={ ' + ','.join(str(v) for v in self.V) + ' }    E={ ' + ','.join(str(e) for e in self.E) + ' }'

    def d_in(self, _v):
        return len([(u,v) for (u,v) in self.E if v == _v])

    def d_out(self, _v):
        return len([(u,v) for (u,v) in self.E if u == _v])

    def d(self, _v):
        return self.d_in(_v) + self.d_out(_v)

    def eulerian_path(self):        # is there a route that visits all edges exactly once?
        Vd = {v: 0 for v in self.V}
        for (u, v) in self.E:
            Vd[u] += 1
            Vd[v] -= 1
        return sum(map(abs, Vd.values())) <= 2

    def eulerian_cycle(self):       # is there a circular route that visits all edges exactly once?
        Vd = {v: 0 for v in self.V}
        for (u, v) in self.E:
            Vd[u] += 1
            Vd[v] -= 1
        return sum(map(abs, Vd.values())) == 0

    def to_undirected_graph(self):     # removes directions from the Graph's edges
        return Graph(self.V, self.E)

    @staticmethod
    def de_bruijn(S, n):                # get de_bruijn (|S|^n) graph
        V = n_letter_words(S, n-1)
        E = [(b[:-1], b[1:]) for b in n_letter_words(S, n)]
        return DiGraph(V, E)


