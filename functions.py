import sympy

def generate_key_pair(key_size: int=1024) -> tuple[tuple[int, int], tuple[int, int]]:
    p, q = sympy.randprime(1<<(key_size//2-1), 1<<(key_size//2)), sympy.randprime(1<<(key_size//2-1), 1<<(key_size//2))

    N = p * q

    e = 65537

    phi = (p - 1) * (q - 1)

    d = pow(e, -1, phi)

    public = (e, N)
    secret = (d, N)

    return public, secret

