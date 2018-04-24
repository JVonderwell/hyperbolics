## hacky script I was using for NN calculations.
## come back eventually

import math
import numpy as np
from scipy.spatial.distance import cdist
import mrpt

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('embedding')
parser.add_argument('outfile')
parser.add_argument('mapfile')

args = parser.parse_args()
emb_file = args.embedding
out_file = args.outfile
map_file = args.mapfile

emb = open(emb_file, 'r')

nodes = list()
points = list()

emb.readline()
for line in emb:
    # cuts off index and scaling factor tau
    node = line.split(',')[0]
    point = ' '.join(line.split(',')[1:-1])

    nodes.append(node)
    points.append(np.fromstring(point, dtype='f', sep=' '))

points = np.asarray(points)

def acosh(x):
    return math.log(x + math.sqrt(x ** 2 - 1))

def dist(x, y):
    z = 2 * (np.linalg.norm(x - y) ** 2)

    uu = 1. + z / ((1.0 - np.linalg.norm(x) ** 2) * (1.0 - np.linalg.norm(y) ** 2))
    return acosh(uu)


k = 10
n_points = 5

first_points = points[:n_points]

exact_neighbors = np.zeros((n_points, k))
for i in range(n_points):
    exact_neighbors[i] = np.argsort(cdist([first_points[i]], points, metric=dist))[0,:k]

index = mrpt.MRPTIndex(points, depth=10, n_trees=1000)
index.build()

approx_neighbors = np.zeros((n_points, k))
for i in range(n_points):
    approx_neighbors[i] = index.ann(first_points[i], k)

map_f = open(map_file, 'r', encoding='utf-8')

int_map = dict()
for line in map_f:
    if line != '\n':
        mapping = line.split(',')
        int_map[int(mapping[0])] = mapping[1]

for n in approx_neighbors[:n_points]:
    line = str(int_map[n[0]]).rstrip() + ': with NN\'s: '
    for val in n[1:]:
        line += int_map[int(val)].rstrip() + ' - '
    print(line + '\n')
        
correct = 0
for i in range(n_points):
    correct += len(np.intersect1d(exact_neighbors[i], approx_neighbors[i]))
print ('Average recall: ' + str(float(correct)/(n_points*k)))
