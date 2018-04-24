from utils import dist
import pandas as pd
import numpy as np


# returns the distance between two tuples
# tuple_file must be line separated tuples with same schema as original dataset
def pair_distance(tuple_file, emb_file, int_map):
    t_file = open(tuple_file, 'r')

    tuple_1 = t_file.readline().rstrip().split(',')
    tuple_2 = t_file.readline().rstrip().split(',')

    emb = pd.read_csv(emb_file)

    if len(tuple_1) != len(tuple_2):
        raise ValueError('tuples not in same schema')

    # for each node in each tuple, store hyp distance
    distances = list()
    for i in range(len(tuple_1)):
        node_1 = int_map[(tuple_1[i], i)]
        node_2 = int_map[(tuple_2[i], i)]

        vec_1 = np.array(emb.iloc[node_1][1:4])
        vec_2 = np.array(emb.iloc[node_2][1:4])

        distances.append(dist(vec_1, vec_2))

    return np.asarray(distances).mean()
