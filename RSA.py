from functions import *

def RSA_encrypt(m: int, public: tuple[int, int]) -> int:

    e, N = public

    c = pow(m, e, N)

    return c

def RSA_decrypt(c: int, secret: tuple[int, int]) -> int:

    d, N = secret

    m = pow(c, d, N)

    return m

