from functions import *

def RSA(m: int, key: tuple[int, int]) -> int:

    ed, N = key

    return pow(m, ed, N)


