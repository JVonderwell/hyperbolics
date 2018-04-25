from utils import dist
import pandas as pd
import numpy as np

class HypDistance:

    def __init__(self, emb_file, int_map):
        self.emb = pd.read_csv(emb_file)
        self.int_map = int_map

    # returns the distance between two tuples
    # tuple_file must be line separated tuples with same schema as original dataset
    def pair_distance_file(self, tuple_file):
        t_file = open(tuple_file, 'r')

        tuple_1 = t_file.readline().rstrip().split(',')
        tuple_2 = t_file.readline().rstrip().split(',')

        if len(tuple_1) != len(tuple_2):
            raise ValueError('tuples not in same schema')

        # for each node in each tuple, store hyp distance
        distances = list()
        for i in range(len(tuple_1)):
            node_1 = self.int_map[(tuple_1[i], i)]
            node_2 = self.int_map[(tuple_2[i], i)]

            vec_1 = np.array(self.emb.iloc[node_1][1:4])
            vec_2 = np.array(self.emb.iloc[node_2][1:4])

            distances.append(dist(vec_1, vec_2))

        return np.asarray(distances).mean()


    def pair_distance(self, tuple_1, tuple_2):

        if len(tuple_1) != len(tuple_2):
            raise ValueError('tuples not in same schema')

        # for each node in each tuple, store hyp distance
        distances = list()
        for i in range(len(tuple_1)):
            node_1 = self.int_map[(tuple_1[i], i)]
            node_2 = self.int_map[(tuple_2[i], i)]

            vec_1 = np.array(self.emb.iloc[node_1][1:4])
            vec_2 = np.array(self.emb.iloc[node_2][1:4])

            distances.append(dist(vec_1, vec_2))

        return np.asarray(distances).mean()
