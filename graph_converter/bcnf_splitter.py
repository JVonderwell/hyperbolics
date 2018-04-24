import pandas as pd


class BCNFSplitter:

    def __init__(self, data_file, fd_file):
        self.data = pd.read_csv(data_file)

        # dict mapping list of LHS to string RHS
        self.fds = list()

        fdf = open(fd_file, 'r')

        # each fd maps list of cols to one col
        for line in fdf:
            split_fd = line.split('-')
            left = tuple(split_fd[0].split(','))
            right = split_fd[1].rstrip('\n')
            self.fds.append([left, right])

    def split_data(self):
        # returns normalized list of list of column indices
        # ex: [[1, 3], [1,2,4]]

        # start with all cols
        tables = [range(self.data.shape[1])]
        i = 0
        while i < len(tables):
            table = self.data.iloc[:, tables[i]]
            viol_fd = self._violated_fd(table)
            if viol_fd != -1:
                a = self.data.columns.get_loc(self.fds[viol_fd][1])
                x = [self.data.columns.get_loc(col)
                     for col in self.fds[viol_fd][0]]

                # XA
                x.append(a)
                tables.append(x)

                # R - A
                table = tables.pop(i)
                table.remove(a)
                tables.append(table)

                i -= 1
            i += 1

        return tables

    def _violated_fd(self, table):
        # returns index of violated fd or -1 if none
        for fd in self.fds:
            left = fd[0]
            right = fd[1]
            if all([s in table.columns for s in left]) \
                    and right in table.columns \
                    and not table.shape[1] == len(left) + 1:
                return self.fds.index(fd)

        return -1
