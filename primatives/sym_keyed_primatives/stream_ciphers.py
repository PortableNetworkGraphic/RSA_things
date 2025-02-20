from functions import bytes_to_bits, bits_to_bytes


class OneTimePad:

    def __init__(self, k: int):
        assert k >= 0
        self.k = k

    def encrypt(self, p: bytes) -> bytes:
        p = bytes_to_bits(p)
        assert p >= 0
        return bits_to_bytes(p ^ self.k)

    def decrypt(self, c: bytes) -> bytes:
        return self.encrypt(c)