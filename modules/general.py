import random
import math
from modules.settings import RAND_MAX


def uniform(x_min: int, x_max: int) -> int:

    va = random.randint(0, RAND_MAX) / RAND_MAX
    va += va / RAND_MAX
    va += va / RAND_MAX

    while ((va <= 0) or (va >= 1.0 - (RAND_MAX ** (-3)))):
        pass

    return math.floor(x_min + va * (x_max - x_min))