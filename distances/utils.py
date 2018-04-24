import math
import numpy as np


def acosh(x):
    return math.log(x + math.sqrt(x ** 2 - 1))

# gets distance between two nodes in hyperbolic space
def dist(x, y):
    z = 2 * (np.linalg.norm(x - y) ** 2)

    uu = 1. + z / ((1.0 - np.linalg.norm(x) ** 2) * (1.0 - np.linalg.norm(y) ** 2))
    return acosh(uu)
