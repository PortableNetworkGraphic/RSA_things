from math import ceil
from functions import *

class IDEA:

    def __init__(self, key: int):
        assert  0 <= key < 2**128, "Class = IDEA, Function = __init__: Key must be between 0 and 2**128"
        self.key = key
        self.subkeys = self.gen_keys()
        self.deckeys = self.inverse_gen_keys()

    @staticmethod
    def mul_inv(Z: int):
        """
        Computes the multiplicative inverse of Z mod 65537 using Extended Euclidean Algorithm.
        Created by ChatGPT bc I don't know what the hell this means.

        https://en.wikipedia.org/wiki/Extended_Euclidean_algorithm
        """
        if Z == 0:
            return 65536  # IDEA treats 0 as 65536
        Z = Z % 65537  # Ensure Z is within mod space
        t, new_t = 0, 1
        r, new_r = 65537, Z

        while new_r != 0:
            quotient = r // new_r
            t, new_t = new_t, t - quotient * new_t
            r, new_r = new_r, r - quotient * new_r

        if r > 1:
            raise ValueError("Z has no multiplicative inverse mod 65537")
        if t < 0:
            t += 65537  # Ensure positive result

        return t

    @staticmethod
    def mul_mod(a, b):
        assert 0 <= a <= 0x10000
        assert 0 <= b <= 0x10000


        if a == 0:
            a = 0x10000
        if b == 0:
            b = 0x10000

        r = (a * b) % 0x10001

        if r == 0x10000:
            r = 0

        assert 0 <= r <= 0xFFFF
        return r

    def gen_keys(self):

        subkeys = []
        key = self.key

        while len(subkeys) < 52:

            for i in range(8):
                subkeys.append((key >> (112 - i * 16)) & 0xFFFF)

            key = rotate(key, 128, 25)

        subkeys = [subkeys[i:i+6] for i in range(0, 54, 6)]

        return subkeys[:8]+[subkeys[8][:4]]

    def inverse_gen_keys(self):

        deckeys = [[0]*6 for _ in range(8)]+[[0]*4]

        deckeys[8][0] = self.mul_inv(self.subkeys[0][0])
        deckeys[8][1] = self.mul_inv(self.subkeys[0][1])
        deckeys[8][2] = (-self.subkeys[0][2]) & 0xFFFF
        deckeys[8][3] = (-self.subkeys[0][3]) & 0xFFFF

        for i in range(8):
            deckeys[i][0] = self.mul_inv(self.subkeys[8 - i][0])
            deckeys[i][1] = self.mul_inv(self.subkeys[8 - i][1])
            deckeys[i][2] = (-self.subkeys[8 - i][2]) & 0xFFFF
            deckeys[i][3] = (-self.subkeys[8 - i][3]) & 0xFFFF
            deckeys[i][4] = self.subkeys[7 - i][4]
            deckeys[i][5] = self.subkeys[7 - i][5]

        return deckeys



    def full_round(self, X1, X2, X3, X4, Z1, Z2, Z3, Z4, Z5, Z6):

        S1 = self.mul_mod(X1, Z1)

        S2 = self.mul_mod(X2, Z2)

        S3 = (X3 + Z3) % 0x10000

        S4 = (X4 + Z4) % 0x10000

        S5 = S1 ^ S3

        S6 = S2 ^ S4

        S7 = self.mul_mod(S5, Z5)

        S8 = (S7 + S6) % 0x10000

        S9 = self.mul_mod(S8, Z6)

        S10 = (S7 + S9) % 0x10000

        S11 = S1 ^ S9

        S12 = S3 ^ S9

        S13 = S2 ^ S10

        S14 = S4 ^ S10

        return S11, S13, S12, S14

    def encrypt_block(self, block: int) -> int:

        assert 0 <= block < 2**64, "Block must be integer within the range 0 to 2**64."

        P1, P2, P3, P4 = split_bin(block, 4, 16)

        for i in range(8):
            P1, P2, P3, P4 = self.full_round(P1, P2, P3, P4, *self.subkeys[i])

        P1 = self.mul_mod(P1, self.subkeys[8][0])
        P2 = self.mul_mod(P2, self.subkeys[8][1])
        P3 = (P3 + self.subkeys[8][2]) % 0x10000
        P4 = (P4 + self.subkeys[8][3]) % 0x10000

        return (P1 << 48) | (P2 << 32) | (P3 << 16) | P4

    def decrypt_block(self, block: int) -> int:
        """
        The decrypt function is effectively ideentical to the encrypt function, but uses
        a different set of keys.
        """

        assert 0 <= block < 2**64, "Block must be integer within the range 0 to 2**64."

        P1, P2, P3, P4 = split_bin(block, 4, 16)

        for i in range(8):
            P1, P2, P3, P4 = self.full_round(P1, P2, P3, P4, *self.deckeys[i])

        P1 = self.mul_mod(P1, self.deckeys[8][0])
        P2 = self.mul_mod(P2, self.deckeys[8][1])
        P3 = (P3 + self.deckeys[8][2]) % 0x10000
        P4 = (P4 + self.deckeys[8][3]) % 0x10000

        return concatenate_bin([P1, P2, P3, P4], 16)


    def encrypt(self, binary: int):

        blocks = split_bin(binary, ceil((len(bin(binary))-2)/64), 64)

        encrypted_blocks = []

        for block in blocks:
            encrypted_blocks.append(self.encrypt_block(block))

        return concatenate_bin(encrypted_blocks, 64), self.key

    def decrypt(self, binary: int):

        encrypted_blocks = split_bin(binary, ceil((len(bin(binary))-2)/64), 64)

        decrypted_blocks = []
        for block in encrypted_blocks:
            decrypted_blocks.append(self.decrypt_block(block))

        return concatenate_bin(decrypted_blocks, 64), self.key

