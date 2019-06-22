from copy import deepcopy

from cstechnion.mivne.List import List


# class OneSidedEdge:
#     def __init__(self, v):
#         self.v = v
#         self.twin = None


# class NeighborsList:
#     def __init__(self):
#         self.e_in = List()
#         self.e_out = List()


class Graph:
    def __init__(self, V=[], E=[]):
        self.V = V
        # self.lists = {v: NeighborsList() for v in V}
        self.neighbors = {v: List() for v in V}
        self.d = {v: 0 for v in V}
        for e in E:
            self.add_edge(e)

    def add_vertex(self, v):    # add new vertex to graph
        if v not in self.V:
            self.V.append(v)
            self.neighbors[v] = List()
            self.d[v] = 0

    def add_edge(self, e):
        (u, v) = e
        self.neighbors[u] += v
        self.d[u] += 1
        self.neighbors[v] += u
        self.d[v] += 1

    def __iadd__(self, e):
        self.add_edge(e)
        return self

    def connected(self, u, v):  # is there an edge (u,v)
        return v in self.neighbors[u]

    def __contains__(self, e):  # is e in Graph.E
        (u,v) = e
        return self.connected(u, v)

    def __len__(self):
        return len(self.V)

    def __bool__(self):
        return len(self.V) > 0

    def __str__(self):
        return '   '.join(['(' + str(v) + '):' + str(self.neighbors[v]) for v in self.V])

        # self.lists[u].e_out.push_first(v)
        # self.lists[v].e_in.push_first(u)

        # self.lists[u].e_out.first.value.twin = self.lists[v].e_in.first
        # self.lists[v].e_in.first.value.twin = self.lists[u].e_out.first


class DiGraph:
    def __init__(self, V=[], E=[]):
        self.V = V
        self.neighbors = {v: List() for v in V}     # out
        self.d_in = {v: 0 for v in V}
        self.d_out = {v: 0 for v in V}
        for e in E:
            self += e

    def add_vertex(self, v):    # add new vertex to graph
        if v not in self.V:
            self.V.append(v)
            self.neighbors[v] = List()
            self.d_in[v] = 0
            self.d_out[v] = 0

    def add_edge(self, e):
        (u, v) = e
        self.neighbors[u] += v
        self.d_out[u] += 1
        self.d_in[v] += 1

    def __iadd__(self, e):
        self.add_edge(e)
        return self

    def connected(self, u, v):  # is there an edge (u,v)
        return v in self.neighbors[u]

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

    @staticmethod
    def find_first_source(sources):      # sources is the group of all vertexes with d_in[v] = 0
        """ return the first source in sources, after removing it from the sources List """
        if sources:
            s = sources.first.value
            sources.delete_first()
            return s
        return None

    def remove_source(self, s, sources):    # delete the given source-vertex from the Graph
        if s in self.V:
            for u in self.neighbors[s]:
                self.d_in[u] -= 1
                if self.d_in[u] == 0:
                    sources += u
            self.neighbors[s] = List()
            self.d_in.pop(s)
            self.d_out.pop(s)
            self.V.remove(s)

    def topological_sort(self):
        """ return mapping of all vertexes to their topological index. None is graph is cyclic (topological failed) """
        G = deepcopy(self)
        sources = List([v for v in self.V if self.d_in[v] == 0])
        N, i = {}, 0
        while G:
            s = G.find_first_source(sources)
            if s is None: return None
            N[s], i = i, i+1
            G.remove_source(s, sources)
        return N

    def is_cyclic(self):    # is there a cycled-route in self-graph
        return self.topological_sort() is None

    def to_undirected_graph(self):      # removes directions from edges
        g = Graph(deepcopy(self.V))
        g.d = {v: self.d_in[v]+self.d_out[v] for v in g.V}
        g.neighbors = {v: deepcopy(self.neighbors[v]) for v in g.V}
        for v in g.V:
            for u in self.neighbors[v]:
                g.neighbors[u] += v
        return g

    def __str__(self):
        return '   '.join(['(' + str(v) + '):' + str(self.neighbors[v]) for v in self.V])
