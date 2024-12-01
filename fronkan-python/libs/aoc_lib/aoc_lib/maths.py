from functools import reduce
from typing import Iterable
import operator


def prod(nums: Iterable[int]) -> int:
    return reduce(operator.mul, nums)

def clamp(val, min_val, max_val):
    if val < min_val:
        return min_val
    if val > max_val:
        return max_val
    return val
