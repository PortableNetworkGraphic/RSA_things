class OneTimePad:

    def __init__(self, k: int):
        assert k >= 0
        self.k = k

    def encrypt(self, p: int) -> int:
        assert p >= 0
        return p ^ self.k

    def decrypt(self, c: int) -> int:
        return self.encrypt(c)