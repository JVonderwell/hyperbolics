from parser import Parser
from bcnf_splitter import BCNFSplitter

class Converter:

    def __init__(self):
        self.parser = Parser()


    def save_graph(self, filename, fdfile, outfile, weighting=None):

        parser = self.parser

        f = open(filename, 'r')

        colnames = f.readline().split(',')

        if fdfile is not None:
            splitter = BCNFSplitter(filename, fdfile)
            tables = splitter.split_data()
        else:
            tables = [range(len(colnames))]

        for line in f:
            split = line.rstrip('\n').split(',')
            for table in tables:
                for i in range(len(table) - 1):
                    col_1 = table[i]
                    col_2 = table[i+1]
                    node_1 = (split[col_1], col_1)
                    node_2 = (split[col_2], col_2)
                    parser.add_edge(node_1, node_2)

                # add edges for last col to first col
                col_1 = table[0]
                col_2 = table[len(table) - 1]

                node_1 = (split[col_1], col_1)
                node_2 = (split[col_2], col_2)
                parser.add_edge(node_1, node_2)

        parser.save_edges(outfile, weighting)

    def get_map(self):
        return self.parser.get_map()
