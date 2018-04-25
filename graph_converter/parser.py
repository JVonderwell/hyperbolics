class Parser:

    def __init__(self):
        self.edges = set()

        # maps unique nodes to ints
        self.int_map = dict()
        self.curr = 0

        # init count maps - used for determining weights of edges

        # maps edges to occurrence count
        self.edge_count_map = dict()

        # maps nodes to occurrence count
        self.node_count_map = dict()

    def _map_node(self, node):
        # maps unique (val, attr) pairs to ints
        if node not in self.int_map:
            self.int_map[node] = self.curr
            self.curr += 1

    def _count_edge(self, edge):
        # counts appearances of edge - used for weighting
        if edge not in self.edges:
            self.edge_count_map[edge] = 1
        else:
            self.edge_count_map[edge] += 1

    def _count_node(self, node):
        # counts appearance of node on left side of edge
        int_node = self.int_map[node]
        if int_node not in self.node_count_map:
            self.node_count_map[int_node] = 1
        else:
            self.node_count_map[int_node] += 1
            
    def add_edge(self, node_1, node_2):
        # takes two (val, attr) tuples and adds an edge between them
        self._map_node(node_1)
        self._map_node(node_2)

        self._count_node(node_1)

        edge = (self.int_map[node_1], self.int_map[node_2])
        self._count_edge(edge)

        self.edges.add(edge)

    def save_edges(self, outfile, weighted):

        out = open(outfile, 'w')
        
        for edge in sorted(self.edges):
            str_edge = str(edge[0]) + ' ' + str(edge[1])

            if weighted == 'count':
                str_edge += ' ' + str(1.0 / self.edge_count_map[edge])
            elif weighted == 'proportion':
                prop = 1.0 / (float(self.edge_count_map[edge]) / self.node_count_map[edge[0]])
                str_edge += ' ' + str(prop)

            out.write(str_edge + '\n')

    def get_map(self):
        if not self.int_map:
            raise ValueError('no nodes added yet')
        return self.int_map

