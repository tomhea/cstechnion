from copy import deepcopy


class Graph:
    def __init__(self, V, E=[]):
        self.V = V
        self.neighbors = {v: {u: False for u in V} for v in V}
        self.d = {v: 0 for v in V}
        for e in E:
            self.add_edge(e)

    def add_edge(self, e):
        (u, v) = e
        self.d[u] += not self.neighbors[u][v]
        self.d[v] += not self.neighbors[v][u]
        self.neighbors[u][v] = True
        self.neighbors[v][u] = True

    def __iadd__(self, e):
        self.add_edge(e)
        return self

    def connected(self, u, v):  # is there an edge (u,v)
        return self.neighbors[u][v]

    def __contains__(self, e):  # is e in Graph.E
        (u,v) = e
        return self.connected(u, v)

    def __len__(self):
        return len(self.V)

    def __bool__(self):
        return len(self.V) > 0

    def __str__(self):
        return '   '.join(['(' + str(v) + '):' + str('-->'.join([''] + [str(u) for u in self.V if self.neighbors[v][u]] + ['null'])) for v in self.V])


class DiGraph:
    def __init__(self, V, E=[]):
        self.V = V
        self.neighbors = {v: {u: False for u in V} for v in V}
        self.d_in = {v: 0 for v in V}
        self.d_out = {v: 0 for v in V}
        for e in E:
            self += e

    def add_edge(self, e):
        (u, v) = e
        self.d_out[u] += not self.neighbors[u][v]
        self.d_in[v] += not self.neighbors[v][u]
        self.neighbors[u][v] = True

    def __iadd__(self, e):
        self.add_edge(e)
        return self

    def connected(self, u, v):  # is there an edge (u,v)
        return self.neighbors[u][v]

    def __contains__(self, e):  # is e in Graph.E
        (u,v) = e
        return self.connected(u, v)

    def __len__(self):
        return len(self.V)

    def __bool__(self):
        return len(self.V) > 0

    def __deepcopy__(self, memo={}):
        g = DiGraph([], [])
        g.V = deepcopy(self.V)
        g.neighbors = deepcopy(self.neighbors)
        g.d_in = deepcopy(self.d_in)
        g.d_out = deepcopy(self.d_out)
        return g

    def find_first_source(self):
        """ return the first vertex with d_in[v] = 0 """
        for v in self.V:
            if not self.d_in[v]:
                return v
        return None

    def remove_source(self, s):
        """ remove the given source from the Graph """
        if s in self.V:
            for u in self.V:
                if self.neighbors[s][u]:
                    self.neighbors[s][u] = False
                    self.d_in[u] -= 1
            self.d_in.pop(s)
            self.d_out.pop(s)
            self.V.remove(s)

    def topological_sort(self):
        """ return mapping of all vertexes to their topological index. None is graph is cyclic (topological failed) """
        G = deepcopy(self)
        N, i = {}, 0
        while G:
            s = G.find_first_source()
            if not s: return None
            N[s], i = i, i+1
            G.remove_source(s)
        return N

    def is_cyclic(self):    # is there a cycled-route in self-graph
        return self.topological_sort() is None

    def to_undirected_graph(self):      # removes directions from edges
        g = Graph(deepcopy(self.V))
        g.d = {v: self.d_in[v]+self.d_out[v] for v in g.V}
        g.neighbors = {v: {u: False for u in g.V} for v in g.V}
        for v in g.V:
            for u in g.V:
                if self.neighbors[u][v]:
                    g.neighbors[v][u] = True
                    g.neighbors[u][v] = True
        return g

    def __str__(self):
        return '   '.join(['(' + str(v) + '):' + str('-->'.join([''] + [str(u) for u in self.V if self.neighbors[v][u]] + ['null'])) for v in self.V])
