import random
import math

def get_uniform_rng(a, b):
    return a + (b - a) * random.uniform(0,1)


def get_exponential_rng(lmbd):
    lmbd_part = -(1 / lmbd)
    log_part = math.log(1 - random.uniform(0,1))
    result = lmbd_part * log_part
    return result


def get_0_1_rng():
    return random.uniform(0,1)