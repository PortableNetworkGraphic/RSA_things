from functions import *
import sympy
import hashlib

class RSA:

    def __init__(self, key_size: int=1024):
        self.key_size = key_size
        self.public, self.secret = RSA.generate_key_pair(self.key_size)

    @staticmethod
    def generate_key_pair(key_size: int = 1024) -> tuple[tuple[int, int], tuple[int, int]]:
        p, q = sympy.randprime(1 << (key_size // 2 - 1), 1 << (key_size // 2)), sympy.randprime(
            1 << (key_size // 2 - 1), 1 << (key_size // 2))

        N = p * q

        e = 65537

        phi = (p - 1) * (q - 1)

        d = pow(e, -1, phi)

        public = (e, N)
        secret = (d, N)

        return public, secret

    @staticmethod
    def encrypt(m: int, public: tuple[int, int]) -> int:

        e, N = public

        return pow(m, e, N)

    def decrypt(self, m: int) -> int:

        d, N = self.secret

        return pow(m, d, N)

    def sign(self, m: int) -> int:

        hashed = encode_bytes_to_bits(hashlib.sha256(decode_bits_to_bytes(m)).digest())

        return self.encrypt(hashed, self.secret)

    @staticmethod
    def verify(m: int, signature: int, public: tuple[int, int]) -> bool:

        d, N = public

        hashed = encode_bytes_to_bits(hashlib.sha256(decode_bits_to_bytes(m)).digest())

        return hashed == pow(signature, d, N)
